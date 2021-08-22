import os

from flask import Flask, request, render_template, send_file

import findcontacts

app = Flask(__name__)


app.config['FILES_UPLOADS'] = "static\\files\\"

@app.route('/')
def hello_world():
    return render_template('1.html')

@app.route('/credentials', methods=['POST', 'GET'])
def save_credentials():
    save_credentials.username = request.form['Email address']
    save_credentials.password = request.form['Password']
    return render_template('2.html')

@app.route("/multiple", methods=['POST', 'GET'])
def multiple():
    return render_template('multiple.html', download = " Download Wouldn't work now!!", messagea="Submit a file and be patience, please don't close or change window while in process, you'll recieve a message after process is completed", messageb='After completion message press download')

@app.route("/single", methods=['POST', 'GET'])
def single():
    return render_template('single.html')

@app.route("/singlesearch", methods=['POST', 'GET'])
def singlesearch():
    singlesearch.comp = request.form['comp']
    singlesearch.pos = request.form['pos']
    find = findcontacts.extract(save_credentials.username, save_credentials.password)
    datadict = find.contacts_extraction(singlesearch.comp, singlesearch.pos)
    print(datadict)
    val =[]
    for k,v in datadict.items():
        strg = k + ' : ' + v
        val.append(strg)
    for i in range(5):
        val.append(' ')
    return render_template('single.html', Details1=val[0], Details2=val[1], Details3=val[2], Details4=val[3], Details5=val[4])

@app.route("/multiplesearch", methods=['POST', 'GET'])
def multiplesearch():
    file = request.files['fileinput']
    file.save(os.path.join(app.config['FILES_UPLOADS'], "testfile.txt"))
    findm = findcontacts.extract(save_credentials.username, save_credentials.password,multiple=True,filename='static/files/testfile.txt')
#     findm.contacts_extraction()
    return render_template('multiple.html', messagea='Your Information is ready to be downloaded!', messageb=' ', download='Download Now!')

@app.route("/downloads", methods=['POST', 'GET'])
def download():
    return send_file('Contact_Results.csv')


if __name__ == '__main__':
    app.run(debug=True)
