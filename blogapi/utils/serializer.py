from marshmallow import Schema,fields
from blogapi.models.post import Post

class UserSchema(Schema):
    public_id = fields.String()
    name = fields.String()
    admin = fields.Boolean()

class TokenSchema(Schema):
    token = fields.String()
    expire = fields.DateTime()
    user = fields.Nested(UserSchema)


class PostSchema(Schema):
    class Meta:
        model = Post
        include_fk = True

    id = fields.Integer()
    title = fields.String()
    description =fields.String()
    priority =fields.String()
    status =fields.String()
    time_publish = fields.DateTime()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    is_public = fields.Boolean()
    author = fields.Nested(UserSchema)
