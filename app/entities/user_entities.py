from app.config.database_config import Base
from sqlalchemy import Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped


class UserEntities(Base):
    """
    Represents the user entity in the database.
    """

    __tablename__ = "users"

    # Primary key for the user record
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Unique username for the user
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Unique email address for the user
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Hashed password for the user
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Status of the user account (active/inactive)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Timestamp when the user was created
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # Timestamp when the user was last updated
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
