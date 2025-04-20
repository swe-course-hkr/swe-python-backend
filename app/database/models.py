from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy.types import String
from sqlalchemy import DateTime
from app.database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    _password: Mapped[str] = mapped_column("password", String, nullable=False)
    isOnline: Mapped[bool] = mapped_column(default=False)
    failed_logins: Mapped[int] = mapped_column(default=0)
    can_login_after: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def __init__(self, **kwargs):
        required_fields = ["username", "email"]

        for field in required_fields:
            if field not in kwargs:
                raise ValueError(f"Missing required field: {field}")

        super().__init__(**kwargs)


    @property
    def password(self):
        return self._password


    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)


    def password_matches(self, plain_password):
        return check_password_hash(self._password, plain_password)


    @validates("username")
    def validate_username(self, key, username):
        if not username or username == "":
            raise ValueError("Username cannot be empty")
        return username

    @validates("email")
    def validate_email(self, key, email):
        if not email or email == "":
            raise ValueError("Email cannot be empty")
        return email
    
    @validates("password")
    def validate_password(self, key, password):
        if not password or password == "":
            raise ValueError("Password cannot be empty")
        return password

    def toDict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "isOnline": self.isOnline
        }


class DeviceModel(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)

    value: Mapped[float] = mapped_column(
        nullable=False,
        default=0.00
    )

    status: Mapped[bool] = mapped_column(
        nullable=False,
        default=False
    )

    description: Mapped[str] = mapped_column(
        nullable=False,
        default=""
    )

    modified_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.now
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.now
    )


    def __init__(self, **kwargs):
        required_fields = ["name", "type"]

        for field in required_fields:
            if field not in kwargs:
                raise ValueError(f"Missing required field: {field}")


        super().__init__(**kwargs)


    @validates("name")
    def validate_name(self, key, name):
        if not name or name == "":
            raise ValueError("Name cannot be empty")
        return name


    @validates("status")
    def validate_status(self, key, status):
        if status not in (True, False):
            raise ValueError("Status can only be True or False")
        return status


    @validates("type")
    def validate_type(self, key, type):
        print("validating type...", type)
        if (not type) or (type == ""):
            raise ValueError("Type cannot be empty")
        return type


    @validates("value")
    def validate_value(self, key, value):
        if (not value) or (value < 0):
            raise ValueError("Value cannot be empty or negative")
        return value


    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "value": self.value,
            "status": self.status,
            "description": self.description,
            "modified_at": self.modified_at.isoformat(),
            "created_at": self.created_at.isoformat()
        }


class LogModel(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    device_id: Mapped[int] = mapped_column(nullable=False)
    action: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.now
    )

    level: Mapped[str] = mapped_column(
        nullable=False,
        default="info"
    ) # or.. warning, error

    def toDict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "device_id": self.device_id,
            "action": self.action,
            "created_at": self.created_at.isoformat(),
            "level": self.level
        }


class RefreshTokenModel(db.Model):
    token: Mapped[str] = mapped_column(primary_key=True)
    isActive: Mapped[bool] = mapped_column(
        nullable=False,
        default=True
    )


    def __init__(self, **kwargs):
        if "token" not in kwargs:
            raise ValueError(f"Missing required field: token")

        super().__init__(**kwargs)


    def validateToken(self, key, token):
        if len(token) == 0:
            raise ValueError(f"Invalid Token")

        return token