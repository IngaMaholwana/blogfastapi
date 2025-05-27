from sqlalchemy.orm import Session
from app.database import SessionLocal

def get_db():
    """
    Dependency for providing a database session.

    This function creates a new database session using the `SessionLocal` factory.
    It ensures that the session is properly closed after use, even if an exception occurs.

    Yields:
        Session: A SQLAlchemy database session.

    How it works:
    - A new session is created by calling `SessionLocal()`.
    - The `yield` statement provides the session to the calling function.
    - After the calling function completes, the `finally` block ensures that the session is closed,
      releasing any resources associated with it.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()