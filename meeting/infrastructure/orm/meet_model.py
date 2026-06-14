from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.database import Base 


class MeetModel(Base):
    __tablename__ = "meets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    meet_hash = Column(String(64), unique=True, index=True, nullable=False)
    start_time = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    creator = relationship("UserModel")
    participants = relationship("MeetParticipantModel", back_populates="meet", cascade="all, delete-orphan")