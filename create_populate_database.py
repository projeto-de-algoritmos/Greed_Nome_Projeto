import os
import requests


origin_cities = [("15", "Samambaia"), ("16", "Recanto das Emas")]

destiny_city = ("25", "Plano Piloto")

base_url_bus_routes_id = ("https://www.sistemas.dftrans.df.gov.br/linha/ra/")

bus_routes_id = {}


def populate_bus_routes_id():
    for origin_city in origin_cities:
        response = requests.get(
            base_url_bus_routes_id + origin_city[0] + "/ra/" + destiny_city[0]
        ).json()

        data = ""
        path = origin_city[0] + "_" + destiny_city[0]

        i = 0
        for bus_route in response:
            if bus_route['numero']:
                bus_route_id = bus_route['numero']

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


def create_database():
    os.mkdir("./database/")
    os.mkdir("./database/bus_routes_id/")


def main():
    create_database()
    popula_database()


if __name__ == '__main__':
    main()
    exit()
