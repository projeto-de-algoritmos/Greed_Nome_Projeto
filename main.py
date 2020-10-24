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
    average_duration_bus_routes = {}
    bus_routes_start_times = []

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

    number_buses = 0
    bus_occupancy_end_time = []
    bus_data = {}
    for bus_routes_start_time in bus_routes_start_times:
        average_duration_bus_route = (
            average_duration_bus_routes[bus_routes_start_time[1]]
        )
        bus_routes_end_time = (
            bus_routes_start_time[0] + average_duration_bus_route
        )

        if bus_occupancy_end_time and (
            bus_routes_start_time[0] > bus_occupancy_end_time[0][0]
        ):
            bus = int(bus_occupancy_end_time.pop(0)[1])
            bus_occupancy_end_time.append((bus_routes_end_time, str(bus)))
            bus_occupancy_end_time.sort()

            bus_data[bus].append(
                (
                    bus_routes_start_time[0],
                    bus_routes_start_time[1],
                    bus_routes_end_time
                )
            )
        else:
            number_buses = number_buses + 1
            bus_occupancy_end_time.append(
                (bus_routes_end_time, str(number_buses))
            )
            bus_occupancy_end_time.sort()

            bus_data[number_buses] = []
            bus_data[number_buses].append(
                (
                    bus_routes_start_time[0],
                    bus_routes_start_time[1],
                    bus_routes_end_time
                )
            )

    return render_template("result.html", data=number_buses)


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
