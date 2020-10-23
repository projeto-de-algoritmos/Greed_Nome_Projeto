import os
import requests


origin_cities = [("15", "Samambaia"), ("16", "Recanto das Emas")]

destiny_city = ("25", "Plano Piloto")

base_url_bus_routes_id = "https://www.sistemas.dftrans.df.gov.br/linha/ra/"

bus_routes_id = {}

base_url_schedules_bus_routes = (
    "https://www.sistemas.dftrans.df.gov.br/horario/linha/numero/"
)


def populate_schedules_bus_routes():
    for path in bus_routes_id:
        data_archive_path = "./database/schedules_bus_routes/" + path + '/'
        os.mkdir(data_archive_path)

        for bus_route_id in bus_routes_id[path]:
            response = requests.get(
                base_url_schedules_bus_routes + bus_route_id
            ).json()

            data_archive = open(data_archive_path + bus_route_id + ".txt", 'w')

            for schedules_data in response:
                if (
                    schedules_data["duracaoMedia"] and
                    schedules_data["horarios"] and (
                        schedules_data["sentido"] == "CIRCULAR" or
                        schedules_data["sentido"] == "IDA"
                    )
                ):
                    data_archive.writelines(
                        schedules_data["duracaoMedia"]
                    )

                    data = ""
                    for schedule_data in schedules_data["horarios"]:
                        if (
                            schedule_data["diasLabel"] == "SEG_SEX" and (
                                schedule_data["sentido"] == "CIRCULAR" or
                                schedule_data["sentido"] == "IDA"
                            )
                        ):
                            data_archive = open(
                                data_archive_path + bus_route_id + ".txt", 'r'
                            )
                            data = data_archive.readlines()
                            data.append(',' + schedule_data['horario'])

                            data_archive = open(
                                data_archive_path + bus_route_id + ".txt", 'w'
                            )
                            data_archive.writelines(data)


def populate_bus_routes_id():
    for origin_city in origin_cities:
        response = requests.get(
            base_url_bus_routes_id + origin_city[0] + "/ra/" + destiny_city[0]
        ).json()

        data = ""
        path = origin_city[0] + '_' + destiny_city[0]

        i = 0
        for bus_route in response:
            if bus_route["numero"]:
                bus_route_id = bus_route["numero"]

                if i == 0:
                    i = 1
                    data = bus_route_id
                    bus_route_id[path] = [bus_route_id]
                else:
                    data = data + "," + bus_route_id
                    bus_route_id[path].append(bus_route_id)

        data_archive = open("./database/bus_routes_id/" + path + ".txt", 'w')
        data_archive.writelines(data)


def popula_database():
    populate_bus_routes_id()
    populate_schedules_bus_routes()


def create_database():
    os.mkdir("./database/")
    os.mkdir("./database/bus_routes_id/")
    os.mkdir("./database/schedules_bus_routes/")


def main():
    create_database()
    popula_database()


if __name__ == "__main__":
    main()
    exit()
