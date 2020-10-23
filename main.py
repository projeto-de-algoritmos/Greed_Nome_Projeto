from flask import Flask, request, redirect, render_template, url_for
from waitress import serve

app = Flask(__name__)

city_options = [("15", "Samambaia"), ("16", "Recanto das Emas")]


@app.route('/', methods=["GET", "POST"])
def home_page():
    city = request.form.get("city_select")
    if city == "15" or city == "16":
        return redirect(url_for('result', city_id=city))

    return render_template("home_page.html", data=city_options)


@app.route("/result/<city_id>", methods=["GET", "POST"])
def result(city_id):
    return(str(city_id))


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
