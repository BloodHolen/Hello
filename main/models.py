from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('client', 'Авторизированный клиент'),
    ]
    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, default='client')
    patronymic = models.CharField('Отчество', max_length=150, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'.strip()


class Category(models.Model):
    name = models.CharField('Категория', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField('Производитель', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField('Поставщик', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField('Единица измерения', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.name


class Product(models.Model):
    article = models.CharField('Артикул', max_length=50, unique=True)
    name = models.CharField('Наименование товара', max_length=500)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name='Единица измерения')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Поставщик')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name='Производитель')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория товара')
    discount = models.PositiveIntegerField('Действующая скидка, %', default=0)
    quantity = models.PositiveIntegerField('Кол-во на складе', default=0)
    description = models.TextField('Описание товара', blank=True)
    photo = models.ImageField('Фото', upload_to='products/', blank=True, null=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (100 - self.discount) / 100
        return self.price

    def __str__(self):
        return f'{self.article} - {self.name}'


class PickupPoint(models.Model):
    address = models.CharField('Адрес', max_length=500, unique=True)

    class Meta:
        verbose_name = 'Пункт выдачи'
        verbose_name_plural = 'Пункты выдачи'

    def __str__(self):
        return self.address


class Order(models.Model):
    STATUS_CHOICES = [
        ('новый', 'Новый'),
        ('выдан', 'Выдан'),
    ]
    code = models.CharField('Код заказа', max_length=50, unique=True)
    order_number = models.IntegerField('Номер заказа')
    order_date = models.DateField('Дата заказа')
    delivery_date = models.DateField('Дата доставки')
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.CASCADE, verbose_name='Пункт выдачи')
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиент')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='новый')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.order_number} от {self.order_date}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField('Количество')

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f'{self.product.article} x {self.quantity}'
