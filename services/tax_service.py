def calculate_simples_tax(revenue: float):

    if revenue <= 180000:
        rate = 0.06

    elif revenue <= 360000:
        rate = 0.112

    elif revenue <= 720000:
        rate = 0.135

    elif revenue <= 1800000:
        rate = 0.16

    else:
        rate = 0.19

    tax = revenue * rate

    return {
        "revenue": revenue,
        "tax_rate": rate,
        "estimated_tax": tax
    }