from sqlalchemy.orm import Mapped, mapped_column, validates
from app.database import db
from datetime import datetime

class UserModel(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str]
    status: Mapped[bool] = mapped_column(default=False)

    def __init__(self, **kwargs):
        required_fields = ["username", "email"]

        for field in required_fields:
            if field not in kwargs:
                raise ValueError(f"Missing required field: {field}")

        super().__init__(**kwargs)

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
            "status": self.status
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
