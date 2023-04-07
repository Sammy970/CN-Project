# Importing Dependencies
import pymongo
import pikepdf
import random
import string

# MongoDB Connection
client = pymongo.MongoClient("mongodb+srv://OmkarMK:Omkar321@cluster0.m43xxjz.mongodb.net/test")
db = client["testDb"]
collection = db["testCollection"]

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
def writingKey(filePath, nameOfFile):
    pdf = pikepdf.Pdf.open(filePath, allow_overwriting_input=True)
    pdf.docinfo['/chaavi'] = key
    pdf.save(nameOfFile + '.pdf')

# Inserting Object into database
def insertKeyDB(key, prn):
    object = {"chaavi": key, "PRN": prn}
    collection.insert_one(object)

# Retrieving chaavi (key) from the metadata of PDF
def retrievingKey(filePath):
    pdf = pikepdf.Pdf.open(filePath, allow_overwriting_input=True)
    pdfMetadeta = pdf.docinfo
    pdfChaavi = pdfMetadeta['/chaavi']
    return pdfChaavi

# Retrieving chaavi from database
def retrievingKeyDB(PRN):
    result = collection.find_one({"PRN":PRN})
    dbChaavi = result["chaavi"]
    return dbChaavi

# # Comparison
def compare(pdfChaavi, dbChaavi):
    if (pdfChaavi == dbChaavi):
        print ('The PDF is genuine')
    else:
        print ('The PDF is not genuine')

# Main Code:

print("Hello and Welcome")
print("Please choose one option: ")
print("1. Writing Key")
print("2. Verifying PDF")

result = input()

if(result == "1"):
    print("--------------------------------")
    print("Please enter your PRN: ")
    PRN = input()
    key = generate_key(30)
    print("--------------------------------")
    print("Please enter the path to your PDF File: (with .pdf extension)")
    filePath = input()
    print("Entered file path = " + filePath)
    print("--------------------------------")
    print("Enter the filename to which you want to save your new PDF: (without .pdf extension) ")
    fileName = input()
    writingKey(filePath, fileName)
    insertKeyDB(key, PRN)
    print("Successfully Done!!")

elif (result == "2"):
    print("--------------------------------")
    print("Please enter your PRN: ")
    PRN = input()
    print("--------------------------------")
    print("Please enter the path to your PDF File: (with .pdf extension) ")
    filePath = input()
    print("Entered file path = " + filePath)
    print("--------------------------------")
    pdfChaavi = retrievingKey(filePath)
    dbChaavi = retrievingKeyDB(PRN)
    compare(pdfChaavi, dbChaavi)
    print("--------------------------------")

else:
    print("Please choose one of the following options")