import sqlite3


def fillDatabase():
    con = sqlite3.connect("trainstationDB.db")
    cursor = con.cursor()

    cursor.execute('INSERT INTO Trainstation VALUES (0,"Bodø",4.1)')
    cursor.execute('INSERT INTO Trainstation VALUES (1,"Fauske",34.0)')
    cursor.execute('INSERT INTO Trainstation VALUES (2,"Mo i Rana",3.5)')
    cursor.execute('INSERT INTO Trainstation VALUES (3,"Mosjøen",6.8)')
    cursor.execute('INSERT INTO Trainstation VALUES (4,"Steinkjer",3.6)')
    cursor.execute('INSERT INTO Trainstation VALUES (5,"Trondheim S",5.1)')

    cursor.execute('INSERT INTO TrackStretch VALUES (0,"Nordlandsbanen","Diesel")')

    cursor.execute("INSERT INTO PartialTrackStretch VALUES (0,0,60,1,0,1)")
    cursor.execute("INSERT INTO PartialTrackStretch VALUES (1,0,170,1,1,2)")
    cursor.execute("INSERT INTO PartialTrackStretch VALUES (2,0,90,1,2,3)")
    cursor.execute("INSERT INTO PartialTrackStretch VALUES (3,0,280,1,3,4)")
    cursor.execute("INSERT INTO PartialTrackStretch VALUES (4,0,120,2,4,5)")

    cursor.execute("INSERT INTO IntermediateStationOnTrackStretch VALUES (0,0,0)")
    cursor.execute("INSERT INTO IntermediateStationOnTrackStretch VALUES (0,1,1)")
    cursor.execute("INSERT INTO IntermediateStationOnTrackStretch VALUES (0,2,2)")
    cursor.execute("INSERT INTO IntermediateStationOnTrackStretch VALUES (0,3,3)")
    cursor.execute("INSERT INTO IntermediateStationOnTrackStretch VALUES (0,4,4)")
    cursor.execute("INSERT INTO IntermediateStationOnTrackStretch VALUES (0,5,5)")

    cursor.execute('INSERT INTO Wagon VALUES (0,"SJ-sittevogn-1")')
    cursor.execute('INSERT INTO Wagon VALUES (1,"SJ-sittevogn-1")')
    cursor.execute('INSERT INTO Wagon VALUES (2,"SJ-sovevogn-1")')
    cursor.execute('INSERT INTO Wagon VALUES (3,"SJ-sittevogn-1")')
    cursor.execute('INSERT INTO Wagon VALUES (4,"SJ-sittevogn-1")')

    cursor.execute("INSERT INTO SittingWagon VALUES (0,3,4)")
    cursor.execute("INSERT INTO SittingWagon VALUES (1,3,4)")
    cursor.execute("INSERT INTO SleepingWagon VALUES (2,4)")
    cursor.execute("INSERT INTO SittingWagon VALUES (3,3,4)")
    cursor.execute("INSERT INTO SittingWagon VALUES (4,3,4)")

    cursor.execute('INSERT INTO Operator VALUES (0,"SJ")')

    cursor.execute("INSERT INTO OperatorOwnsVagon VALUES (0,0)")
    cursor.execute("INSERT INTO OperatorOwnsVagon VALUES (0,1)")

    cursor.execute('INSERT INTO WeekDay VALUES (0,"Monday")')
    cursor.execute('INSERT INTO WeekDay VALUES (1,"Thirday")')
    cursor.execute('INSERT INTO WeekDay VALUES (2,"Wednesday")')
    cursor.execute('INSERT INTO WeekDay VALUES (3,"Tuesday")')
    cursor.execute('INSERT INTO WeekDay VALUES (4,"Friday")')
    cursor.execute('INSERT INTO WeekDay VALUES (5,"Saturday")')
    cursor.execute('INSERT INTO WeekDay VALUES (6,"Sunday")')

    cursor.execute("INSERT INTO TrainRoute VALUES (0,0,0,0)")
    cursor.execute("INSERT INTO TrainRoute VALUES (1,0,0,0)")
    cursor.execute("INSERT INTO TrainRoute VALUES (2,0,0,1)")

    cursor.execute(
        "INSERT INTO IntermediateStationOnTrainRoute VALUES (0,0,time('17:34:00'),'')"
    )
    cursor.execute(
        "INSERT INTO IntermediateStationOnTrainRoute VALUES (0,1,time('16:49:00'),time('16:49:00'))"
    )
    cursor.execute(
        "INSERT INTO IntermediateStationOnTrainRoute VALUES (0,2,time('14:31:00'),time('14:31:00'))"
    )
    cursor.execute(
        "INSERT INTO IntermediateStationOnTrainRoute VALUES (0,3,time('13:20:00'),time('13:20:00'))"
    )
    cursor.execute(
        "INSERT INTO IntermediateStationOnTrainRoute VALUES (0,4,time('09:51:00'),time('09:51:00'))"
    )
    cursor.execute(
        "INSERT INTO IntermediateStationOnTrainRoute VALUES (0,5,'',time('07:49:00'))"
    )

    cursor.execute(
        "INSERT INTO IntermediateStationOnTrainRoute VALUES (1,0,time('09:05:00'),'')"
    )
    cursor.execute(
        "INSERT INTO IntermediateStationOnTrainRoute VALUES (1,1,time('08:19:00'),time('08:19:00'))"
    )
    cursor.execute(
        "INSERT INTO IntermediateStationOnTrainRoute VALUES (1,2,time('05:55:00'),time('05:55:00'))"
    )
    cursor.execute(
        "INSERT INTO IntermediateStationOnTrainRoute VALUES (1,3,time('04:41:00'),time('04:41:00'))"
    )
    cursor.execute(
        "INSERT INTO IntermediateStationOnTrainRoute VALUES (1,4,time('00:57:00'),time('00:57:00'))"
    )
    cursor.execute(
        "INSERT INTO IntermediateStationOnTrainRoute VALUES (1,5,'',time('23:05:00'))"
    )

    cursor.execute(
        "INSERT INTO IntermediateStationOnTrainRoute VALUES (2,2,'',time('08:11:00'))"
    )
    cursor.execute(
        "INSERT INTO IntermediateStationOnTrainRoute VALUES (2,3,time('09:14:00'),time('09:14:00'))"
    )
    cursor.execute(
        "INSERT INTO IntermediateStationOnTrainRoute VALUES (2,4,time('12:31:00'),time('12:31:00'))"
    )
    cursor.execute(
        "INSERT INTO IntermediateStationOnTrainRoute VALUES (2,5,time('14:13:00'),'')"
    )

    cursor.execute("INSERT INTO WagonLayout VALUES (0,0,1)")
    cursor.execute("INSERT INTO WagonLayout VALUES (0,1,2)")
    cursor.execute("INSERT INTO WagonLayout VALUES (1,2,1)")
    cursor.execute("INSERT INTO WagonLayout VALUES (1,3,2)")
    cursor.execute("INSERT INTO WagonLayout VALUES (2,4,1)")

    cursor.execute("INSERT INTO TrainRouteRunsWeekdays VALUES (0,0)")
    cursor.execute("INSERT INTO TrainRouteRunsWeekdays VALUES (0,1)")
    cursor.execute("INSERT INTO TrainRouteRunsWeekdays VALUES (0,2)")
    cursor.execute("INSERT INTO TrainRouteRunsWeekdays VALUES (0,3)")
    cursor.execute("INSERT INTO TrainRouteRunsWeekdays VALUES (0,4)")
    cursor.execute("INSERT INTO TrainRouteRunsWeekdays VALUES (1,0)")
    cursor.execute("INSERT INTO TrainRouteRunsWeekdays VALUES (1,1)")
    cursor.execute("INSERT INTO TrainRouteRunsWeekdays VALUES (1,2)")
    cursor.execute("INSERT INTO TrainRouteRunsWeekdays VALUES (1,3)")
    cursor.execute("INSERT INTO TrainRouteRunsWeekdays VALUES (1,4)")
    cursor.execute("INSERT INTO TrainRouteRunsWeekdays VALUES (1,5)")
    cursor.execute("INSERT INTO TrainRouteRunsWeekdays VALUES (1,6)")
    cursor.execute("INSERT INTO TrainRouteRunsWeekdays VALUES (2,0)")
    cursor.execute("INSERT INTO TrainRouteRunsWeekdays VALUES (2,1)")
    cursor.execute("INSERT INTO TrainRouteRunsWeekdays VALUES (2,2)")
    cursor.execute("INSERT INTO TrainRouteRunsWeekdays VALUES (2,3)")
    cursor.execute("INSERT INTO TrainRouteRunsWeekdays VALUES (2,4)")

    cursor.execute("INSERT INTO TrainRouteInstance VALUES (0, 0, date('2023-04-03'))")
    cursor.execute("INSERT INTO TrainRouteInstance VALUES (1, 0, date('2023-04-04'))")
    cursor.execute("INSERT INTO TrainRouteInstance VALUES (2, 1, date('2023-04-03'))")
    cursor.execute("INSERT INTO TrainRouteInstance VALUES (3, 1, date('2023-04-04'))")
    cursor.execute("INSERT INTO TrainRouteInstance VALUES (4, 2, date('2023-04-03'))")
    cursor.execute("INSERT INTO TrainRouteInstance VALUES (5, 2, date('2023-04-04'))")




    cursor.execute(
        'INSERT INTO Customer VALUES(0, "Per", "per@gmail.com", "Høgskoleringen 1, 7034 Trondheim", 88888888)'
    )

    ## Script for adding the PassengerPlaces for all trainrouteinstances
    cursor.execute('SELECT InstanceID, TrainRouteID FROM TrainRouteInstance')
    trainrouteInstances = cursor.fetchall()
    wagonForInstance = []
    for instance in trainrouteInstances:
        getWagonType = ["""
        SELECT wl.WagonID, st.NumberOfRows, st.RowWidth, sl.NumberOfCompartments FROM TrainRoute tr 
        INNER JOIN WagonLayout wl ON tr.TrainRouteID = wl.TrainRouteID 
            LEFT JOIN SittingWagon st ON wl.WagonID = st.WagonID
            left join SleepingWagon sl on wl.WagonID = sl.WagonID
            WHERE tr.TrainRouteID = ? ORDER BY wl.Sequence  
        """, [instance[1]]]    
        cursor.execute(getWagonType[0],getWagonType[1])
        wagonTypes = cursor.fetchall()

        wagonForInstance.append([instance[0],wagonTypes])

    for wagInst in wagonForInstance:
        i = 1
        for wagon in wagInst[1]:
            if wagon[3] == None:
                numOfPlaces = wagon[1]*wagon[2]
                for j in range(numOfPlaces):
                    cursor.execute('INSERT INTO PassengerPlace VALUES(?,?,?)',[i,wagon[0],wagInst[0]])
                    i+=1
            else:
                numOfPlaces = wagon[3]*2
                for j in range(numOfPlaces):
                    cursor.execute('INSERT INTO PassengerPlace VALUES(?,?,?)',[i,wagon[0],wagInst[0]])
                    i+=1
                    

    con.commit()
    con.close()
