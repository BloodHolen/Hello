from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q

from .models import Product, Order, OrderItem, Category, Supplier, Unit, Manufacturer, PickupPoint, User
from .decorators import role_required
import os
from django.conf import settings
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO


def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        messages.error(request, 'Неверный логин или пароль')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def home(request):
    return redirect('login')


def product_list(request):
    user = request.user
    is_guest = not user.is_authenticated
    is_manager = user.is_authenticated and user.role == 'manager'
    is_admin = user.is_authenticated and user.role == 'admin'
    can_filter = is_manager or is_admin

    products = Product.objects.select_related('category', 'manufacturer', 'supplier', 'unit').all()

    suppliers = Supplier.objects.all()

    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '')
    supplier_filter = request.GET.get('supplier', '')

    if can_filter:
        if search_query:
            sq = search_query.lower()
            products = [p for p in products if
                sq in p.name.lower() or
                sq in p.article.lower() or
                sq in (p.description or '').lower() or
                sq in p.category.name.lower() or
                sq in p.manufacturer.name.lower() or
                sq in p.supplier.name.lower()
            ]
        if supplier_filter:
            products = products.filter(supplier__name=supplier_filter)
        if sort_by == 'price_asc':
            products = products.order_by('price')
        elif sort_by == 'price_desc':
            products = products.order_by('-price')
        elif sort_by == 'qty_asc':
            products = products.order_by('quantity')
        elif sort_by == 'qty_desc':
            products = products.order_by('-quantity')

    context = {
        'products': products,
        'is_guest': is_guest,
        'can_filter': can_filter,
        'suppliers': suppliers,
        'search_query': search_query,
        'sort_by': sort_by,
        'supplier_filter': supplier_filter,
        'user_full_name': str(user) if user.is_authenticated else '',
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'product_list_partial.html', context)
    return render(request, 'product_list.html', context)


def resize_image(uploaded_file):
    img = Image.open(uploaded_file)
    img = img.convert('RGB')
    img.thumbnail((300, 200), Image.LANCZOS)
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    buffer.seek(0)
    return InMemoryUploadedFile(
        buffer, None, uploaded_file.name, 'image/jpeg',
        buffer.tell(), None
    )


@role_required('admin')
def product_add(request):
    if request.method == 'POST':
        article = request.POST['article']
        name = request.POST['name']
        category_id = request.POST['category']
        manufacturer_id = request.POST['manufacturer']
        supplier_id = request.POST['supplier']
        unit_id = request.POST['unit']
        price = request.POST['price']
        discount = request.POST.get('discount', 0)
        quantity = request.POST.get('quantity', 0)
        description = request.POST.get('description', '')

        if float(price) < 0:
            messages.error(request, 'Цена не может быть отрицательной')
            return redirect('product_add')
        if int(quantity) < 0:
            messages.error(request, 'Количество не может быть отрицательным')
            return redirect('product_add')

        product = Product.objects.create(
            article=article,
            name=name,
            category_id=category_id,
            manufacturer_id=manufacturer_id,
            supplier_id=supplier_id,
            unit_id=unit_id,
            price=price,
            discount=discount,
            quantity=quantity,
            description=description,
        )
        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            photo = resize_image(photo)
            product.photo.save(photo.name, photo, save=True)
        messages.success(request, 'Товар успешно добавлен')
        return redirect('product_list')

    context = {
        'categories': Category.objects.all(),
        'manufacturers': Manufacturer.objects.all(),
        'suppliers': Supplier.objects.all(),
        'units': Unit.objects.all(),
        'is_edit': False,
    }
    return render(request, 'product_form.html', context)


@role_required('admin')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.article = request.POST['article']
        product.name = request.POST['name']
        product.category_id = request.POST['category']
        product.manufacturer_id = request.POST['manufacturer']
        product.supplier_id = request.POST['supplier']
        product.unit_id = request.POST['unit']
        product.price = request.POST['price']
        product.discount = request.POST.get('discount', 0)
        product.quantity = request.POST.get('quantity', 0)
        product.description = request.POST.get('description', '')

        if float(product.price) < 0:
            messages.error(request, 'Цена не может быть отрицательной')
            return redirect('product_edit', pk=pk)
        if int(product.quantity) < 0:
            messages.error(request, 'Количество не может быть отрицательным')
            return redirect('product_edit', pk=pk)

        if 'photo' in request.FILES:
            if product.photo:
                old_path = product.photo.path
                if os.path.exists(old_path):
                    os.remove(old_path)
            photo = request.FILES['photo']
            photo = resize_image(photo)
            product.photo.save(photo.name, photo, save=True)

        product.save()
        messages.success(request, 'Товар успешно обновлён')
        return redirect('product_list')

    context = {
        'product': product,
        'categories': Category.objects.all(),
        'manufacturers': Manufacturer.objects.all(),
        'suppliers': Supplier.objects.all(),
        'units': Unit.objects.all(),
        'is_edit': True,
    }
    return render(request, 'product_form.html', context)


@role_required('admin')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if OrderItem.objects.filter(product=product).exists():
        messages.error(request, 'Товар присутствует в заказе и не может быть удалён')
        return redirect('product_list')
    if product.photo:
        old_path = product.photo.path
        if os.path.exists(old_path):
            os.remove(old_path)
    product.delete()
    messages.success(request, 'Товар удалён')
    return redirect('product_list')


@role_required('admin', 'manager')
def order_list(request):
    orders = Order.objects.select_related('pickup_point', 'client').prefetch_related('items__product').all()
    context = {
        'orders': orders,
        'is_admin': request.user.role == 'admin',
        'user_full_name': str(request.user),
    }
    return render(request, 'order_list.html', context)


@role_required('admin')
def order_add(request):
    if request.method == 'POST':
        code = request.POST['code']
        order_number = request.POST['order_number']
        order_date = request.POST['order_date']
        delivery_date = request.POST['delivery_date']
        pickup_point_id = request.POST['pickup_point']
        client_id = request.POST['client']
        status = request.POST['status']

        order = Order.objects.create(
            code=code,
            order_number=order_number,
            order_date=order_date,
            delivery_date=delivery_date,
            pickup_point_id=pickup_point_id,
            client_id=client_id,
            status=status,
        )

        product_ids = request.POST.getlist('product_id[]')
        quantities = request.POST.getlist('quantity[]')
        for pid, qty in zip(product_ids, quantities):
            if pid and qty:
                OrderItem.objects.create(order=order, product_id=pid, quantity=qty)

        messages.success(request, 'Заказ успешно добавлен')
        return redirect('order_list')

    context = {
        'clients': User.objects.filter(role='client'),
        'pickup_points': PickupPoint.objects.all(),
        'products': Product.objects.all(),
        'is_edit': False,
    }
    return render(request, 'order_form.html', context)


@role_required('admin')
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.code = request.POST['code']
        order.order_number = request.POST['order_number']
        order.order_date = request.POST['order_date']
        order.delivery_date = request.POST['delivery_date']
        order.pickup_point_id = request.POST['pickup_point']
        order.client_id = request.POST['client']
        order.status = request.POST['status']
        order.save()

        order.items.all().delete()
        product_ids = request.POST.getlist('product_id[]')
        quantities = request.POST.getlist('quantity[]')
        for pid, qty in zip(product_ids, quantities):
            if pid and qty:
                OrderItem.objects.create(order=order, product_id=pid, quantity=qty)

        messages.success(request, 'Заказ успешно обновлён')
        return redirect('order_list')

    context = {
        'order': order,
        'clients': User.objects.filter(role='client'),
        'pickup_points': PickupPoint.objects.all(),
        'products': Product.objects.all(),
        'is_edit': True,
    }
    return render(request, 'order_form.html', context)


@role_required('admin')
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    messages.success(request, 'Заказ удалён')
    return redirect('order_list')
