import re
import unidecode

def slugify(text, replacement='_'):
    text = unidecode.unidecode(text).lower()
    return re.sub(r'\W+', replacement, text)
