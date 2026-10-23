# Import every model here so Base.metadata knows all tables before create_all() runs.
from app.models.user import Role, User

__all__ = ["Role", "User"]
