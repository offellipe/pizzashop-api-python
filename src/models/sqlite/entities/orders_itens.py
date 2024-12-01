from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
)
from src.models.sqlite.settings.base import Base


class OrderItems(Base):
    __tablename__ = "order_items"

    id = Column(String, primary_key=True)
    order_id = Column(
        String,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id = Column(
        String,
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True,
    )
    quantity = Column(Integer, nullable=False, default=1)
    price_in_cents = Column(Integer, nullable=False)

    def __repr__(self):
        return (
            f"OrderItems [\n"
            f"  id={self.id},\n"
            f"  order_id={self.order_id},\n"
            f"  product_id={self.product_id},\n"
            f"  quantity={self.quantity},\n"
            f"  price_in_cents={self.price_in_cents}\n"
            f"]"
        )
