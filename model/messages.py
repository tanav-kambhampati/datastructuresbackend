from datetime import datetime
from __init__ import db

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, sender_id, receiver_id, content):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content

    def serialize(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'content': self.content,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_messages(cls):
        return cls.query.all()

    @classmethod
    def get_messages_between_users(cls, sender_id, receiver_id):
        return cls.query.filter_by(sender_id=sender_id, receiver_id=receiver_id).all()