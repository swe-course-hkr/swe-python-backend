from app.database.models import UserModel
from app.database import db
from datetime import timedelta, datetime

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


    def get_user_by_username(username: str):
        return db.session.query(UserModel) \
            .filter(UserModel.username == username) \
            .first()


    def get_user_by_id(userID):
        try:
            user = db.session\
            .query(UserModel)\
            .filter(UserModel.id == userID)\
            .first()
            return user
        except ValueError as e:
            print(e)


    # for debugging purposes
    def fetch():
        users = db.session.query(UserModel).all()
        return users
    
    
    def increaseFailedLoginAttemps(user):
        user.failed_logins += 1

    
    def setTimeout(user):
        user.can_login_after = datetime.now() + timedelta(minutes=3)
        user.failed_logins = 0
    

    def resetTimeout(user):
        user.can_login_after = None
        user.failed_logins = 0
        db.session.commit()
