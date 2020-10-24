from flask import Flask, request, redirect, render_template, url_for
from waitress import serve

app = Flask(__name__)

city_options = [("15", "Samambaia"), ("16", "Recanto das Emas")]

average_duration_bus_routes = {}

bus_routes_start_times = []


@app.route('/', methods=["GET", "POST"])
def home_page():
    city = request.form.get("city_select")
    if city == "15" or city == "16":
        return redirect(url_for('result', city_id=city))

    return render_template("home_page.html", data=city_options)


@app.route("/result/<city_id>", methods=["GET", "POST"])
def result(city_id):
    data_bus_routes_id = open(
        "./database/bus_routes_id/" + city_id + "_25.txt", 'r'
    )
    bus_routes_id = data_bus_routes_id.readlines()[0].split(",")
    data_bus_routes_id.close()

    for bus_route_id in bus_routes_id:
        data_schedules_bus_route = open(
            "./database/schedules_bus_routes/" + city_id + "_25/" +
            bus_route_id + ".txt"
        )
        schedules_bus_route = (
            data_schedules_bus_route.readlines()[0].split(',')
        )
        data_schedules_bus_route.close()

        average_duration_bus_routes[bus_route_id] = 2*int(
            schedules_bus_route[0]
        )

        for schedule_bus_route in schedules_bus_route[1:]:
            schedule = schedule_bus_route.split(':')
            hours = int(schedule[0])
            minutes = int(schedule[1])

            start_time = hours*60 + minutes
            bus_routes_start_times.append((start_time, bus_route_id))

    bus_routes_start_times.sort()
    return(str(bus_routes_start_times))


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
