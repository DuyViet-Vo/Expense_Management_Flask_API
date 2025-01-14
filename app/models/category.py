from datetime import datetime

from app.extensions import db

class Category(db.Model):
    __tablename__ = "category"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "create_at": self.create_at,
            "update_at": self.update_at
        }
