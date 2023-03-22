import sqlite3


def createDatabase():
    con = sqlite3.connect("trainstationDB.db")
    cursor = con.cursor()

    cursor.execute("""PRAGMA encoding = "UTF-8" """)

    cursor.execute(
        """CREATE TABLE Trainstation(
    StationsID INTEGER NOT NULL,
    Name TEXT NOT NULL,
    Height INTEGER,
    CONSTRAINT Trainstation_PK PRIMARY KEY (StationsID)
    )"""
    )

    cursor.execute(
        """CREATE TABLE TrackStretch(
    TrackID INTEGER NOT NULL,
    Name TEXT NOT NULL,
    PropulsionEnergy TEXT,
    StartStation INTEGER NOT NULL,
    EndStation INTEGER NOT NULL,
    CONSTRAINT TrackStretch_PK PRIMARY KEY (TrackID),
    CONSTRAINT TrackStretch_FK FOREIGN KEY (StartStation) REFERENCES Trainstation(StationsID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    CONSTRAINT TrackStretch_FK FOREIGN KEY (EndStation) REFERENCES Trainstation(StationsID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
    )"""
    )

    cursor.execute(
        """CREATE TABLE IntermediateStationOnTrackStretch(
    TrackID INTEGER NOT NULL,
    StationsID INTEGER NOT NULL,
    CONSTRAINT IntermediateStationOnTrackStretch_PK PRIMARY KEY (TrackID, StationsID),
    CONSTRAINT IntermediateStationOnTrackStretch_FK1 FOREIGN KEY (TrackID) REFERENCES TrackStretch(TrackID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    CONSTRAINT IntermediateStationOnTrackStretch_FK2 FOREIGN KEY (StationsID) REFERENCES Trainstation(StationsID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
    )"""
    )

    cursor.execute(
        """CREATE TABLE IntermediateStationOnTrainRoute(
    TrainRouteID INTEGER NOT NULL,
    StationsID INTEGER NOT NULL,
    ArrivalTime INTEGER,
    DepartureTime INTEGER,
    CONSTRAINT IntermediateStationOnTrainRoute_PK PRIMARY KEY (TrainRouteID, StationsID),
    CONSTRAINT IntermediateStationOnTrainRoute_FK1 FOREIGN KEY (TrainRouteID) REFERENCES TrainRoute(TrainRouteID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    CONSTRAINT IntermediateStationOnTrainRoute_FK2 FOREIGN KEY (StationsID) REFERENCES Trainstation(StationsID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
    )"""
    )

    cursor.execute(
        """CREATE TABLE Wagon(
    WagonID INTEGER NOT NULL,
    Name TEXT NOT NULL,
    CONSTRAINT Wagon_PK PRIMARY KEY (WagonID)
    )"""
    )

    cursor.execute(
        """CREATE TABLE SittingWagon(
    WagonID INTEGER NOT NULL,
    NumberOfRows INTEGER,
    RowWidth INTEGER,
    CONSTRAINT SittingWagon_PK PRIMARY KEY (WagonID),
    CONSTRAINT SittingWagon_FK FOREIGN KEY (WagonID) REFERENCES Wagon(WagonID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
    )"""
    )

    cursor.execute(
        """CREATE TABLE SleepingWagon(
    WagonID INTEGER NOT NULL,
    NumberOfCompartments INTEGER,
    CONSTRAINT SleepingWagon_PK PRIMARY KEY (WagonID),
    CONSTRAINT SleepingWagon_FK FOREIGN KEY (WagonID) REFERENCES Wagon(WagonID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
    )"""
    )

    cursor.execute(
        """CREATE TABLE Operator(
    OperatorID INTEGER NOT NULL,
    Name TEXT NOT NULL,
    CONSTRAINT Operator_PK PRIMARY KEY (OperatorID)
    )"""
    )

    cursor.execute(
        """CREATE TABLE OperatorOwnsVagon(
    OperatorID INTEGER NOT NULL,
    WagonID INTEGER NOT NULL,
    CONSTRAINT OperatorOwnsVagon_PK PRIMARY KEY (OperatorID, WagonID),
    CONSTRAINT OperatorOwnsVagon_FK1 FOREIGN KEY (OperatorID) REFERENCES Operator(OperatorID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    CONSTRAINT OperatorOwnsVagon_FK2 FOREIGN KEY (WagonID) REFERENCES Wagon(WagonID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
    )"""
    )

    cursor.execute(
        """CREATE TABLE TrainRoute(
    TrainRouteID INTEGER NOT NULL,
    StartStation INTEGER NOT NULL,
    EndStation INTEGER NOT NULL,
    DepartureTime INTEGER,
    Arrival time INTEGER,
    TrackID INTEGER NOT NULL,
    OperatorID INTEGER NOT NULL,
    CONSTRAINT TrainRoute_PK PRIMARY KEY (TrainRouteID),
    CONSTRAINT TrainRoute_FK1 FOREIGN KEY (StartStation) REFERENCES Trainstation(StartStation)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    CONSTRAINT TrainRoute_FK2 FOREIGN KEY (EndStation) REFERENCES Trainstation(EndStation)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    CONSTRAINT TrainRoute_FK3 FOREIGN KEY (TrackID) REFERENCES TrackStretch(TrackID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    CONSTRAINT TrainRoute_FK4 FOREIGN KEY (OperatorID) REFERENCES Operator(OperatorID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
    )"""
    )

    cursor.execute(
        """CREATE TABLE WeekDay(
    WeekDayID INTEGER NOT NULL,
    Name TEXT NOT NULL,
    CONSTRAINT WeekDay_PK PRIMARY KEY (WeekDayID)
    )"""
    )

    cursor.execute(
        """CREATE TABLE TrainRouteRunsWeekdays(
    TrainRouteID INTEGER NOT NULL,
    WeekDayID INTEGER NOT NULL,
    CONSTRAINT TrainRouteRunsWeekdays_PK PRIMARY KEY (TrainRouteID, WeekDayID),
    CONSTRAINT TrainRouteRunsWeekdays_FK1 FOREIGN KEY (TrainRouteID) REFERENCES TrainRoute(TrainRouteID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    CONSTRAINT TrainRouteRunsWeekdays_FK2 FOREIGN KEY (WeekDayID) REFERENCES WeekDay(WeekDayID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
    )"""
    )

    cursor.execute(
        """CREATE TABLE PassengerPlace(
    PassengerPlaceID INTEGER NOT NULL,
    WagonID INTEGER NOT NULL,
    CONSTRAINT PassengerPlace_PK PRIMARY KEY (PassengerPlaceID, WagonID),
    CONSTRAINT PassengerPlace_FK FOREIGN KEY (WagonID) REFERENCES Wagon(WagonID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
    )"""
    )
    cursor.execute(
        """CREATE TABLE Customer(
    CustomerNumber INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Email TEXT UNIQUE,
    Address TEXT NOT NULL,
    TelephoneNumber INTEGER UNIQUE
    )"""
    )

    cursor.execute(
        """CREATE TABLE CustomerOrder(
    OrderNumber INTEGER NOT NULL,
    Time INTEGER,
    CustomerNumber INTEGER NOT NULL,
    CONSTRAINT CustomerOrder_PK PRIMARY KEY (OrderNumber, CustomerNumber),
    CONSTRAINT CustomerOrder_FK FOREIGN KEY (CustomerNumber) REFERENCES Customer(CustomerNumber)
    ON UPDATE CASCADE
    ON DELETE CASCADE
    )"""
    )

    cursor.execute(
        """CREATE TABLE TrainRouteInstance(
    InstanceID INTEGER NOT NULL,
    TrainRouteID INTEGER NOT NULL,
    Time INTEGER,
    CONSTRAINT TrainRouteInstance_PK PRIMARY KEY (InstanceID, TrainRouteID),
    CONSTRAINT TrainRouteInstance_FK FOREIGN KEY (TrainRouteID) REFERENCES TrainRoute(TrainRouteID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
    )"""
    )

    cursor.execute(
        """CREATE TABLE Ticket(
    TicketID INTEGER NOT NULL,
    OrderNumber INTEGER NOT NULL,
    InstanceID INTEGER NOT NULL,
    PassengerPlaceID INTEGER NOT NULL,
    CONSTRAINT Ticket_PK PRIMARY KEY (TicketID),
    CONSTRAINT Ticket_FK1 FOREIGN KEY (OrderNumber) REFERENCES CustomerOrder(OrderNumber)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    CONSTRAINT Ticket_FK2 FOREIGN KEY (InstanceID) REFERENCES TrainRouteInstance(InstanceID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    CONSTRAINT Ticket_FK3 FOREIGN KEY (PassengerPlaceID) REFERENCES PassengerPlace(PassengerPlaceID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
    )"""
    )

    cursor.execute(
        """CREATE TABLE WagonLayout(
    TrainRouteID INTEGER NOT NULL,
    WagonID INTEGER NOT NULL,
    Sequence INTEGER,
    CONSTRAINT WagonLayout_PK PRIMARY KEY (TrainRouteID, Sequence),
    CONSTRAINT WagonLayout_FK1 FOREIGN KEY (TrainRouteID) REFERENCES TrainRoute(TrainRouteID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    CONSTRAINT WagonLayout_FK2 FOREIGN KEY (WagonID) REFERENCES Wagon(WagonID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
    )"""
    )

    cursor.execute(
        """CREATE TABLE PartialTrackStretch(
    PartialTrackStretchID INTEGER NOT NULL,
    PartOfTrackStretch INTEGER NOT NULL,
    Length INTEGER,
    Track INTEGER,
    StartStation INTEGER NOT NULL,
	  EndStation INTEGER NOT NULL,
    CONSTRAINT PartialTrackStretch_PK PRIMARY KEY (PartialTrackStretchID, PartOfTrackStretch),
    CONSTRAINT PartialTrackStretch_FK1 FOREIGN KEY (StartStation) REFERENCES Trainstation(StartStation)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    CONSTRAINT PartialTrackStretch_FK2 FOREIGN KEY (EndStation) REFERENCES Trainstation(EndStation)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    CONSTRAINT PartialTrackStretch_FK3 FOREIGN KEY (PartOfTrackStretch) REFERENCES TrackStretch(PartOfTrackStretch)
    ON UPDATE CASCADE
    ON DELETE CASCADE
    )"""
    )

    cursor.execute(
        """CREATE TABLE TicketOnPartialTrackStretch(
    TicketID INTEGER NOT NULL,
    PartialTrackStretchID INTEGER NOT NULL,
    CONSTRAINT TicketOnPartialTrackStretch_PK PRIMARY KEY (TicketID, PartialTrackStretchID),
    CONSTRAINT TicketOnPartialTrackStretch_FK1 FOREIGN KEY (TicketID) REFERENCES Ticket(TicketID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    CONSTRAINT TicketOnPartialTrackStretch_FK2 FOREIGN KEY (PartialTrackStretchID) REFERENCES PartialTrackStretch(PartialTrackStretchID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
    )"""
    )

    con.commit()
    con.close()
