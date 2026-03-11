def estimate_inss(revenue: float):

    payroll_estimate = revenue * 0.28

    inss = payroll_estimate * 0.20

    return {
        "estimated_payroll": payroll_estimate,
        "inss_estimate": inss
    }