import functools
#from datetime import time
from flask import jsonify, make_response
# from flask_httpauth import HTTPBasicAuth
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from xrserver import db

# Import module models
from .models import contentAccess
# from ..mailsetup import email_send
from .schemas import contentAccessSchema

mod_content_access = Blueprint(
    'content_access', __name__, url_prefix='/contentAccess')


@mod_content_access.route('/contentInvite', methods=('GET', 'POST', 'PUT'))
def contentInvite():
    if request.method == "POST":
        try:
            emailList = list((request.form["email"]).split(","))
            contentId = request.form['contentId']
            
            print(type(emailList), 'email', emailList)
        except Exception as e:
            return make_response(
                jsonify({"status": "fail", "message": str(e), "data": ""})
            )
        
        if contentAccess.query.filter_by(content_id=contentId).first() is not None:
            error = "Duplicate contentid".format(contentId)
            responseObject = {"status": "fail",
                             "message": error}
            return make_response(jsonify(responseObject))
        else:


            for email in emailList:
                # email_send(email, 5)
                content = contentAccess()
                content.content_id = contentId
                content.invitee_email = email

                db.session.add(content)
                db.session.commit()
                print(email)
            responseObject = {"status": "success",
                            "data": emailList,"contentId":contentId, "message": ""}
            return make_response(jsonify(responseObject))
        

    return make_response(
        jsonify({"status": "fail", "message": "check method type.", "data": ""})
    )
