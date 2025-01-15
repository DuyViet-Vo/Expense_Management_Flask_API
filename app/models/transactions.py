from datetime import datetime


from app.extensions import db

class Transaction(db.Model):
    __tablename__="transactions"

    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    account = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    user = db.relationship("User", backref="transactions")
    category_deltai = db.relationship("Category", backref="transactions")

    def to_dict(self):
        return {
            "id": self.id,
            "group": self.group,
            "account":{
                "id": self.user.id,
                "username": self.user.username,
                "email": self.user.email,
            },
            "category":{
                "id": self.category_deltai.id,
                "name": self.category_deltai.name
            },
            "amount": self.amount,
            "description": self.description,
            "create_at": self.create_at,
            "update_at": self.update_at,
        }
