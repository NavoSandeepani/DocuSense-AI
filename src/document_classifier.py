def classify_document(text):

    text = text.lower()

    # CV / Resume
    if (
        "education" in text
        or "experience" in text
        or "skills" in text
        or "projects" in text
        or "curriculum vitae" in text
        or "resume" in text
    ):
        return "CV / Resume"

    # Research Paper
    elif (
        "abstract" in text
        or "introduction" in text
        or "methodology" in text
        or "results" in text
        or "conclusion" in text
        or "references" in text
    ):
        return "Research Paper"

    # ID Card
    elif (
        "identity" in text
        or "nic" in text
        or "national identity card" in text
        or "හැඳුනුම්පත" in text
    ):
        return "ID Card"

    # Certificate
    elif (
        "certificate" in text
        or "certified" in text
        or "awarded" in text
        or "completion" in text
    ):
        return "Certificate"

    # Invoice
    elif (
        "invoice" in text
        or "amount" in text
        or "total" in text
        or "payment" in text
        or "bill" in text
    ):
        return "Invoice"

    # Form
    elif (
        "application" in text
        or "form" in text
        or "applicant" in text
    ):
        return "Form"

    else:
        return "Unknown"