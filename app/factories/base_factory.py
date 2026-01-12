# app/factories/base_factory.py
from app.extension import db
from app.utils.decorators import static_all_methods


@static_all_methods
class BaseFactory:

    def create_one(make_func, model_class):
        """
        Create one record in DB using make_func to generate data dict.
        """
        data = make_func()  # data is a dict
        obj = model_class(**data)  # convert to SQLAlchemy model instance
        db.session.add(obj)
        db.session.commit()
        return obj

    def create_many(make_func, model_class, count=1):
        """
        Create many records in DB using make_func to generate data dicts.
        """
        objects = []
        for _ in range(count):
            data = make_func()
            obj = model_class(**data)
            db.session.add(obj)
            objects.append(obj)

        db.session.commit()
        return objects
