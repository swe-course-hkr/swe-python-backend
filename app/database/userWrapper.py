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
