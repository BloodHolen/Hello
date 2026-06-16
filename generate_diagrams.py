import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages


def draw_er_diagram():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('ER-диаграмма базы данных "МирИгрушек"', fontsize=16, fontweight='bold', pad=20)

    tables = [
        {
            'name': 'User',
            'x': 1, 'y': 8, 'width': 3, 'height': 1.2,
            'fields': ['PK id (INT)', 'username (VARCHAR)', 'password (VARCHAR)',
                       'first_name (VARCHAR)', 'last_name (VARCHAR)', 'patronymic (VARCHAR)',
                       'role (VARCHAR)', 'email (VARCHAR)']
        },
        {
            'name': 'Product',
            'x': 6, 'y': 8, 'width': 3.5, 'height': 1.4,
            'fields': ['PK id (INT)', 'article (VARCHAR)', 'name (VARCHAR)',
                       'price (DECIMAL)', 'discount (INT)', 'quantity (INT)',
                       'description (TEXT)', 'photo (VARCHAR)',
                       'FK category_id (INT)', 'FK manufacturer_id (INT)',
                       'FK supplier_id (INT)', 'FK unit_id (INT)']
        },
        {
            'name': 'Category',
            'x': 10.5, 'y': 8.5, 'width': 2.5, 'height': 0.5,
            'fields': ['PK id (INT)', 'name (VARCHAR)']
        },
        {
            'name': 'Manufacturer',
            'x': 10.5, 'y': 7, 'width': 2.5, 'height': 0.5,
            'fields': ['PK id (INT)', 'name (VARCHAR)']
        },
        {
            'name': 'Supplier',
            'x': 10.5, 'y': 5.5, 'width': 2.5, 'height': 0.5,
            'fields': ['PK id (INT)', 'name (VARCHAR)']
        },
        {
            'name': 'Unit',
            'x': 10.5, 'y': 4, 'width': 2.5, 'height': 0.5,
            'fields': ['PK id (INT)', 'name (VARCHAR)']
        },
        {
            'name': 'Order',
            'x': 1, 'y': 4.5, 'width': 3, 'height': 1,
            'fields': ['PK id (INT)', 'code (VARCHAR)', 'order_number (INT)',
                       'order_date (DATE)', 'delivery_date (DATE)',
                       'status (VARCHAR)',
                       'FK pickup_point_id (INT)', 'FK client_id (INT)']
        },
        {
            'name': 'OrderItem',
            'x': 6, 'y': 4, 'width': 3, 'height': 0.7,
            'fields': ['PK id (INT)', 'quantity (INT)',
                       'FK order_id (INT)', 'FK product_id (INT)']
        },
        {
            'name': 'PickupPoint',
            'x': 1, 'y': 1.5, 'width': 2.5, 'height': 0.5,
            'fields': ['PK id (INT)', 'address (VARCHAR)']
        },
    ]

    for t in tables:
        rect = mpatches.FancyBboxPatch(
            (t['x'], t['y'] - t['height']), t['width'], t['height'],
            boxstyle="round,pad=0.1", facecolor='#F5DEB3', edgecolor='#000', linewidth=1.5
        )
        ax.add_patch(rect)
        ax.text(t['x'] + t['width'] / 2, t['y'] - 0.2, t['name'],
                ha='center', va='top', fontsize=11, fontweight='bold')
        field_text = '\n'.join(t['fields'])
        ax.text(t['x'] + t['width'] / 2, t['y'] - t['height'] + 0.1, field_text,
                ha='center', va='bottom', fontsize=7, fontfamily='monospace')

    connections = [
        (6.5, 8, 6.5, 7.6, 'Category 1 → N Product'),
        (8.5, 8, 8.5, 7.6, 'Manufacturer 1 → N Product'),
        (6.5, 7.6, 10.5, 8.0, ''),
        (8.5, 7.6, 10.5, 6.5, ''),
        (6.5, 6.6, 6.5, 5.4, 'Supplier 1 → N Product'),
        (8.5, 6.6, 8.5, 5.4, ''),
        (6.5, 6.6, 10.5, 5.0, ''),
        (8.5, 6.6, 8.5, 5.4, ''),
        (6.5, 6.6, 10.5, 3.5, ''),
        (6.5, 8, 10.5, 8.0, ''),
        (6.5, 8, 10.5, 6.5, ''),
        (2.5, 4.5, 2.5, 2.0, ''),
        (4, 4.5, 4, 2.0, ''),
        (3, 3.5, 6, 3.3, 'Order 1 → N OrderItem'),
        (4, 3.3, 6, 3.3, ''),
        (7.5, 4, 7.5, 3.3, 'Product 1 ← N OrderItem'),
        (9, 7.6, 10.5, 8.5, ''),
        (9, 7.6, 10.5, 8.0, ''),
    ]

    for x1, y1, x2, y2, label in connections:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', lw=1, color='#333'))
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx, my, label, ha='center', va='bottom', fontsize=7,
                    style='italic', color='#333',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

    with PdfPages('er_diagram.pdf') as pdf:
        pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    print('ER diagram saved to er_diagram.pdf')


def draw_block_schema():
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    ax.set_title('Алгоритм разработки приложения\n(ГОСТ 19.701-90)', fontsize=14, fontweight='bold', pad=20)

    def draw_box(x, y, w, h, text, color='#F5DEB3', shape='rect'):
        if shape == 'ellipse':
            ellipse = mpatches.Ellipse((x + w / 2, y + h / 2), w, h, facecolor=color, edgecolor='#000', linewidth=1.5)
            ax.add_patch(ellipse)
        elif shape == 'diamond':
            diamond = mpatches.Polygon(
                [(x + w / 2, y), (x + w, y + h / 2), (x + w / 2, y + h), (x, y + h / 2)],
                facecolor=color, edgecolor='#000', linewidth=1.5
            )
            ax.add_patch(diamond)
        else:
            rect = mpatches.FancyBboxPatch(
                (x, y), w, h, boxstyle="round,pad=0.05", facecolor=color, edgecolor='#000', linewidth=1.5
            )
            ax.add_patch(rect)

        ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=8, fontweight='bold')

    def draw_arrow(x1, y1, x2, y2):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', lw=1.5, color='#000'))

    draw_box(3, 10.5, 4, 1, 'Начало', '#DEB887', 'ellipse')
    draw_arrow(5, 10.5, 5, 9.5)

    draw_box(2, 8.5, 6, 1, 'Загрузка приложения\n(Старт Django-сервера)', '#F5DEB3')
    draw_arrow(5, 8.5, 5, 7.5)

    draw_box(2.5, 6.5, 5, 1, 'Отображение окна входа\n(логин/пароль)', '#F5DEB3')
    draw_arrow(5, 6.5, 5, 5.5)

    draw_box(2, 4.5, 6, 1, 'Проверка авторизации', '#DEB887', 'diamond')
    draw_arrow(5, 4.5, 5, 3.5)
    ax.text(5.2, 4.0, 'Да', fontsize=8)
    draw_arrow(2, 5, 0.5, 5)
    ax.text(1.8, 4.8, 'Нет', fontsize=8)

    draw_box(0, 3.5, 3.5, 0.8, 'Отображение товаров\n(роль: Гость)', '#ADD8E6')
    draw_arrow(5, 3.5, 5, 2.5)

    draw_box(2.5, 1.5, 5, 1, 'Определение роли\nпользователя', '#DEB887', 'diamond')
    draw_arrow(5, 1.5, 5, 0.5)
    draw_arrow(2.5, 2.0, 0.5, 2.0)
    ax.text(2.0, 1.8, 'Клиент', fontsize=7)
    draw_arrow(7.5, 2.0, 9.5, 2.0)
    ax.text(8.0, 1.8, 'Менеджер', fontsize=7)

    draw_box(0, -0.5, 3.5, 0.8, 'Просмотр товаров\n(без фильтрации)', '#F5DEB3')

    draw_box(6, 3.5, 3.5, 0.8, 'Просмотр товаров\n(с фильтрацией, сортировкой, поиском)', '#F5DEB3')
    draw_arrow(9.5, 3.9, 9.5, 3.0)
    draw_box(6, 2.0, 3.5, 0.8, 'Просмотр заказов', '#F5DEB3')
    draw_arrow(9.5, 2.4, 9.5, 1.2)

    draw_box(6, 0.2, 3.5, 0.8, 'Добавление/редактирование/\nудаление (Администратор)', '#DEB887')

    with PdfPages('block_schema.pdf') as pdf:
        pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    print('Block schema saved to block_schema.pdf')


if __name__ == '__main__':
    draw_er_diagram()
    draw_block_schema()
