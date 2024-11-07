from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException, Request

from .config import settings

class DatabaseManager:
    def __init__(self):
        self.client = None
        self.database = None

    def init_database(self, db_name: Optional[str] = None):
        if db_name:
            db_engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI(db_name)))
        else:
            db_engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI()))

        db: Session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)()

        try:
            yield db 
        finally:
            db.close()
            
            
def get_master_db():
    db_manager = DatabaseManager()
    return next(db_manager.init_database())


def get_tenant_db(request: Request):
    db_manager = DatabaseManager()
    return next(db_manager.init_database(request.state.db))

def create_tenant_db(db_name: str)-> Session:
    db_manager = DatabaseManager()
    return next(db_manager.init_database(db_name))
