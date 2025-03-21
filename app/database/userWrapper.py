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


    # TODO: Create method done By AC