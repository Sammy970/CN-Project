from flask import *
from functions import *
import pymongo

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/makePDF", methods=['POST', 'GET'])
def makingPDF():
    return render_template("makePDF.html")


@app.route("/formData", methods=['POST', 'GET'])
def formData():
    PRN = request.form['PRN']
    # PRN = int(PRN)
    keyLength = request.form['key']
    # key = int(key)
    newPdfName = request.form['newPdfName']
    # newPdfName = newPdfName + '.pdf'
    filePDF = request.files['PdfFile']
    filePDF.save('./uploads/' + newPdfName + '.pdf')
    return redirect(url_for('adding_security', data1=PRN, data2=keyLength, data3=newPdfName))


@app.route("/adding_security", methods=['POST', 'GET'])
def adding_security():

    PRN = request.args.get('data1')
    keyLength = request.args.get('data2')
    newPdfName = request.args.get('data3')

    filePath = './uploads/' + newPdfName + '.pdf'

    keyNum = int(keyLength)
    print(type(keyNum))
    key = generate_key(keyNum)

    writingKey(filePath, newPdfName, key)
    insertKeyDB(key, PRN)

    filePath = './security_docs/' + newPdfName + '.pdf'

    height, width, num_array = adding_image(filePath, PRN)

    return render_template('security_data.html', keyData=key, heightData=height, widthData=width, numData=num_array)


@app.route("/verifyPDF", methods=['POST', 'GET'])
def verifyPDF():
    return render_template('verifyPDF.html')


@app.route("/uploadVerifyPDF", methods=['POST'])
def uploadVerifyPDF():

    newPdfName = request.form['newPdfName']

    filePDF = request.files['PdfFile']
    filepath = './user_uploads/' + newPdfName + '.pdf'
    filePDF.save(filepath)

    extract_img_pdf(filepath)


    return "hello"


if __name__ == "__main__":
    app.run(debug=True)
