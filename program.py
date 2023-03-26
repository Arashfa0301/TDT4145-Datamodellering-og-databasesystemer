import sqlite3

from prettytable import PrettyTable
from datetime import date


con = sqlite3.connect("trainstationDB.db")
cursor = con.cursor()
loggedInUser = None


def executeCursorSelect(sql, parameters):
    cursor.execute(sql, parameters)
    return cursor.fetchall()


def trainRoutesByDayAndTrainStation(trainStation, day):
    print("")
    try: 
        stationID = executeCursorSelect(
            "SELECT StationsID FROM Trainstation WHERE Name=?", [trainStation]
        )[0][0]
    except:
        print("Not a valid trainstation.")
        return

    try:
        weekDayID = executeCursorSelect(
            "SELECT WeekDayID FROM WeekDay WHERE Name=?", [day]
        )[0][0]
    except:
        print("Not a valid weekday.")

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


def trainRoutesByStartAndEndStationsAndDayAndTime(startStation, endStation, day, time):
    print("")
    try:
        startStationID = executeCursorSelect("SELECT StationsID FROM Trainstation WHERE name = ?", [startStation])[0][0]
    except:
        print("Not a valid start station.")
        return
    
    try: 
        endStationID = executeCursorSelect("SELECT StationsID FROM Trainstation WHERE name = ?", [endStation])[0][0]
    except:
        print("Not a valid end station.")
        return

    if time == "":
        time = "00:00:00"

    if day == "":
        day = date.today()

    result = executeCursorSelect("""
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
	  """, [startStationID, endStationID, day, time]
    )

    stationTimeTable = PrettyTable()

    stationTimeTable.field_names = ["TrainRoute","Date", "Departure Station", "Departure Time", "Arrival Station", "Arrival Time"]
    for i in result:
        stationTimeTable.add_row([i[0],i[1],i[2],i[3],i[4],i[5]])

    print(stationTimeTable)
    print("")


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

    # this goes to shit when the private key is id. total shit
    # This just doesn't work atm, it doesn't actually insert into the database it seems.
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
        "SELECT Name, Email, Address, TelephoneNumber FROM Customer WHERE Email = ?",
        [email],
    )

    while user == []:
        print("\nThe provided email was not found.")
        print("Please try again\n")
        email = input("Email: ")
        user = executeCursorSelect(
            "SELECT Name, Email, Address, TelephoneNumber FROM Customer WHERE Email = ?",
            [email],
        )

    print("\nWonderful!!! You are now logged in\n")

    global loggedInUser
    loggedInUser = {
        "name": user[0][0],
        "email": user[0][1],
        "address": user[0][2],
        "telephoneNumber": user[0][3],
    }


def main():
    print("\nWelcome to the trainstation database :)\n")
    print("Please register a user og login if you allready have a user")
    print("  1 -> Register")
    print("  2 -> Login")
    print("")

    response = input("What do you want to do... : ")
    print("")

    register() if (response == "1") else login()

    while True:
        print(
            " - Type 1 to list all the available trainRoutes at a given day and trainStation\n "
        )
        print(
            " - Type 2 to list all the available trainRoutes that pass though given start and end stations at a given day and time\n "
        )
        response = input("Type in your answer: ")
        print("")

        match response:
            case "1":
                trainStation = input("Which trainStation do you wish to check: ")
                day = input("Which weekday do you wish to check for (E.g. Monday, Tuesday, etc.): ")
                trainRoutesByDayAndTrainStation(trainStation, day)

            case "2":
                startStation = input("What's the start station: ")
                endStation = input("What's the end station: ")
                day = input("Which day do you wish to travel (yyyy-MM-dd): ")
                time = input("At what time do you wish to travel (hh:mm:ss):")
                trainRoutesByStartAndEndStationsAndDayAndTime(
                    startStation, endStation, day, time
                )

            case _:
                con.close()
                exit()


main()
