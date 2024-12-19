

# db_config.py
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }

# Configuración de la base de datos
# DATABASE_URL = "mysql+pymysql://user:password@localhost/task_manager"
DATABASE_URL = "mysql+pymysql://ufcfvt5yzwcsfapk:9Jabq94WP5OyIoqQUqPv@bc8oaw9bbknn6wpqdvse-mysql.services.clever-cloud.com:3306/bc8oaw9bbknn6wpqdvse"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas
Base.metadata.create_all(bind=engine)



