import sqlite3
from prettytable import PrettyTable

con = sqlite3.connect("trainstationDB.db")
cursor = con.cursor()
loggedInUser = None


def executeCursorSelect(sql, parameters):
    cursor.execute(sql, parameters)
    return cursor.fetchall()

def buyTickets(TrainRouteInstance):
    testRoute = 0


    # Vogner på en rute
    getAvailableSeatsQuery = """
    SELECT wl.WagonID FROM TrainRoute tr INNER JOIN WagonLayout wl ON tr.TrainRouteID = wl.TrainRouteID WHERE tr.TrainRouteID = 1 ORDER BY wl.Sequence
    """
    getShit = """
    SELECT wl.WagonID, st.NumberOfRows, st.RowWidth, sl.NumberOfCompartments FROM TrainRoute tr 
    INNER JOIN WagonLayout wl ON tr.TrainRouteID = wl.TrainRouteID 
        LEFT JOIN SittingWagon st ON wl.WagonID = st.WagonID
        left join SleepingWagon sl on wl.WagonID = sl.WagonID
        WHERE tr.TrainRouteID = 0 ORDER BY wl.Sequence  
    """
    ## Men får med null verdier, kan bruke case for å hindre det.
    triQuery = ["SELECT * FROM TrainRouteInstance",[]]
    result = executeCursorSelect(triQuery[0],triQuery[1])

    query = """INSERT INTO Ticket (OrderNumber, InstanceID) VALUES (2,0)"""
    #actual_shit = executeCursorSelect("SELECT * FROM Ticket",[])
    for i in result:
        print(i)





# Print a wagon with available seats (by ID)
def printWagon(type, numRowsOrCol, rowWidth, availableSeats, startIDWagon):
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
                if k in availableSeats:
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
        for i in range(numRowsOrCol):
            if k in availableSeats:
                comp = compartmentPrinter(k)
                print(comp)
                print("|    |———————|")
            else:
                comp = ""
                comp += f"|    |X-----#|\n"
                comp += f"|   X|       |\n"
                comp += f"|    |X-----#|"
                print(comp)
        print(" ------------ ")

# Help function to print compartments
def compartmentPrinter(number):
    bed1 = number*2 - 1
    bed2 = number*2
    compartment = ""
    if number < 5:
        compartment += f"|    |{bed1}-----#|\n"
        compartment += f"|   {number}|       |\n"
        compartment += f"|    |{bed2}-----#|"
    elif number==5:
        compartment += f"|    |{bed1}-----#|\n"
        compartment += f"|   {number}|       |\n"
        compartment += f"|    |{bed2}----#|"
    elif number<10:
        compartment += f"|    |{bed1}----#|\n"
        compartment += f"|  {number}|       |\n"
        compartment += f"|    |{bed2}----#|"
    elif number<50:
        compartment += f"|    |{bed1}----#|\n"
        compartment += f"| {number}|       |\n"
        compartment += f"|    |{bed2}----#|"
    return compartment