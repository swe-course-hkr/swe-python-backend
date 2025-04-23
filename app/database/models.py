from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy.types import String
from sqlalchemy import DateTime
from app.database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(db.Model):
    """
    models for the user table in database.

    attributes:
    - id (int): primary key.
    - username (str): unique username for the user.
    - email (str): unique email for the user.
    - _password (str): hashed password for the user.
    - isOnline (bool): online status of the user.
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    _password: Mapped[str] = mapped_column("password", String, nullable=False)
    isOnline: Mapped[bool] = mapped_column(default=False)
    failed_logins: Mapped[int] = mapped_column(default=0)
    can_login_after: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def __init__(self, **kwargs):
        """
        creates UserModel instance.

        raises:
        - ValueError: if the required fields (username and email) are not given.
        """
        required_fields = ["username", "email"]

        for field in required_fields:
            if field not in kwargs:
                raise ValueError(f"Missing required field: {field}")

        super().__init__(**kwargs)


    @property
    def password(self): 
        """
        gets the hashed password of user.
        """
        return self._password


    @password.setter
    def password(self, password):
        """
        sets and hashes the password before storing it.

        args:
        - password (str): plaintext password.
        """
        self._password = generate_password_hash(password)


    def password_matches(self, plain_password):
        """
        checks if plaintext password matches the stored hashed password.

        args:
        - plain_password (str): password to check.

        rturns:
        True if passwords match, False otherwise.
        """
        return check_password_hash(self._password, plain_password)


    @validates("username")
    def validate_username(self, key, username):
        """
        validates the username is not empty.
        """
        if not username or username == "":
            raise ValueError("Username cannot be empty")
        return username

    @validates("email")
    def validate_email(self, key, email):
        """
        validates the email is not empty.
        """
        if not email or email == "":
            raise ValueError("Email cannot be empty")
        return email
    
    def toDict(self):
        """
        converts the user instance to a dictionary.

        returns:
        dictionary representation of the user.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "isOnline": self.isOnline
        }


class DeviceModel(db.Model):
    """
    model of device (sensor) in the system.

    atributes:
    - id (int): primary key.
    - name (str): name of the device.
    - type (str): type of the device.
    - value (float): value associated with the device.
    - status (bool): current state of the device (on/off).
    - description (str): description for the device.
    - modified_at (datetime): öast modified timestamp.
    - created_at (datetime): created timestamp.
    """
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
        """
        creates a DeviceModel instance.

        raises:
        - ValueError: if required fields are missing (name and type).
        """
        required_fields = ["name", "type"]

        for field in required_fields:
            if field not in kwargs:
                raise ValueError(f"Missing required field: {field}")


        super().__init__(**kwargs)


    @validates("name")
    def validate_name(self, key, name):
        """
        validates the name is not empty.
        """
        if not name or name == "":
            raise ValueError("Name cannot be empty")
        return name


    @validates("status")
    def validate_status(self, key, status):
        """
        validates status is a boolean.
        """
        if status not in (True, False):
            raise ValueError("Status can only be True or False")
        return status


    @validates("type")
    def validate_type(self, key, type):
        """
        validates type is not empty.
        """
        print("validating type...", type)
        if (not type) or (type == ""):
            raise ValueError("Type cannot be empty")
        return type


    @validates("value")
    def validate_value(self, key, value):
        """
        validates the value is non-negative.

        rturns:
        the validated value.
        """
        if (not value) or (value < 0):
            raise ValueError("Value cannot be empty or negative")
        return value


    def toDict(self):
        """
        converts the device instance to a dictionary.

        returns:
        dictionary representation of the device.
        """
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
    """
    model of log entry for user actions on devices.

    attributes:
    - id (int): primary key.
    - user_id (int): ID of user who performed the action.
    - device_id (int): ID of the device on which action was taken.
    - action (str): description of the action.
    - created_at (datetime): timestamp of the action.
    - level (str): level of access?
    """
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
        """
        converts the log entry to a dictionary.

        returns:
        dictionary representation of the log.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "device_id": self.device_id,
            "action": self.action,
            "created_at": self.created_at.isoformat(),
            "level": self.level
        }


class RefreshTokenModel(db.Model):
    """
    refresh token model entry for a user session.

    attributes:
    - token (str): primary key.
    - isActive (bool): if the token is still active.
    """
    token: Mapped[str] = mapped_column(primary_key=True)
    isActive: Mapped[bool] = mapped_column(
        nullable=False,
        default=True
    )
    username: Mapped[str] = mapped_column(nullable=False)


    def __init__(self, **kwargs):
        """
        creates a RefreshTokenModel instance.

        raises:
        - ValueError: if token is missing.
        """
        if "token" not in kwargs:
            raise ValueError(f"Missing required field: token")

        super().__init__(**kwargs)


    def validateToken(self, key, token):
        """
        validates that the token string is not empty.

        returns:
        the validated token.
        """
        if len(token) == 0:
            raise ValueError(f"Invalid Token")

        return token