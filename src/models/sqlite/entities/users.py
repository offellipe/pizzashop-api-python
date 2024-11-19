from sqlalchemy import Column, String, Integer, DateTime, func, CheckConstraint
from src.models.sqlite.settings.base import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        CheckConstraint("role IN ('admin', 'customer')", name="role_check"),
    )

    def __repr__(self):
        return (
            f"Users [\n"
            f"  id={self.id},\n"
            f"  name={self.name},\n"
            f"  email={self.email},\n"
            f"  role={self.role},\n"
            f"  created_at={self.created_at},\n"
            f"  updated_at={self.updated_at}\n"
            f"]"
        )
