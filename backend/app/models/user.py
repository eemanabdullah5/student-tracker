import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Role(enum.StrEnum):
    STUDENT = "student"
    TEACHER = "teacher"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Stored lowercase (normalised in the service layer); UNIQUE blocks duplicate accounts.
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(100))
    role: Mapped[Role] = mapped_column(
        # Store the lowercase values ("student"), and add a CHECK so SQLite rejects anything else.
        Enum(Role, name="user_role", values_callable=lambda roles: [r.value for r in roles],
             create_constraint=True, validate_strings=True),
        default=Role.STUDENT,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
