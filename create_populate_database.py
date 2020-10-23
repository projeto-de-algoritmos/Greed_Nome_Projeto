import os


def create_database():
    os.mkdir("./database/")
    os.mkdir("./database/bus_routes_id/")


def main():
    create_database()


if __name__ == '__main__':
    main()
    exit()
