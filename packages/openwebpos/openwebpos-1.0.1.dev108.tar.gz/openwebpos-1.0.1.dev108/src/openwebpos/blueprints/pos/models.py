from openwebpos.extensions import db
from openwebpos.utils import gen_order_number
from openwebpos.utils.sql import DateTimeMixin, CRUDMixin


def get_all_ingredients_not_in_menu_item(menu_item_id):
    """
    Return all ingredients not in menu item.

    Args:
        menu_item_id (int): Menu item id.

    Returns:
        list: List of ingredients.
    """
    return Ingredient.query.filter(
        ~Ingredient.menu_item_ingredients.any(
            MenuItemIngredient.menu_item_id == menu_item_id)).all()


class Ingredient(db.Model, DateTimeMixin, CRUDMixin):
    """Ingredient model."""
    __tablename__ = 'ingredients'

    name = db.Column(db.String(255), nullable=False)
    menu_item_ingredients = db.relationship('MenuItemIngredient',
                                            backref='ingredient',
                                            lazy='dynamic')
    menu_item_addons = db.relationship('MenuItemAddon', backref='ingredient',
                                       lazy='dynamic')
    order_item_options = db.relationship('OrderItemOption',
                                         backref='ingredient', lazy='dynamic')
    addon = db.Column(db.Boolean, default=True, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    @staticmethod
    def insert_default_ingredients():
        """Insert default ingredients."""
        ingredients = [
            ('Cheese', True),
            ('Tomato', True),
            ('Lettuce', True),
            ('Onion', True),
            ('Pineapple', True),
            ('Sour Cream', True),
            ('Salsa', True),
            ('Avocado', False),
            ('Cilantro', False),
            ('Lime', False),
            ('Jalapeno', False),
        ]
        for name, addon in ingredients:
            ingredient = Ingredient.query.filter_by(name=name).first()
            if ingredient is None:
                ingredient = Ingredient(name=name, addon=addon)
                ingredient.save()

    def active_toggle(self):
        """Toggle active status."""
        self.active = not self.active
        self.update()

    def addon_toggle(self):
        """Toggle addon status."""
        self.addon = not self.addon
        self.update()

    def is_addon(self):
        """Check if ingredient is an addon."""
        return self.addon

    def __init__(self, **kwargs):
        super(Ingredient, self).__init__(**kwargs)


class MenuType(db.Model, DateTimeMixin, CRUDMixin):
    """Menu type model."""
    __tablename__ = 'menu_types'

    short_name = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    menu_categories = db.relationship('MenuCategory', backref='menu_type',
                                      lazy='dynamic',
                                      cascade='all, delete-orphan')

    def toggle(self):
        """Toggle active status."""
        self.active = not self.active
        return self.update()

    def has_categories(self):
        """Check if menu type has categories."""
        return self.menu_categories.count() > 0

    @staticmethod
    def insert_default_menu_types():
        """Insert default menu types."""
        menu_types = [
            {'short_name': 'food', 'name': 'Food', 'description': 'Food'},
            {'short_name': 'drink', 'name': 'Drink', 'description': 'Drink'},
            {'short_name': 'alcohol', 'name': 'Alcohol',
             'description': 'Alcohol'},
            {'short_name': 'dessert', 'name': 'Dessert',
             'description': 'Dessert'},
            {'short_name': 'other', 'name': 'Other', 'description': 'Other'},
        ]

        for menu_type in menu_types:
            menu_type = MenuType(**menu_type)
            menu_type.save()

    def __init__(self, **kwargs):
        super(MenuType, self).__init__(**kwargs)


class MenuCategory(db.Model, DateTimeMixin, CRUDMixin):
    """Menu category model."""
    __tablename__ = 'menu_categories'

    short_name = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    active = db.Column(db.Boolean, nullable=False, default=True)
    menu_type_id = db.Column(db.Integer, db.ForeignKey('menu_types.id'),
                             nullable=False)
    menu_items = db.relationship('MenuItem', backref='menu_category',
                                 lazy='dynamic', cascade='all, delete-orphan')

    @staticmethod
    def insert_default_menu_categories():
        """Insert default menu categories."""
        menu_categories = [
            {'short_name': 'pizza', 'name': 'Pizza', 'description': 'Pizza',
             'menu_type_id': 1},
        ]

        for menu_category in menu_categories:
            menu_category = MenuCategory(**menu_category)
            menu_category.save()

    def toggle(self):
        """Toggle active status."""
        self.active = not self.active
        return self.update()

    @staticmethod
    def create(**kwargs):
        """Create a new menu category."""
        menu_category = MenuCategory(**kwargs)
        return menu_category.save()

    def __init__(self, **kwargs):
        super(MenuCategory, self).__init__(**kwargs)

        if self.name:
            self.name = self.name.title()


class MenuItem(db.Model, DateTimeMixin, CRUDMixin):
    """Menu item model."""
    __tablename__ = 'menu_items'
    short_name = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    menu_category_id = db.Column(db.Integer,
                                 db.ForeignKey('menu_categories.id'),
                                 nullable=False)
    order_items = db.relationship('OrderItem', backref='menu_item',
                                  lazy='dynamic')
    menu_item_ingredients = db.relationship('MenuItemIngredient',
                                            backref='menu_item', lazy='dynamic',
                                            cascade="all, delete-orphan")
    menu_item_addons = db.relationship('MenuItemAddon', backref='menu_item',
                                       lazy='dynamic',
                                       cascade="all, delete-orphan")

    @staticmethod
    def insert_default_menu_items():
        """Insert default menu items."""
        menu_items = [
            {'short_name': 'pepperoni', 'name': 'Pepperoni',
             'description': 'Pepperoni', 'price': 1000,
             'menu_category_id': 1},
        ]

        for menu_item in menu_items:
            menu_item = MenuItem(**menu_item)
            menu_item.save()

    def toggle(self):
        """Toggle active status."""
        self.active = not self.active
        return self.update()

    def has_ingredients(self):
        """Check if menu item has ingredients."""
        return self.menu_item_ingredients.count() > 0

    def has_addons(self):
        """Check if menu item has addons."""
        return self.menu_item_addons.count() > 0

    def __init__(self, **kwargs):
        super(MenuItem, self).__init__(**kwargs)

        if self.name:
            self.name = self.name.title()


class MenuItemIngredient(db.Model, DateTimeMixin, CRUDMixin):
    """Menu item ingredient model."""
    __tablename__ = 'menu_item_ingredients'

    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'),
                             nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'),
                              nullable=False)

    def __init__(self, **kwargs):
        super(MenuItemIngredient, self).__init__(**kwargs)


class MenuItemAddon(db.Model, DateTimeMixin, CRUDMixin):
    """Menu item addon model."""
    __tablename__ = 'menu_item_addons'

    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'),
                             nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'),
                              nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0.00)

    def __init__(self, **kwargs):
        super(MenuItemAddon, self).__init__(**kwargs)


class OrderType(db.Model, CRUDMixin):
    """Order type model."""
    __tablename__ = 'order_types'
    name = db.Column(db.String(255), nullable=False, unique=True)
    deletable = db.Column(db.Boolean, default=True)
    active = db.Column(db.Boolean, default=True)
    orders = db.relationship('Order', backref='order_type', lazy='dynamic')

    def toggle(self):
        """Toggle active status."""
        self.active = not self.active
        return self.update()

    @staticmethod
    def insert_default_order_types():
        """Insert default order types."""
        order_types = [
            {'name': 'Phone'},
            {'name': 'Takeout', 'deletable': False},
            {'name': 'Dine In', 'deletable': False},
            {'name': 'Delivery', 'deletable': False},
            {'name': 'Drive Thru', 'deletable': False},
        ]

        for order_type in order_types:
            order_type = OrderType(**order_type)
            order_type.save()

    def __init__(self, **kwargs):
        super(OrderType, self).__init__(**kwargs)


class OrderPager(db.Model, CRUDMixin):
    """Order pager model."""
    __tablename__ = 'order_pagers'

    name = db.Column(db.String(255), nullable=False, unique=True)
    short_name = db.Column(db.String(20), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)
    in_use = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='order_pager', lazy='dynamic')

    @staticmethod
    def insert_default_order_pagers():
        """Insert default order pagers."""
        order_pagers = [
            {'name': 'Pager 1', 'short_name': '# 1'},
            {'name': 'Pager 2', 'short_name': '# 2'},
            {'name': 'Pager 3', 'short_name': '# 3'},
            {'name': 'Pager 4', 'short_name': '# 4'},
            {'name': 'Pager 5', 'short_name': '# 5'},
            {'name': 'Pager 6', 'short_name': '# 6'},
            {'name': 'Pager 7', 'short_name': '# 7'},
            {'name': 'Pager 8', 'short_name': '# 8'},
            {'name': 'Pager 9', 'short_name': '# 9'},
            {'name': 'Pager 10', 'short_name': '# 10'}
        ]

        for order_pager in order_pagers:
            order_pager = OrderPager(**order_pager)
            order_pager.save()

    def toggle(self):
        """Toggle active status."""
        self.active = not self.active
        return self.update()

    def toggle_in_use(self):
        """Toggle in use status."""
        self.in_use = not self.in_use
        return self.update()

    def available(self):
        """ Check if pagers exists in database and if pager is available."""
        if OrderPager.query.count() > 0:
            if self.active and not self.in_use:
                return True
        return False

    def __init__(self, **kwargs):
        super(OrderPager, self).__init__(**kwargs)


class Order(db.Model, CRUDMixin):
    """Order model."""
    __tablename__ = 'orders'
    order_number = db.Column(db.String(255), nullable=False, unique=True)
    order_type_id = db.Column(db.Integer, db.ForeignKey('order_types.id'))
    order_pager_id = db.Column(db.Integer, db.ForeignKey('order_pagers.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    order_items = db.relationship('OrderItem', backref='order', lazy='dynamic',
                                  cascade="all, delete-orphan")
    order_sections = db.relationship('OrderSection', backref='order',
                                     lazy='dynamic',
                                     cascade="all, delete-orphan")
    order_messages = db.relationship('OrderMessage', backref='order',
                                     lazy='dynamic',
                                     cascade="all, delete-orphan")
    tax_rate = db.Column(db.Integer, nullable=False, default=825)
    tax_total = db.Column(db.Integer, nullable=False, default=0)
    subtotal = db.Column(db.Integer, nullable=False, default=0)
    total = db.Column(db.Integer, nullable=False, default=0)
    invoice = db.relationship('Invoice', backref='order', uselist=False)
    invoiced = db.Column(db.Boolean, nullable=False, default=False)
    printed = db.Column(db.Boolean, nullable=False, default=False)
    print_count = db.Column(db.Integer, nullable=False, default=0)
    active = db.Column(db.Boolean, default=True)
    order_item_options = db.relationship('OrderItemOption', backref='order',
                                         lazy='dynamic',
                                         cascade="all, delete-orphan")

    def is_printed(self):
        """Check if order has been printed."""
        return self.printed

    def set_printed(self):
        """Set order as printed."""
        self.printed = True
        self.update_print_count()
        return self.update()

    def update_print_count(self):
        """Update print count."""
        self.print_count += 1
        return self.update()

    def is_invoiced(self):
        """Return True if the order has been invoiced."""
        return self.invoiced

    def not_invoiced(self):
        """Return True if the order has not been invoiced."""
        return not self.invoiced

    def set_invoiced(self):
        """Set the order as invoiced."""
        self.invoiced = True
        return self.update()

    def toggle(self):
        """Toggle active status."""
        self.active = not self.active
        return self.update()

    def order_subtotal(self):
        """Return the order subtotal."""
        return sum([order_item.total for order_item in self.order_items])

    def order_tax_total(self):
        """Return the order tax total."""
        return self.order_subtotal() * self.tax_rate / 10000

    def order_total(self):
        """Return the order total."""
        return self.order_subtotal() + self.order_tax_total()

    def total_paid(self):
        """Return the total paid for the order."""
        return sum([payment.amount for payment in self.payments])

    def has_balance(self):
        """Return True if the order has a balance."""
        return self.order_total() > self.invoice.total_paid()

    def has_items(self):
        """Return True if the order has items."""
        return self.order_items.count() > 0

    def has_pager(self):
        """Return True if the order has a pager."""
        return self.order_pager_id is not None

    def has_customer(self):
        """Return True if the order has a customer."""
        return self.customer_id is not None

    def update_totals(self):
        """Update the order totals."""
        self.tax_total = self.order_tax_total()
        self.subtotal = self.order_subtotal()
        self.total = self.order_total()
        return self.update()

    def create_order_section(self, **kwargs):
        """Create an order section."""
        order_section = OrderSection(**kwargs)
        order_section.order_id = self.id
        return order_section.save()

    def order_sections_has_items(self):
        """Return True if order sections has items."""
        return self.order_sections.count() > 0

    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        self.order_number = gen_order_number()
        self.total = self.order_total()
        self.create_order_section()


class OrderItem(db.Model, CRUDMixin):
    """Order item model."""
    __tablename__ = 'order_items'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    order_section_id = db.Column(db.Integer, db.ForeignKey('order_sections.id'))
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'))
    quantity = db.Column(db.Integer, default=1)
    total = db.Column(db.Integer, default=0)
    order_item_options = db.relationship('OrderItemOption',
                                         backref='order_item', lazy='dynamic',
                                         cascade="all, delete-orphan")
    active = db.Column(db.Boolean, default=True)

    def order_item_total(self):
        """Return the order item total."""
        menu_item = MenuItem.query.get(self.menu_item_id)
        return (self.quantity * menu_item.price) + (
                self.quantity * self.order_item_options_total())

    def has_order_item_options(self):
        """Return True if the order item has options."""
        return self.order_item_options.count() > 0

    def has_order_item_addons(self):
        """Return True if the order item has addons."""
        return self.order_item_options.filter_by(option_type='add').count() > 0

    def order_item_options_total(self):
        """Return the order item options total."""
        return sum([order_item_option.price for order_item_option in
                    self.order_item_options])

    def get_order_section_total(self):
        """Return the order section total."""
        return sum(
            [order_item.total for order_item in self.order_section.order_items])

    def update_totals(self):
        """Update the order item totals."""
        self.total = self.order_item_total()
        return self.update()

    def update_quantity(self, quantity):
        """Update the order item quantity."""
        self.quantity = quantity
        return self.update_totals()

    def __init__(self, **kwargs):
        super(OrderItem, self).__init__(**kwargs)

        self.total = self.order_item_total()


class OrderSection(db.Model, CRUDMixin):
    """Order section model."""
    __tablename__ = 'order_sections'

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order_sections = db.relationship('OrderItem', backref='order_section',
                                     lazy='dynamic',
                                     cascade="all, delete-orphan")

    def get_order_section_total(self):
        """Return the order section total."""
        _order_items = OrderItem.query.filter_by(order_section_id=self.id)
        return sum([order_item.total for order_item in _order_items])

    def has_items(self):
        """Return True if the order section has items."""
        return self.order_sections.count() > 0

    def last_section(self):
        """Return True if the order section is the last section."""
        return self.order.order_sections[-1] == self

    def __init__(self, **kwargs):
        super(OrderSection, self).__init__(**kwargs)


class OrderItemOption(db.Model, CRUDMixin):
    """Order item option model."""
    __tablename__ = 'order_item_options'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    order_item_id = db.Column(db.Integer, db.ForeignKey('order_items.id'),
                              nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'),
                              nullable=False)
    option_type = db.Column(db.String(255), nullable=False, default='add')
    price = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, **kwargs):
        super(OrderItemOption, self).__init__(**kwargs)


class OrderMessage(db.Model, CRUDMixin):
    """Order message model."""
    __tablename__ = 'order_messages'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sid = db.Column(db.String(255), nullable=False)

    def __init__(self, **kwargs):
        super(OrderMessage, self).__init__(**kwargs)
