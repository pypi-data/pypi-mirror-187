from flask import Blueprint, render_template, redirect, url_for

from openwebpos.blueprints.pos.forms import MenuTypeForm, MenuCategoryForm, \
    MenuItemForm, MenuItemIngredientForm, MenuItemAddonForm, IngredientForm
from openwebpos.blueprints.pos.models import MenuType, MenuCategory, MenuItem, \
    MenuItemIngredient, MenuItemAddon, Ingredient

bp = Blueprint('menu', __name__, url_prefix='/menu',
               template_folder='../templates')

@bp.route('/')
def index():
    """
    Displays the menu types, categories and items.
    """
    return render_template('admin/menu/index.html', title='Menus')

@bp.get('/types')
def types():
    """Menu types view."""
    menu_types = MenuType.query.all()
    return render_template('admin/menu/types.html', title='Menu Types',
                           menu_types=menu_types)


@bp.route('/types/add', methods=['GET', 'POST'])
def types_add():
    """Menu types add view."""
    form = MenuTypeForm()
    if form.validate_on_submit():
        mt = MenuType()
        form.populate_obj(mt)
        mt.save()
        return redirect(url_for('.types'))
    return render_template('admin/menu/types_add.html', title='Add Menu Type',
                           form=form)


@bp.route('/types/edit/<int:mt_id>', methods=['GET', 'POST'])
def types_edit(mt_id):
    """
    Menu types edit view.

    Arguments:
        mt_id {int} -- Menu type id
    """
    menu_type = MenuType.query.get_or_404(mt_id)
    form = MenuTypeForm(obj=menu_type)
    if form.validate_on_submit():
        form.populate_obj(menu_type)
        menu_type.save()
        return redirect(url_for('.types'))
    return render_template('admin/menu/types_edit.html',
                           title='Edit Menu Type', form=form)


@bp.get('/types/delete/<int:mt_id>')
def types_delete(mt_id):
    """Menu types delete view."""
    menu_type = MenuType.query.get_or_404(mt_id)
    menu_type.delete()
    return redirect(url_for('.types'))


@bp.get('/type/toggle/<int:mt_id>')
def toggle_type(mt_id):
    """Toggle menu type active status."""
    menu_type = MenuType.query.get_or_404(mt_id)
    menu_type.toggle()
    return redirect(url_for('.types'))


@bp.get('/categories')
def categories():
    """Menu categories view."""
    menu_categories = MenuCategory.query.all()
    return render_template('admin/menu/categories.html',
                           title='Menu Categories',
                           menu_categories=menu_categories)


@bp.route('/categories/add', methods=['GET', 'POST'])
def categories_add():
    """Menu categories add view."""
    form = MenuCategoryForm()
    form.menu_type_id.choices = [(mt.id, mt.name) for mt in
                                 MenuType.query.all()]
    if form.validate_on_submit():
        mc = MenuCategory()
        form.populate_obj(mc)
        mc.save()
        return redirect(url_for('.categories'))
    return render_template('admin/menu/categories_add.html',
                           title='Add Menu Category', form=form)


@bp.route('/categories/edit/<int:mc_id>', methods=['GET', 'POST'])
def categories_edit(mc_id):
    """
    Menu categories edit view.

    Arguments:
        mc_id {int} -- Menu category id
    """
    menu_category = MenuCategory.query.get_or_404(mc_id)
    form = MenuCategoryForm(obj=menu_category)
    form.menu_type_id.choices = [(mt.id, mt.name) for mt in
                                 MenuType.query.all()]
    if form.validate_on_submit():
        form.populate_obj(menu_category)
        menu_category.save()
        return redirect(url_for('.categories'))
    return render_template('admin/menu/categories_edit.html',
                           title='Edit Menu Category', form=form)


@bp.get('/categories/delete/<int:mc_id>')
def categories_delete(mc_id):
    """Menu categories delete view."""
    menu_category = MenuCategory.query.get_or_404(mc_id)
    menu_category.delete()
    return redirect(url_for('.categories'))


@bp.get('/category/toggle/<int:mc_id>')
def toggle_category(mc_id):
    """Toggle menu category active status."""
    menu_category = MenuCategory.query.get_or_404(mc_id)
    menu_category.toggle()
    return redirect(url_for('.categories'))


@bp.get('/items')
def items():
    """Menu items view."""
    menu_items = MenuItem.query.all()
    return render_template('admin/menu/items.html', title='Menu Items',
                           menu_items=menu_items)


@bp.route('/items/add', methods=['GET', 'POST'])
def items_add():
    """Menu items add view."""
    form = MenuItemForm()
    form.menu_category_id.choices = [(mc.id, mc.name) for mc in
                                     MenuCategory.query.all()]
    if form.validate_on_submit():
        mi = MenuItem()
        # convert price to cents
        form.price.data = int(form.price.data * 100)
        p = form.price.data
        print(p)
        form.populate_obj(mi)
        mi.save()
        return redirect(url_for('.items'))
    return render_template('admin/menu/items_add.html', title='Add Menu Item',
                           form=form)


@bp.route('/items/edit/<int:mi_id>', methods=['GET', 'POST'])
def items_edit(mi_id):
    """
    Menu items edit view.

    Arguments:
        mi_id {int} -- Menu item id
    """
    menu_item = MenuItem.query.get_or_404(mi_id)
    form = MenuItemForm(obj=menu_item)
    form.menu_category_id.choices = [(mc.id, mc.name) for mc in
                                     MenuCategory.query.all()]
    if form.validate_on_submit():
        form.populate_obj(menu_item)
        menu_item.update()
        return redirect(url_for('.items'))
    return render_template('admin/menu/items_edit.html',
                           title='Edit Menu Item', form=form)


@bp.get('/items/delete/<int:mi_id>')
def items_delete(mi_id):
    """Menu items delete view."""
    menu_item = MenuItem.query.get_or_404(mi_id)
    menu_item.delete()
    return redirect(url_for('.items'))


@bp.get('/item/toggle/<int:mi_id>')
def toggle_item(mi_id):
    """Toggle menu item active status."""
    menu_item = MenuItem.query.get_or_404(mi_id)
    menu_item.toggle()
    return redirect(url_for('.items'))


@bp.get('/item/ingredients/<int:mi_id>')
def item_ingredients(mi_id):
    """
    Menu item ingredients view.

    Arguments:
        mi_id {int} -- Menu item id
    """
    mi_ingredients = MenuItemIngredient.query.filter_by(
        menu_item_id=mi_id).all()
    mi = MenuItem.query.get_or_404(mi_id)
    return render_template('admin/menu/item_ingredients.html',
                           title='Menu Item Ingredients',
                           mi_ingredients=mi_ingredients, mi=mi)


@bp.route('/item/ingredients/add/<int:mi_id>', methods=['GET', 'POST'])
def item_ingredients_add(mi_id):
    """
    Menu item ingredients add view.

    Arguments:
        mi_id {int} -- Menu item id
    """
    form = MenuItemIngredientForm()
    form.set_choices()
    mi = MenuItem.query.get_or_404(mi_id)
    if form.validate_on_submit():
        mii = MenuItemIngredient(menu_item_id=mi_id)
        form.populate_obj(mii)
        mii.save()
        return redirect(url_for('.item_ingredients', mi_id=mi_id))
    return render_template('admin/menu/item_ingredients_add.html', mi=mi,
                           title='Add Menu Item Ingredient', form=form)


@bp.route('/item/ingredients/edit/<int:mii_id>', methods=['GET', 'POST'])
def item_ingredients_edit(mii_id):
    """
    Menu item ingredients edit view.

    Arguments:
        mii_id {int} -- Menu item ingredient id
    """
    mi_ingredient = MenuItemIngredient.query.get_or_404(mii_id)
    mi = MenuItem.query.get_or_404(mi_ingredient.menu_item_id)
    form = MenuItemIngredientForm(obj=mi_ingredient)
    form.set_choices()
    if form.validate_on_submit():
        form.populate_obj(mi_ingredient)
        mi_ingredient.update()
        return redirect(url_for('.item_ingredients',
                                mi_id=mi_ingredient.menu_item_id))
    return render_template('admin/menu/item_ingredients_edit.html', mi=mi,
                           title='Edit Menu Item Ingredient', form=form)


@bp.get('/item/ingredients/delete/<int:mii_id>')
def item_ingredients_delete(mii_id):
    """
    Menu item ingredients delete view.

    Arguments:
        mii_id {int} -- Menu item ingredient id
    """
    mi_ingredient = MenuItemIngredient.query.get_or_404(mii_id)
    mi_ingredient.delete()
    return redirect(url_for('.item_ingredients',
                            mi_id=mi_ingredient.menu_item_id))


@bp.get('/item/addons/<int:mi_id>')
def item_addons(mi_id):
    """
    Menu item addons view.

    Arguments:
        mi_id {int} -- Menu item id
    """
    mi_addons = MenuItemAddon.query.filter_by(menu_item_id=mi_id).all()
    mi = MenuItem.query.get_or_404(mi_id)
    return render_template('admin/menu/item_addons.html',
                           title='Menu Item Addons',
                           mi_addons=mi_addons, mi=mi)


@bp.route('/item/addons/add/<int:mi_id>', methods=['GET', 'POST'])
def item_addons_add(mi_id):
    """
    Menu item addons add view.

    Arguments:
        mi_id {int} -- Menu item id
    """
    form = MenuItemAddonForm()
    form.set_choices(mi_id)
    mi = MenuItem.query.get_or_404(mi_id)
    if form.validate_on_submit():
        mia = MenuItemAddon(menu_item_id=mi_id)
        form.price.data = int(form.price.data * 100)
        form.populate_obj(mia)
        mia.save()
        return redirect(url_for('.item_addons', mi_id=mi_id))
    return render_template('admin/menu/item_addons_add.html', mi=mi,
                           title='Add Menu Item Addon', form=form)


@bp.route('/item/addons/edit/<int:mia_id>', methods=['GET', 'POST'])
def item_addons_edit(mia_id):
    """
    Menu item addons edit view.

    Arguments:
        mia_id {int} -- Menu item addon id
    """
    mi_addon = MenuItemAddon.query.get_or_404(mia_id)
    mi = MenuItem.query.get_or_404(mi_addon.menu_item_id)
    form = MenuItemAddonForm(obj=mi_addon)
    form.set_choices(mi_addon.menu_item_id)
    if form.validate_on_submit():
        form.populate_obj(mi_addon)
        mi_addon.update()
        return redirect(url_for('.item_addons',
                                mi_id=mi_addon.menu_item_id))
    return render_template('admin/menu/item_addons_edit.html', mi=mi,
                           title='Edit Menu Item Addon', form=form)


@bp.get('/item/addons/delete/<int:mia_id>')
def item_addons_delete(mia_id):
    """
    Menu item addons delete view.

    Arguments:
        mia_id {int} -- Menu item addon id
    """
    mi_addon = MenuItemAddon.query.get_or_404(mia_id)
    mi_addon.delete()
    return redirect(url_for('.item_addons',
                            mi_id=mi_addon.menu_item_id))


@bp.get('/ingredients')
def ingredients():
    """Ingredients view."""
    _ingredients = Ingredient.query.all()
    return render_template('admin/menu/ingredients.html',
                           title='Ingredients', ingredients=_ingredients)


@bp.route('/ingredients/add', methods=['GET', 'POST'])
def ingredients_add():
    """Ingredients add view."""
    form = IngredientForm()
    if form.validate_on_submit():
        ingredient = Ingredient()
        form.populate_obj(ingredient)
        ingredient.save()
        return redirect(url_for('.ingredients'))
    return render_template('admin/menu/ingredients_add.html',
                           title='Add Ingredient', form=form)


@bp.route('/ingredients/edit/<int:ingredient_id>', methods=['GET', 'POST'])
def ingredients_edit(ingredient_id):
    """
    Ingredients edit view.

    Arguments:
        ingredient_id {int} -- Ingredient id
    """
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    form = IngredientForm(obj=ingredient)
    if form.validate_on_submit():
        form.populate_obj(ingredient)
        ingredient.update()
        return redirect(url_for('.ingredients'))
    return render_template('admin/menu/ingredients_edit.html',
                           title='Edit Ingredient', form=form)


@bp.get('/ingredients/delete/<int:ingredient_id>')
def ingredients_delete(ingredient_id):
    """
    Ingredients delete view.

    Arguments:
        ingredient_id {int} -- Ingredient id
    """
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    ingredient.delete()
    return redirect(url_for('.ingredients'))


@bp.get('/ingredients/active-toggle/<int:ingredient_id>')
def ingredients_active_toggle(ingredient_id):
    """
    Ingredients active toggle view.

    Arguments:
        ingredient_id {int} -- Ingredient id
    """
    Ingredient.query.get_or_404(ingredient_id).active_toggle()
    return redirect(url_for('.ingredients'))


@bp.get('/ingredients/addon-toggle/<int:ingredient_id>')
def ingredients_addon_toggle(ingredient_id):
    """
    Ingredients addon toggle view.

    Arguments:
        ingredient_id {int} -- Ingredient id
    """
    Ingredient.query.get_or_404(ingredient_id).addon_toggle()
    return redirect(url_for('.ingredients'))
