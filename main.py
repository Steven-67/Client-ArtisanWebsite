from flask import Flask

app = Flask(__name__)

@app.route("/")

def project():
    return("My Project")

if__name__=="__main__"

app.run(host='0,0,0,0', debug=True)
