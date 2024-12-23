from datetime import datetime

from app.extensions import db


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255), nullable=False)
    user_create = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    user = db.relationship("User", backref="groups")


    def to_dict(self):
        return {
            "id": self.id,
            "group_name": self.group_name,
            "user_create": self.user_create,
            "create_at": self.create_at,
            "updated_at": self.updated_at,
            "user": {
                "id": self.user.id,
                "username": self.user.username,
                "email": self.user.email,
            } if self.user else None,
        }
