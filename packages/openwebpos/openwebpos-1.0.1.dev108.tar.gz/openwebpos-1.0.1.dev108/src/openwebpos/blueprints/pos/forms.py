from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField, IntegerField,
                     FloatField)
from wtforms.validators import DataRequired, Length, NumberRange

from openwebpos.blueprints.pos.models import MenuType, MenuCategory, Ingredient, \
    get_all_ingredients_not_in_menu_item


class MenuTypeForm(FlaskForm):
    """
    Form for admin to add or edit a menu type

    Extends:
        FlaskForm

    Variables:
        short_name {StringField} -- Short name of the menu type
        name {StringField} -- Name of the menu type
        description {StringField} -- Description of the menu type
        submit {SubmitField} -- Submit button

    Returns:
        FlaskForm: Form for admin to add or edit a menu type

    Example:
        >>> form = MenuTypeForm()
    """
    short_name = StringField('Short Name',
                             validators=[DataRequired(), Length(max=20)])
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    description = StringField('Description',
                              validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Submit')


class MenuCategoryForm(FlaskForm):
    """
    Form for admin to add or edit a menu category

    Extends:
        FlaskForm

    Variables:
        menu_type_id {SelectField} -- Menu type id
        short_name {StringField} -- Short name of the menu category
        name {StringField} -- Name of the menu category
        description {StringField} -- Description of the menu category
        submit {SubmitField} -- Submit button

    Returns:
        FlaskForm: Form for admin to add or edit a menu category

    Example:
        >>> form = MenuCategoryForm()
    """
    menu_type_id = SelectField('Menu Type', coerce=int)
    short_name = StringField('Short Name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    description = StringField('Description')
    submit = SubmitField('Submit')

    def set_choices(self):
        """Set choices for menu_type_id."""
        self.menu_type_id.choices = [(menu_type.id, menu_type.name)
                                     for menu_type in MenuType.query.all()]


class MenuItemForm(FlaskForm):
    """
    Form for admin to add or edit a menu item

    Extends:
        FlaskForm

    Returns:
        FlaskForm: Form for admin to add or edit a menu item

    Example:
        >>> form = MenuItemForm()
    """
    menu_category_id = SelectField('Menu Category', coerce=int)
    short_name = StringField('Short Name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    description = StringField('Description')
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')

    def set_choices(self):
        """Set choices for menu_category_id."""
        self.menu_category_id.choices = [(menu_category.id, menu_category.name)
                                         for menu_category in
                                         MenuCategory.query.all()]


class QuantityForm(FlaskForm):
    """
    Form for admin to add or edit a quantity

    Extends:
        FlaskForm

    Returns:
        FlaskForm: Form for admin to add or edit a quantity

    Example:
        >>> form = QuantityForm()
    """
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')


class IngredientForm(FlaskForm):
    """
    Form for admin to add or edit an ingredient

    Extends:
        FlaskForm

    Returns:
        FlaskForm: Form for admin to add or edit an ingredient

    Example:
        >>> form = IngredientForm()
    """
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Submit')


class MenuItemIngredientForm(FlaskForm):
    """
    Form for admin to add or edit a menu item ingredient

    Extends:
        FlaskForm

    Returns:
        FlaskForm: Form for admin to add or edit a menu item ingredient

    Example:
        >>> form = MenuItemIngredientForm()
    """
    ingredient_id = SelectField('Ingredient', coerce=int)
    # quantity = IntegerField('Quantity')
    # price = FloatField('Price', validators=[NumberRange(min=0)])
    submit = SubmitField('Submit')

    def set_choices(self):
        """Set choices for ingredient_id."""
        self.ingredient_id.choices = [(ingredient.id, ingredient.name)
                                      for ingredient in
                                      Ingredient.query.all()]


class MenuItemAddonForm(FlaskForm):
    """
    Form for admin to add or edit a menu item addon

    Extends:
        FlaskForm

    Returns:
        FlaskForm: Form for admin to add or edit a menu item addon

    Example:
        >>> form = MenuItemAddonForm()
    """
    ingredient_id = SelectField('Ingredient', coerce=int)
    price = FloatField('Price', validators=[NumberRange(min=0)], default=0.50)
    submit = SubmitField('Submit')

    def set_choices(self, menu_item_id):
        """Set choices for ingredient_id."""
        addon_ingredients = get_all_ingredients_not_in_menu_item(menu_item_id)
        self.ingredient_id.choices = [(ingredient.id, ingredient.name)
                                      for ingredient in
                                      addon_ingredients]


class OrderPagerForm(FlaskForm):
    """
    Form for admin to add pager for orders

    Extends:
        FlaskForm

    Returns:
        FlaskForm: Form for admin to add pager for orders

    Example:
        >>> form = OrderPagerForm()
    """
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=100)])
    short_name = StringField('Short Name',
                             validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Submit')
