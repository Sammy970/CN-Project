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


# Key checking in pdf and DB
def keyCheck(inputFilePath, PRN_num):
    find = collection.find_one({'PRN': PRN_num})
    example = pikepdf.open(inputFilePath)
    docMetadeta = example.docinfo
    try:
        key_doc = docMetadeta['/chaavi']
    except:
        pdf_state = "false"
        return pdf_state
    else:
        key_DB = find["chaavi"]
        if (key_doc == key_DB):
            pdf_state = "true"
            return pdf_state
        else:
            pdf_state = "false"
            return pdf_state


# Adding Invisible Watermark Image to PDF Function
def adding_image(inputFilePath, PRN):

    pdf_doc = fitz.open(inputFilePath)
    total_pages = pdf_doc.page_count
    resize_img()
    image = fitz.Pixmap("./images/resized_img.png")
    height = image.height
    width = image.width

    if (pdf_doc.page_count == 1):
        num_pages = 1
    else:
        num_pages = pdf_doc.page_count - 1

    num_array = num_of_pages(num_pages)
    adding_to_db(num_array, PRN, height, width, total_pages)
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


def adding_to_db(num_array, PRN, height, width, total_pages):

    object_to_update = collection.find_one({"PRN": PRN})

    size = {
        "height": height,
        "width": width
    }

    if (object_to_update):
        collection.update_one({"PRN": PRN}, {'$set': {"pageNum": num_array}})
        collection.update_one({"PRN": PRN}, {'$set': {"size": size}})
        collection.update_one(
            {"PRN": PRN}, {'$set': {"total_pages": total_pages}})

        print('New key-value pair added successfully!')
    else:
        print('Object not found in the collection.')

    return "hello"


def extract_img_pdf(newFilePath, PRN_num):
    example = pikepdf.open(newFilePath)
    find = collection.find_one({"PRN": PRN_num})
    contains = ''

    total_pages_state = "true"

    total_pages = len(example.pages)
    total_pages_db = find['total_pages']

    if (total_pages == total_pages_db):

        pages_with_img = find['pageNum']
        for x in pages_with_img:
            page = example.pages[x]
            variable = list(page.images.keys())
            if '/fzImg0' in variable:
                contains = 'true'
            else:
                contains = 'false'
        return contains, total_pages_state
    else:
        total_pages_state = "false"
        contains.append('false')
        return contains, total_pages_state


def details_img(inputFilePath, PRN_num):
    example = pikepdf.open(inputFilePath)
    find = collection.find_one({"PRN": PRN_num})

    pages_with_img = find['pageNum']

    for x in pages_with_img:
        page = example.pages[x]
        pdfimage = page.images['/fzImg0']
        width = pdfimage.Width
        height = pdfimage.Height
        db_width = find['size']['width']
        db_height = find['size']['height']

        if (width == db_width and height == db_height):
            pdf_state = 'true'
        else:
            pdf_state = 'false'

    return pdf_state


def random_hei_wei():
    ran_height = random.randint(320, 560)
    ran_width = random.randint(640, 980)
    return ran_height, ran_width


def resize_img():
    image = Image.open('./images/trans.png')
    ran_height, ran_width = random_hei_wei()
    resized_img = image.resize((ran_width, ran_height))
    resized_img.save('./images/resized_img.png')
