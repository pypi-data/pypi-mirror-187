from .admin.views import admin as admin_blueprint
from .pos.views import pos as pos_bp
from .user.views import user as user_bp

blueprints = [
    user_bp,
    pos_bp,
    admin_blueprint
]
