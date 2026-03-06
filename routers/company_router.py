from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import SessionLocal
from models.company import Company
from models.user import User

from schemas.company import CompanyCreate, CompanyResponse

from services.auth_service import get_current_user, check_user_plan


router = APIRouter(prefix="/companies", tags=["Companies"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE COMPANY

@router.post("/", response_model=CompanyResponse)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # verifica se já existe empresa com mesmo CNPJ para o usuário
    existing_company = db.query(Company).filter(
        Company.cnpj == company.cnpj,
        Company.user_id == current_user.id
    ).first()

    if existing_company:
        raise HTTPException(
            status_code=400,
            detail="Empresa com este CNPJ já existe"
        )

    # verifica plano do usuário
    plan = check_user_plan(current_user)

    if plan == "FREE":
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


# LIST COMPANIES

@router.get("/", response_model=list[CompanyResponse])
def list_companies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Company).filter(
        Company.user_id == current_user.id
    ).all()


# GET COMPANY

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
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    return company


# DELETE COMPANY

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
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    db.delete(company)
    db.commit()

    return {"message": "Empresa deletada com sucesso"}