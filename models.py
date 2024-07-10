from sqlalchemy import Column, Integer, String, Text, BigInteger

from database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(BigInteger)
    sender_name = Column(String)
    receiver_id = Column(BigInteger)
    receiver_name = Column(String)
    content = Column(Text)
    voice_file_path = Column(String, nullable=True)
