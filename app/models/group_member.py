from datetime import datetime

from app.extensions import db


class GroupMember(db.Model):
    __tablename__ = "group_members"

    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    group = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    create_at = db.Column(db.Datetime, default=datetime.now)

    def to_dict(self):
        return {"id": self.id, "account": self.account, "group": self.group, "create_at": self.create_at}
