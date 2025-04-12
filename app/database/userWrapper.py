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