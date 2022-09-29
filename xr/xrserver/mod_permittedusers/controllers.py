import functools
#from datetime import time
from flask import jsonify, make_response
# from flask_httpauth import HTTPBasicAuth
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from xrserver import db

# Import module models
from .models import PermittedUsers

from .schemas import PermittedUsersSchema

mod_permitted_users = Blueprint('permitted_users', __name__, url_prefix='/permittedusers')

@mod_permitted_users.route('/add', methods=('GET', 'POST', 'PUT'))
def content():
    if request.method == 'POST':
        try :
            eventID = request.form['EventID']
            contentID = request.form['ContentID']
            media_id=request.form['media_id']
            user_email=request.form['user_email']

        except Exception as e :
            return make_response(jsonify({'status' : 'fail', 'message' : str(e), 'data' : 'Missing form data'}))

        error = None
        if not eventID:
            error = 'Missing "eventID"'
        elif not contentID:
            error = 'Missing "contentID"'
        elif not media_id :
            error = 'Missing "media_id"'
        elif not user_email :
            error = 'Missing "user_email"'
        elif PermittedUsers.query.filter_by(content_id=contentID, session_id=eventID).first() is not None : 
            error = 'Duplicate content'
        
        if error is not None:
            print('sending fail status')
            responseObject = {
                'status': 'fail',
                'message': error,
                'data' : ''
            }    
            return make_response(jsonify(responseObject))

        else:
            content = PermittedUsers()
            content.session_id = eventID
            content.content_id = contentID
            content.media_id=media_id
            content.user_email=user_email
            db.session.add(content)
            db.session.commit()

            responseObject = {
                'status': 'success',
                'message': 'Data added',
                'data' : ''
            }
            return make_response(jsonify(responseObject))
            
    return make_response(jsonify({'status':'fail', 'message' : 'check method type.','data': ''}))

@mod_permitted_users.route('/get', methods=('GET', 'POST', 'PUT'))
def getcontent():
    if request.method == 'POST':
        try :
            eventID = request.form['EventID']

        except Exception as e :
            return make_response(jsonify({'status' : 'fail', 'message' : str(e), 'data' : 'Missing form data'}))

        error = None
        if not eventID:
            eventID = 'Missing "eventID"'
        
        if error is not None:
            print('sending fail status')
            responseObject = {
                'status': 'fail',
                'message': error,
                'data' : ''            }    
            return make_response(jsonify(responseObject))

        else:
            con = PermittedUsers.query.filter_by(session_id=eventID).all()
            
            if not con:
                return make_response(jsonify({'status':'fail', 'message' : 'Data with given event ID not found','data': ''}))
            else:
                schema = PermittedUsersSchema()
                data = schema.dump(con,many=True)
                responseObject = {
                        'status': 'success',
                        'message': 'session contents data retrieved sucessfully',
                        'data' : data
                    }
                return make_response(jsonify(responseObject))

            
    return make_response(jsonify({'status':'fail', 'message' : 'check method type.','data': ''}))
