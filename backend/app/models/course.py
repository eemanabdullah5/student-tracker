from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Course(Base):
    __tablename__ = "courses"
    # A teacher can't create two courses with the same title (e.g. a double-clicked "Create").
    __table_args__ = (UniqueConstraint("teacher_id", "title", name="uq_course_teacher_title"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    # RESTRICT: a teacher who still owns courses can't be deleted, so grades are never wiped by accident.
    # The FK can't check the user is a *teacher*; the service layer enforces that.
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
