import pikepdf
import pymongo
import random
import string
import fitz

# Image Resizing
from PIL import Image

# MongoDB Connection
client = pymongo.MongoClient(
    "mongodb+srv://OmkarMK:Omkar321@cluster0.m43xxjz.mongodb.net/test")
db = client["testDb"]
collection = db["testCollection"]


# Generate Key Function
def generate_key(length):
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    numbers = string.digits
    special_characters = string.punctuation
    all_characters = uppercase_letters + \
        lowercase_letters + numbers + special_characters
    password = ''.join(random.choice(all_characters) for i in range(length))
    return password

# Writing key generated to the metadata of PDF


def writingKey(filePath, nameOfFile, key):
    pdf = pikepdf.Pdf.open(filePath, allow_overwriting_input=True)
    pdf.docinfo['/chaavi'] = key
    pdf.save('./security_docs/' + nameOfFile + '.pdf')

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


def retrievingKeyDB(PRN, collection):
    result = collection.find_one({"PRN": PRN})
    dbChaavi = result["chaavi"]
    return dbChaavi

# Comparison


def compare(pdfChaavi, dbChaavi):
    if (pdfChaavi == dbChaavi):
        print('The PDF is genuine')
    else:
        print('The PDF is not genuine')


# Adding Invisible Watermark Image to PDF Function
def adding_image(inputFilePath, PRN):

    pdf_doc = fitz.open(inputFilePath)

    resize_img()

    image = fitz.Pixmap("./images/resized_img.png")

    height = image.height
    width = image.width

    if (pdf_doc.page_count == 1):
        num_pages = 1
    else:
        num_pages = pdf_doc.page_count - 1

    num_array = num_of_pages(num_pages)

    adding_to_db(num_array, PRN, height, width)

    len_num_array = len(num_array)

    for i in range(len_num_array):
        pageNum = num_array[i]
        page = pdf_doc[pageNum]
        page.insert_image(fitz.Rect(50, 50, 200, 200), pixmap=image)

    pdf_doc.saveIncr()
    pdf_doc.close()

    return height, width, num_array


def num_of_pages(num_pages):
    randomList = []

    if (num_pages == 1):
        randomList.append(0)
        return randomList

    else:
        for i in range(random.randint(1, num_pages)):
            r = random.randint(0, num_pages)

            if r not in randomList:
                randomList.append(r)

        return randomList


def adding_to_db(num_array, PRN, height, width):

    object_to_update = collection.find_one({"PRN": PRN})

    size = {
        "height": height,
        "width": width
    }

    if (object_to_update):
        collection.update_one({"PRN": PRN}, {'$set': {"pageNum": num_array}})
        collection.update_one({"PRN": PRN}, {'$set': {"size": size}})

        print('New key-value pair added successfully!')
    else:
        print('Object not found in the collection.')

    return "hello"


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
    if (contains == "true"):
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
