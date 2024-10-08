{
    'name': 'Kế Hoạch Kinh Doanh',
    'version': '1.0',
    'category': 'Sales',
    'description': """
        KH kinh doanh
    """,
    'author': 'Erik.',
    'depends': ['sale'],
    'data': [
        'views/plan_sale_order.xml',
        'views/sale_order_inherit.xml',
        'views/email_template_views.xml',
        # 'security/ir.model.access.csv',
        'security/plan_sale_order_security.xml',
    ],
}