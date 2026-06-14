from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.database import Base 



class MeetParticipantModel(Base):
    __tablename__ = "meet_participants"

    meet_id = Column(Integer, ForeignKey("meets.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    joined_at = Column(DateTime, default=datetime.utcnow)

    meet = relationship("MeetModel", back_populates="participants")
    user = relationship("UserModel") 