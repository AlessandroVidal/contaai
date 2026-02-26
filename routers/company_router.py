from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from models.company import Company
from schemas.company import CompanyCreate, CompanyResponse


router = APIRouter(prefix="/companies", tags=["Companies"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from services.auth_service import get_current_user
from services.auth_service import check_user_plan
from models.user import User

@router.post("/", response_model=CompanyResponse)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    if current_user.plan == "FREE":
        total_companies = db.query(Company).filter(
            Company.user_id == current_user.id
        ).count()

        if total_companies >= 1:
            raise HTTPException(
                status_code=403,
                detail="Plano FREE permite apenas 1 empresa. Faça upgrade para PRO."
            )

    new_company = Company(
        name=company.name,
        cnpj=company.cnpj,
        user_id=current_user.id
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company


@router.get("/", response_model=list[CompanyResponse])
def list_companies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Company).filter(
        Company.user_id == current_user.id
    ).all()


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()

    if not company:
        return {"error": "Empresa não encontrada"}

    return company

@router.delete("/{company_id}")
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()

    if not company:
        return {"error": "Empresa não encontrada"}

    db.delete(company)
    db.commit()

    return {"message": "Empresa deletada com sucesso"}