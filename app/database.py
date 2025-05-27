from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Define the database URL for the SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
"""
This is the connection URL for the SQLite database.
- `sqlite:///./blog.db`: Specifies that the database is a SQLite database and the file `blog.db` is located in the current directory.
"""

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
"""
The `engine` is the core interface to the database.
- `create_engine`: Creates a connection to the database using the specified URL.
- `connect_args={"check_same_thread": False}`: This argument is specific to SQLite and allows multiple threads to use the same database connection.
"""

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
The `SessionLocal` is a factory for creating database sessions.
- `autocommit=False`: Disables automatic commits; transactions must be explicitly committed.
- `autoflush=False`: Disables automatic flushing of changes to the database; changes are flushed only when explicitly committed.
- `bind=engine`: Binds the session to the database engine, so all sessions created by this factory will use the same database connection.
"""

# Create a base class for the ORM models
Base = declarative_base()
"""
The `Base` class is the declarative base for all ORM models.
- Models will inherit from this class to define database tables.
- This base class provides metadata and functionality for mapping Python classes to database tables.
"""