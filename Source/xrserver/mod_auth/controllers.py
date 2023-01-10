import secrets
from sqlalchemy import desc
from .models import User
from xrserver import db
from .schemas import UserSchema
import functools
from flask_sqlalchemy import SQLAlchemy
import urllib.parse
from  config import app_build_quest_value,app_build_windows_value,private_container_value,public_container_value,storage_account_value,front_base_url_value,storage_account_key_value,google_login_key_value,facebook_key_value,webgl_link_value
# from datetime import time
import time
from xrserver.mod_companyinfo.models import Companyinfo
from flask import jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

# Akhil...........................
from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
import random

# ................................
########### Siddharth ###########
from ..mailsetup import email_send
import datetime
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
s = URLSafeTimedSerializer("secretCode!")
# vrcode generator
# Getting systemRandom class instance out of secrets module


def vrotp():
    secretsGenerator = secrets.SystemRandom()
    vrcode = secretsGenerator.randrange(100000, 999999)
    return vrcode


########### Siddharth ###########
auth = HTTPBasicAuth(scheme="Bearer")
mod_auth = Blueprint("auth", __name__, url_prefix="/auth")
mod_user = Blueprint("user", __name__)





# To View Download Links
@mod_auth.route('/downloadlink', methods=('GET', ))
def downloadlink():
    if request.method == 'GET':
        # user = User.query.order_by(desc(User.date_created)).all()
    
            respData = {'app_build_quest_uri':app_build_quest_value,'app_build_windows_uri':app_build_windows_value,'google_login_key_value':google_login_key_value,'facebook_key_value':facebook_key_value}
            responseObject = {
                'status': 'success',
                'data': respData,
                'message': ''
            }
            # username, company_name, email, role, gender
            return make_response(jsonify(responseObject))

    return make_response(jsonify({'status': 'fail', 'message': 'check method type.', 'data': ''})), 202

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


########### Siddharth ###########

# Token Confirmation
@mod_auth.route("/confirm_email/<token>")
def confirm_email(token):
    try:
        if token is not None:
            email = s.loads( token, salt="email-confirm", max_age=3600)
            update_user = User.query.filter_by(email=email).first()
            update_user.is_active = True
            update_user.token = ""
            db.session.commit()
            return redirect(front_base_url_value+'login', code=302)
    except SignatureExpired as e:
        flash("The confirmation link is invalid or has expired.", "danger")
        return "<h1>The token is expired!</h1>"
        # return make_response(jsonify({"status": "fail", "message": str(e), "data": ""}))
    return "<h1>The token works!</h1>"

# password reset verify


@mod_auth.route("/reset_Password_verify/<token>")
def reset_Password_verify(token):
    try:
        if token is not None:
            email = s.loads(token, salt="email-confirm", max_age=600)
            update_user = User.query.filter_by(email=email).first()
            update_user.is_active = True
            db.session.commit()
            return redirect(front_base_url_value+'updatePassword', code=302)
            # return make_response(jsonify({
            #             "status": "success",
            #             "message": "Account is activated.",
            #             "data": "",
            #         }
            #     )
            # )
    except SignatureExpired as e:
        flash("The confirmation link is invalid or has expired.", "danger")
        return "<h1>The token is expired!</h1>"
        # return make_response(jsonify({"status": "fail", "message": str(e), "data": ""}))
    return "<h1>The token works!</h1>"

########### Siddharth ###########

# User Registration


@mod_auth.route("/register", methods=("GET", "POST"))
def register():
    # get the post data
    if request.method == "POST":
        try:
            email = request.form["email"]
            password = request.form["password"]
            # firstname = request.form["FirstName"]
            # lastname = request.form["LastName"]
            gender = request.form["Gender"]
            role = request.form["Role"]
            company_name = request.form['companyName']
            # phonenumber = request.form["PhoneNumber"]
            #date_of_birth = request.form["dob"]
            username = request.form["UserName"]
            token = s.dumps(email, salt="email-confirm")
            is_active = False
            g.user = user
        except Exception as e:
            return make_response(
                jsonify({"status": "fail", "message": str(e), "data": ""})
            )

        error = None

        if (
            email is None
            or password is None
            or username is None
            # or firstname is None
            # or lastname is None
            or gender is None
            # or role is None
            # or dob is None
        ):
            error = "Please enter all required fields."
        # check if user already exists
        if User.query.filter_by(email=email).first() is not None:
            error = "User {} is already registered.".format(email)

        # insert the user
        if error is None:
            new_user = User(
                email=email,
                password_hash=generate_password_hash(
                    password, method="sha256"),
                # last_name=lastname,
                # first_name=firstname,
                gender=gender,
                role=role,
                company_name=company_name,
                #date_of_birth = dob,
                token=token,
                is_active=is_active,
                user_name=username,
                # phone_number=phonenumber,
            )
            db.session.add(new_user)
            db.session.commit()

            print("success")
            email_send(email, 1, '' ,token)
            return make_response(
                jsonify(
                    {
                        "status": "success",
                        "message": "Registered successfully, Please check your email to activate the account.",
                        "data": "",
                        # "token": token,
                    }
                )
            )

        else:
            # flash(error)
            # print(error)

            return make_response(
                jsonify({"status": "fail", "message": error, "data": ""})
            )

    return make_response(
        jsonify({"status": "fail", "message": "Check method type.", "data": ""})
    )


# User Registration by Admin
@mod_auth.route("/addUser", methods=("GET", "POST"))
def addUser():
    if request.method == "POST":
        try:
            firstname = request.form["FirstName"]
            lastname = request.form["LastName"]
            gender = request.form["Gender"]
            role = request.form["Role"]
            company_name = request.form['companyName']
            email = request.form["email"]
            phonenumber = request.form["PhoneNumber"]
            username = request.form["UserName"]
            password = 'Password@123'
            token = s.dumps(email, salt="email-confirm")
            is_active = False
            # g.user = user
        except Exception as e:
            return make_response(
                jsonify({"status": "fail", "message": str(e), "data": ""})
            )

        error = None

        if (
            email is None
            or username is None
            or gender is None
            or role is None
            or company_name is None
        ):
            error = "Please enter all required fields."
        # check if user already exists
        if User.query.filter_by(email=email).first() is not None:
            error = "User {} is already registered.".format(email)

        # insert the user
        if error is None:
            new_user = User(
                email=email,
                password_hash=generate_password_hash(password, method="sha256"),
                last_name=lastname,
                first_name=firstname,
                gender=gender,
                role=role,
                company_name=company_name,
                token=token,
                is_active=is_active,
                user_name=username,
                phone_number=phonenumber,
            )
            db.session.add(new_user)
            db.session.commit()

            print("success")
            email_send(email, 7, '',token)
            return make_response(
                jsonify(
                    {
                        "status": "success",
                        "message": "Registered successfully.",
                        "data": "",
                        # "token": token,
                    }
                )
            )

        else:
            flash(error)
            return make_response(
                jsonify({"status": "fail", "message": error, "data": ""})
            )

    return make_response(
        jsonify({"status": "fail", "message": "Check method type.", "data": ""})
    )

# # Download Link
# @mod_auth.route("/downloadlink", methods=("GET", "POST"))
# def downloadlink():
#     data={
#         "questlink":app_build_quest_value,
#         "windowslink":app_build_windows_value
#     }
#     return make_response(
#         jsonify(
#             {
#                 "status": "success",
#                 "data": data,
#                 "message": ""
#             }
#         )
#     )

# User login
@mod_auth.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        start_time = time.time()
        try:
            email = request.form["email"]
            password = request.form["password"]

        except Exception as e:
            return make_response(
                jsonify({"status": "fail", "message": str(e), "data": ""})
            )
            
        error = None

        if not email:
            error = 'Missing "email"'
        elif not password:
            error = 'Missing "password"'
        else:
            user = User.query.filter_by(email=email).first()
            if user is None:
                error = "Entered email doesn't exist. Please register"
            elif not user.verify_password(password):
                error = "Login failed. Incorrect password."

        if error is None:
            user = User.query.filter_by(email=email).first()
            if user.is_active is False and user.token != "":
                error = "The given email address has not been activated. To activate your account, you must first confirm the email address."
                return make_response(
                    jsonify({"status": "fail", "message": error, "data": ""})
                )
            else:
                privatetoken=get_private_sas_token()
                publictoken=get_public_sas_token()
                compData=db.session.query(Companyinfo.company_id, Companyinfo.company_name, Companyinfo.license_key, Companyinfo.no_of_license,Companyinfo  ).join(User,(User.company_name==Companyinfo.company_id)).filter(User.email ==email).first()
                if compData is None:
                    company= user.company_name
                    company_id= ""
                    license_key= ""
                    no_of_license= ""
                else:                    
                    company= compData.company_name
                    company_id= compData.company_id
                    license_key= compData.license_key
                    no_of_license= compData.no_of_license

                userData = {
                    "email": email,
                    # "first_name": user.first_name,
                    # "last_name": user.last_name,
                    "user_name": user.user_name,
                    "gender": user.gender,
                    "role": user.role,
                    "company": company,
                    "company_id": company_id,
                    "license_key": license_key,
                    "no_of_license": no_of_license,
                    "system_id": user.system_ID,
                    "login_status": user.login_status,           
                    "privatetoken":privatetoken,
                    "publictoken":publictoken,
                    "publiccontainer":public_container_value,
                    "privatecontainer":private_container_value,
                    "storageaccount":storage_account_value,                    
                    "webgl_link":webgl_link_value
                }
                #print('private_container_name=',private_container_value)
                end_time = time.time()
                duration= end_time - start_time
                print("duration", duration)
                print(f'Time taken to run: {time.time() - start_time} seconds')
                return make_response(
                    jsonify(
                        {
                            "status": "success",
                            "data": {"token": user.is_active, "user_data": userData},
                            "message": "",
                            "Time taken": duration
                        }
                    )
                )
            
        else:
            return make_response(
                jsonify({"status": "fail", "message": error, "data": ""})
            )   
    return make_response(
        jsonify({"status": "fail", "message": "Check method type.", "data": ""})
    )
    

# xr-device login


@mod_auth.route("/device_login", methods=("GET", "POST"))
def device_login():
    if request.method == "POST":
        try:
            email = request.form["email"]
            password = request.form["password"]
            system_ID = request.form["system_id"]

        except Exception as e:
            return make_response(
                jsonify({"status": "fail", "message": str(
                    e), "data": "Not working!"})
            )

        error = None
        if not system_ID:
            error = 'Missing "systemID"'
            
        if not system_ID:
            login_status = False
        else:
            login_status = True

        if not email:
            error = 'Missing "email"'
        elif not password:
            error = 'Missing "password"'
        else:
            user = User.query.filter_by(email=email).first()
            if user is None:
                error = "Incorrect email."
            elif not user.verify_password(password):
                error = "Incorrect password."

        if error is None:
            privatetoken=get_private_sas_token()
            publictoken=get_public_sas_token()
            user = User.query.filter_by(email=email).first()
           
            if user.is_active is False:
                error = "Account is not verified."
                return make_response(jsonify({"status": "fail", "message": error, "data": ""}))
            # elif user.system_ID is not None and user.login_status is True:
            #     error = "Account is already active, Please logout from previous device and try again!!"
            #     return make_response(jsonify({"status": "fail", "message": error, "data": ""}))
            elif user.system_ID is None and user.login_status is False:
                error = "Account is already active, Please logout from previous device and try again!!"
                return make_response(jsonify({"status": "fail", "message": error, "data": ""}))
            elif user.system_ID is not None and user.login_status is True and user.system_ID != system_ID:
                status_status(email, login_status, system_ID)
                compData=db.session.query(Companyinfo.company_id, Companyinfo.company_name, Companyinfo.license_key, Companyinfo.no_of_license,Companyinfo  ).join(User,(User.company_name==Companyinfo.company_id)).filter(User.email ==email).first()
                if compData is None:
                    company= user.company_name
                    company_id= ""
                    license_key= ""
                    no_of_license= ""
                else:                    
                    company= compData.company_name
                    company_id= compData.company_id
                    license_key= compData.license_key
                    no_of_license= compData.no_of_license
                userData = {
                    "email": email,
                    # "first_name": user.first_name,
                    # "last_name": user.last_name,
                    "user_name": user.user_name,
                    "gender": user.gender,
                    "role": user.role,
                    "company": company,
                    "company_id": company_id,
                    "license_key": license_key,
                    "no_of_license": no_of_license,
                    "system_id": user.system_ID,
                    "login_status": user.login_status,
                    "privatetoken":privatetoken,
                    "publictoken":publictoken,
                    "publiccontainer":public_container_value,
                    "privatecontainer":private_container_value,
                    "storageaccount":storage_account_value,                    
                    "webgl_link":webgl_link_value    
                    
                }
                return make_response(jsonify({"status": "success", "message": user.email+" is logged in with new Device ID. "+ user.system_ID, "data": userData}))
            else:
                compData=db.session.query(Companyinfo.company_id, Companyinfo.company_name, Companyinfo.license_key, Companyinfo.no_of_license,Companyinfo  ).join(User,(User.company_name==Companyinfo.company_id)).filter(User.email ==email).first()
                if compData is None:
                    company= user.company_name
                    company_id= ""
                    license_key= ""
                    no_of_license= ""
                else:                    
                    company= compData.company_name
                    company_id= compData.company_id
                    license_key= compData.license_key
                    no_of_license= compData.no_of_license
                status_status(email, login_status, system_ID)
                userData = {
                    "email": email,
                    # "first_name": user.first_name,
                    # "last_name": user.last_name,
                    "user_name": user.user_name,
                    "gender": user.gender,
                    "role": user.role,
                    "company": company,
                    "company_id": company_id,
                    "license_key": license_key,
                    "no_of_license": no_of_license,
                    "system_id": user.system_ID,
                    "login_status": user.login_status,
                    "privatetoken":privatetoken,
                    "publictoken":publictoken,
                    "publiccontainer":public_container_value,
                    "privatecontainer":private_container_value,
                    "storageaccount":storage_account_value,                    
                    "webgl_link":webgl_link_value
                  
                }
                return make_response(
                    jsonify(
                        {
                            "status": "success",
                            "data": {"token": user.is_active, "user_data": userData},
                            "message": "Same device logged in.",
                        }
                    )
                )
        else:
            return make_response(
                jsonify({"status": "fail", "message": error, "data": ""})
            )

    return make_response(
        jsonify({"status": "fail", "message": "Check method type.", "data": ""})
    )

# device status reset


def status_status(email, login_status, system_ID):
    if email is not None:
        update_user = User.query.filter_by(email=email).first()
        update_user.login_status = login_status
        update_user.system_ID = system_ID
        db.session.commit()
        return "Success, device is activated"


# device logout functionality for xr-application
@mod_auth.route("/device_logout", methods=("GET", "POST"))
def device_logout():
    if request.method == "POST":
        try:
            email = request.form['email']
        except Exception as e:
            return make_response(jsonify({"status": "fail", "message": str(e), "data": "Entered Data is missing"}))

        error = None
        if (email is None):
            return "Please enter all required fields."
        # check if user already exists
        if User.query.filter_by(email=email).first() is None:
            return "Please enter correct email address.".format(email)
            
        if not email:
            return 'Enter valid email'
        else:
            update_status = User.query.filter_by(email=email).first()
            update_status.login_status = False
            update_status.system_ID = ""
            db.session.commit()
            message = 'Logged out Successfully.'
            return make_response(jsonify({"status": "success", "message": message, "data": ""}))
    return make_response(
        jsonify({"status": "fail", "message": "check method type.", "data": ""})
    )


# get user
@mod_auth.route("/getUser", methods=("GET", "POST", "DELETE"))
def user():
    if request.method == "POST":
        try:
            email = request.form["email"]
        except Exception as e:
            return make_response(
                jsonify({"status": "fail", "message": str(e), "data": ""})
            )

        user = (
            db.session.query(
                User.first_name,
                User.last_name,
                User.phone_number,
                User.gender,
                User.role,
                User.user_name,
                User.is_active,
                User.email,
                User.date_of_birth,
                User.company_name,
                User.system_ID,
                User.login_status
            )
            .filter_by(email=email)
            .first()
        )

        if user is None:
            error = "No existing user"
            responseObject = {"status": "fail", "data": "", "message": error}
            return make_response(jsonify(responseObject))

        else:
            user_schema = UserSchema()
            data = user_schema.dump(user)
            responseObject = {"status": "success", "data": data, "message": ""}
        return make_response(jsonify(responseObject))

    return make_response(
        jsonify({"status": "fail", "message": "check method type.", "data": ""}))

# View Users table list with accordingly pagination
@mod_auth.route('/getuserpaginationlist',methods=('GET','POST'))
def getuserpagination():

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('size', 5, type=int)
    email = request.args.get('email', '', type=str)
    company_id = request.args.get('company_id', '', type=str)
    company_id=company_id.strip()
    if email is None:
        if company_id is None or company_id=='':
            bookmarks = db.session.query(User.company_name.label("usercompany"),User.user_name,User.first_name,User.last_name,User.gender,User.email,User.phone_number,User.vrcode,User.role,User.is_active,Companyinfo.company_id,Companyinfo.company_name).join(Companyinfo, User.company_name == Companyinfo.company_id,isouter = True).paginate(page=page, per_page=per_page,error_out=False)
            #bookmarks = User.query(User.company_name,User.user_name,User.first_name,User.last_name,User.gender,User.email,User.phone_number,User.vrcode,User.role,User.is_active,Companyinfo.company_id,Companyinfo.company_name).join(Companyinfo,
            #Companyinfo.company_id == User.company_name,
            #isouter = True #Add this to implement left outer join
            #).paginate(page=page, per_page=per_page,error_out=False)
        else:
            bookmarks = db.session.query(User.company_name.label("usercompany"),User.user_name,User.first_name,User.last_name,User.gender,User.email,User.phone_number,User.vrcode,User.role,User.is_active,Companyinfo.company_id,Companyinfo.company_name).join(Companyinfo, User.company_name == Companyinfo.company_id,isouter = True).filter(User.company_name==company_id).paginate(page=page, per_page=per_page,error_out=False)
    else:
        email = "%{}%".format(email)
        if company_id is None or company_id=='':
            bookmarks = db.session.query(User.company_name.label("usercompany"),User.user_name,User.first_name,User.last_name,User.gender,User.email,User.phone_number,User.vrcode,User.role,User.is_active,Companyinfo.company_id,Companyinfo.company_name).join(Companyinfo, User.company_name == Companyinfo.company_id,isouter = True).filter(User.email.like(email)).paginate(page=page, per_page=per_page,error_out=False)     
            #bookmarks = User.query(User.company_name,Companyinfo.company_id,User.user_name,User.first_name,User.last_name,User.gender,User.email,User.phone_number,User.vrcode,User.role,User.is_active).join(Companyinfo,
            #Companyinfo.company_id == User.company_name,
            #isouter = True #Add this to implement left outer join
            #).filter(User.email.like(email)).paginate(page=page, per_page=per_page,error_out=False)
        else:
            bookmarks = db.session.query(User.company_name.label("usercompany"),User.user_name,User.first_name,User.last_name,User.gender,User.email,User.phone_number,User.vrcode,User.role,User.is_active,Companyinfo.company_id,Companyinfo.company_name).join(Companyinfo, User.company_name == Companyinfo.company_id,isouter = True).filter(User.company_name==company_id).filter(User.email.like(email)).paginate(page=page, per_page=per_page,error_out=False)     
    
  
    data = []

    for bookmark in bookmarks.items:
        company=""
        if bookmark.company_name=="" or bookmark.company_name is None:
            company=bookmark.usercompany
        else:
            company=bookmark.company_name
        
        data.append({
            'company_name': company,
            'company_id': bookmark.company_id,
            'user_name': bookmark.user_name,
            'first_name': bookmark.first_name,
            'last_name': bookmark.last_name,
            'gender': bookmark.gender,
            'email': bookmark.email,
            'phone_number': bookmark.phone_number,
            'vrcode': bookmark.vrcode,
            'role': bookmark.role,
            'is_active': bookmark.is_active,
        })

    """ meta = {
        "page": bookmarks.page,
        'pages': bookmarks.pages,
        'total_count': bookmarks.total,
        'prev_page': bookmarks.prev_num,
        'next_page': bookmarks.next_num,
        'has_next': bookmarks.has_next,
        'has_prev': bookmarks.has_prev,

    } """

    return jsonify({'data': data, "totalItems": bookmarks.total,"totalPages":bookmarks.pages,"currentPage":bookmarks.page}),202
# View Users table list
@mod_auth.route('/getUsersList', methods=('GET', 'POST', 'PUT'))
def getUsersList():
    if request.method == 'GET':
        # user = User.query.order_by(desc(User.date_created)).all()
        user = db.session.query(User.company_name,
                                User.user_name,
                                User.first_name,
                                User.last_name,
                                User.gender,
                                User.email,
                                User.phone_number,
                                User.vrcode,
                                User.role,
                                User.is_active,
                                ).all()
        if user is not None:
            user_schema = UserSchema()
            data = user_schema.dump(user, many=True)
            respData = {'user': data}
            responseObject = {
                'status': 'success',
                'data': respData,
                'message': ''
            }
            # username, company_name, email, role, gender
        return make_response(jsonify(responseObject))

    return make_response(jsonify({'status': 'fail', 'message': 'check method type.', 'data': ''})), 202

# Get Users list based on company name and if empty it will display all users


@mod_auth.route('/getCompanyUsersList', methods=('GET', 'POST', 'PUT'))
def getCompanyUsersList():
    if request.method == 'POST':
        try:
            company_name = request.form['company_name']
        except Exception as e:
            return make_response(jsonify({'status': 'fail', 'message': str(e), 'data': 'missing Company Name'}))

        print(company_name)

        if not company_name:
            # error = "No Company Name Entered"
            com = db.session.query(User.user_name,
                                   User.company_name,
                                   User.email,
                                   User.role,
                                   User.gender).all()
            user_schema = UserSchema()
            data = user_schema.dump(com, many=True)
            responseObject = {
                'status': 'success',
                'data': data,
                'message': ''
            }
            return make_response(jsonify(responseObject)), 202
        else:
            # error = "Company name Entered"
            com = db.session.query(User.user_name,
                                   User.company_name,
                                   User.email,
                                   User.role,
                                   User.gender).filter_by(company_name=company_name).all()
            user_schema = UserSchema()
            data = user_schema.dump(com, many=True)
            responseObject = {
                'status': 'success',
                'data': data,
                'message': ''
            }

            return make_response(jsonify(responseObject)), 202
    return make_response(jsonify({'status': 'fail', 'message': 'check method type.', 'data': ''}))

# reset password


@mod_auth.route("/resetPassword", methods=("GET", "POST", "DELETE"))
def resetPassword():
    if request.method == "POST":
        try:
            email = request.form["email"]
        except Exception as e:
            return make_response(
                jsonify(
                    {"status": "fail", "message": str(
                        e), "data": "Data is missing"}
                )
            )
        # print(email)
        user = User.query.filter_by(email=email).first()
        if user is None:
            print("email not found")
            error = "No existing user"
            responseObject = {"status": "fail", "data": "", "message": error}
            return make_response(jsonify(responseObject))
        else:
            token = s.dumps(email, salt="email-confirm")
            user.is_active = False
            user.token = token
            db.session.commit()
            email_send(email, 7, '', token)

            responseObject = {
                "status": "success",
                "data": "",
                "message": "Reset Password sent to Mail!",
                "token": token,
                "email": email,
            }
        return make_response(jsonify(responseObject))

    return make_response(
        jsonify({"status": "fail", "message": "check method type.", "data": ""})
    )

# update password


@mod_auth.route("/updatePassword", methods=("GET", "POST"))
def updatePassword():
    if request.method == "POST":
        try:
            uemail = request.form['email']
            upass = request.form['password']
        except Exception as e:
            return make_response(
                jsonify(
                    {"status": "fail", "message": str(
                        e), "data": "Data is missing"}
                )
            )

        user = User.query.filter_by(email=uemail).first()
        # return user.email

        if user.email is None and user.token is None:
            return "data is missing"
        else:
            password_hash = generate_password_hash(upass, method="sha256")
            user.password_hash = password_hash
            user.token = ''
            user.is_active = True
            db.session.commit()
            email_send(user.email, 9)

            responseObject = {
                "status": "success",
                "data": "",
                "message": "Password Reset successful!"
            }
        return make_response(jsonify(responseObject))
    return make_response(
        jsonify({"status": "fail", "message": "check method type.", "data": ""})
    )


# generate VR code from Web
@mod_auth.route("/generatevrcode", methods=("GET", "POST"))
def generatevrcode():
    tmp = request.form
    for tmp in request.form:
        print(tmp)
    if request.method == "POST":
        try:
            email = request.form['email']
            print(email)
        except Exception as e:
            return make_response(
                jsonify(
                    {"status": "fail", "message": str(
                        e), "data": "Data is missing"}
                )
            )
        user = User.query.filter_by(email=email).first()
        # return user.email
        print(user)

        if user.email is None:
            return "User is missing"
        else:
            user.vrcode = vrotp()
            db.session.commit()

            responseObject = {
                "status": "success",
                "data": user.vrcode,
                "message": "VR Code Generated successfully!"
            }
        return make_response(jsonify(responseObject))

    return make_response(
        jsonify({"status": "fail", "message": "Check method type.", "data": ""})
    )

# User login in VR via OTP
@mod_auth.route("/vrlogin", methods=("GET", "POST"))
def vrlogin():
    # VR OTP login
    if request.method == "POST":
        try:
            vrcode = request.form["vrcode"]

        except Exception as e:
            return make_response(
                jsonify({"status": "fail", "message": str(e), "data": ""})
            )
        # check if user vrcode exists
        if User.query.filter_by(vrcode=vrcode).first() is None:
            error = "vrcode {} doesn't exist.".format(vrcode)
            return make_response(
                jsonify(

                    {
                        "status": "fail",
                        "data": "",
                        "message": error,
                    }
                )
            )
        else:
            privatetoken=get_private_sas_token()
            publictoken=get_public_sas_token()
            user = User.query.filter_by(vrcode=vrcode).first()
            userData = {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "user_name": user.user_name,
                "privatetoken":privatetoken,
                "publictoken":publictoken,
                "publiccontainer":public_container_value,
                "privatecontainer":private_container_value,
                "storageaccount":storage_account_value,                    
                "webgl_link":webgl_link_value                
            }  # , 'is_active' : user.is_active

            user.vrcode = ''
            db.session.commit()
            email_send(user.email, 10)
            return make_response(
                jsonify(
                    {
                        "status": "success",
                        "data": {"Account Status": user.is_active, "user_data": userData},
                        "message": "VR device connected",
                    }
                )
            )

    return make_response(
        jsonify({"status": "fail", "message": "Check method type.", "data": ""})
    )


# delete user

@mod_auth.route('/deleteUser', methods=('GET', 'POST', 'PUT'))
def deleteUsers():
    if request.method == 'POST':
        try:
            email = request.form["email"]
        except Exception as e:
            return make_response(
                jsonify({"status": "fail", "message": str(e), "data": ""})
            )
        user = User.query.filter_by(email=email).first()

        if user is None:
            error = "No existing user"
            responseObject = {"status": "fail", "data": "", "message": error}
            return make_response(jsonify(responseObject))

        else:
            db.session.delete(user)
            db.session.commit()
            responseObject = {"status": "success", "data": email,
                              "message": f"User {email} deleted Successfully!"}
        return make_response(jsonify(responseObject))

    return make_response(jsonify({'status': 'fail', 'message': 'check method type.', 'data': ''})), 202


# User Details Update API
@mod_auth.route("/userUpdate", methods=["PUT"])
def userUpdate():
    if request.method == "PUT":
        try:
            email = request.form["email"]
            firstname = request.form["FirstName"]
            lastname = request.form["LastName"]
            phonenumber = request.form["PhoneNumber"]
            username = request.form["UserName"]
            gender = request.form["Gender"]
            role = request.form["Role"]

        except Exception as e:
            return make_response(jsonify({"status": "fail", "message": str(e), "data": "Data is missing"}))

        user = User.query.filter_by(email=email).first()

        if not username:
            username = user.user_name
        else:
            username = username

        if not firstname:
            firstname = user.first_name
        else:
            firstname = firstname

        if not lastname:
            lastname = user.first_name
        else:
            lastname = lastname

        if not phonenumber:
            phonenumber = user.first_name
        else:
            phonenumber = phonenumber

        if not gender:
            gender = user.gender
        else:
            gender = gender

        if not role:
            role = user.role
        else:
            role = role

        if user.email is None:
            return "data is missing"
        else:
            user.user_name = username
            user.first_name = firstname
            user.last_name = lastname
            user.phone_number = phonenumber
            user.gender = gender
            user.role = role

            db.session.commit()

            responseObject = {
                "status": "success",
                "data": "",
                "message": f"User {email} details updated successfully!"
            }
        return make_response(jsonify(responseObject))
    return make_response(
        jsonify({"status": "fail", "message": "check method type.", "data": ""})
    )


# Change password
@mod_auth.route("/changePassword", methods=("GET", "POST"))
def changePassword():
    if request.method == "POST":
        try:
            email = request.form['email']
            oldpass = request.form['password']
            newpass = request.form['newpassword']
        except Exception as e:
            return make_response(jsonify({"status": "fail", "message": str(e), "data": "Entered Data is missing"}))

        error = None

        if not email and not oldpass and not newpass:
            return 'Enter valid details'
        else:
            user = User.query.filter_by(email=email).first()
            # firstname = (User.query(User.first_name).filter_by(email=email).first())
            print("user", user.email)
            if not user.verify_password(oldpass):
                # error = "Whoops! Password do not match."
                error = "Entered old password is wrong."
                return make_response(jsonify({"status": "fail", "message": error, "data": ""}))
            else:
                user.password_hash = generate_password_hash(
                    newpass, method="sha256")
                db.session.commit()
                message = 'Password successfully changed.'
                email_send(user.email, 9)
                return make_response(jsonify({"status": "success", "message": message, "data": ""}))
    return make_response(
        jsonify({"status": "fail", "message": "check method type.", "data": ""})
    )

# social user login
@mod_auth.route("/sociallogin", methods=("GET", "POST"))
def social_login():
    if request.method == "POST":
        try:
            email = request.form["email"]
            userName = request.form["userName"]
            imagePath = request.form["imagePath"]
            provider = request.form['provider']
            # isSocialUSer = request.form['isSocialUser']
            token = request.form['token']

        except Exception as e:
            return make_response(
                jsonify({"status": "fail", "message": str(
                    e), "data": "Not working!"})
            )

        error = None
        privatetoken=get_private_sas_token()
        publictoken=get_public_sas_token()
        if not email:
            error = 'Missing email'
        elif not userName:
            error = 'Missing userName'
        elif not imagePath:
            error = 'Missing imagePath'
        # elif not isSocialUSer:
        #     error = 'Missing isSocialUser'
        elif not provider:
            error = 'Missing provider'
        else:
            user = User.query.filter_by(email=email).first()
            print('user', user)
            if user is not None:
                error = "account already registered with this email."
                return make_response(
                    jsonify(
                        {
                            "status": "success",
                            "data": {"user_data": {
                            "privatetoken":privatetoken,
                            "publictoken":publictoken,
                            "publiccontainer":public_container_value,
                            "privatecontainer":private_container_value,
                            "storageaccount":storage_account_value,                    
                            "webgl_link":webgl_link_value
                            }},
                            "message": " Login Success"
                        }
                    )
                )

        if error is None:
            default_password = "Password@123"
            new_user = User(
                email=email,
                password_hash=generate_password_hash(
                default_password, method="sha256"),
                gender='undisclosed',
                role='User',
                company_name='undisclosed',
                token=token,
                is_active=1,
                user_name=userName,
                image_path=imagePath,
                is_social_user=True,
                provider=provider
            )
            db.session.add(new_user)
            db.session.commit()
            
            return make_response(
                jsonify(
                    {
                        "status": "success",
                        "data": {"user_data": {
                            "privatetoken":privatetoken,
                            "publictoken":publictoken,
                            "publiccontainer":public_container_value,
                            "privatecontainer":private_container_value,
                            "storageaccount":storage_account_value,                    
                            "webgl_link":webgl_link_value
                        }},
                        "message": " Login Success"
                    }
                )
            )
        else:
            return make_response(
                jsonify({"status": "fail", "message": error, "data": ""})
            )

    return make_response(
        jsonify({"status": "fail", "message": "Check method type.", "data": ""})
    )


from datetime import datetime, timedelta
from azure.storage.blob import generate_container_sas, ContainerSasPermissions


# account_name = "xrdemo"
# account_key = "6ENSAfOyVGzLff0sOk8bsAspMnXYdju7OjjZefgshK9y+Xv387ZR0RpYXexCG6/i0bqOIcR6RTu/+AStTUrfDg=="
# private_container_name = "xrconnect-demo"
# public_container_name = "public-container"

#account_name = "xrconn"
#account_key = "wqP//FaN72a+JVFIgr1w7lnVObSkj5e4UmQEMOAWjVI3GDZ5aU7SNIjlqRSNhrcOfeCqqIEuXn909MGwqlu7gQ=="
#private_container_name = "staging-server"
#public_container_name = "public-container"

# using generate_private_container_sas
@mod_auth.route("/getprivatesastoken")
def get_private_sas_token():
    container_sas_token = generate_container_sas(
        account_name=storage_account_value,
        container_name=private_container_value,
        account_key=storage_account_key_value,
        permission=ContainerSasPermissions(read=True, write=True, delete=True, list=True,add=True,create=True),
        start = datetime.utcnow(),
        expiry = datetime.utcnow() + timedelta(hours=24)
    )
    #start=datetime.utcnow() + timedelta(hours=5, minutes=30),
    #token=container_sas_token.replace('%3A', ':')
    #token=urllib.parse.unquote(container_sas_token)
    #container_sas_token="sp=racwdli&st=2022-05-20T02:53:43Z&se=2022-06-30T10:53:43Z&sv=2020-08-04&sr=c&sig=PmH5I2uSXittWE7vqhVyg4Hc8S%2B%2FZecm0mg0aNCJCCM%3D"
    #token=urllib.parse.unquote(container_sas_token)
    # blob_url_with_container_sas_token = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{container_sas_token}"
    return f"{container_sas_token}"

# using generate_public_container_sas
@mod_auth.route("/getpublicsastoken")
def get_public_sas_token():
    container_sas_token = generate_container_sas(
        account_name=storage_account_value,
        container_name=public_container_value,
        account_key=storage_account_key_value,
        permission=ContainerSasPermissions(read=True, write=True, delete=True, list=True,add=True, create=True),
        start=datetime.utcnow(),
        expiry=datetime.utcnow() + timedelta(hours=24)
    )
    #token=container_sas_token.replace('%3A', ':')
	# token=urllib.parse.unquote(container_sas_token)
    #container_sas_token="sp=racwdli&st=2022-05-20T02:52:44Z&se=2022-06-30T10:52:44Z&sv=2020-08-04&sr=c&sig=hFLMKlBB1ivmyKjnbLDWkR6eWz7rH4%2FS1pbwF5y02Xo%3D"
    #token=urllib.parse.unquote(container_sas_token)
    # blob_url_with_container_sas_token = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{container_sas_token}"
    return f"{container_sas_token}"

# using generate_public_container_sas
@mod_auth.route("/checkpassword", methods=("GET", "POST"))
def checkpassword():
    password="Password@123"
    password_hash=generate_password_hash(password, method="sha256")

    return password_hash


# User checkpin
@mod_auth.route("/checkpin", methods=("GET", "POST"))
def checkpin():
    if request.method == "POST":
        start_time = time.time()
        try:

            pin = request.form["pin"]

        except Exception as e:
            return make_response(
                jsonify({"status": "fail", "message": str(e), "data": ""})
            )

        error = None

        if not pin:
            error = 'Missing "Pin"'

        if error is None:
            if pin == '1234':
                end_time = time.time()
                duration = end_time - start_time
                return make_response(
                    jsonify(
                        {
                            "status": "success",
                            "message": "enter pin is correct",
                            "Time taken": duration,
                        }
                    )
                )
            else:
                end_time = time.time()
                duration = end_time - start_time
                return make_response(
                    jsonify(
                        {"status": "fail", "message": 'please enter correct pin', "data": "", "Time taken": duration})
                )

        else:
            end_time = time.time()
            duration = end_time - start_time
            return make_response(
                jsonify({"status": "fail", "message": error,
                        "data": "", "Time taken": duration})
            )
    return make_response(
        jsonify({"status": "fail", "message": "Check method type.", "data": ""})
    )