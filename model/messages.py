from datetime import datetime
from __init__ import db, app

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(255), nullable=False)
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
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
def initMessages():
    print("Initialization messages")
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        m1 = Message(sender_id= 0, receiver_id= 1, content='Hello! Ready for work?') 
        m2 = Message(sender_id= 1, receiver_id= 0, content="Lets build a pyramid scheme!")
        messages = [m1, m2]
        for message in messages:
            try:
                message.create()
            except:
                db.session.remove()
                
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_messages(cls):
        return cls.query.all()

    @classmethod
    def get_messages_between_users(cls, sender_id, receiver_id):
        return cls.query.filter_by(sender_id=sender_id, receiver_id=receiver_id).all()
    
