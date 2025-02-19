from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class TranslationTask(Base):
    __tablename__ = "translation_tasks"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    languages = Column(JSON, nullable=False)
    status = Column(String, default="in progress", nullable=False)
    translation = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(datetime.timezone.utc), onupdate=datetime.now(datetime.timezone.utc))

class TranslationResult(Base):
    __tablename__ = "translation_results"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("translation_requests.id"), nullable=False)
    language = Column(String, nullable=False)
    translated_text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class IndividualTranslations(Base):
    __tablename__ = "individual_translations"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("translation_requests.id"), nullable=False)
    translated_text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# to ensure tables are created in the database
engine = create_engine("postgresql+psycopg2://postgres:0000@localhost:5432/alphaloops_translator")
Base.metadata.create_all(engine)