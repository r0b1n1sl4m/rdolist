from app.extensions import db


class ModelMixin(object):
    """
    Common database fields and functions.
    """

    # Common fields
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def save(self):
        """
        Save model data.
        :return: Model instance
        """
        db.session.add(self)
        return self

    def delete(self):
        """
        Delete model data.
        """
        db.session.delete(self)
