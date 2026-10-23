# Import every model here so Base.metadata knows all tables before create_all() runs.
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import Role, User

__all__ = ["Course", "Enrollment", "Role", "User"]
