from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/preent", methods=['POST'])
def printName():
    name = request.form.get('name')
    return render_template('namePreent.html', name = name)


app.run(host="0.0.0.0", port=80)