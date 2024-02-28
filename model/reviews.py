from datetime import datetime
from __init__ import db, app

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, rating, comment):
        self.user_id = user_id
        self.rating = rating
        self.comment = comment

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'rating': self.rating,
            'comment': self.comment,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

def initReviews():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        r1 = Review(user_id=1, rating=5, comment='Great experience!')
        r2 = Review(user_id=2, rating=4, comment='Good service.')
        reviews = [r1, r2]
        for review in reviews:
            try:
                review.create()
            except Exception as e:
                print(f"Error creating review: {e}")
                db.session.rollback()
