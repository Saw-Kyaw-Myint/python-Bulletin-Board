# app/seeders/user_seeder.py
from app.factories.post_factory import PostFactory
from app.factories.user_factory import UserFactory


def run():
    UserFactory.create_many(10)
    PostFactory.create_many(10)
