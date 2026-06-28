import re

def extract_information(text):

    info = {}

    # Dates
    dates = re.findall(r"\d{4}/\d{2}/\d{2}", text)

    if dates:
        info["Dates"] = dates

    # Numbers
    numbers = re.findall(r"\d{6,}", text)

    if numbers:
        info["Numbers"] = numbers

    # Emails
    emails = re.findall(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        text
    )

    if emails:
        info["Emails"] = emails

    # Phone numbers
    phones = re.findall(
        r"(?:\+94|0)?7\d{8}",
        text
    )

    if phones:
        info["Phone Numbers"] = phones

    return info