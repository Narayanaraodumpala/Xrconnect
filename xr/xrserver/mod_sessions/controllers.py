import functools
from datetime import time,datetime

from flasgger import swag_from

from xrserver.mod_sessionmedia.controllers import deleteSessionMedia
from xrserver.mod_inviteelist.schemas import InvieeListSchema
from xrserver.mod_inviteelist.controllers import inviteEmail
from datetime import datetime

from sqlalchemy.sql.type_api import INDEXABLE
from sqlalchemy import or_
from xrserver.mod_inviteelist.models import InviteeList
from flask import jsonify, make_response
from sqlalchemy import desc
# from flask_httpauth import HTTPBasicAuth
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from xrserver import db
# Import module models
from .models import Session
from .schemas import SessionSchema

# importing session users 

from xrserver.mod_sessionusers.models import SessionUsers
## Custom Functions
from datetime import datetime, timedelta, date
# def start():
#     return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

# def end(n):
#     return (datetime.strptime(startdate, '%d-%m-%Y %H:%M:%S') + timedelta(minutes=n)).strftime('%d-%m-%Y %H:%M:%S')

# def sessionIDname():
#     return str(date.today())
now = datetime.now() # current date and time

mod_sessions = Blueprint('sessions', __name__, url_prefix='/sessions')

# adding new session
@mod_sessions.route('/add', methods=('GET', 'POST', 'PUT'))
def sessions():
    if request.method == 'POST':
        try :
            sessionid = request.form['EventID']
            eventname = request.form['EventName']
            eventtype = request.form['EventType']
            parenteventname = request.form['ParentEventName']
            sessionstatus = request.form['SessionStatus']
            accesstype  = request.form['AccessType']
            maxusers = request.form['MaxUsers']
            hostUserEmail = request.form['HostUserEmail']
            description = request.form['Description']
            category = request.form['Category']
            environmentid = request.form['EnvironmentID']
            startdate = request.form['StartDate']
            enddate = request.form['EndDate']
            # enddate_val = int(request.form['EndDate'])

        except Exception as e :
            return make_response(jsonify({'status' : 'fail', 'message' : str(e), 'data' : 'Missing form Data'}))
            
        error = None

        # sessionid = str(now.strftime('%d-%m-%Y'))+eventname
        # sessionid = str(now.strftime('%d-%m-%Y %H:%M:%S'))+eventname
        # enddate = (datetime.strptime(startdate, '%d-%m-%Y %H:%M:%S') + timedelta(minutes=enddate_val)).strftime('%d-%m-%Y %H:%M:%S')
        # startdate = start()
        # enddate = end()

        if not sessionid :
            error = 'Missing "SessionID"'
        elif not eventname:
            error = 'Missing "EventName"'
        elif not sessionstatus :
            error = 'Missing "SessionStatus"'
        elif not accesstype :
            error = 'Missing "AccessType"'
        elif not maxusers :
            error = 'Missing "MaxUsers"'
        elif not hostUserEmail :
            error = 'Missing "HostUserEmail"'
        elif not environmentid :
            error = 'Missing "EnvironmentID"'
        elif Session.query.filter_by(session_id=sessionid,event_name = eventname).first() is not None :
            error = 'Duplicate session'


        if error is None:
            ses = Session()
            ses.session_id = sessionid
            ses.event_name = eventname
            ses.event_type = eventtype
            ses.session_status = sessionstatus
            ses.access_type = accesstype
            ses.max_users = maxusers
            ses.host_user_email = hostUserEmail
            ses.category = category
            ses.environment_id = environmentid
            if startdate :
                ses.start_date = datetime.strptime(startdate,'%d-%m-%Y %H:%M:%S')
            if enddate :
                ses.end_date = datetime.strptime(enddate,'%d-%m-%Y %H:%M:%S')            
            ses.description = description
            ses.parent_event_name = parenteventname

            db.session.add(ses)
            db.session.commit()
            print('Success')
            responseObject = {
                    'status': 'success',
                    'message': 'session data added sucessfully',
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

# adding new session
@mod_sessions.route('/addEvent', methods=('GET', 'POST', 'PUT'))
def sessions_addEvent():
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
            # eventtype = request.form['EventType']
            # parenteventname = request.form['ParentEventName']
            # sessionstatus = request.form['SessionStatus']
            # maxusers = request.form['MaxUsers']
            # category = request.form['Category']
            # environmentid = request.form['EnvironmentID']

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
        # elif not environmentid :
        #     environmentid = '10'
        # elif not eventtype :
        #     eventtype = 'SESSION_MAIN'
        #     # error = 'Missing "eventtype" and updated the feild with 10'
        # elif not parenteventname :
        #     parenteventname = 'DEFAULT_PARENTNAME'
        #     # error = 'Missing "parenteventname" and updated the feild with DEFAULT_PARENTNAME'
        # elif not sessionstatus :
        #     sessionstatus = 'ACTIVE'
        #     # error = 'Missing "sessionstatus" and updated the feild with ACTIVE'
        # elif not maxusers :
        #     maxusers = '10'
        #     # error = 'Missing "maxusers" and updated the feild with 10'
        # elif not category :
        #     accesstype = 'TEAM'
        #     # error = 'Missing "category" and updated the feild with TEAM'
        #     # error = 'Missing "environmentid" and updated the feild with 10'
        # elif not startdate :
        #     startdate = '2021-05-03 10:10:35'
        # elif not enddate :
        #     enddate = '2021-05-03 10:10:35'
        elif Session.query.filter_by(session_id=sessionid,event_name = eventname).first() is not None :
            error = 'Duplicate session'


        # if not environmentid :
        #     environmentid = '10'
        # else:
        #     return 

        if error is None:
            ses = Session()
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
            ses.environment_id = '10'

            db.session.add(ses)
            db.session.commit()
            print('Success')
            responseObject = {
                    'status': 'success',
                    'message': 'session data added sucessfully',
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



# getting single sessionID      
@mod_sessions.route('/get', methods=('GET', 'POST', 'PUT'))
def getSession():
    if request.method == 'POST':
        try :
            sessionid = request.form['SessionID']
        except Exception as e :
            return make_response(jsonify({'status' : 'fail', 'message' : str(e),'data' : 'missing session id'}))
            
        print(sessionid)
        ses = Session.query.filter_by(session_id=sessionid).first()

        if ses is None :
            error = 'No existing session'
            responseObject = {
                'status': 'fail',
                'message': error,
                'data' : ''
            }
            return make_response(jsonify(responseObject)), 202
        
        else:
            session_schema = SessionSchema()
            data = session_schema.dump(ses)  
            responseObject = {
                'status': 'success',
                'data': data,
                'message' : ''
            } 
            
            return make_response(jsonify(responseObject)), 202
            
    return make_response(jsonify({'status':'fail', 'message' : 'check method type.','data': ''}))
    

# view table list 
@mod_sessions.route('/getActList', methods=['GET'])

def getList():
    if request.method == 'GET':
        # sessions = db.session.query(Session.access_type,Session.category,Session.description).all()
        sessions = Session.query.order_by(desc(Session.start_date)).all()
        if sessions is not None :
            session_schema = SessionSchema()
            data = session_schema.dump(sessions,many = True )
            respData = {'sessions' : data}
            responseObject = {
                'status': 'success',    
                'data': respData,
                'message' : ''                
            }  
        return make_response(jsonify(responseObject))
        
    return make_response(jsonify({'status':'fail', 'message' : 'check method type.','data': ''})), 202


# delete        
@mod_sessions.route('/delete', methods=('GET', 'POST', 'PUT'))
def deleteSession():
    if request.method == 'POST':
        try :
            sessionid = request.form['SessionID']
        except Exception as e :
            return make_response(jsonify({'status' : 'fail', 'message' : str(e),'data' : 'missing session id'}))
           
        ses = Session.query.filter_by(session_id=sessionid).first()

        if ses is not None :
            deleteSessionMedia(sessionid)
            db.session.delete(ses)
            db.session.commit()
            return make_response(jsonify({'status':'success', 'message' : 'Event deleted successfully','data': ''}))
        else :
            return make_response(jsonify({'status':'fail', 'message' : 'Entry not found.','data': ''}))
    return make_response(jsonify({'status':'fail', 'message' : 'check method type.','data': ''}))


# View Session Events based on logged in user_email
@mod_sessions.route('/getPrivateSessionList', methods=('GET', 'POST', 'PUT'))
def getPrivateSessionList():
    if request.method == "POST":
        try:
            email = request.form['email']

        except Exception as e:
            return make_response(
                jsonify({"status": "fail", "message": str(e), "data": ""})
            )
        todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)

        #InvitePrivSelected = db.session.query(Session.session_id, Session.event_name, Session.access_type, Session.description, Session.start_date, 
        #                    Session.end_date, Session.environment_id, Session.category,Session.host_user_email, SessionUsers).join(SessionUsers, (SessionUsers.user_id== email) & (Session.session_id == SessionUsers.session_id) & (Session.access_type == '1')).filter(Session.start_date >= todays_datetime).all()
        InvitePrivSelected = db.session.query(Session.session_id, Session.event_name, Session.access_type, Session.description, Session.start_date, 
                            Session.end_date, Session.environment_id, Session.category,Session.host_user_email, InviteeList).join(InviteeList, (InviteeList.invitee_email== email) & (Session.session_id == InviteeList.session_id) & (Session.access_type == '1')).filter(Session.start_date >= todays_datetime).all() 
        # b = Session.query.filter_by((Session.access_type =='public') | (Session.access_type =='private-1')).all()
        displayPrivateSelected = Session.query.filter_by(host_user_email = email, access_type ='1').filter(Session.start_date >= todays_datetime).all()
        # displayPrivate = Session.query.filter_by(access_type ='1').all()
        displayPublicAll = Session.query.filter_by(access_type ='0').filter(Session.start_date >= todays_datetime).all()
        
        # result = InvitePrivSelected + displayPrivate + displayPublicAll + displayPrivateSelected
        result = InvitePrivSelected +  displayPublicAll + displayPrivateSelected

        if not result:
            error = "No Events Found"
            responseObject = {"status": "fail", "data": [], "message": error}
            return responseObject
        else:
            content_schema = SessionSchema()
            data = content_schema.dump(result,many = True)
            respData = {'EventList' : data}
            responseObject = {
                'status': 'success',    
                'data': respData,
                'message' : ''                
            }
            return make_response(jsonify(responseObject))
        
    return make_response(jsonify({'status':'fail', 'message' : 'check method type.','data': ''}))


    # View Session Events based on logged in user_email
@mod_sessions.route('/getCalendarSessionList', methods=('GET', 'POST', 'PUT'))

def getCalendarSessionList():
    if request.method == "GET":
        try:
            email=request.args.get('email','')
            gte=request.args.get('gte','')
            lte=request.args.get('lte','')

        except Exception as e:
            return make_response(
                 jsonify({"status": "fail", "message": str(e), "data": ""})
            )

        todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)

        #InvitePrivSelected = db.session.query(Session.session_id, Session.event_name, Session.access_type, Session.description, Session.start_date, 
        #                    Session.end_date, Session.environment_id, Session.category,Session.host_user_email, SessionUsers).join(SessionUsers, (SessionUsers.user_id== email) & (Session.session_id == SessionUsers.session_id) & (Session.access_type == '1')).filter(Session.start_date >= todays_datetime).all()
        InvitePrivSelected = db.session.query(Session.session_id, Session.event_name, Session.access_type, Session.description, Session.start_date, 
                            Session.end_date, Session.environment_id, Session.category,Session.host_user_email, InviteeList).join(InviteeList, (InviteeList.invitee_email== email) & (Session.session_id == InviteeList.session_id) & (Session.access_type == '1')).filter(or_(Session.start_date >= gte,Session.start_date <= lte) ).all() 
        # b = Session.query.filter_by((Session.access_type =='public') | (Session.access_type =='private-1')).all()
        displayPrivateSelected = Session.query.filter_by(host_user_email = email, access_type ='1').filter(or_(Session.start_date >= gte,Session.start_date >= lte)).all()
        # displayPrivate = Session.query.filter_by(access_type ='1').all()
        displayPublicAll = Session.query.filter_by(access_type ='0').filter(or_(Session.start_date >= gte,Session.start_date >= lte)).all()
        
        # result = InvitePrivSelected + displayPrivate + displayPublicAll + displayPrivateSelected
        result = InvitePrivSelected +  displayPublicAll + displayPrivateSelected

        if not result:
            error = "No Events Found"
            responseObject = {"status": "fail", "data": [], "message": error}
            return responseObject
        else:
            content_schema = SessionSchema()
            data = content_schema.dump(result,many = True)
            respData = data
            responseObject = {
                'status': 'success',    
                'data': respData,
                'message' : ''                
            }
            return make_response(jsonify(responseObject))
        
    return make_response(jsonify({'status':'fail', 'message' : 'check method type.','data': ''}))



# for edit or update the session( event with the event id attribute )
@mod_sessions.route("/editEventname", methods=["PUT"])
def userUpdate():
    if request.method == "PUT":
        try:
            sessionid = request.form['EventID']
            eventname = request.form['EventName']
            # content = request.form['content']

        except Exception as e:
            return make_response(jsonify({"status": "fail", "message": str(e), "data": "Data is missing"}))

        session = Session.query.filter_by(session_id=sessionid).first()

        if not sessionid:
            sessionid = session.session_id
        else:
            sessionid = sessionid

        if not eventname:
            eventname = session.event_name
        else:
            eventname = eventname

        # if not content:
        #     content = session.content
        # else:
        #     content = content

        if session.session_id is None:
            return "session id  is missing"
        # else:
            # session.session_id = sessionid
            # session.event_name = eventname
            # # session.content= content
            #
            # db.session.commit()
            #
            # responseObject = {
            #     "status": "success",
            #     "data": "",
            #     "message": f"User {eventname} details updated successfully!"
            # }
        else:
         session.session_id = sessionid
         session.event_name = eventname
         # user.last_name = lastname
         # user.phone_number = phonenumber
         # user.gender = gender
         # user.role = role

         db.session.commit()
         print('request accpted')

        responseObject = {
            "status": "success",
            "data": "",
            "message": f"User {eventname} details updated successfully!"
        }
        return make_response(jsonify(responseObject))


    # return make_response(
    #     jsonify({"status": "fail", "message": "check method type.", "data": ""})
    # )

    return make_response(jsonify({'status': 'fail', 'message': 'check method type.', 'data': ''}))