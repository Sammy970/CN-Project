from flask import *
from functions import *
import pymongo
import os

app = Flask(__name__)
# Set a secret key for session security, replace with your own key
app.secret_key = 'Samyak_Jain'


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/makePDF", methods=['POST', 'GET'])
def makingPDF():
    path = './uploads'
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    path1 = './security_docs'
    isExist = os.path.exists(path1)
    if not isExist:
        os.makedirs(path1)
    return render_template("makePDF.html")


@app.route("/formData", methods=['POST', 'GET'])
def formData():

    PRN = request.form['PRN']
    keyLength = request.form['key']
    newPdfName = request.form['newPdfName']
    session['name_of_file'] = newPdfName
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


@app.route('/download', methods=['GET'])
def download():
    name_of_file = session.get('name_of_file')
    name_of_file = name_of_file + '.pdf'
    headers = {
        'Content-Disposition': 'attachment; filename=' + '"' + name_of_file + '"',
        'Content-Type': 'application/pdf',
    }
    filePath = './security_docs/' + name_of_file
    return send_file(filePath, as_attachment=True, mimetype='application/pdf')


@app.route("/verifyPDF", methods=['POST', 'GET'])
def verifyPDF():
    path2 = './user_uploads'
    isExist = os.path.exists(path2)
    if not isExist:
        os.makedirs(path2)
    return render_template('verifyPDF.html')


@app.route("/uploadVerifyPDF", methods=['POST', 'GET'])
def uploadVerifyPDF():

    PRN = request.form['PRN']
    newPdfName = request.form['newPdfName']
    filePDF = request.files['PdfFile']
    filepath = './user_uploads/' + newPdfName + '.pdf'
    filePDF.save(filepath)

    key_pdf_state = keyCheck(filepath, PRN)

    contains_img, total_pages_state = extract_img_pdf(filepath, PRN)

    if 'false' in contains_img:
        details_pdf_state = 'false'
        contains_img = 'false'
    else:
        details_pdf_state = details_img(filepath, PRN)

    # return key_pdf_state + " " + details_pdf_state
    return render_template('verified_data.html',
                           keyState=key_pdf_state,
                           totalpages_state=total_pages_state,
                           contains_img_state=contains_img,
                           img_details_state=details_pdf_state
                           )


if __name__ == "__main__":
    app.run(debug=True)
