BEGIN TRANSACTION;

DROP TABLE IF EXISTS "Jernbanestasjon";
CREATE TABLE IF NOT EXISTS "Jernbanestasjon" (
	"StasjonsID"	INTEGER NOT NULL,
	"Navn"	TEXT,
	"Høyde"	INTEGER,
	PRIMARY KEY("StasjonsID")
);

DROP TABLE IF EXISTS "Banestrekning";
CREATE TABLE IF NOT EXISTS "Banestrekning" (
	"BaneID"	INTEGER NOT NULL,
	"Navn"	TEXT,
	"Fremdriftsenergi"	TEXT,
	"StartStasjon"	INTEGER NOT NULL,
	"SluttStasjon"	INTEGER NOT NULL,
	FOREIGN KEY("SluttStasjon") REFERENCES "Jernbanestasjon"("StasjonsID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("StartStasjon") REFERENCES "Jernbanestasjon"("StasjonsID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("BaneID")
);

DROP TABLE IF EXISTS "MellomStasjonPåStrekning";
CREATE TABLE IF NOT EXISTS "MellomStasjonPåStrekning" (
	"BaneID"	INTEGER NOT NULL,
	"StasjonsID"	INTEGER NOT NULL,
	FOREIGN KEY("BaneID") REFERENCES "Banestrekning"("BaneID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("StasjonsID") REFERENCES "Jernbanestasjon"("StasjonsID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("BaneID","StasjonsID")
);

DROP TABLE IF EXISTS "Vogn";
CREATE TABLE IF NOT EXISTS "Vogn" (
	"VognID"	INTEGER NOT NULL,
	"Navn"	TEXT,
	PRIMARY KEY("VognID")
);

DROP TABLE IF EXISTS "SitteVogn";
CREATE TABLE IF NOT EXISTS "SitteVogn" (
	"VognID"	INTEGER NOT NULL,
	"AntallRader"	INTEGER,
	"RadBredde"	INTEGER,
	FOREIGN KEY("VognID") REFERENCES "Vogn"("VognID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("VognID")
);

DROP TABLE IF EXISTS "SoveVogn";
CREATE TABLE IF NOT EXISTS "SoveVogn" (
	"VognID"	INTEGER NOT NULL,
	"AntallKupeer"	INTEGER,
	FOREIGN KEY("VognID") REFERENCES "Vogn"("VognID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("VognID")
);

DROP TABLE IF EXISTS "Operatør";
CREATE TABLE IF NOT EXISTS "Operatør" (
	"OperatørID"	INTEGER NOT NULL,
	"Navn"	TEXT,
	PRIMARY KEY("OperatørID")
);

DROP TABLE IF EXISTS "OperatørEierVogn";
CREATE TABLE IF NOT EXISTS "OperatørEierVogn" (
	"OperatørID"	INTEGER NOT NULL,
	"VognID"	INTEGER NOT NULL,
	FOREIGN KEY("OperatørID") REFERENCES "Operatør"("OperatørID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("VognID") REFERENCES "Vogn"("VognID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("OperatørID","VognID")
);
DROP TABLE IF EXISTS "BilettPåStrekning";
CREATE TABLE IF NOT EXISTS "BilettPåStrekning" (
	"Billettnummer"	INTEGER NOT NULL,
	"DelstrekningID"	INTEGER NOT NULL,
	FOREIGN KEY("Billettnummer") REFERENCES "Billett"("Billettnummer") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("DelstrekningID") REFERENCES "Delstrekning"("DelstrekningID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("Billettnummer","DelstrekningID")
);

DROP TABLE IF EXISTS "Togruteforekomst";
CREATE TABLE IF NOT EXISTS "Togruteforekomst" (
	"ForekomstID"	INTEGER NOT NULL,
	"TogruteID"	INTEGER NOT NULL,
	"Tid"	INTEGER,
	FOREIGN KEY("TogruteID") REFERENCES "Togrute"("TogruteID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("ForekomstID","TogruteID")
);

DROP TABLE IF EXISTS "Kunde";
CREATE TABLE IF NOT EXISTS "Kunde" (
	"Kundenummer"	INTEGER NOT NULL,
	"Navn"	TEXT,
	"Epost"	TEXT UNIQUE,
	"Adresse"	TEXT,
	"Mobilnummer"	INTEGER UNIQUE,
	PRIMARY KEY("Kundenummer")
);

DROP TABLE IF EXISTS "Kundeordre";
CREATE TABLE IF NOT EXISTS "Kundeordre" (
	"Ordrenummer"	INTEGER NOT NULL,
	"Tid"	INTEGER,
	"Kundenummer"	INTEGER NOT NULL,
	FOREIGN KEY("Kundenummer") REFERENCES "Kunde"("Kundenummer") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("Ordrenummer","Kundenummer")
);

DROP TABLE IF EXISTS "Plass";
CREATE TABLE IF NOT EXISTS "Plass" (
	"PlassID"	INTEGER NOT NULL,
	"VognID"	INTEGER NOT NULL,
	FOREIGN KEY("VognID") REFERENCES "Vogn"("VognID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("PlassID","VognID")
);

DROP TABLE IF EXISTS "Delstrekning";
CREATE TABLE IF NOT EXISTS "Delstrekning" (
	"DelstrekningID"	INTEGER NOT NULL,
	"DelAvStrekning"	INTEGER NOT NULL,
	"Lengde"	INTEGER,
	"Spor"	INTEGER,
	"StartStasjon"	INTEGER NOT NULL,
	"SluttStasjon"	INTEGER NOT NULL,
	FOREIGN KEY("SluttStasjon") REFERENCES "Jernbanestasjon"("StasjonsID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("StartStasjon") REFERENCES "Jernbanestasjon"("StasjonsID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("DelAvStrekning") REFERENCES "Banestrekning"("BaneID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("DelstrekningID","DelAvStrekning")
);

DROP TABLE IF EXISTS "MellomStasjonPåTogrute";
CREATE TABLE IF NOT EXISTS "MellomStasjonPåTogrute" (
	"TogruteID"	INTEGER NOT NULL,
	"StasjonsID"	INTEGER NOT NULL,
	"Ankomsttid"	INTEGER,
	"Avganstid"	INTEGER,
	FOREIGN KEY("TogruteID") REFERENCES "Togrute"("TogruteID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("StasjonsID") REFERENCES "Jernbanestasjon"("StasjonsID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("TogruteID","StasjonsID")
);

DROP TABLE IF EXISTS "Vognoppsett";
CREATE TABLE IF NOT EXISTS "Vognoppsett" (
	"TogruteID"	INTEGER NOT NULL,
	"VognID"	INTEGER NOT NULL,
	"Rekkefølge"	INTEGER,
	FOREIGN KEY("VognID") REFERENCES "Vogn"("VognID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("TogruteID") REFERENCES "Togrute"("TogruteID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("TogruteID","VognID")
);

DROP TABLE IF EXISTS "Billett";
CREATE TABLE IF NOT EXISTS "Billett" (
	"Billettnummer"	INTEGER NOT NULL,
	"Ordrenummer"	INTEGER NOT NULL,
	"Togruteforekomst"	INTEGER NOT NULL,
	"PlassID"	INTEGER NOT NULL,
	FOREIGN KEY("Togruteforekomst") REFERENCES "Togruteforekomst"("ForekomstID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("PlassID") REFERENCES "Plass"("PlassID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("Ordrenummer") REFERENCES "Kundeordre"("Ordrenummer") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("Billettnummer")
);

DROP TABLE IF EXISTS "TogruteKjørerUkedager";
CREATE TABLE IF NOT EXISTS "TogruteKjørerUkedager" (
	"TogruteID"	INTEGER NOT NULL,
	"UkedagID"	INTEGER NOT NULL,
	FOREIGN KEY("TogruteID") REFERENCES "Togrute"("TogruteID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("UkedagID") REFERENCES "Ukedag"("UkedagID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("TogruteID","UkedagID")
);

DROP TABLE IF EXISTS "Togrute";
CREATE TABLE IF NOT EXISTS "Togrute" (
	"TogruteID"	INTEGER NOT NULL,
	"StartStasjon"	INTEGER NOT NULL,
	"Avganstid"	INTEGER,
	"SluttStasjon"	INTEGER NOT NULL,
	"Ankomsttid"	INTEGER,
	"BaneID"	INTEGER NOT NULL,
	"OperatørID"	INTEGER NOT NULL,
	FOREIGN KEY("OperatørID") REFERENCES "Operatør"("OperatørID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("StartStasjon") REFERENCES "Jernbanestasjon"("StasjonsID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("BaneID") REFERENCES "Banestrekning"("BaneID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("SluttStasjon") REFERENCES "Jernbanestasjon"("StasjonsID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("TogruteID")
);

DROP TABLE IF EXISTS "Ukedag";
CREATE TABLE IF NOT EXISTS "Ukedag" (
	"UkedagID"	INTEGER NOT NULL,
	"Navn"	TEXT,
	PRIMARY KEY("UkedagID")
);
COMMIT;
