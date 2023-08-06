import importlib.util
import os
import sys
from datetime import datetime
from importlib.metadata import version

from flask import (Flask, send_from_directory, redirect, url_for,
                   render_template, request, current_app)
from sqlalchemy.exc import OperationalError
from sqlalchemy_utils import database_exists

from openwebpos.blueprints import blueprints
from openwebpos.blueprints.admin.models import Company, Branch
from openwebpos.blueprints.billing.models import PaymentMethod
from openwebpos.blueprints.pos.models import (
    MenuType, MenuCategory, MenuItem, OrderType, Ingredient, OrderPager)
from openwebpos.blueprints.user.models import User, Role, Permission, \
    RolePermission
from openwebpos.extensions import db, login_manager, toolbar
from openwebpos.utils import create_folder, create_file, gen_urlsafe_token
from openwebpos.utils.money import cents_to_dollars


def insert_default_data() -> None:
    """
    Insert default data into the database.
    """
    # Insert default user
    Company.insert_default_company()
    Branch.insert_default_branch()
    Role.insert_default_roles()
    Permission.insert_default_permissions()
    RolePermission.insert_default_role_permissions()
    User.insert_default_user()
    MenuType.insert_default_menu_types()
    OrderType.insert_default_order_types()
    PaymentMethod.insert_default_payment_methods()
    MenuCategory.insert_default_menu_categories()
    MenuItem.insert_default_menu_items()
    Ingredient.insert_default_ingredients()
    OrderPager.insert_default_order_pagers()


def open_web_pos(app_path=os.getcwd(), instance_dir=os.path.join(os.getcwd(), 'instance')):
    """
    Create the Flask app instance.

    Args:
        app_path (str): Path to the app directory.
        instance_dir (str): Path to the instance folder.

    Returns:
        Flask: Flask app instance.
    """
    template_dir = 'ui/templates'
    static_dir = 'ui/static'
    base_path = os.path.abspath(os.path.dirname(__file__))

    # Create instance folder if it doesn't exist
    if os.path.isdir(instance_dir):
        if os.path.isfile(os.path.join(instance_dir, '__init__.py')) is False:
            create_file(file_path=instance_dir,
                        file_name='__init__.py')
    else:
        create_folder(folder_path=app_path, folder_name='instance')

    # Create the upload folder if it doesn't exist
    if os.path.isdir(os.path.join(app_path, 'uploads')) is False:
        create_folder(folder_path=app_path, folder_name='uploads')

    # create_file(file_path=os.getcwd(), file_name='.env',
    #             file_content=f'SECRET_KEY="{gen_urlsafe_token(64)}"')

    app = Flask(__name__, template_folder=template_dir,
                static_folder=static_dir, instance_relative_config=True,
                instance_path=instance_dir)

    # Default settings
    app.config.from_pyfile(os.path.join(base_path, 'config/settings.py'))
    # Instance settings (overrides default settings)
    app.config.from_pyfile(os.path.join('settings.py'), silent=True)

    @app.context_processor
    def utility_processor():

        def format_currency(amount, convert_to_dollars=True) -> str:
            """
            Format currency.

            Args:
                amount (int): Amount to format.
                convert_to_dollars (bool): Convert to dollars.

            Returns:
                str: Formatted currency.

            TODO: Add the ability to change the currency symbol.
            """
            # currency_symbol = app.config['CURRENCY_SYMBOL', '$']
            currency_symbol = '$'
            if convert_to_dollars:
                amount = cents_to_dollars(amount)
            return f'{currency_symbol}{amount:,.2f}'

        def format_phone_number(number: str) -> str:
            """
            Format phone number.

            Args:
                number (str): Phone number.

            Returns:
                str: Formatted phone number.
            """
            return f'({number[0:3]}) {number[3:6]}-{number[6:10]}'

        def convert_to_hex(value: int) -> str:
            """
            Convert string to hex.

            Args:
                value (int): Value to convert.

            Returns:
                str: Hex value.
            """
            return hex(value)

        def openwebpos_version():
            """
            Get the application version.

            Returns:
                str: Application version.

            Example:
                {{ openwebpos_version() }}
            """
            try:
                if "openwebpos" in sys.modules:
                    return version("openwebpos")
                else:
                    spec = importlib.util.find_spec("openwebpos")
                    if spec is None:
                        return "0.0.0"
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    return version("openwebpos")
            except ModuleNotFoundError:
                return "openwebpos not installed"

        def get_package_version(package: str) -> str:
            """
            Get installed package version.

            Args:
                package: String: Name of package

            Return:
                String: Package version

            Example:
                {{ get_package_version('flask') }}
            """
            try:
                if package in sys.modules:
                    # Module is already loaded
                    return version(package)
                else:
                    # Module is not loaded
                    spec = importlib.util.find_spec(package)
                    if spec is None:
                        return 'Not Installed'
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    return version(package)
            except ModuleNotFoundError:
                return f'{package} not installed'

        def company_name() -> str:
            """
            Get company name from database.

            Returns:
                String: Company name.

            Example:
                {{ company_name() }}
            """
            try:
                from openwebpos.blueprints.admin.models import Company
            except ModuleNotFoundError:
                return 'Company Name'
            company = Company.query.first()
            return company.name if company else 'OpenWebPOS'

        def previous_url() -> str:
            """
            Get previous URL.

            Returns:
                String: Previous URL.

            Example:
                {{ previous_url() }}
            """
            return request.referrer

        return dict(get_package_version=get_package_version,
                    company_name=company_name,
                    openwebpos_version=openwebpos_version,
                    previous_url=previous_url, format_currency=format_currency,
                    format_phone_number=format_phone_number,
                    convert_to_hex=convert_to_hex)

    @app.template_filter()
    def format_datetime(value, schema='full'):
        """
        Format datetime object to a string.

        schema: full, short, time, date

        Args:
            value (datetime): Datetime object.
            schema (str): Schema to format the datetime. Default: 'full'
                        default: YYYY-MM-DD HH:MM:SS
                        date: YYYY-MM-DD
                        short_date: MM/DD/YYYY
                        time: HH:MM:SS

        Returns:
            str: Formatted datetime.

        Examples:
            {{ datetime | format_datetime }}
            {{ datetime | format_datetime('short') }}

        """
        if value is None:
            return ''

        if schema == 'full':
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif schema == 'date':
            return value.strftime('%Y-%m-%d')
        elif schema == 'short':
            return value.strftime('%m/%d/%y')
        elif schema == 'time':
            return value.strftime('%H:%M:%S')

    # Register routes
    routes(app)

    # Load extensions
    extensions(app)

    return app


def extensions(app):
    """
    Register Extensions.

    Args:
        app (Flask): Flask app instance.
    """
    # from openwebpos.extensions import db, login_manager
    db.init_app(app)
    login_manager.init_app(app)
    toolbar.init_app(app)

    @login_manager.user_loader
    def load_user(uid):
        """
        Load user from the database.

        Args:
            uid (int): User ID.

        Returns:
            User: User object.

        TODO: Add exception errors to log file.
        """
        try:
            return User.query.get(uid)
        except OperationalError:
            print('Database not configured')

    login_manager.login_view = 'user.login'

    return app


def routes(app):
    """
    Register Routes.

    Args:
        app (Flask): Flask app instance.
    """
    from openwebpos.forms import DatabaseConfigForm

    @app.route('/')
    def index():
        if database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            return redirect(url_for('pos.index'))
        return redirect(url_for('database_config'))

    @app.route('/sw.js', methods=['GET'])
    def sw():
        return current_app.send_static_file('sw.js')

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.get('/database_config')
    def database_config():
        form = DatabaseConfigForm()
        if database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            return redirect(url_for('pos.index'))
        return render_template('database_config.html', title='Database Config',
                               form=form)

    @app.post('/database_config')
    def database_config_post():
        form = DatabaseConfigForm()
        if form.validate_on_submit():
            if form.dialect.data == 'sqlite':
                create_file(file_path=os.getcwd(),
                            file_name='instance/settings.py',
                            file_mode='w',
                            file_content="DB_DIALECT = 'sqlite'\n")
                db.create_all()
                insert_default_data()
                lines = [
                    "DB_CONFIGURED=True",
                    "DB_DIALECT=" + "'" + form.dialect.data + "'"
                ]
                with open(os.path.join(os.getcwd(), '.env'), 'w') as f:
                    f.write('\n'.join(lines))
                return redirect(url_for('user.login'))
            else:
                dialect = "DB_DIALECT = " + "'" + form.dialect.data + "'" + "\n"
                create_file(file_path=os.getcwd(),
                            file_name='instance/settings.py',
                            file_mode='w',
                            file_content=dialect)
                try:
                    db.create_all()
                    insert_default_data()
                except ConnectionError:
                    pass
                lines = [
                    "DB_CONFIGURED=True",
                    "DB_DIALECT=" + "'" + form.dialect.data + "'",
                    "DB_USER=" + "'" + form.username.data + "'",
                    "DB_PASS=" + "'" + form.password.data + "'",
                    "DB_HOST=" + "'" + form.host.data + "'",
                    "DB_PORT=" + "'" + form.port.data + "'",
                    "DB_NAME=" + "'" + form.database.data + "'"
                ]
                with open(os.path.join(os.getcwd(), '.env'), 'w') as f:
                    f.write('\n'.join(lines))
                return redirect(url_for('user.login'))
        return redirect(url_for('pos.index'))

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app
