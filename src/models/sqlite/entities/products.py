from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime,
    func,
    Text,
)
from src.models.sqlite.settings.base import Base


class Products(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price_in_cents = Column(Integer, nullable=False)
    restaurant_id = Column(
        String, ForeignKey("restaurants.id"), nullable=False
    )
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return (
            f"Products [\n"
            f"  id={self.id},\n"
            f"  name={self.name},\n"
            f"  description={self.description},\n"
            f"  price_in_cents={self.price_in_cents},\n"
            f"  restaurant_id={self.restaurant_id},\n"
            f"  created_at={self.created_at},\n"
            f"  updated_at={self.updated_at}\n"
            f"]"
        )
