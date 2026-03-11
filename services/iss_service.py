def calculate_iss(revenue: float, municipio: str):

    # exemplo 
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