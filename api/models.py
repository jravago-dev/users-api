from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    first_name = Column(String(50), default="First Name")
    last_name = Column(String(50),  default="Last Name")
    gender = Column(String(10),  default="N/A")
    nick_name = Column(String(50),  default="Default")
    birth_date = Column(DateTime)
    date_created = Column(DateTime)

    account = relationship("Accounts", back_populates="user")


class Accounts(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    email_address = Column(String(50))
    user_name = (Column(String(50)))
    hashed_password = Column(String(255))
    is_activated = Column(Boolean)
    is_locked = Column(Boolean)

    user = relationship("Users", back_populates="account")
