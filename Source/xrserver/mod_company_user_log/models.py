# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from xrserver import db
from xrserver import app
import time
from ..models import Base
from flask import jsonify, make_response
        
class Companyuserlog(Base):

    __tablename__ = 'company_user_log'
    
    id = db.Column(db.Integer, index = True, nullable = False, primary_key = True)
    user_id = db.Column(db.String(128)) # will store more information based on content type
    company_id =  db.Column(db.String(150))
    license_key = db.Column(db.String(25))
    device_id = db.Column(db.String(256))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    status =  db.Column(db.String(25))