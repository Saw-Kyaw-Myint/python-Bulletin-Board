from marshmallow import fields

from app.extension import ma
from app.models.post import Post
from app.models.user import User


class UserRelationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("id", "name", "email")


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        ordered = True
        exclude = ["deleted_at"]

    creator = fields.Nested(
        UserRelationSchema, only=("id", "name", "email"), dump_only=True
    )

    updater = fields.Nested(
        UserRelationSchema, only=("id", "name", "email"), dump_only=True
    )
