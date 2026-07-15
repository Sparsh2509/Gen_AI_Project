# entities.py
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str) -> dict:
    if not text.strip():
        return {"Person": [], "Organization": [], "Location": [], "Date": []}

    doc = nlp(text[:5000])
    entities = {
        "Person": set(),
        "Organization": set(),
        "Location": set(),
        "Date": set()
    }

    for ent in doc.ents:
        name = ent.text.strip()
        if not name:
            continue

        if ent.label_ == "PERSON":
            entities["Person"].add(name)
        elif ent.label_ == "ORG":
            entities["Organization"].add(name)
        elif ent.label_ in ("GPE", "LOC"):
            entities["Location"].add(name)
        elif ent.label_ == "DATE":
            entities["Date"].add(name)

    return {k: sorted(list(v)) for k, v in entities.items()}
