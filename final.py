# Importing Dependencies
import pymongo
import pikepdf
import random
import string
import fitz

# Image Resizing
from PIL import Image

# importing functions
from functions import *

# MongoDB Connection
client = pymongo.MongoClient("mongodb+srv://OmkarMK:Omkar321@cluster0.m43xxjz.mongodb.net/test")
db = client["testDb"]
collection = db["testCollection"]


# Function

def adding_image(inputFilePath):
    pdf_doc = fitz.open(inputFilePath)
    resize_img()
    image = fitz.Pixmap("resized_img.png")
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
    image = Image.open('../test.png')
    ran_height, ran_width = random_hei_wei()
    resized_img = image.resize((ran_width, ran_height))
    resized_img.save('resized_img.png')



# Main Code:

print("Hello and Welcome")
print("Please choose one option: ")
print("1. Writing Key")
print("2. Verifying PDF")
print("3. Add Image")
print("4. Check Image")

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
    writingKey(filePath, fileName, key)
    insertKeyDB(key, PRN, collection)
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
    dbChaavi = retrievingKeyDB(PRN, collection)
    compare(pdfChaavi, dbChaavi)
    print("--------------------------------")

elif (result == "3"):
    inputFilePath = input()
    # newFileName = input()
    adding_image(inputFilePath)
    # newFilePath = newFileName + '.pdf'

elif (result == "4"):
    inputFilePath = input()
    variable, contains = extract_img_pdf(inputFilePath)
    print(contains)
    width, height = details_img(inputFilePath, contains, variable)
    print("Width =  ", width)
    print("Height = ", height)

else:
    print("Please choose one of the following options")