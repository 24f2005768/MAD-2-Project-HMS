from models import User, db 

class UserService():

    @staticmethod
    def get_by_id(id):
        user = User.query.get(id)
        if not user:
            return 400
        return user 