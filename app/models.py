from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class TranslationTask(Base):
    __tablename__ = "translation_tasks"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    languages = Column(JSON, nullable=False)
    status = Column(String, default="in progress", nullable=False)
    translations = Column(JSON, default={})
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class TranslationResult(Base):
    __tablename__ = "translation_results"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("translation_tasks.id"), nullable=False)
    language = Column(String, nullable=False)
    translated_text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

class IndividualTranslations(Base):
    __tablename__ = "individual_translations"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("translation_tasks.id"), nullable=False)
    translated_text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

# to ensure tables are created in the database
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/translation_service")
Base.metadata.create_all(engine)