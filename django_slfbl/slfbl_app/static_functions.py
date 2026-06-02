import string

from unidecode import unidecode

# These functions CANNOT import anything from the models or db_functions files, as they are used in those files.
# Any functions that need to be used in those files should be added here.

def normalizeName(objectName):
    name = objectName.lower()
    name = unidecode(name)  # Remove accents and special characters
    translator = str.maketrans('', '', string.punctuation)
    name = name.translate(translator)  # Remove punctuation
    name = ' '.join(name.split())  # Remove extra whitespace
    return name