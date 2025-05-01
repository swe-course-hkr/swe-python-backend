from app.database.models import UserModel
from datetime import datetime
from app.database import db

class UserDatabase:

    def update_user_details(user_id, **kwargs):

        db.session.query(UserModel) \
            .filter(UserModel.id == user_id) \
            .update(kwargs)
        db.session.commit()

        return db.session.query(UserModel).filter(UserModel.id == user_id).first()


    def create_user(**kwargs):
        try:
            new_user = UserModel(**kwargs)
            db.session.add(new_user)
            db.session.commit()
        except ValueError as e:
            raise e
        
        return new_user



    # for debugging purposes
    def fetch():
        users = db.session.query(UserModel).all()
        return users
    
    def userExists(username):
        user = db.session.query(UserModel).filter(UserModel.username == username).first()

        if user: 
            return True
        else: return False

    def emailExists(email):
        user = db.session.query(UserModel).filter(UserModel.email == email).first()

        if user: 
            return True
        else: return False


