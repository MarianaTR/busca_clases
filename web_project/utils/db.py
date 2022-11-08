from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


conection_db = 'postgresql://flyjgczkrvrjbx:2e2a76a0b2b618fbccc4116c1095b61fc2957eb5bc8a815293002f2a858ffb1d@ec2-3-93-206-109.compute-1.amazonaws.com:5432/d1dcghgqeegb86'
base = declarative_base()

engine = create_engine(conection_db)

Session = sessionmaker(bind=engine)