import pytz
from datetime import datetime
from openwebpos.extensions import db

timezone = pytz.timezone('America/Chicago')
now = datetime.now(tz=timezone)


class DateTimeMixin(object):
    """
    Mixin to add created_at and updated_at fields to models.
    """
    created_at = db.Column(db.DateTime(timezone=True), default=now)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=now)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)


class CRUDMixin(object):
    """
    Mixin that adds convenience methods for CRUD (create, read, update, delete)
    operations.
    """

    def save(self, commit=True):
        """
        Save the record.

        Args:
            commit (bool): Commit the record. Default: True

        Returns:
            Model: Model instance.
        """
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def read(self):
        """
        Return the model as a dictionary.

        Returns:
            dict: Model as a dictionary.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update(self, **kwargs):
        """
        Update specific fields of a record.

        Args:
            **kwargs: Keyword arguments to pass to the model.

        Returns:
            Model: Model instance.
        """
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save() or self

    def delete(self):
        """
        Remove the record from the database.

        Returns:
            Model: Model instance.
        """
        db.session.delete(self)
        return db.session.commit()

    def __str__(self):
        """
        Return the string representation of the model.

        Returns:
            str: String representation of the model.
        """
        obj_id = hex(id(self))
        columns = [c.name for c in self.__table__.columns]
        data = ', '.join(['{}={}'.format(c, getattr(self, c)) for c in columns])
        return '<{} {}>'.format(obj_id, data)
