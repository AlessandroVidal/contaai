from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from schemas.user import UserCreate, UserResponse
from services.auth_service import (
    create_user,
    get_user_by_email,
    verify_password,
    create_access_token
)

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    return create_user(db, user.name, user.email, user.password)



@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):

    db_user = get_user_by_email(db, user.email)

    if not db_user:
        raise HTTPException(status_code=400, detail="Email ou senha inválidos")

    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Email ou senha inválidos")

    access_token = create_access_token(data={"sub": db_user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

    @router.post("/upgrade")
def upgrade_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    current_user.plan = "PRO"
    db.commit()
    return {"message": "Plano atualizado para PRO"}