from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey
from src.models.sqlite.settings.base import Base


class Restaurants(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"))  # Chave estrangeira
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return (
            f"Restaurants [\n"
            f"  id={self.id},\n"
            f"  name={self.name},\n"
            f"  description={self.description},\n"
            f"  created_at={self.created_at},\n"
            f"  updated_at={self.updated_at}\n"
            f"]"
        )
