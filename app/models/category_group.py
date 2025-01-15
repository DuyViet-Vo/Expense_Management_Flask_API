from app.extensions import db
from datetime import datetime
from sqlalchemy.orm import relationship
class CategoryGroup(db.Model):
    __tablename__ = "category_group"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    group = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    category_detail = db.relationship('Category', backref='category_groups')

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "group": self.group,
            "create_at": self.create_at,
            "update_at": self.update_at
        }