from flask import Flask, render_template, request, url_for
from waitress import serve

app = Flask(__name__)

city_options = [("15", "Samambaia"), ("16", "Recanto das Emas")]


@app.route('/')
def home_page():
    return render_template("home_page.html", data=city_options)


@app.route("/result", methods=["GET", "POST"])
def result():
    select = request.form.get("city_select")
    return(str(select))


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
