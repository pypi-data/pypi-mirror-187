import sqlalchemy as sa
import sqlalchemy.orm
from flask_login import LoginManager
from flask_sqlalchemy import Model, SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension


class CustomModel(Model):
    @sa.orm.declared_attr
    def id(cls):
        for base in cls.__mro__[1:-1]:
            if getattr(base, "__table__", None) is not None:
                col_type = sa.ForeignKey(base.id)
                break
        else:
            col_type = sa.Integer
        return sa.Column(col_type, primary_key=True)


db = SQLAlchemy(model_class=CustomModel)
login_manager = LoginManager()
toolbar = DebugToolbarExtension()
