import functools
#from datetime import time
from flask import jsonify, make_response
# from flask_httpauth import HTTPBasicAuth
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from xrserver import db

# Import module models
from .models import InviteeList
from ..mailsetup import email_send
from .schemas import InvieeListSchema

mod_invitee_list = Blueprint(
    'invitee_list', __name__, url_prefix='/inviteeList')


@mod_invitee_list.route('/inviteEmail', methods=('GET', 'POST', 'PUT'))
def inviteEmail():
    if request.method == "POST":
        try:
            emailList = list((request.form["email"]).split(","))
            sessionId = request.form['eventID']
            print(type(emailList), 'email', emailList)
        except Exception as e:
            return make_response(
                jsonify({"status": "fail", "message": str(e), "data": ""})
            )

        for email in emailList:
            email_send(email, 5)
            content = InviteeList()
            content.session_id = sessionId
            content.invitee_email = email
            content.invite_link = 'https://demo.xrconnect.com/web/login'

            db.session.add(content)
            db.session.commit()
            print(email)
        responseObject = {"status": "success",
                          "data": emailList,"eventID":sessionId, "message": "Invitation Sent Successfully"}
        return make_response(jsonify(responseObject))

    return make_response(
        jsonify({"status": "fail", "message": "check method type.", "data": ""})
    )
