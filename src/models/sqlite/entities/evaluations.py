from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime,
    Text,
    func,
)
from sqlalchemy.orm import relationship
from src.models.sqlite.settings.base import Base


class Evaluations(Base):
    __tablename__ = "evaluations"

    id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(String, ForeignKey("restaurants.id"), nullable=False) # noqa
    rate = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Definindo os relacionamentos
    customer = relationship("Users", back_populates="evaluations", foreign_keys=[customer_id]) # noqa
    restaurant = relationship("Restaurants", back_populates="evaluations", foreign_keys=[restaurant_id]) # noqa

    def __repr__(self):
        return (
            f"Evaluations [\n"
            f"  id={self.id},\n"
            f"  customer_id={self.customer_id},\n"
            f"  restaurant_id={self.restaurant_id},\n"
            f"  rate={self.rate},\n"
            f"  comment={self.comment},\n"
            f"  created_at={self.created_at}\n"
            f"]"
        )
