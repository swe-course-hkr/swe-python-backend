'''
UserDatabase utility class for handling user-related database operations.

Methods:
- update_user_details(user_id, **kwargs) -> Updates fields of a user by their ID. Accepts keyword arguments for fields to update. Returns the updated user object.

- create_user(**kwargs) -> Creates and stores a new user in the database using provided fields. Raises ValueError if the input is invalid. Returns the newly created user object.

- get_user_by_username(username: str) -> Retrieves a user object from the database by matching the username. Returns None if not found.

- get_user_by_id(userID) -> Retrieves a user object using their ID. Returns None if not found. Prints exception if a ValueError occurs.

- fetch() -> Returns a list of all users in the database (Primarily used for debugging)
'''

from app.database.models import UserModel
from app.database import db
from datetime import timedelta, datetime
from sqlalchemy.exc import IntegrityError

class UserDatabase:

    def update_user_details(user_id, **kwargs):
        user = UserDatabase.get_user_by_id(user_id)

        if user is None:
            return None, f"User with ID: {user_id} not found"

        if "email" in kwargs:
            existingUser = UserDatabase.get_user_by_email(kwargs["email"])
            if existingUser:
                return None, f"Email '{kwargs['email']}' is already taken"

            user.email = kwargs["email"]

        if "username" in kwargs:
            existingUser = UserDatabase.get_user_by_username(kwargs["username"])
            if existingUser:
                return None, f"Username '{kwargs['username']}' is already taken"

            user.username = kwargs["username"]

        if "password" in kwargs:
            user._password = kwargs["password"]

        db.session.commit()

        return user, None


    def create_user(**kwargs):
        try:
            new_user = UserModel(**kwargs)
            db.session.add(new_user)
            db.session.commit()
        except ValueError as e:
            return None, str(e)
        except IntegrityError as e:
            errorMsg = e.args[0]

            if "email" in errorMsg:
                return None, "Email is already taken."

            if "username" in errorMsg:
                return None, "Username is already taken."

            return None, str(e.args[0])
        
        return new_user, None


    def get_user_by_username(username: str):
        return db.session.query(UserModel) \
            .filter(UserModel.username == username) \
            .first()
    

    def get_user_by_email(email: str):
        return db.session.query(UserModel) \
            .filter(UserModel.email == email) \
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


    def increaseFailedLoginAttemps(user):
        user.failed_logins += 1
        db.session.commit()


    def setTimeout(user):
        user.can_login_after = datetime.now() + timedelta(minutes=3)
        user.failed_logins = 0
        db.session.commit()
    

    def resetTimeout(user):
        user.can_login_after = None
        user.failed_logins = 0
        db.session.commit()
