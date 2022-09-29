

# ---------    By Narayanarao Dumpala --------------#


# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.

from audioop import avg
import functools
from datetime import time, datetime
from xrserver.mod_sessionmedia.controllers import deleteSessionMedia
from xrserver.mod_inviteelist.schemas import InvieeListSchema
from xrserver.mod_inviteelist.controllers import inviteEmail
from sqlalchemy import func
from sqlalchemy.sql.type_api import INDEXABLE
from xrserver.mod_inviteelist.models import InviteeList
from flask import jsonify, make_response
from sqlalchemy import desc
# from flask_httpauth import HTTPBasicAuth
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import time

from xrserver import db
# Import module models
from .models import Aviation

from .schemas import AviationSchema
## Custom Functions
from datetime import datetime, timedelta, date
# import datetime
# date = datetime.date.today()
# def start():
#     return datetime.now().strftime("%d-%m-%Y %H:%M:%S")12

# def end(n):
#     return (datetime.strptime(startdate, '%d-%m-%Y %H:%M:%S') + timedelta(minutes=n)).strftime('%d-%m-%Y %H:%M:%S')

# def sessionIDname():
#     return str(date.today())
now = datetime.now()  # current date and time

mod_add_aviation_api = Blueprint(
    'add_aviation_api', __name__, url_prefix='/aviation')


# adding new session
@mod_add_aviation_api.route('/add', methods=('GET', 'POST', 'PUT'))
def add_sessions():
    if request.method == 'POST':
        mode = None
        event_id = None
        ip_address = None
        device_id = None
        help = None

        # timestampTime = None
        # timestampDate = None
        module = None
        edate = None
        etime = None
        idle_time = None
        # teleportation = None
        # component = None
        # action = None
        modeEndTime = None
        modeEndDate = None
        idleStartTime = None
        idleStartDate = None
        modeStartTime = None
        modeStartDate = None
        idlEndTime = None
        idlEndDate = None
        # teleportStartPos = None
        # teleportEndPos = None
        operation = None
        operationStartTime = None
        operationStartDate = None
        operationEndTime = None
        operationEnddate = None
        project_name = None
        try:
            session_id = request.form['session_id']
            user_id = request.form['user_id']
            start_time = request.form['start_time']
            user_name = request.form['user_name']
            start_data_time = start_time.split(' ')

            start_date = start_data_time[0]
            start_time = start_data_time[1]

            if 'mode' in request.form:
                mode = request.form['mode']
            if 'event_id' in request.form:
                event_id = request.form['event_id']

            if 'ip_address' in request.form:
                ip_address = request.form['ip_address']
            if 'project_name' in request.form:
                project_name = request.form['project_name']
            if 'device_id' in request.form:
                device_id = request.form['device_id']
            # if 'timestampTime' in request.form:
            #     timestampTime = request.form['timestampTime']
            #     if (timestampTime != ""):
            #         end_time_dsate = timestampTime.split(' ')
            #         timestampTime = end_time_dsate[1]
            #         print('timestampTime=', modeEndTime)

            #         timestampDate = end_time_dsate[0]
            #         print('modeEndDate=', timestampDate)

            if 'module' in request.form:
                module = request.form['module']
            if 'help' in request.form:
                help = request.form['help']
            if 'end_time' in request.form:
                end_times = request.form['end_time']
                print(end_times)
                if (end_times != ""):
                    end_time_dsate = end_times.split(' ')
                    edate = end_time_dsate[0]
                    etime = end_time_dsate[1]

            if 'idle_time' in request.form:
                idle_time = request.form['idle_time']
            # if 'teleportation' in request.form:
            #     teleportation = request.form['teleportation']
            # if 'component' in request.form:
            #     component = request.form['component']
            # if 'action' in request.form:
            #     action = request.form['action']
            if 'modeEndTime' in request.form:
                modeEndTime = request.form['modeEndTime']
                if (modeEndTime != ""):
                    end_time_dsate = modeEndTime.split(' ')
                    modeEndTime = end_time_dsate[1]
                    print('modeEndTime=', modeEndTime)

                    modeEndDate = end_time_dsate[0]
                    print('modeEndDate=', modeEndDate)

            if 'idleStartTime' in request.form:
                idleStartTime = request.form['idleStartTime']
                if (idleStartTime != ""):
                    end_time_dsate = idleStartTime.split(' ')
                    idleStartTime = end_time_dsate[1]
                    print('idleStartTime=', modeEndTime)

                    idleStartDate = end_time_dsate[0]
                    print('idleStartDate=', modeEndDate)

            if 'modeStartTime' in request.form:
                modeStartTime = request.form['modeStartTime']
                if (modeStartTime != ""):
                    end_time_dsate = modeStartTime.split(' ')
                    modeStartTime = end_time_dsate[1]
                    print('modeStartTime=', modeEndTime)

                    modeStartDate = end_time_dsate[0]
                    print('modeStartDate=', modeEndDate)

            if 'idlEndTime' in request.form:
                idlEndTime = request.form['idlEndTime']
                if (idlEndTime != ""):
                    end_time_dsate = idlEndTime.split(' ')
                    idlEndTime = end_time_dsate[1]
                    print('idlEndTime=', modeEndTime)

                    idlEndDate = end_time_dsate[0]
            #         print('idlEndDate=', modeEndDate)
            # if 'teleportStartPos' in request.form:
            #     teleportStartPos = request.form['teleportStartPos']
            # if 'teleportEndPos' in request.form:
            #     teleportEndPos = request.form['teleportEndPos']
            if 'operation' in request.form:
                operation = request.form['operation']
            if 'operationStartTime' in request.form:

                operationStartTime = request.form['operationStartTime']
                if (operationStartTime != ""):
                    end_time_dsate = operationStartTime.split(' ')
                    operationStartTime = end_time_dsate[1]
                    print('operationStartTime=', operationStartTime)

                    operationStartDate = end_time_dsate[0]
                    print('operationStartDate=', operationStartDate)
            if 'operationEndTime' in request.form:
                operationEndTime = request.form['operationEndTime']
                if (operationEndTime != ""):
                    end_time_dsate = operationEndTime.split(' ')
                    operationEndTime = end_time_dsate[1]
                    print('operationEndTime=', operationEndTime)

                    operationEnddate = end_time_dsate[0]
                    print('operationEnddate=', operationEnddate)

        except Exception as e:
            return make_response(jsonify({'status': 'fail', 'message': str(e), 'data': 'Missing form Data'}))

        error = None

        if not session_id:
            error = 'Missing "session_id"'

        elif not start_time:
            error = 'Missing "start_time"'

        elif not user_id:
            error = 'Missing "user_id"'

        elif not user_name:
            error = 'Missing "user_name"'
        if Aviation.query.filter_by(session_id=session_id, user_id=user_id, user_name=user_name, start_time=start_time).first() is not None:
            print('success for duplicates')
            responseObject = {
                'status': 'success',
                'message': 'session data added sucessfully',
                'data': ''
            }
            return make_response(jsonify(responseObject)), 202
        else:

            if error is None:
                ses = Aviation()
                ses.session_id = session_id
                ses.event_id = event_id

                ses.start_time = start_time
                ses.start_date = start_date
                ses.end_time = etime
                ses.end_date = edate
                ses.ip_address = ip_address
                ses.user_id = user_id
                ses.device_id = device_id
                # ses.timestampTime = timestampTime
                # ses.timestampDate = timestampDate

                ses.module = module
                ses.mode = mode
                ses.user_name = user_name
                ses.idle_time = idle_time
                # ses.teleportation = teleportation
                # ses.component = component
                # ses.action = action
                ses.idleStartTime = idleStartTime
                ses.idleStartDate = idleStartDate
                ses.modeStartTime = modeStartTime
                ses.modeStartDate = modeStartDate
                ses.modeEndTime = modeEndTime
                ses.modeEndDate = modeEndDate
                ses.idlEndTime = idlEndTime
                ses.idlEndDate = idlEndDate
                # ses.teleportStartPos = teleportStartPos
                # ses.teleportEndPos = teleportEndPos
                ses.operation = operation
                ses.operationStartTime = operationStartTime
                ses.operationStartDate = operationStartDate

                ses.operationEndTime = operationEndTime
                ses.operationEnddate = operationEnddate
                ses.project_name = project_name
                ses.help = help

                db.session.add(ses)
                db.session.commit()

                print('Success')
                responseObject = {
                    'status': 'success',
                    'message': 'session data added sucessfully',
                    'data': ''
                }
                return make_response(jsonify(responseObject)), 202

            else:
                responseObject = {
                    'status': 'fail',
                    'message': error,
                    'data': ''
                }

                return make_response(jsonify(responseObject)), 401
    print('request accepted')

    return make_response(jsonify({'status': 'fail', 'message': 'check method type.', 'data': ''}))


# fetch one session(event logs ) list based upon user_id
@mod_add_aviation_api.route('/getSessionList', methods=('GET', 'POST', 'PUT'))
def getSessionList():
    if request.method == 'GET' or 'POST':
        # user = User.query.order_by(desc(User.date_created)).all()
        try:

            result = request.args.get('user_id')

        except Exception as e:
            return make_response(
                jsonify(
                    {"status": "fail", "message": 'user_id is required', "data": ""})
            )
        user = db.session.query(
            Aviation.id,
            Aviation.session_id,
            Aviation.user_id,
            Aviation.user_name,
            Aviation.event_id,
            Aviation.mode,
            Aviation.module,
            Aviation.ip_address,
            Aviation.device_id,
            # Aviation.timestampTime,
            # Aviation.timestampDate,
            Aviation.idle_time,
            # Aviation.teleportation,
            Aviation.date_created,

            Aviation.start_time,
            Aviation.start_date,
            Aviation.end_time,
            Aviation.end_date,
            # Aviation.component,
            # Aviation.action,
            Aviation.modeEndTime,
            Aviation.modeEndDate,
            Aviation.idleStartTime,
            Aviation.idleStartDate,
            Aviation.modeStartTime,
            Aviation.modeStartDate,
            Aviation.idlEndTime,
            Aviation.idlEndDate,
            # Aviation.teleportStartPos,
            # Aviation.teleportEndPos,
            Aviation.operation,
            Aviation.operationStartTime,
            Aviation.operationStartDate,
            Aviation.operationEndTime,
            Aviation.operationEnddate,
            Aviation.project_name,
            Aviation.help
        ).filter_by(user_id=result).all()

        if not user:
            error = "No existing user"
            responseObject = {"status": "fail", "data": "", "message": error}
            return make_response(jsonify(responseObject))

        else:
            user_schema = AviationSchema()
            data = user_schema.dump(user, many=True)
            responseObject = {"status": "success", "data": data, "message": ""}
        return make_response(jsonify(responseObject))

    return make_response(
        jsonify({"status": "fail", "message": "check method type.", "data": ""}))

# fetch  all session list


@mod_add_aviation_api.route('/SessionsList', methods=('GET', 'POST', 'PUT'))
def SessionsList():
    if request.method == 'GET':
        # user = User.query.order_by(desc(User.date_created)).all()
        user = db.session.query(
            Aviation.id,
            Aviation.session_id,
            Aviation.user_id,
            Aviation.user_name,
            Aviation.event_id,
            Aviation.mode,
            Aviation.module,
            Aviation.ip_address,
            Aviation.device_id,
            # Aviation.timestampTime,
            # Aviation.timestampDate,
            Aviation.idle_time,
            # Aviation.teleportation,
            Aviation.date_created,

            Aviation.start_time,
            Aviation.start_date,
            Aviation.end_time,
            Aviation.end_date,
            # Aviation.component,
            # Aviation.action,
            Aviation.modeEndTime,
            Aviation.modeEndDate,
            Aviation.idleStartTime,
            Aviation.idleStartDate,
            Aviation.modeStartTime,
            Aviation.modeStartDate,
            Aviation.idlEndTime,
            Aviation.idlEndDate,
            # Aviation.teleportStartPos,
            # Aviation.teleportEndPos,
            Aviation.operation,
            Aviation.operationStartTime,
            Aviation.operationStartDate,
            Aviation.operationEndTime,
            Aviation.operationEnddate,
            Aviation.project_name,
            Aviation.help

        ).all()
        if user is not None:
            session_schema = AviationSchema()
            data = session_schema.dump(user, many=True)
            respData = {'session': data}
            responseObject = {
                'status': 'success',
                'data': respData,
                'message': ''
            }
            # username, company_name, email, role, gender
        return make_response(jsonify(responseObject))

    return make_response(jsonify({'status': 'fail', 'message': 'check method type.', 'data': ''})), 202


@mod_add_aviation_api.route('/getSessionListPagination', methods=('GET', 'POST', 'PUT'))
def getSessionListPagination():
    if request.method == 'GET':
        sessions = db.session.query(
            Aviation.user_id,
            Aviation.user_name,
            Aviation.session_id,
            Aviation.event_id,
            Aviation.mode,
            Aviation.module,
            func.group_concat(Aviation.start_time)
        ).group_by('user_id', 'session_id', 'module', 'mode').all()
        #.filter(Aviation.module!=None)

        if sessions is not None:
            session_schema = AviationSchema()
            data = session_schema.dump(sessions, many=True)
            respData = {'sessions': data}
            responseObject = {
                'status': 'success',
                'data': respData,
                'message': ''
            }
            # username, company_name, email, role, gender
        return make_response(jsonify(responseObject))

    return make_response(jsonify({'status': 'fail', 'message': 'check method type.', 'data': ''})), 202


@mod_add_aviation_api.route('/getSessionListDetails', methods=('GET', 'POST', 'PUT'))
def getSessionListDetails():
    if request.method == 'GET':
        try:
            #operation=request.args.get('operation',None)
            # event_id=request.args.get('event_id',None)
            mode = request.args.get('mode', None)
            module = request.args.get('module', None)
            session_id = request.args.get('session_id', None)
            user_id = request.args.get('user_id', None)
            # user_name=request.args.get('user_name',None)
            #if operation=="":
            #    operation=None
            if mode == "":
                mode = None
            if module == "":
                module = None
            if session_id == "":
                session_id = None
            if user_id == "":
                user_id = None

        except Exception as e:
            return make_response(
                jsonify({"status": "fail", "message": str(e), "data": ""})
            )

        sessions = db.session.query(
            Aviation.user_id,
            Aviation.user_name,
            Aviation.session_id,
            Aviation.event_id,
            Aviation.mode,
            Aviation.module,
            Aviation.operation,
            Aviation.operationStartTime,
            Aviation.operationStartDate,
            Aviation.operationEndTime,
            Aviation.operationEnddate
        ).filter_by(user_id=user_id, session_id=session_id, module=module, mode=mode).all()

        if sessions is not None:
            session_schema = AviationSchema()
            data = session_schema.dump(sessions, many=True)
            respData = {'sessions': data}
            responseObject = {
                'status': 'success',
                'data': respData,
                'message': ''
            }
            # username, company_name, email, role, gender
        return make_response(jsonify(responseObject))

    return make_response(jsonify({'status': 'fail', 'message': 'check method type.', 'data': ''})), 202

# fetch record by project name


@mod_add_aviation_api.route('/getSessionListbyProjectName', methods=('GET', 'POST', 'PUT'))
def getSessionListbyProjectName():
    if request.method == 'POST':
        # user = User.query.order_by(desc(User.date_created)).all()
        try:

            result = request.form['project_name']

        except Exception as e:
            return make_response(
                jsonify(
                    {"status": "fail", "message": 'user_id is required', "data": ""})
            )
        user = db.session.query(
            Aviation.id,
            Aviation.session_id,
            Aviation.user_id,
            Aviation.user_name,
            Aviation.event_id,
            Aviation.mode,
            Aviation.module,
            Aviation.ip_address,
            Aviation.device_id,
            # Aviation.timestampTime,
            # Aviation.timestampDate,
            Aviation.idle_time,
            # Aviation.teleportation,
            Aviation.date_created,

            Aviation.start_time,
            Aviation.start_date,
            Aviation.end_time,
            Aviation.end_date,
            # Aviation.component,
            # Aviation.action,
            Aviation.modeEndTime,
            Aviation.modeEndDate,
            Aviation.idleStartTime,
            Aviation.idleStartDate,
            Aviation.modeStartTime,
            Aviation.modeStartDate,
            Aviation.idlEndTime,
            Aviation.idlEndDate,
            # Aviation.teleportStartPos,
            # Aviation.teleportEndPos,
            Aviation.operation,
            Aviation.operationStartTime,
            Aviation.operationStartDate,
            Aviation.operationEndTime,
            Aviation.operationEnddate,
            Aviation.project_name,
            Aviation.help
        ).filter_by(project_name=result).all()
        print('session exist')
        print(user)

        if not user:
            error = "No existing result"
            responseObject = {"status": "fail", "data": "", "message": error}
            return make_response(jsonify(responseObject))

        else:
            user_schema = AviationSchema()
            data = user_schema.dump(user, many=True)
            responseObject = {"status": "success", "data": data, "message": ""}
        return make_response(jsonify(responseObject))

    return make_response(
        jsonify({"status": "fail", "message": "check method type.", "data": ""}))


# fetch one session(event logs ) list based upon user_name
@mod_add_aviation_api.route('/getSessionListbyUser', methods=('GET', 'POST', 'PUT'))
def getSessionListbyUser():
    if request.method == 'GET' or 'POST':
        # user = User.query.order_by(desc(User.date_created)).all()
        try:

            result = request.args.get('user_name')

        except Exception as e:
            return make_response(
                jsonify(
                    {"status": "fail", "message": 'user_name is required', "data": ""})
            )
        user = db.session.query(
            Aviation.id,
            Aviation.session_id,
            Aviation.user_id,
            Aviation.user_name,
            Aviation.event_id,
            Aviation.mode,
            Aviation.module,
            Aviation.ip_address,
            Aviation.device_id,
            # Aviation.timestampTime,
            # Aviation.timestampDate,
            Aviation.idle_time,
            # Aviation.teleportation,
            Aviation.date_created,

            Aviation.start_time,
            Aviation.start_date,
            Aviation.end_time,
            Aviation.end_date,
            # Aviation.component,
            # Aviation.action,
            Aviation.modeEndTime,
            Aviation.modeEndDate,
            Aviation.idleStartTime,
            Aviation.idleStartDate,
            Aviation.modeStartTime,
            Aviation.modeStartDate,
            Aviation.idlEndTime,
            Aviation.idlEndDate,
            # Aviation.teleportStartPos,
            # Aviation.teleportEndPos,
            Aviation.operation,
            Aviation.operationStartTime,
            Aviation.operationStartDate,
            Aviation.operationEndTime,
            Aviation.operationEnddate,
            Aviation.project_name,
            Aviation.help
        ).filter_by(user_name=result).all()

        if not user:
            error = "No existing user"
            responseObject = {"status": "fail", "data": "", "message": error}
            return make_response(jsonify(responseObject))

        else:
            user_schema = AviationSchema()
            data = user_schema.dump(user, many=True)
            responseObject = {"status": "success", "data": data, "message": ""}
        return make_response(jsonify(responseObject))

    return make_response(
        jsonify({"status": "fail", "message": "check method type.", "data": ""}))


@mod_add_aviation_api.route('/getSessionListbyDate', methods=('GET', 'POST', 'PUT'))
def getSessionListbyDate():
    if request.method == 'GET' or 'POST':
        # user = User.query.order_by(desc(User.date_created)).all()
        try:

            # result = request.args.get('date_created')
            pass

        except Exception as e:
            return make_response(
                jsonify(
                    {"status": "fail", "message": 'user_name is required', "data": ""})
            )
        user = db.session.query(Aviation).filter(
            Aviation.date_created > '2022-08-16').filter(Aviation.date_created <= '2022-08-22')

        # query=SELECT * FROM `user` WHERE `date_created`>'2022-08-16' and `date_created`<='2022-08-22'

        if not user:
            error = "No existing user"
            responseObject = {"status": "fail", "data": "", "message": error}
            return make_response(jsonify(responseObject))

        else:
            user_schema = AviationSchema()
            data = user_schema.dump(user, many=True)
            responseObject = {"status": "success", "data": data, "message": ""}
        return make_response(jsonify(responseObject))

    return make_response(
        jsonify({"status": "fail", "message": "check method type.", "data": ""}))
