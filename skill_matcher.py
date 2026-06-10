import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_skills(text, skills_list):
    doc = nlp(text.lower())
    skill_set = set()
    for token in doc:
        if token.text in skills_list:
            skill_set.add(token.text)
    return list(skill_set)
