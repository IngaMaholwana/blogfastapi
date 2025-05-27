from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.dependencies import get_db
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta

# Create a router for user-related endpoints
router = APIRouter()

# Initialize a password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define the OAuth2 scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Generate a JSON Web Token (JWT) for user authentication.

    Args:
        data (dict): The data to encode in the token (e.g., user information).
        expires_delta (timedelta, optional): The token's expiration time. Defaults to 15 minutes.

    Returns:
        str: The encoded JWT token.

    This function creates a JWT token by encoding the provided data along with an expiration time.
    The token is signed using the SECRET_KEY and ALGORITHM defined in the configuration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user (schemas.UserCreate): The user data (username, email, password).
        db (Session): The database session dependency.

    Returns:
        schemas.UserOut: The registered user's details.

    This function hashes the user's password using bcrypt, creates a new user in the database,
    and returns the user's details (excluding the password).
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user and generate an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The login form data (username and password).
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary containing the access token and token type.

    Raises:
        HTTPException: If the username or password is incorrect.

    This function verifies the user's credentials by checking the username and password
    against the database. If valid, it generates a JWT access token for the user.
    """
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}