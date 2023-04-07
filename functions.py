import pikepdf
import pymongo
import random
import string

# Generate Key Function
def generate_key(length):
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    numbers = string.digits
    special_characters = string.punctuation
    all_characters = uppercase_letters + lowercase_letters + numbers + special_characters
    password = ''.join(random.choice(all_characters) for i in range(length))
    return password

# Writing key generated to the metadata of PDF
def writingKey(filePath, nameOfFile, key):
    pdf = pikepdf.Pdf.open(filePath, allow_overwriting_input=True)
    pdf.docinfo['/chaavi'] = key
    pdf.save(nameOfFile + '.pdf')

# Inserting Object into database
def insertKeyDB(key, prn, collection):
    object = {"chaavi": key, "PRN": prn}
    collection.insert_one(object)

# Retrieving chaavi (key) from the metadata of PDF
def retrievingKey(filePath):
    pdf = pikepdf.Pdf.open(filePath, allow_overwriting_input=True)
    pdfMetadeta = pdf.docinfo
    pdfChaavi = pdfMetadeta['/chaavi']
    return pdfChaavi

# Retrieving chaavi from database
def retrievingKeyDB(PRN, collection):
    result = collection.find_one({"PRN":PRN})
    dbChaavi = result["chaavi"]
    return dbChaavi

# # Comparison
def compare(pdfChaavi, dbChaavi):
    if (pdfChaavi == dbChaavi):
        print ('The PDF is genuine')
    else:
        print ('The PDF is not genuine')
