from sqlalchemy.orm import Mapped, mapped_column, validates
from app.db import db

class ThingModel(db.Model):
    uid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[bool] = mapped_column(nullable=False, default=False)
    description: Mapped[str] = mapped_column(nullable=False, default="")

    @validates("name")
    def validate_name(self, key, name):
        if not name or name == "":
            raise ValueError("Name cannot be empty")
        return name
    
    @validates("status")
    def validate_status(self, key, status):
        if (status is None) or (status not in (True, False)):
            raise ValueError("Status cannot be null")
        return status

