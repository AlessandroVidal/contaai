def get_simples_rate(revenue: float, annex: int):

    tables = {
        1: [
            (180000, 0.06),
            (360000, 0.112),
            (720000, 0.135),
            (1800000, 0.16)
        ],

        3: [
            (180000, 0.06),
            (360000, 0.112),
            (720000, 0.135),
            (1800000, 0.16)
        ]
    }

    brackets = tables.get(annex)

    for limit, rate in brackets:
        if revenue <= limit:
            return rate

    return 0.19


def calculate_simples_tax(revenue: float, annex: int):

    rate = get_simples_rate(revenue, annex)

    tax = revenue * rate

    return {
        "simples_rate": rate,
        "simples_tax": tax
    }