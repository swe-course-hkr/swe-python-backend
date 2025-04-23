'''
Database utility class for managing logs, devices, and refresh tokens in the system.

Methods:

fetch_logs(log_level: str = "info", user_id: int = None, device_id: int = None) -> list[LogModel]:
Fetches logs filtered by log level, user ID, and device ID. Returns logs in descending order of creation time.

write_log(log_level: str, action: str, user_id: int, device_id: int):
Creates a new log entry with the given log level, action description, user ID, and device ID.
AC<3

update_device(device_id: int, **kwargs) -> DeviceModel:
Updates fields of an existing device and refreshes its 'modified_at' timestamp. Returns the updated device object.

add_device(**kwargs) -> DeviceModel:
Creates a new device using the provided keyword arguments. Returns the newly created device.

remove_device(device_id: int) -> int:
Deletes a device by its ID. Returns the number of rows affected (0 if device not found).

fetch_all_devices() -> list[DeviceModel]:
Retrieves and returns a list of all devices in the database.

create_refresh_token(token: str) -> RefreshTokenModel:
Creates and stores a new refresh token entry in the database. Returns the created token object.

refresh_token_is_active(token: str) -> bool:
Checks if a given refresh token exists and is marked as active.
AC<3

update_refresh_token(token: str, **kwargs):
Updates the refresh token record identified by the token string with provided fields.
'''

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


    def create_refresh_token(token, username):
        try:
            newToken = RefreshTokenModel(token=token, username=username)
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
        
    def get_token(token):
        t = db.session.query(RefreshTokenModel) \
            .filter(RefreshTokenModel.token == token)\
            .first()
        return t
