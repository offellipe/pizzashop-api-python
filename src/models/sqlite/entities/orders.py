from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    CheckConstraint,
    func,
)
from src.models.sqlite.settings.base import Base


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(
        String, ForeignKey("users.id", ondelete="SET NULL"), nullable=False
    )
    restaurant_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    status = Column(String, nullable=False, default="pending")
    total_in_cents = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())

    __table_args__ = (
        CheckConstraint(
            "status IN ("
            "'pending', 'processing', 'delivering', 'delivered', 'canceled')",
            name="status_check"
        ),
    )

    def __repr__(self):
        return (
            f"Orders [\n"
            f"  id={self.id},\n"
            f"  customer_id={self.customer_id},\n"
            f"  restaurant_id={self.restaurant_id},\n"
            f"  status={self.status},\n"
            f"  total_in_cents={self.total_in_cents},\n"
            f"  created_at={self.created_at}\n"
            f"]"
        )
