from app import db


class ModelMixin(object):
    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self
