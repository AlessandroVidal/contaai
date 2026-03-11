from sqlalchemy.orm import Session
from models.company import Company
from models.revenue import Revenue


def calculate_simples_nacional(revenue: float):

    # Faixas simplificadas (exemplo inicial)
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
        "revenue": revenue,
        "tax_rate": rate,
        "estimated_tax": tax
    }


def calculate_company_tax(db: Session, company_id: int):

    revenue = db.query(Revenue).filter(
        Revenue.company_id == company_id
    ).order_by(
        Revenue.month.desc()
    ).first()

    if not revenue:
        return {
            "message": "Nenhum faturamento registrado"
        }

    return calculate_simples_nacional(revenue.revenue)