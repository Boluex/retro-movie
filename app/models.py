from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cartoon(Base):
    __tablename__ = "cartoons"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False, index=True)
    year = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    poster_url = Column(String, nullable=False)
    hero_image_url = Column(String, nullable=True)
    video_url = Column(String, nullable=True) # Added for actual video playback

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Cartoon(id={self.id}, title='{self.title}')>"


class MovieRequest(Base):
    __tablename__ = "movie_requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    movie_name = Column(String, nullable=False)
    user_email = Column(String, nullable=False) # Changed from 'email' for clarity
    status = Column(String, default="pending", nullable=False) # e.g., pending, approved, rejected

    requested_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<MovieRequest(id={self.id}, movie_name='{self.movie_name}', status='{self.status}')>"