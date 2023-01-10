from xrserver import ma
from .models import Companyuserlog
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

class CompanyuserlogSchema(SQLAlchemySchema):
    class Meta:
        model = Companyuserlog
       
    id = auto_field()
    user_id = auto_field()
    company_id = auto_field()
    license_key = auto_field()
    device_id = auto_field()
    start_date = auto_field()
    end_date = auto_field()
    status = auto_field()