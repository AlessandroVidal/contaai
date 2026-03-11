from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import SessionLocal
from models.revenue import Revenue
from models.company import Company
from models.user import User

from schemas.revenue import RevenueCreate, RevenueResponse

from services.auth_service import get_current_user


router = APIRouter(prefix="/revenue", tags=["Revenue"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{company_id}", response_model=RevenueResponse)
def create_revenue(
    company_id: int,
    data: RevenueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()

    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    revenue = Revenue(
        company_id=company_id,
        month=data.month,
        revenue=data.revenue
    )

    db.add(revenue)
    db.commit()
    db.refresh(revenue)

    return revenue