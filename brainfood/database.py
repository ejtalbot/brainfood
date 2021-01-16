from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.declarative import declared_attr, declarative_base

engine = create_engine('sqlite:///data.db', convert_unicode=True, connect_args={"check_same_thread": False}, poolclass=StaticPool)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

class CustomBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def as_dict(cls):
       return {c.name: getattr(cls, c.name) for c in cls.__table__.columns}

Base = declarative_base(cls=CustomBase)
Base.query = db_session.query_property()

class CustomBase:
	def __init():
		super().__init__

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
