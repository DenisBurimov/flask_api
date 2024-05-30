from app import db
from uuid import uuid4


class ModelMixin(object):
    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self
