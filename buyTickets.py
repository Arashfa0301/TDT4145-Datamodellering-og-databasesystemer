import sqlite3
from prettytable import PrettyTable
from datetime import datetime

con = sqlite3.connect("trainstationDB.db")
cursor = con.cursor()
loggedInUser = None


def executeCursorSelect(sql, parameters):
    cursor.execute(sql, parameters)
    return cursor.fetchall()

def buyTickets(InstanceID, TrainRouteID, loggedInUser):
    #Get wagons on trainroute
    try:
        getWagonType = ["""
        SELECT wl.WagonID, st.NumberOfRows, st.RowWidth, sl.NumberOfCompartments FROM TrainRoute tr 
        INNER JOIN WagonLayout wl ON tr.TrainRouteID = wl.TrainRouteID 
            LEFT JOIN SittingWagon st ON wl.WagonID = st.WagonID
            left join SleepingWagon sl on wl.WagonID = sl.WagonID
            WHERE tr.TrainRouteID = ? ORDER BY wl.Sequence  
        """, [TrainRouteID]]
        wagonArray = executeCursorSelect(getWagonType[0],getWagonType[1])
        nonAvailableSeatsPerWagon = []
        navSQuery = ["SELECT t.PassengerPlaceID FROM Ticket t INNER JOIN PassengerPlace p ON t.PassengerPlaceID = p.PassengerPlaceID WHERE p.InstanceID = ?",[InstanceID]]
        tempNon = []
        tempNon = executeCursorSelect(navSQuery[0],navSQuery[1])
        for seat in tempNon:
            nonAvailableSeatsPerWagon.append(seat[0])
        #vogner = executeCursorSelect("SELECT w.Name, w.WagonID FROM Wagon w INNER JOIN WagonLayout wl ON wl.TrainRouteID = ? ORDER BY wl.Sequence", [TrainRouteID])
        vogner = []
        for wagon in wagonArray:
            vogner.append(executeCursorSelect("SELECT w.Name FROM Wagon w WHERE w.WagonID = ?", [wagon[0]])[0])
        print("This train has these carriages: ")
        i = 1
        for vogn in vogner:
            print(f"{i}: {vogn[0]}")
            i+=1
        chosenWagonI = input("Pick a carriage:")
        chosenWagon = wagonArray[int(chosenWagonI)-1]
        print("Here are the available seats (X = Unavailable):")
        firstSeat = executeCursorSelect("SELECT p.PassengerPlaceID FROM PassengerPlace p WHERE p.InstanceID = ? AND p.WagonID = ? ORDER BY p.PassengerPlaceID LIMIT 1",[InstanceID, chosenWagon[0]])
        isSleeping = executeCursorSelect("SELECT * FROM SleepingWagon WHERE WagonID = ?",[chosenWagon[0]])
        if not (len(isSleeping)==0):
            printWagon(int(chosenWagon[0]), int(chosenWagon[3]),0,nonAvailableSeatsPerWagon,firstSeat[0][0])
        else:
            printWagon(int(chosenWagon[0]),int(chosenWagon[1]),int(chosenWagon[2]),nonAvailableSeatsPerWagon,firstSeat[0][0])
        tickets = []
        while True:
            chosenPlace = input("Choose a seat:")
            checkPlace = executeCursorSelect("SELECT * FROM PassengerPlace WHERE PassengerPlaceID = ? AND InstanceID = ?",[int(chosenPlace), InstanceID])
            if len(checkPlace) == 0:
                print("This seat does not exist on this journey.")
                continue
            if int(chosenPlace) in nonAvailableSeatsPerWagon or int(chosenPlace) in tickets:
                print("That seat is not available.")
            else:
                tickets.append(int(chosenPlace))
                chooseAnother = input("Do you want to buy another from this carriage? (Y/N):")
                if chooseAnother == 'Y':
                    continue
                else:
                    break
        
        booking = executeCursorSelect("SELECT COUNT(*) FROM CustomerOrder WHERE CustomerNumber = ?",[loggedInUser["CustomerNumber"]])[0]
        time = datetime.now()
        cancelBook = input(f"Confirm booking (Y/N): ")
        if not cancelBook == "Y":
            return 0
        cursor.execute("INSERT INTO CustomerOrder VALUES(?,?,?)",[booking[0],time.strftime("%Y-%m-%d %H:%M:%S"),loggedInUser["CustomerNumber"]])
        for ticket in tickets:
            cursor.execute("INSERT INTO Ticket (OrderNumber, InstanceID, PassengerPlaceID) VALUES(?,?,?)",[booking[0],InstanceID,ticket])
        ## Men får med null verdier, kan bruke case for å hindre det.

        query = """INSERT INTO Ticket (OrderNumber, InstanceID) VALUES (2,0)"""
        #actual_shit = executeCursorSelect("SELECT * FROM Ticket",[])
    except Exception as error:
        print("""
        Something went wrong, you might have inputted something illegal.
        You can try again if you want to.
        """)
        return 0
    con.commit()
    print("Booking confirmed.")




# Print a wagon with available seats (by ID)
def printWagon(type, numRowsOrCol, rowWidth, nonAvailableSeats, startIDWagon):
    start = " "
    end = " "

    if(type == 0):
        widthOfSeat = "-----" * rowWidth
        print(start + widthOfSeat + end)
        # SittingWagon
        k = startIDWagon
        for i in range(numRowsOrCol):
            row = "|"
            for j in range(rowWidth):
                p = "X"
                if k not in nonAvailableSeats:
                    p = k
                if(k<10):
                    row += f" [ {p}]"
                elif(k<100):
                    row += f" [{p}]"    
                k+=1
            row += " |"
            print(row)
            if(i<numRowsOrCol-1):
                print("|"+"     "*(rowWidth) + " |")
        print(start + widthOfSeat + end)
    elif(type == 1):
        k = startIDWagon
        print(" ------------ ")
        for i in range(numRowsOrCol*2):
            if k >= startIDWagon + numRowsOrCol*2:
                break
            if k not in nonAvailableSeats and k+1 not in nonAvailableSeats:
                if k < 10:
                    comp = (f"|    |{k}-----#|")
                elif k < 100:
                    comp = (f"|    |{k}----#|")
                elif k < 1000:
                    comp = (f"|    |{k}---#|")
                print(comp)
                if not k % 2 == 0:
                    print("| Dør|       |")
                else:
                    print("|    |———————|")
                    
            else:
                comp = f"|    |X-----#|\n"
                comp += f"| Dør|       |\n"
                comp += f"|    |X-----#|\n"
                comp += "|    |———————|"
                print(comp)
                k+=1
            k+=1
        print(" ------------ ")

# Help function to print compartments
def compartmentPrinter(number):
    bed1 = number
    bed2 = number + 1
    compartment = ""
    if number+1 < 10:
        compartment += f"|    |{bed1}-----#|\n"
        compartment += f"|    |        |\n"
        compartment += f"|    |{bed2}-----#|"
    elif number+1<100:
        compartment += f"|    |{bed1}----#|\n"
        compartment += f"|    |        |\n"
        compartment += f"|    |{bed2}----#|"
    elif number+1<1000:
        compartment += f"|    |{bed1}---#|\n"
        compartment += f"|    |        |\n"
        compartment += f"|    |{bed2}---#|"
    return compartment