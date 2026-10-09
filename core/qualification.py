
ELIGIBILITY_FIELDS = [
    "property_type",
    "ownership",
    "original_documents",
    "loan_amount",
    "occupation_income",
    "property_value",
    "tenure",
]

def evaluate_qualification(data):
    property_type = str(data.get("property_type", "")).lower()
    ownership = str(data.get("ownership", "")).lower()
    documents = str(data.get("original_documents", "")).lower()
    amount = data.get("loan_amount")
    occupation = str(data.get("occupation", "")).lower()
    income_mode = str(data.get("income_mode", "")).lower()
    tenure = data.get("tenure")

    if property_type and any(
        word in property_type for word in ["agricultural", "agriculture"]
    ):
        return "DISQUALIFIED: Agricultural property"

    if ownership and not any(
        word in ownership for word in ["self", "joint", "own", "co-owner"]
    ):
        return "REVIEW: Clarify property ownership"

    if documents and any(
        word in documents for word in ["no", "unavailable", "photocopy", "not available"]
    ):
        return "DISQUALIFIED: Original documents unavailable"

    if income_mode and any(
        word in income_mode for word in ["cash", "cash only"]
    ):
        return "DISQUALIFIED: Cash income"

    if amount is not None and float(amount) > 7500000:
        return "CLARIFY: Offer maximum is ₹75,00,000"

    if tenure is not None and not 3 <= int(tenure) <= 15:
        return "DISQUALIFIED: Tenure must be 3–15 years"

    if occupation and not any(
        word in occupation for word in ["salaried", "self-employed", "self employed"]
    ):
        return "REVIEW: Clarify occupation"

    if len(str(data.get("property_value", "")).strip()) == 0:
        return "INCOMPLETE: Property market value required"

    if all(data.get(field) not in (None, "") for field in ELIGIBILITY_FIELDS):
        return "PRELIMINARILY QUALIFIED: Human expert review required"

    return "INCOMPLETE: Collect remaining eligibility details"