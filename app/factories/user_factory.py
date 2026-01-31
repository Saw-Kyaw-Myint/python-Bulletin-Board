# app/factories/user_factory.py
from faker import Faker

from app.enum.user import UserRole
from app.factories.base_factory import BaseFactory
from app.models import User
from app.utils.hash import hash_password
import random

fake = Faker()


class UserFactory:

    # create admin account
    def create_admin():
        admin = User.query.filter_by(email="admin@admin.com").first()
        if admin:
            return admin

        return BaseFactory.create_one(
            lambda: {
                "name": "Admin",
                "email": "admin@admin.com",
                "password": hash_password("Admin123@"),
                "phone": "09999999999",
                "address": "Admin Address",
                "role": UserRole.ADMIN.value,
            },
            User,
        )
    
    def create_user():
        admin = User.query.filter_by(email="user@user.com").first()
        if admin:
            return admin

        return BaseFactory.create_one(
            lambda: {
                "name": "User",
                "email": "user@user.com",
                "password": hash_password("User123@"),
                "phone": "09999999999",
                "address": "User Address",
                "role": UserRole.USER.value,
            },
            User,
        )

    def make_data():
        """Return fake user data (not saved to DB)."""
        admin = UserFactory.create_admin()
        user = UserFactory.create_user()
        return {
            "name": fake.name(),
            "email": fake.unique.email(),
            "password": hash_password("Password123@"),
            "phone": "09451340513",
            "address": fake.address(),
            "create_user_id": random.choice([admin.id, user.id]),
        }

    def create():
        return BaseFactory.create_one(UserFactory.make_data, User)

    def create_many(count=10):
        return BaseFactory.create_many(UserFactory.make_data, User, count)
