import sqlite3

from prettytable import PrettyTable
from datetime import date
from buyTickets import buyTickets
from buyTickets import findPartialTrackStretch

con = sqlite3.connect("trainstationDB.db")
cursor = con.cursor()
loggedInUser = None


def executeCursorSelect(sql, parameters):
    cursor.execute(sql, parameters)
    return cursor.fetchall()


def trainRoutesByDayAndTrainStation():
    while True:
        trainStation = input("Which trainStation do you wish to check: ")
        day = input(
            "Which weekday do you wish to check for (E.g. Monday, Tuesday, etc.): "
        )
        try:
            stationID = executeCursorSelect(
                "SELECT StationsID FROM Trainstation WHERE Name=?", [trainStation]
            )[0][0]
            weekDayID = executeCursorSelect(
                "SELECT WeekDayID FROM WeekDay WHERE Name=?", [day]
            )[0][0]
            break
        except:
            print("Innvalid input ")

    result = executeCursorSelect(
        """SELECT r.TrainRouteID, i.ArrivalTime as Arrival, i.DepartureTime as Departure
    FROM TrainRoute r
    INNER JOIN TrainRouteRunsWeekDays w USING (TrainRouteID)
    INNER JOIN IntermediateStationOnTrainRoute i USING (TrainRouteID)
    WHERE i.StationsID = ? AND w.WeekDayID = ?
    """,
        [stationID, weekDayID],
    )

    startAndEndstations = []
    for i in result:
        startStation = executeCursorSelect(
            """SELECT ts.Name
            FROM Trainstation ts
            INNER JOIN IntermediateStationOnTrainRoute i1 USING (StationsID)
            INNER JOIN TrainRoute r USING (TrainRouteID)
	        WHERE r.TrainRouteID = ?
	        ORDER BY
		        CASE WHEN r.MainDirection = 0 THEN ts.StationsID ELSE '' END DESC,
		        CASE WHEN r.MainDirection = 1 THEN ts.StationsID ELSE '' END ASC LIMIT 1""",
            [i[0]],
        )

        endStation = executeCursorSelect(
            """SELECT ts.Name
            FROM Trainstation ts
            INNER JOIN IntermediateStationOnTrainRoute i1 USING (StationsID)
            INNER JOIN TrainRoute r USING (TrainRouteID)
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
    print("")


def trainRoutesByStartAndEndStationsAndDayAndTime():
    print("")
    while True:
        startStation = input("What's the start station: ")
        endStation = input("What's the end station: ")
        day = input("Which day do you wish to travel (yyyy-MM-dd): ")
        time = input("At what time do you wish to travel (hh:mm:ss): ")
        try:
            startStationID = executeCursorSelect(
                "SELECT StationsID FROM Trainstation WHERE name = ?", [startStation]
            )[0][0]
            endStationID = executeCursorSelect(
                "SELECT StationsID FROM Trainstation WHERE name = ?", [endStation]
            )[0][0]
            break
        except:
            print("Innvalid inputs. Try again")

    result = executeCursorSelect(
        """
    WITH StationsWithOrder AS
        (SELECT TrainRouteID,  StationsID, StationOrder, MainDirection, ArrivalTime, DepartureTime
        FROM IntermediateStationOnTrainRoute
        INNER JOIN TrainRoute USING (TrainRouteID)
        INNER JOIN IntermediateStationOnTrackStretch USING (TrackID, StationsID)
        WHERE StationsID = ?1 OR StationsID = ?2)

    SELECT TrainRouteID, Time as Date, DepartureStation, DepartureTime, ArrivalStation, ArrivalTime, InstanceID
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
    AND ((Time = date(?3) AND DepartureTime >= time(?4))
    OR Time = date(?3, "+1 day"))
    ORDER BY Date ASC, DepartureTime ASC
    """,
        [
            startStationID,
            endStationID,
            date.today() if day == "" else day,
            "00:00:00" if time == "" else time,
        ],
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

    print(stationTimeTable)
    print("\n")
    return result


def buyAvailableTicketsOnGivenTrainRoute():
    # Run the search function first and pass into here:
    # 0 Should be the id
    result = trainRoutesByStartAndEndStationsAndDayAndTime()
    print(
        """"
To choose: Write the index (first =  1) of
the travel you want to buy tickets to."""
    )
    while True:
        chosenTravel = int(input("On which route do you want to travel?: ")) - 1
        startStation = input("Input the start station: ")
        endStation = input("Input the end station: ")
        try:
            result[chosenTravel]
            break
        except Exception as error:
            print("Not a legal route.")
            continue

    buyTickets(
        result[chosenTravel][6],
        result[chosenTravel][0],
        loggedInUser,
        startStation,
        endStation,
    )


def ticketsByLoggedinCustomer():
    result = executeCursorSelect(
        """SELECT co.OrderNumber, co.Time, tri.TrainRouteID, t.PassengerPlaceID, tri.Time, c.Name

        NATURAL JOIN Ticket t
        NATURAL JOIN Customer c
        NATURAL JOIN PassengerPlace pp
        INNER JOIN TrainRouteInstance tri
            USING (InstanceID)
        NATURAL JOIN TrainRoute tr
            WHERE c.Email == ?
        """,
        [loggedInUser["email"]],
    )

    pt = PrettyTable()
    pt.field_names = [
        "Order number",
        "Purchase date",
        "Train route",
        "Seat/Bed number",
        "Ticket date",
        "Customer",
        "From Station",
        "To Station",
    ]
    for i in result:
        trackStretches = executeCursorSelect(
            """
        SELECT StartStation, EndStation, StationOrder, MainDirection  FROM IntermediateStationOnTrackStretch
        INNER JOIN IntermediateStationOnTrainRoute USING (StationsID)
        INNER JOIN PartialTrackStretch on StationsID = StartStation
        INNER JOIN TicketOnPartialTrackStretch USING (PartialTrackStretchID)
        INNER JOIN TrainRoute USING (TrainRouteID)
        WHERE TrainRouteID = ?
        ORDER BY StationOrder ASC
        """,
            [i[2]],
        )
        if trackStretches[0][3] == 1:  # Check which direction the trainroute goes
            fromStation = trackStretches[0][0]  # Set from station
            toStation = trackStretches[-1][1]  # Set to station
        else:
            fromStation = trackStretches[-1][1]  # Set from station
            toStation = trackStretches[0][0]  # Set to station

        fromStation = executeCursorSelect(
            "SELECT Name FROM Trainstation WHERE StationsID = ?", [fromStation]
        )[0][0]
        toStation = executeCursorSelect(
            "SELECT Name FROM Trainstation WHERE StationsID = ?", [toStation]
        )[0][0]

        pt.add_row([i[0], i[1], i[2], i[3], i[4], i[5], fromStation, toStation])

    print(pt, "\n")


def register():
    print("Thank you for wanting to be registered as a new customer.\n")
    print("Please type in your information:")

    name = input("  Name: ")
    email = input("  Email: ")
    address = input("  Address: ")
    tellephone_number = input("  Telephone number: ")

    while (
        executeCursorSelect(
            "SELECT Email FROM Customer WHERE Email = ? AND TelephoneNumber = ?",
            [email, tellephone_number],
        )
        != []
    ):
        print(
            "The chosen email or the tellephone number is not avaiable, because it's already used."
        )
        print("\nPlease try again:)")
        name = input("  Name: ")
        email = input("  Email: ")
        address = input("  Address: ")
        tellephone_number = input("  Telephone number: ")

    cursor.execute(
        "INSERT INTO Customer(Name, Email, Address, TelephoneNumber) VALUES (?, ?, ?, ?)",
        [name, email, address, tellephone_number],
    )
    con.commit()
    print("\nFantastic!! You are now registered as a user.")
    print("You now will be transfer to the login interface.\n")

    login()


def login():
    email = input("Email: ")
    user = executeCursorSelect(
        "SELECT CustomerNumber, Name, Email, Address, TelephoneNumber  FROM Customer WHERE Email = ?",
        [email],
    )

    while user == []:
        print("\nThe provided email was not found.")
        print("Please try again\n")
        email = input("Email: ")
        user = executeCursorSelect(
            "SELECT * FROM Customer WHERE Email = ?",
            [email],
        )

    print("\nWonderful!!! You are now logged in\n")

    global loggedInUser
    loggedInUser = {
        "CustomerNumber": user[0][0],
        "name": user[0][1],
        "email": user[0][2],
        "address": user[0][3],
        "telephoneNumber": user[0][4],
    }


def displayUserInfo():
    result = executeCursorSelect(
        """SELECT Name, Email, Address, TelephoneNumber FROM Customer WHERE Email = ?
        """,
        [loggedInUser["email"]],
    )[0]

    pt = PrettyTable()

    pt.field_names = [
        "Name",
        "Email",
        "Address",
        "Telephone Number",
    ]
    pt.add_row([result[0], result[1], result[2], result[3]])
    print(pt, "\n")


def main():
    print("\nWelcome to the trainstation database :)\n")
    print("Please register a user og login if you allready have a user")
    print("  1 -> Register")
    print("  2 -> Login\n")

    response = input("What do you want to do... : ")
    print("")

    register() if (response == "1") else login()

    while True:
        print(
            " - Type 1 to list all the avaiable train routes at a given weekday and train station\n "
        )
        print(
            " - Type 2 to list all the available train routes that pass through given start and end stations at a given day and time\n "
        )

        print(" - Type 3 to buy tickets on a given route\n")
        print(" - Type 4 to see all your bought tickets\n")
        print(" - Type 9 to see user information")

        response = input("Type in your answer: ")

        print("")

        match response:
            case "1":
                trainRoutesByDayAndTrainStation()

            case "2":
                trainRoutesByStartAndEndStationsAndDayAndTime()

            case "3":
                buyAvailableTicketsOnGivenTrainRoute()

            case "4":
                ticketsByLoggedinCustomer()

            case "9":
                displayUserInfo()

            case _:
                con.close()
                exit()


main()
