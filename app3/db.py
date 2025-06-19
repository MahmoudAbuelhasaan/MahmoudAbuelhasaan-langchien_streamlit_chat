# db design & oparitions
from sqlalchemy import create_engine,Column,Integer,String,Text,DateTime,ForeignKey
from sqlalchemy.orm import sessionmaker,declarative_base,relationship
from datetime import datetime

Base = declarative_base()

# DB Design 
class Conversation(Base):
    __tablename__ = "conversation"
    id =  Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # relations 
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    role = Column(String(50), nullable=False)  # 'user', 'ai'
    # relations 
    conversation_id = Column(Integer, ForeignKey('conversation.id'))
    conversation = relationship("Conversation", back_populates="messages")

# create db 
engine = create_engine("sqlite:///chat_history.db")
SessionLocal = sessionmaker(bind=engine)
# create all tebles
Base.metadata.create_all(engine)

# DB Oparations

def get_session():
    # return new session 
    return SessionLocal()

def create_conversation(session,title):
    "create new conversation"
    conv = Conversation(title=title)
    session.add(conv)
    session.commit()
    return conv

def add_message(session,conversation_id,content,role):
    "add new message to existing conversation"
    msg = Message(content=content,role=role,conversation_id=conversation_id,)
    session.add(msg)
    session.commit()
    return msg

def get_conversations(session):
    "get all conersations"
    return session.query(Conversation).order_by(Conversation.created_at.desc()).all()

def get_messages(session,conversation_id):
    return session.query(Message).filter_by(conversation_id=conversation_id).order_by(Message.created_at.desc()).all()











