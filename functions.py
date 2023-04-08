import pikepdf
import pymongo
import random
import string

import fitz
# Image Resizing
from PIL import Image


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



def adding_image(inputFilePath):
    pdf_doc = fitz.open(inputFilePath)
    resize_img()
    image = fitz.Pixmap("./images/resized_img.png")
    page = pdf_doc[0]
    page.insert_image(fitz.Rect(50, 50, 200, 200), pixmap=image)
    pdf_doc.saveIncr()
    pdf_doc.close()

def extract_img_pdf(newFilePath):
    example = pikepdf.open(newFilePath)
    page1 = example.pages[0]
    variable = list(page1.images.keys())
    if '/fzImg0' in variable:
        contains = "true"
    else:
        contains = "false"
    return variable, contains

def details_img(inputFilePath, contains, variable):
    if(contains == "true"):
        example = pikepdf.open(inputFilePath)
        page1 = example.pages[0]
        pdfimage = page1.images['/fzImg0']
        width = pdfimage.Width
        height = pdfimage.Height
        return width, height
    else:
        return print("Nope")


def random_hei_wei():
    ran_height = random.randint(320, 560)
    ran_width = random.randint(640, 980)
    return ran_height, ran_width


def resize_img():
    image = Image.open('./images/trans.png')
    ran_height, ran_width = random_hei_wei()
    resized_img = image.resize((ran_width, ran_height))
    resized_img.save('./images/resized_img.png')

