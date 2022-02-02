import flask
from flask import send_from_directory, request
import base64
from Crypto.Cipher import AES

app = flask.Flask(__name__)

def decrypt(ct):
    from Crypto.Util.Padding import pad, unpad
    data = base64.b64decode(ct)
    cipher1 = AES.new("$71Pfb052473A3s6".encode("utf8"), AES.MODE_CBC, "0000000000000000".encode("utf8"))
    pt = unpad(cipher1.decrypt(data), 16)
    return pt

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/favicon.png')

@app.route('/')
@app.route('/home')
def home():
    encdata = request.args.get('encdata')
    return decrypt(encdata)

if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    app.debug = True
    app.run()
