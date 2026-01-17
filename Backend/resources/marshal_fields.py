from flask_restful import fields

admin_fields = {
    "name": fields.String
}

user_fields = {
    "user_id": fields.Integer,
    "user_name": fields.String,
    "user_password": fields.String,
    "contact_number": fields.String,
    "email": fields.String,
    # "user_admin": fields.Nested(admin_fields)
}