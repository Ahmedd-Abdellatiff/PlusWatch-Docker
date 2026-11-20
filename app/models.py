from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    url = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WebsiteCheck(Base):
    __tablename__ = "website_checks"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, nullable=False, index=True)
    status_code = Column(Integer, nullable=True)
    response_time = Column(Integer, nullable=True)
    is_up = Column(Boolean, nullable=False)
    checked_at = Column(DateTime(timezone=True), server_default=func.now())