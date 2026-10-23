from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Assignment(Base):
    __tablename__ = "assignments"
    __table_args__ = (
        UniqueConstraint("course_id", "title", name="uq_assignment_course_title"),
        # max_score is a divisor in percentage maths, so it must be positive.
        CheckConstraint("max_score > 0", name="ck_assignment_max_score_positive"),
        # Weights are relative (Quiz=1, Exam=3); weighted score divides by their sum.
        CheckConstraint("weight > 0", name="ck_assignment_weight_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    # RESTRICT: assignments hold data, so a course with assignments can't be deleted.
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="RESTRICT"))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default="")
    # Required, so "missing submission" (past due, nothing submitted) is always defined. Stored in UTC.
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    max_score: Mapped[float] = mapped_column(Float)
    weight: Mapped[float] = mapped_column(Float, default=1.0)
