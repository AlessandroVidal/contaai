from sqlalchemy.orm import Session
from models.company import Company
from models.revenue import Revenue


# -----------------------------


def calculate_simples_nacional(revenue: float):

    if revenue <= 180000:
        rate = 0.06

    elif revenue <= 360000:
        rate = 0.112

    elif revenue <= 720000:
        rate = 0.135

    else:
        rate = 0.16

    tax = revenue * rate

    return {
        "simples_rate": rate,
        "simples_tax": tax
    }


# -----------------------------
# ISS MUNICIPAL


def calculate_iss(revenue: float, municipio: str):

    iss_rates = {
        "RIO DE JANEIRO": 0.05,
        "SAO PAULO": 0.05
    }

    rate = iss_rates.get(municipio.upper(), 0.02)

    tax = revenue * rate

    return {
        "iss_rate": rate,
        "iss_tax": tax
    }


# -----------------------------
# INSS ESTIMADO


def estimate_inss(revenue: float):

    payroll_estimate = revenue * 0.28

    inss = payroll_estimate * 0.20

    return {
        "estimated_payroll": payroll_estimate,
        "inss_estimate": inss
    }




def calculate_company_tax(db: Session, company_id: int):

    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    if not company:
        return {"message": "Empresa não encontrada"}

    revenue = db.query(Revenue).filter(
        Revenue.company_id == company_id
    ).order_by(
        Revenue.month.desc()
    ).first()

    if not revenue:
        return {"message": "Nenhum faturamento registrado"}

    revenue_value = revenue.revenue

    simples = calculate_simples_nacional(revenue_value)

    iss = calculate_iss(revenue_value, company.municipio)

    inss = estimate_inss(revenue_value)

    total = (
        simples["simples_tax"]
        + iss["iss_tax"]
        + inss["inss_estimate"]
    )

    return {
        "revenue": revenue_value,

        "simples": simples,

        "iss": iss,

        "inss": inss,

        "total_tax_estimate": total
    }