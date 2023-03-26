import sqlite3

from prettytable import PrettyTable


con = sqlite3.connect("trainstationDB.db")
cursor = con.cursor()
loggedInUser = None


def executeCursorSelect(sql, parameters):
    cursor.execute(sql, parameters)
    return cursor.fetchall()


def trainRoutesByDayAndTrainStation(trainStation, day):
    stationID = executeCursorSelect(
        "SELECT StationsID FROM Trainstation WHERE Name=?", [trainStation]
    )[0][0]

    weekDayID = executeCursorSelect(
        "SELECT WeekDayID FROM WeekDay WHERE Name=?", [day]
    )[0][0]

    result = executeCursorSelect(
        """SELECT r.TrainRouteID, i.ArrivalTime as Arrival, i.DepartureTime as Departure
    FROM TrainRoute r
    INNER JOIN TrainRouteRunsWeekDays w ON w.TrainRouteID = r.TrainRouteID
    INNER JOIN IntermediateStationOnTrainRoute i ON r.TrainRouteID = i.TrainRouteID
    WHERE i.StationsID = ? AND w.WeekDayID = ?
    """,
        [stationID, weekDayID],
    )

    startAndEndstations = []
    for i in result:
        startStation = executeCursorSelect(
            """SELECT ts.Name FROM Trainstation ts INNER JOIN IntermediateStationOnTrainRoute i1 ON i1.StationsID = ts.StationsID INNER JOIN TrainRoute r ON r.TrainRouteID = i1.TrainRouteID
	        WHERE r.TrainRouteID = ?
	        ORDER BY
		        CASE WHEN r.MainDirection = 0 THEN ts.StationsID ELSE '' END DESC,
		        CASE WHEN r.MainDirection = 1 THEN ts.StationsID ELSE '' END ASC LIMIT 1""",
            [i[0]],
        )

        endStation = executeCursorSelect(
            """SELECT ts.Name FROM Trainstation ts INNER JOIN IntermediateStationOnTrainRoute i1 ON i1.StationsID = ts.StationsID INNER JOIN TrainRoute r ON r.TrainRouteID = i1.TrainRouteID
	        WHERE r.TrainRouteID = ?
	        ORDER BY
		        CASE WHEN r.MainDirection = 0 THEN ts.StationsID ELSE '' END ASC,
		        CASE WHEN r.MainDirection = 1 THEN ts.StationsID ELSE '' END DESC LIMIT 1""",
            [i[0]],
        )
        startAndEndstations.append([startStation[0][0], endStation[0][0]])

    stationTimeTable = PrettyTable()

    stationTimeTable.field_names = [
        "TrainRouteID",
        "From",
        "To",
        "Arrival",
        "Departure",
    ]
    print("\n")
    print("=====================")
    for i in range(len(result)):
        stationTimeTable.add_row(
            [
                result[i][0],
                startAndEndstations[i][0],
                startAndEndstations[i][1],
                result[i][1],
                result[i][2],
            ]
        )

    print(stationTimeTable)
    print("=====================")


def trainRoutesByStartAndEndStationsAndDayAndTime(startStation, endStation, day, time):
    startStationID = executeCursorSelect(
        "SELECT StationsID FROM Trainstation WHERE name = ?", [startStation]
    )[0][0]
    endStationID = executeCursorSelect(
        "SELECT StationsID FROM Trainstation WHERE name = ?", [endStation]
    )[0][0]

    result = executeCursorSelect(
        """
    WITH StationsWithOrder AS
        (SELECT TrainRouteID,  StationsID, StationOrder, MainDirection, ArrivalTime, DepartureTime
        FROM IntermediateStationOnTrainRoute
        INNER JOIN TrainRoute USING (TrainRouteID)
        INNER JOIN IntermediateStationOnTrackStretch USING (TrackID, StationsID)
        WHERE StationsID = ?1 OR StationsID = ?2)
    SELECT TrainRouteID, Time as Date, DepartureStation, DepartureTime, ArrivalStation, ArrivalTime
    FROM TrainRouteInstance
    INNER JOIN
        (SELECT TrainRouteID, MainDirection, minStation, minStationOrder, maxStation,maxStationOrder,
        CASE WHEN MainDirection = 1 THEN mi.DepartureTime ELSE ma.DepartureTime END AS DepartureTime,
        CASE WHEN MainDirection = 1 THEN ma.ArrivalTime ELSE mi.ArrivalTime END AS ArrivalTime,
        CASE WHEN MainDirection = 1 THEN mi.StationName ELSE ma.StationName END AS DepartureStation,
        CASE WHEN MainDirection = 1 THEN ma.StationName ELSE mi.StationName END AS ArrivalStation
        FROM
            (SELECT TrainRouteID, StationsID AS minStation, min(StationOrder) AS minStationOrder, MainDirection, DepartureTime, ArrivalTime, Name as StationName
            FROM StationsWithOrder
            INNER JOIN Trainstation USING (StationsID)
            GROUP BY TrainRouteID)
        AS mi
        INNER JOIN
            (SELECT TrainRouteID, StationsID AS maxStation, max(StationOrder) AS maxStationOrder, DepartureTime, ArrivalTime, Name as StationName
            FROM StationsWithOrder
            INNER JOIN Trainstation USING (StationsID)
            GROUP BY TrainRouteID)
        AS ma
        USING (TrainRouteID))
    USING (TrainRouteID)
    WHERE ((MainDirection == 1 AND minStation = ?1 AND maxStation == ?2)
    OR (MainDirection == 0 AND maxStation = ?1 AND minStation == ?2))
    AND (Time = date(?3) or Time = date(?3, "+1 day"))
     AND DepartureTime >= time(?4)
	  """,
        [startStationID, endStationID, day, "00:00:00" if time == "" else time],
    )

    stationTimeTable = PrettyTable()

    stationTimeTable.field_names = [
        "TrainRoute",
        "Date",
        "Departure Station",
        "Departure Time",
        "Arrival Station",
        "Arrival Time",
    ]
    for i in result:
        stationTimeTable.add_row([i[0], i[1], i[2], i[3], i[4], i[5]])

    print(stationTimeTable, "\n")


def ticketsByLoggedinCustomer():
    result = executeCursorSelect(
        """SELECT co.OrderNumber, co.Time, t.InstanceID, t.PassengerPlaceID, tri.Time, c.Name FROM CustomerOrder co NATURAL JOIN Ticket t
        INNER JOIN TrainRouteInstance tri ON t.InstanceID = tri.InstanceID Natural JOIN Customer c
            WHERE c.Email == ?
        """,
        [loggedInUser["email"]],
    )

    pt = PrettyTable()

    pt.field_names = [
        "Order number",
        "Purchase date",
        "train route instance id",
        "passanger place id",
        "ticket valid date",
        "ticket customer",
    ]
    for i in result:
        pt.add_row([i[0], i[1], i[2], i[3], i[4], i[5]])
    print(pt, "\n")


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
            "SELECT Name, Email, Address, TelephoneNumber FROM Customer WHERE Email = ?",
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
    print("\n")

    response = input("what to do... :")
    print("\n")

    register() if (response == "1") else login()

    while True:
        print(
            " - Type 1 to list all the available trainRoutes at a given day and trainStation\n "
        )
        print(
            " - Type 2 to list all the available trainRoutes that pass though given start and end stations at a given day and time\n "
        )
        response = input("Type in your answer: ")
        print("\n")

        match response:
            case "1":
                trainStation = input("Which trainStation do you wish to check: ")
                day = input("Which day do you wish to check for: ")
                trainRoutesByDayAndTrainStation(trainStation, day)

            case "2":
                startStation = input("Start station: ")
                endStation = input("End station: ")
                day = input("Which day do you wish to travel: ")
                time = input("At what time do you wish to travel: ")
                trainRoutesByStartAndEndStationsAndDayAndTime(
                    startStation, endStation, day, time
                )
            case "3":
                ticketsByLoggedinCustomer()

            case _:
                con.close()
                exit()


main()
