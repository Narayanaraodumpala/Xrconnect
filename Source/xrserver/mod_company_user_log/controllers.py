import functools
#from datetime import time
from flask import jsonify, make_response, send_from_directory, send_file
from flask import stream_with_context, Response

import base64
from base64 import b64encode
from json import dumps
import io
import os
import random
import string
#import psutil
from werkzeug.utils import secure_filename

# from flask_httpauth import HTTPBasicAuth
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from xrserver import db,app

# Import module models
from xrserver.mod_companyinfo.models import Companyinfo
from .models import Companyuserlog
from .schemas import  CompanyuserlogSchema
mod_company_user_log = Blueprint('companyuserlog', __name__, url_prefix='/companyuserlog')

# Opening new User Logs
@mod_company_user_log.route('/openUserLog', methods=("GET", "POST"))
def openUserLog():
    if request.method == 'POST':
        try :
            company_id  = request.form['company_id']
            user_id = request.form['user_id']
            device_id = request.form['device_id']
            license_key = request.form['license_key']
            start_date = request.form['start_date']
            status = request.form['status']
    
        except Exception as e :
            return make_response(jsonify({'status' : 'fail', 'message' : str(e), 'data' : 'Missing form Data'}))
            
        error = None

        if not company_id:
            error = 'Missing "Company ID"'
        elif not user_id:
            error = 'Missing "User ID"'
        elif not device_id:
            error = 'Missing "Device ID"'
        elif not license_key:
            error = 'Missing "License Key"'
        elif not status:
            error = 'Missing "Status"'
        elif not start_date:
            error = 'Missing "Start Date"'
        elif status!='open' :
            error = 'Status Must be "open"'

       
        #error = 'User already opened the log please the Close log and then open'

        if error is None: 
            if Companyuserlog.query.filter_by(company_id=company_id,user_id = user_id,device_id=device_id,license_key=license_key,status=status).first() is None :

                cinfo = Companyuserlog()
                cinfo.company_id = company_id
                cinfo.user_id = user_id
                cinfo.license_key = license_key
                cinfo.device_id = device_id
                cinfo.start_date=start_date
                cinfo.status=status
                db.session.add(cinfo)
                db.session.commit()

            companyinfo=Companyinfo.query.filter_by(license_key=license_key).first()
            companyuserlog=Companyuserlog.query.filter_by(license_key=license_key,status='open').count()

            responseObject = {
                'status': 'success',
                'message': 'User Log Opened. No of License for this company are '+ str(companyinfo.no_of_license) + " and Active Users are "+ str(companyuserlog),
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

# Close new User Logs
@mod_company_user_log.route('/closeUserLog', methods=("GET", "POST"))
def closeUserLog():
    if request.method == 'POST':
        try :
            company_id  = request.form['company_id']
            user_id = request.form['user_id']
            device_id = request.form['device_id']
            license_key = request.form['license_key']
            end_date = request.form['end_date']
            status = request.form['status']
    
        except Exception as e :
            return make_response(jsonify({'status' : 'fail', 'message' : str(e), 'data' : 'Missing form Data'}))
            
        error = None

        if not company_id:
            error = 'Missing "Company ID"'
        elif not user_id:
            error = 'Missing "User ID"'
        elif not device_id:
            error = 'Missing "Device ID"'
        elif not license_key:
            error = 'Missing "License Key"'
        elif not status:
            error = 'Missing "Status"'
        elif not end_date:
            error = 'Missing "End Date"'
        elif status!='close' :
            error = 'Status Must be "close"'
        

        #elif Companyuserlog.query.filter_by(company_id=company_id,user_id = user_id,device_id=device_id,license_key=license_key,status=status).first() is not None :
        #    error = 'User already closed the log'

        if error is None:
            
            db.session.query(
                Companyuserlog
            ).filter_by(
                company_id=company_id,user_id = user_id,device_id=device_id,license_key=license_key,status='open'
            ).update({
                Companyuserlog.end_date: end_date,
                Companyuserlog.status: status
            })

            db.session.commit()

            companyinfo=Companyinfo.query.filter_by(license_key=license_key).first()
            companyuserlog=Companyuserlog.query.filter_by(license_key=license_key,status='open').count()

            responseObject = {
                    'status': 'success',
                    'message': 'User Log Closed. No of License for this company are '+ str(companyinfo.no_of_license) + " and Active Users are "+ str(companyuserlog),
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

# get company details based on company ID
@mod_company_user_log.route("/getCompanyDetails", methods=("GET", "POST", "DELETE"))
def getCompanyDetails():
    if request.method == "POST":
        try:
            companyid = request.form["companyid"]
        
        except Exception as e :
            return make_response(jsonify({'status' : 'fail', 'message' : str(e), 'data' : 'Missing form Data'}))

        compData = (
            db.session.query(
                Companyinfo.date_created,
                Companyinfo.company_id,
                Companyinfo.company_name,
                Companyinfo.ceo_name,
                Companyinfo.email,
                Companyinfo.number,
                Companyinfo.website,
                Companyinfo.address,
                Companyinfo.status,
                Companyinfo.technology,
                Companyinfo.company_created_by
            ).filter_by(company_id=companyid).first())

        if compData is None:
            error = "No existing company Data"
            responseObject = {"status": "fail", "data": "", "message": error}
            return make_response(jsonify(responseObject))

        else:
            comp_schema = CompanyinfoSchema()
            data = comp_schema.dump(compData)
            responseObject = {"status": "success", "data": data, "message": ""}
        return make_response(jsonify(responseObject))

    return make_response(
        jsonify({"status": "fail", "message": "check method type.", "data": ""}))

# View list of companies
@mod_company_user_log.route('/getCompanyList', methods=('GET', 'POST', 'PUT'))
def getCompanyList():
    if request.method == 'GET':
        # user = User.query.order_by(desc(User.date_created)).all()
        compData = db.session.query(Companyinfo.date_created,
                Companyinfo.company_id,
                Companyinfo.company_name,
                Companyinfo.ceo_name,
                Companyinfo.email,
                Companyinfo.number,
                Companyinfo.website,
                Companyinfo.address,
                Companyinfo.status,
                Companyinfo.technology,
                Companyinfo.no_of_license,
                Companyinfo.license_key,
                Companyinfo.company_created_by).all()
        if compData is not None:
            comp_schema = CompanyinfoSchema()
            data = comp_schema.dump(compData,many = True)
            respData = {'compData' : data}
            responseObject = {
                'status': 'success',
                'data': respData,
                'message' : ''
            }
            # username, company_name, email, role, gender
        return make_response(jsonify(responseObject))
        
    return make_response(jsonify({'status':'fail', 'message' : 'check method type.','data': ''})), 202

# Get companies list based on companyid and if empty it will display all companies data
@mod_company_user_log.route('/getCompanyBasedList', methods=('GET', 'POST', 'PUT'))
def getCompanyBasedList():
    if request.method == 'POST':
        try :
            companyid = request.form['companyid']
        
        except Exception as e : 
            return make_response(jsonify({'status' : 'fail', 'message' : str(e),'data' : 'missing Company Name'}))

        if not companyid:
            # error = "No Company Name Entered"
            compData = db.session.query(Companyinfo.date_created,
                Companyinfo.company_id,
                Companyinfo.company_name,
                Companyinfo.ceo_name,
                Companyinfo.email,
                Companyinfo.number,
                Companyinfo.website,
                Companyinfo.address,
                Companyinfo.status,
                Companyinfo.technology,
                Companyinfo.no_of_license,
                Companyinfo.license_key,
                Companyinfo.company_created_by).all()
            comp_schema = CompanyinfoSchema()
            data = comp_schema.dump(compData,many = True)
            responseObject = {
                'status': 'success',
                'data': data,
                'message' : ''
            } 
            return make_response(jsonify(responseObject)), 202
        else:
            # error = "Company name Entered"
            compData = db.session.query(Companyinfo.date_created,
                Companyinfo.company_id,
                Companyinfo.company_name,
                Companyinfo.ceo_name,
                Companyinfo.email,
                Companyinfo.number,
                Companyinfo.website,
                Companyinfo.address,
                Companyinfo.status,
                Companyinfo.technology,
                Companyinfo.company_created_by).filter_by(company_id=companyid).all()
            comp_schema = CompanyinfoSchema()
            data = comp_schema.dump(compData,many = True)
            responseObject = {
                'status': 'success',
                'data': data,
                'message' : ''
            } 
            
            return make_response(jsonify(responseObject)), 202    
    return make_response(jsonify({'status':'fail', 'message' : 'check method type.','data': ''}))

# deleting a company
@mod_company_user_log.route('/deleteCompany', methods=('GET', 'POST', 'PUT'))
def deleteCompany():
    if request.method == 'POST':
        try:
            companyid = request.form["companyid"]
        
        except Exception as e : 
            return make_response(jsonify({'status' : 'fail', 'message' : str(e),'data' : 'missing Company Name'}))

        compData = Companyinfo.query.filter_by(company_id=companyid).first()

        if compData is None:
            error = "No existing compData"
            responseObject = {"status": "fail", "data": "", "message": error}
            return make_response(jsonify(responseObject))

        else:
            db.session.delete(compData)
            db.session.commit()
            responseObject = {"status": "success", "data": companyid, "message": "Company deleted successfully"}
        return make_response(jsonify(responseObject))

    return make_response(jsonify({'status': 'fail', 'message': 'check method type.', 'data': ''})), 202

@mod_company_user_log.route("/generate_key_string", methods=("GET", "POST"))
def generate_key_string():
    tokens= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    segment_chars = 5
    num_segments = 4
    key_string = ''
    for x in range(num_segments):
        segment = ''
        for y in range(segment_chars):
            segment+=random.choice(tokens)
        
        key_string+=segment
        if(x<(num_segments-1)):
            key_string+='-'
        
    return key_string
    """ charecter_set='-'
    if uppercase:
        charecter_set+=string.ascii_uppercase
    if lowecase:
        charecter_set+=string.ascii_lowercase
    if numbers:
        charecter_set+=string.digits
    return ''.join(random.choice(charecter_set) for i in range(length)) """


# Update company infomation
@mod_company_user_log.route("/updateCompany", methods=["PUT"])
def updateCompany():
    if request.method == "PUT":
        try:
            company_id  = request.form['companyid']
            companyName = request.form['company_name']
            ceo_name = request.form['ceo_name']
            email = request.form['email']
            number = request.form['number']
            website = request.form['website']
            address = request.form['address']
            status = request.form['status']
            # technology = request.form['technology']

        except Exception as e:
            return make_response(jsonify({"status": "fail", "message": str(e), "data": "Data is missing"}))
            
        compData = Companyinfo.query.filter_by(company_id=company_id).first()

        if not ceo_name:
            ceo_name = compData.ceo_name
        else:
            ceo_name = ceo_name

        if not companyName:
            company_name = compData.company_name
        else:
            company_name = companyName

        if not email:
            email = compData.email
        else:
            email = email
        
        if not number:
            number = compData.number
        else:
            number = number

        if not website:
            website = compData.website
        else:
            website = website

        if not address:
            address = compData.address
        else:
            address = address
        
        if not status:
            status = compData.status
        else:
            status = status

        if compData.company_id is None:
            return "Data is missing"
        else:
            compData.company_name = company_name
            compData.ceo_name = ceo_name
            compData.email = email
            compData.number = number
            compData.website = website
            compData.address = address
            compData.status = status

            db.session.commit()

            responseObject = {
                "status": "success",
                "data": "",
                "message": "Company details updated successfully!"
            }
        return make_response(jsonify(responseObject))
    return make_response(
        jsonify({"status": "fail", "message": "check method type.", "data": ""})
    )
