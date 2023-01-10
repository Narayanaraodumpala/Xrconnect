import functools
from datetime import time,datetime
from xrserver.mod_inviteelist.schemas import InvieeListSchema
from xrserver.mod_inviteelist.controllers import inviteEmail

from sqlalchemy.sql.type_api import INDEXABLE
from xrserver.mod_inviteelist.models import InviteeList
from flask import jsonify, make_response
from sqlalchemy import desc
# from flask_httpauth import HTTPBasicAuth
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from xrserver import db
# Import module models
from .models import Event
from .schemas import EventSchema

## Custom Functions
from datetime import datetime, timedelta, date
# now = datetime.now() # current date and time

mod_event = Blueprint('event', __name__, url_prefix='/event')

# adding new session
@mod_event.route('/addEvent', methods=('GET', 'POST', 'PUT'))
def addEvent():
    if request.method == 'POST' or request.method == 'PUT':
        try :
            sessionid = request.form['EventID']
            eventname = request.form['EventName']
            accesstype  = request.form['AccessType']
            hostUserEmail = request.form['HostUserEmail']
            description = request.form['Description']
            startdate = request.form['StartDate']
            enddate = request.form['EndDate']
            environmentid = request.form['EnvironmentID']
            applicationid = request.form['ApplicationID']
            tools_id = request.form['ToolsID']

        except Exception as e :
            return make_response(jsonify({'status' : 'fail', 'message' : str(e), 'data' : 'Missing form Data'}))
            
        error = None

        if not sessionid :
            error = 'Missing "EventID"'
        elif not eventname:
            error = 'Missing "EventName"'
        elif not accesstype :
            error = 'Missing "AccessType"'
        elif not hostUserEmail :
            error = 'Missing "HostUserEmail"'
        elif not description :
            error = 'Missing "Description"'
        
        elif Event.query.filter_by(session_id=sessionid,event_name = eventname).first() is not None :
            error = 'Duplicate session'

        if error is None:
            ses = Event()
            ses.session_id = sessionid
            ses.event_name = eventname
            ses.access_type = accesstype
            ses.host_user_email = hostUserEmail
            if startdate :
                ses.start_date = datetime.strptime(startdate,'%d-%m-%Y %H:%M:%S')
            if enddate :
                ses.end_date = datetime.strptime(enddate,'%d-%m-%Y %H:%M:%S')
            ses.description = description
            ses.event_type = 'SESSION_MAIN'
            ses.parent_event_name = 'DEFAULT_PARENTNAME'
            ses.session_status = 'ACTIVE'
            ses.max_users = '10'
            ses.category = 'TEAM'
            ses.environment_id = environmentid
            ses.application_id = applicationid
            ses.tools_id = tools_id

            db.session.add(ses)
            db.session.commit()
            print('Success')
            responseObject = {
                    'status': 'success',
                    'message': 'Event Created Sucessfully!',
                    'data' : ''
                }
            return make_response(jsonify(responseObject)), 202
        
        else:
            responseObject = {
                'status': 'fail',
                'message': error,
                'data' : ''
            }    
        
            return make_response(jsonify(responseObject)), 401
        
    return make_response(jsonify({'status':'fail', 'message' : 'check method type.','data': ''}))


# Display Events List based on logged in user_email
@mod_event.route('/getEventList', methods=('GET', 'POST', 'PUT'))
def getPrivateSessionList():
    if request.method == "POST":
        try:
            email = request.form['email']

        except Exception as e:
            return make_response(jsonify({"status": "fail", "message": str(e), "data": ""}))
        
        InvitePrivSelected = db.session.query(Event.session_id, Event.event_name, Event.access_type, Event.description, Event.start_date, 
                            Event.end_date, Event.environment_id, Event.category,Event.host_user_email, InviteeList).join(InviteeList, 
                            (InviteeList.invitee_email== email) & (Event.session_id == InviteeList.session_id) & (Event.access_type== '2')).all()

        displayPrivateSelected = Event.query.filter_by(host_user_email = email, access_type ='2').all()
        displayPrivate = Event.query.filter_by(access_type ='1').all()
        displayPublicAll = Event.query.filter_by(access_type ='0').all()
        
        result = InvitePrivSelected + displayPrivate + displayPublicAll + displayPrivateSelected

        if not result:
            error = "No Data Found"
            responseObject = {"status": "fail", "data": "", "message": error}
            return responseObject
        else:
            content_schema = EventSchema()
            data = content_schema.dump(result,many = True)
            respData = {'EventList' : data}
            responseObject = {
                'status': 'success',    
                'data': respData,
                'message' : ''                
            }
            return make_response(jsonify(responseObject))
        
    return make_response(jsonify({'status':'fail', 'message' : 'check method type.','data': ''}))


# getting single eventid details
@mod_event.route('/getEvent', methods=('GET', 'POST', 'PUT'))
def getEvent():
    if request.method == 'POST':
        try :
            eventid = request.form['eventid']
        except Exception as e :
            return make_response(jsonify({'status' : 'fail', 'message' : str(e),'data' : 'missing session id'}))
            
        print(eventid)
        ses = Event.query.filter_by(session_id=eventid).first()

        if ses is None :
            error = 'No existing session'
            responseObject = {
                'status': 'fail',
                'message': error,
                'data' : ''
            }
            return make_response(jsonify(responseObject)), 202
        
        else:
            event_schema = EventSchema()
            data = event_schema.dump(ses)  
            responseObject = {
                'status': 'success',
                'data': data,
                'message' : ''
            } 
            
            return make_response(jsonify(responseObject)), 202
            
    return make_response(jsonify({'status':'fail', 'message' : 'check method type.','data': ''}))
    

# Update AmbienceID (Not using)
@mod_event.route("/updateEvent", methods=("GET", "POST", "PUT"))
def updateEvent():
    if request.method == "PUT":
        try:
            eventid = request.form['EventID']
            # environmentid = request.form['ApplicationID']
            environmentid = request.form['AmbienceID']

        except Exception as e:
            return make_response(
                jsonify(
                    {"status": "fail", "message": str(
                        e), "data": "Data is missing"}
                )
            )

        ses = Event.query.filter_by(session_id=eventid).first()
        # return user.email

        if ses.session_id is None:
            return "data is missing"
        else:
            ses.environment_id = environmentid
            ses.event_type = ambienceid
            
            db.session.commit()

            responseObject = {
                "status": "success",
                "data": "",
                "message": "New data added successfully!"
            }
        return make_response(jsonify(responseObject))
    return make_response(
        jsonify({"status": "fail", "message": "check method type.", "data": ""})
    )


# view table list  # Not using (This API will display all the events)
@mod_event.route('/getActList', methods=('GET', 'POST', 'PUT'))
def getList():
    if request.method == 'GET':
        # sessions = db.session.query(Session.access_type,Session.category,Session.description).all()
        sessions = Event.query.order_by(desc(Event.start_date)).all()
        if sessions is not None :
            session_schema = EventSchema()
            data = session_schema.dump(sessions,many = True )
            respData = {'Events' : data}
            responseObject = {
                'status': 'success',    
                'data': respData,
                'message' : ''                
            }  
        return make_response(jsonify(responseObject))
        
    return make_response(jsonify({'status':'fail', 'message' : 'check method type.','data': ''})), 202

       
# delete        
@mod_event.route('/delete', methods=('GET', 'POST', 'PUT'))
def delete():
    if request.method == 'POST':
        try :
            eventid = request.form['eventid']
        except Exception as e :
            return make_response(jsonify({'status' : 'fail', 'message' : str(e),'data' : 'missing session id'}))
           
        ses = Event.query.filter_by(session_id=eventid).first()

        if ses is not None :
            db.session.delete(ses)
            db.session.commit()
            return make_response(jsonify({'status':'success', 'message' : 'Data deleted successfully','data': ''}))
        else :
            return make_response(jsonify({'status':'fail', 'message' : 'Entry not found.','data': ''}))
    return make_response(jsonify({'status':'fail', 'message' : 'check method type.','data': ''}))


