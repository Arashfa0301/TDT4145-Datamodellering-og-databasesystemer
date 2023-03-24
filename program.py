import sqlite3
from prettytable import PrettyTable


con = sqlite3.connect("trainstationDB.db")
cursor = con.cursor()
loggedInUser = None


def executeCursorSelect(sql, parameters):
    cursor.execute(sql, parameters)
    return cursor.fetchall()


def trainRoutesByDayAndTrainStation(trainStation, day):
    dayQuery = ["SELECT WeekDayID FROM WeekDay WHERE Name=?",[day]]
    stationQuery = ["SELECT StationsID FROM Trainstation WHERE Name=?", [trainStation]]

    selTrainS = executeCursorSelect(stationQuery[0],stationQuery[1])
    weekDay = executeCursorSelect(dayQuery[0],dayQuery[1])

    query = ["""SELECT r.TrainRouteID, t1.Name, t2.Name, i.ArrivalTime as Arrival, i.DepartureTime as Departure
    FROM TrainRoute r 
    INNER JOIN TrainRouteRunsWeekDays w ON w.TrainRouteID = r.TrainRouteID
    INNER JOIN Trainstation t1 ON r.StartStation = t1.StationsID
    INNER JOIN Trainstation t2 ON r.EndStation = t2.StationsID
    INNER JOIN IntermediateStationOnTrainRoute i ON r.TrainRouteID = i.TrainRouteID
    WHERE i.StationsID = ? AND w.WeekDayID = ?
    """,[selTrainS[0][0], weekDay[0][0]]]
    
    result = executeCursorSelect(query[0], query[1])
    stationTimeTable = PrettyTable()

    stationTimeTable.field_names = ["ID","From","To","Arrival","Departure"]
    print("=====================")
    for i in result:
        stationTimeTable.add_row([i[0],i[1],i[2],i[3],i[4]])

    print(stationTimeTable)
    print("=====================")
    print("\n")


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
    # This just doesn't work atm, it doesn't actually insert into the database it seems.
    cursor.execute(
        "INSERT INTO Customer(Name, Email, Address, TelephoneNumber) VALUES (?, ?, ?, ?)",
        [name, email, address, tellephone_number],
    )
    con.commit()
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
        "name": user[0][0],
        "email": user[0][1],
        "address": user[0][2],
        "telephoneNumber": user[0][3],
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
