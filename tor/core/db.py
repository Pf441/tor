from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db', echo=True)

from tor.core.models import Base

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
