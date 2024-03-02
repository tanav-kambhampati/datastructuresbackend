from datetime import datetime
from __init__ import db, app

class Review(db.Model):
    __tablename__ = 'salaries'

    id = db.Column(db.Integer, primary_key=True)
    jobreccomendation = db.Column(db.Integer, nullable=True)
    salaries = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

    def __init__(self, jobreccomendation, salaries, timestamp=None):
        self.jobreccomendation = jobreccomendation
        self.salaries = salaries
        if timestamp is None:
            timestamp = datetime.utcnow()
        self.timestamp = timestamp


    def read(self):
        return {
            'id': self.id,
            'jobreccomendation': self.jobreccomendation,
            'salaries': self.salaries,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
     }
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

def initSurveyData():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        surveys = [
            Survey(question="What is your favorite color?", answer="Blue"),
            Survey(question="How often do you exercise?", answer="Three times a week")
        ]
        for survey in surveys:
            try:
                survey.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.rollback()
                print("Error: Failed to add survey data due to integrity violation")

