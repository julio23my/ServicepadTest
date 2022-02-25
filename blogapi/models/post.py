from blogapi.extensions import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(100))
    priority = db.Column(db.String(20))
    status = db.Column(db.String(20))
    time_publish = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    is_public = db.Column(db.Boolean)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)