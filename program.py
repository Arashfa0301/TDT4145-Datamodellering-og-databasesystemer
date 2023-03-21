import sqlite3


con = sqlite3.connect("trainstationDB.db")
cursor = con.cursor()
loggedInUser = None


def executeCursorSelect(sql, parameters):
    cursor.execute(sql, parameters)
    return cursor.fetchall()


def trainRoutesByDayAndTrainStation(trainStation, day):
    print("To be implemented")


def trainRoutesByStartAndEndStationsAndDayAndTime(startStation, endStation, day, time):
    print("asdf")


def register():
    print("Thank you for wanting to be registered as a new customer.")
    print("Please type in your information")

    name = input("Name: ")
    email = input("Email: ")
    address = input("Address: ")
    tellephone_number = input("Telephone number: ")

    while (
        executeCursorSelect(
            "SELECT Email FROM Customer WHERE Email = ? AND TelephoneNumber = ?",
            [email, tellephone_number],
        )
        != []
    ):
        print(
            "Either the email or the tellephone number is unfortunately allready registered on another customer."
        )
        print("Please try again :)")
        name = input("Name: ")
        email = input("Email: ")
        address = input("Address: ")
        tellephone_number = input("Telephone number: ")

    # this goes to shit when the private key is id. total shit
    cursor.execute(
        "INSERT INTO Customer(Name, Email, Address, TelephoneNumber) VALUES (?, ?, ?, ?)",
        [name, email, address, tellephone_number],
    )

    print("Fantastic!! You are now registered as a user.")
    print("You now will be transfer to the login interface. ")

    login()


def login():
    email = input("Epost: ")
    user = executeCursorSelect(
        "SELECT Name, Email, Address, TelephoneNumber FROM Customer WHERE Email = ?",
        [email],
    )

    while user == []:
        print("The provided email was not found.")
        print("Please try again. ")
        email = input("Epost: ")
        user = executeCursorSelect(
            "SELECT Email FROM Customer WHERE Email = ?",
            [email],
        )

    print("Wonderful!!! You are now logged in ")

    global loggedInUser
    loggedInUser = {
        "name": user[0],
        "email": user[1],
        "address": user[2],
        "telephoneNumber": user[3],
    }


def main():
    print("Welcome to the trainstation database :)")
    print("Please register a user og login if you allready have a user")
    print("- 1 -> Register")
    print("- 2 -> Login")
    response = input("what to do... :")

    register() if (response == "1") else login()

    while True:
        print(
            " - Type 1 to list all the available trainRoutes at a given day and trainStation\n "
        )
        print(
            " - Type 2 to list all the available trainRoutes that pass though given start and end stations at a given day and time\n "
        )
        response = input("Type in your answer: ")

        match response:
            case "1":
                trainStation = input("Which trainStation do you wish to check: ")
                day = input("Which day do you wish to check for: ")
                trainRoutesByDayAndTrainStation(trainStation, day)

            case "2":
                startStation = input("Start station: ")
                endStation = input("End station: ")
                day = input("While day do you wish to travel: ")
                time = input("At white time do you wish to travel: ")
                trainRoutesByStartAndEndStationsAndDayAndTime(
                    startStation, endStation, day, time
                )

            case _:
                con.close()
                exit()


main()
