from sqlalchemy import select
from app.database.models import LogModel, DeviceModel, RefreshTokenModel
from datetime import datetime
from app.database import db

class Database:
    def fetch_logs(
        log_level: str = "info",
        user_id: int = None,
        device_id: int = None
    ) -> list[LogModel]:
        # TODO: implement a parameter to accept ..
        # .. date ranges (before, after, from-to)
        stmt = select(LogModel) \
            .where(LogModel.level == log_level)
        
        if (user_id):
            stmt = stmt.where(LogModel.user_id == user_id)
        
        if (device_id):
            stmt = stmt.where(LogModel.device_id == device_id)

        stmt = stmt.order_by(LogModel.created_at.desc())
        result = db.session.execute(stmt).scalars().all()
        return result


    def write_log(log_level: str, action: str, user_id: int, device_id: int):
        db.session.add(LogModel(
            level=log_level,
            action=action,
            user_id=user_id,
            device_id=device_id
        ))
        db.session.commit()


    def update_device(device_id: int, **kwargs) -> int:
        kwargs["modified_at"] = datetime.now()

        db.session.query(DeviceModel) \
            .filter(DeviceModel.id == device_id) \
            .update(kwargs)

        db.session.commit()
        return db.session.query(DeviceModel).filter(DeviceModel.id == device_id).first()


    def add_device(**kwargs) -> DeviceModel:
        try:
            new_device = DeviceModel(**kwargs)
            db.session.add(new_device)
            db.session.commit()
        except ValueError as e:
            raise e

        return new_device


    def remove_device(device_id: int) -> int:
        count = db.session.query(DeviceModel) \
            .filter(DeviceModel.id == device_id) \
            .delete()

        db.session.commit()
        return count


    def fetch_all_devices():
        devices = db.session.query(DeviceModel).all()
        return devices


    def create_refresh_token(token):
        try:
            newToken = RefreshTokenModel(token=token)
            db.session.add(newToken)
            db.session.commit()
        except ValueError as e:
            raise e

        return newToken


    def refresh_token_is_active(token):
        t = db.session.query(RefreshTokenModel)\
            .filter(RefreshTokenModel.token == token)\
            .first()

        return (t is not None) and t.isActive


    def update_refresh_token(token, **kwargs):
        db.session.query(RefreshTokenModel)\
            .filter(RefreshTokenModel.token == token)\
            .update(kwargs)
