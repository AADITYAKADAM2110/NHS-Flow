def check_compliance(supplier, rules):
    """
    Check if the supplier complies with the given rules.
    """

    if rules["require_gdpr_compliance"] and not supplier["gdpr_compliant"]:
        return False
    if rules["allow_only_nhs_approved_suppliers"] and not supplier["nhs_approved"]:
        return False
    
    return True