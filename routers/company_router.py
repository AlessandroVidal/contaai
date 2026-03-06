from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import re

from db import SessionLocal
from models.company import Company
from models.user import User

from schemas.company import CompanyCreate, CompanyResponse

from services.auth_service import get_current_user, check_user_plan
from services.cnpj_service import get_cnpj_data


router = APIRouter(prefix="/companies", tags=["Companies"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CONSULTAR CNPJ

@router.get("/cnpj/{cnpj}")
def consult_cnpj(
    cnpj: str,
    current_user: User = Depends(get_current_user)
):

    cnpj = re.sub(r"\D", "", cnpj)

    if len(cnpj) != 14:
        raise HTTPException(status_code=400, detail="CNPJ inválido")

    return get_cnpj_data(cnpj)


# CREATE COMPANY AUTOMÁTICO

@router.post("/", response_model=CompanyResponse)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    cnpj = re.sub(r"\D", "", company.cnpj)

    if len(cnpj) != 14:
        raise HTTPException(status_code=400, detail="CNPJ inválido")

    # evita duplicação
    existing_company = db.query(Company).filter(
        Company.cnpj == cnpj,
        Company.user_id == current_user.id
    ).first()

    if existing_company:
        raise HTTPException(
            status_code=400,
            detail="Empresa com este CNPJ já cadastrada"
        )

    # verifica plano
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

    # CONSULTA API CNPJ
    cnpj_data = get_cnpj_data(cnpj)

    name = cnpj_data["razao_social"]

    new_company = Company(
        name=name,
        cnpj=cnpj,
        user_id=current_user.id
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company


# LISTAR EMPRESAS

@router.get("/", response_model=list[CompanyResponse])
def list_companies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return db.query(Company).filter(
        Company.user_id == current_user.id
    ).all()


# BUSCAR EMPRESA

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
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return company


# DELETAR EMPRESA

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
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    db.delete(company)
    db.commit()

    return {"message": "Empresa deletada com sucesso"}