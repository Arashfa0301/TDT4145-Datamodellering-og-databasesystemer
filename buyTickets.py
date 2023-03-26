import sqlite3
from prettytable import PrettyTable
from datetime import datetime

con = sqlite3.connect("trainstationDB.db")
cursor = con.cursor()
loggedInUser = None


def executeCursorSelect(sql, parameters):
    cursor.execute(sql, parameters)
    return cursor.fetchall()

def buyTickets(InstanceID, TrainRouteID, loggedInUser, startStation, endStation):
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
        
        # FindPartialTrackStretch
        partialTrackStretchIDs = findPartialTrackStretch(startStation,endStation,TrainRouteID)
    
        nonAvailableSeatsPerWagon = []
        # TODO: This needs to be changed

        ## Her henter du alle, hvis den er inne i her
        tempNon = []
        for partialTrackStretchID in partialTrackStretchIDs:
            navSQuery = ["""SELECT t.PassengerPlaceID FROM Ticket t 
                        INNER JOIN TicketOnPartialTrackStretch tp ON t.TicketID = tp.TicketID
                        WHERE tp.PartialTrackStretchID = ?
                        """,[partialTrackStretchID]]
            tempNon.append(executeCursorSelect(navSQuery[0],navSQuery[1]))   

        for seatInstances in tempNon:
            for seat in seatInstances:
                nonAvailableSeatsPerWagon.append(seat[0])

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
            printWagon(1, int(chosenWagon[3]),0,nonAvailableSeatsPerWagon,firstSeat[0][0])
        else:
            printWagon(0,int(chosenWagon[1]),int(chosenWagon[2]),nonAvailableSeatsPerWagon,firstSeat[0][0])
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
        
        # TODO: Insert into ticket on partial track stretch
        for ticket in tickets:
            cursor.execute("INSERT INTO Ticket (OrderNumber, InstanceID, PassengerPlaceID) VALUES(?,?,?)",[booking[0],InstanceID,ticket])
            cursor.execute("SELECT TicketID FROM Ticket WHERE OrderNumber = ? AND InstanceID = ? AND PassengerPlaceID = ?",[booking[0],InstanceID,ticket])
            ticketID = cursor.fetchall()
            for partialTrackStretchID in partialTrackStretchIDs:
                cursor.execute("INSERT INTO TicketOnPartialTrackStretch VALUES (?,?)",[ticketID[0][0],partialTrackStretchID])
    except Exception as error:
        print("""
        Something went wrong, you might have inputted something illegal.
        You can try again if you want to.
        """)
        return 0
    con.commit()
    print("Booking confirmed.")


def findPartialTrackStretch(startStation, endStation,TrainRouteID):
    # Sjekk hovedretning, hvis den er med trackstretch finn start = start, deretter end = start
    # Hvis mot hovedretning, bruk start = end, deretter end = end
    # iterer til du finner end = start, så legger du til alle imellom i en liste og returnerer det.
    # Select hvor du finner en partial track stretch med startstasjon, for loop som finner endStation

    partTrackStretches = executeCursorSelect("SELECT * FROM PartialTrackStretch",[])
    
    startStationID = executeCursorSelect("SELECT StationsID FROM Trainstation WHERE Name = ?",[startStation])[0][0]

    endStationID = executeCursorSelect("SELECT StationsID FROM Trainstation WHERE Name = ?",[endStation])[0][0]

    direction = executeCursorSelect("SELECT MainDirection FROM TrainRoute WHERE TrainRouteID = ?", [TrainRouteID])[0][0]

    # When it does go with maindirection
    partOfTrackIDs = []
    if direction == 1:
        partTrackStretches.sort(key=lambda x:x[5])
        for partTrack in partTrackStretches:
            if startStationID == partTrack[4]:
                partOfTrackIDs.append(partTrack[0])
            elif not len(partOfTrackIDs) == 0:
                if endStationID == partTrack[4]:
                    break
                else:
                    partOfTrackIDs.append(partTrack[0])

    #When it doesn't
    elif direction == 0:
        partTrackStretches.sort(reverse=True, key=lambda x:x[5])
        for partTrack in partTrackStretches:
            if startStationID == partTrack[5]:
                partOfTrackIDs.append(partTrack[0])
            elif not len(partOfTrackIDs) == 0:
                if endStationID == partTrack[5]:
                    break
                else:
                    partOfTrackIDs.append(partTrack[0])

    return partOfTrackIDs
        
        

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