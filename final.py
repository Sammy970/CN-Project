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