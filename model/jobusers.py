""" database dependencies to support sqliteDB examples """

from datetime import date

import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError

''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''



# Define the job class to manage actions in the 'jobs' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) job represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class JobUsers(db.Model):
    __tablename__ = 'jobsusers'  # table title is plural, class title is singular

    # Define the job schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _jobid = db.Column(db.Integer)
    _userid = db.Column(db.Integer)
    _dateApplied = db.Column(db.Date)


    
    # constructor of a job object, initializes the instance variables within object (self)
    def __init__(self, jobid, userid, dateApplied=date.today()):
        self._jobid = jobid
        self._userid = userid
        self._dateApplied = dateApplied
       

    # a title getter method, extracts title from object
    @property
    def jobid(self):
        return self._jobid
    
    # a setter function, allows jobid to be updated after initial object creation
    @jobid.setter
    def jobid(self, jobid):
        self._jobid = jobid
    
    @property
    def userid(self):
        return self._userid
    
    # a setter function, allows userid to be updated after initial object creation
    @userid.setter
    def userid(self, userid):
        self._userid = userid

    @property
    def dateApplied(self):
        dateApplied_string = self._dateApplied.strftime('%m-%d-%Y')
        return dateApplied_string
    
    # a setter function, allows userid to be updated after initial object creation
    @dateApplied.setter
    def dateApplied(self, dateApplied):
        self._dateApplied = dateApplied
    
    # a getter method, extracts email from object
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())
   
    # qualification is used to store python dictionary data 

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from job(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to jobs table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "jobid": self.jobid,
            "userid": self.userid,
            "dateApplied": self.dateApplied,
   
            
            # "posts": [post.read() for post in self.posts]
        }
        


    # CRUD update: updates job title, field, phone
    # returns self
    def update(self, title="", description="", field=""):
        """only updates values with length"""
        if len(title) > 0:
            self.title = title
        if len(description) > 0:
            self.description = description
        if len(field) > 0:
            self.set_field(field)
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initJobsUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        jobs = [
            JobUsers(jobid=1, userid=2, dateApplied=date(1847, 2, 11)),
            JobUsers(jobid=2, userid=3, dateApplied=date(2024, 4, 12))
        ]
        for job in jobs:
            try:
                job.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate title, or error: {job.title}")
