-- Host: 127.0.0.1    Database: nursingHomeDB
-- ------------------------------------------------------
-- Server version       8.0.44

drop database nursingHomeDB;
create database nursingHomeDB;
use nursingHomeDB;

DROP TABLE IF EXISTS `faculty_type`;
DROP TABLE IF EXISTS `payment_system`;
DROP TABLE IF EXISTS `medication`;
DROP TABLE IF EXISTS `phone_number`;
DROP TABLE IF EXISTS `faculty`;
DROP TABLE IF EXISTS `trusted_family`;
DROP TABLE IF EXISTS `patient`;
DROP TABLE IF EXISTS `patient_room`;
DROP TABLE IF EXISTS `patient_med`;
DROP TABLE IF EXISTS `payment_summary`;
DROP TABLE IF EXISTS `assigned_room`;
DROP TABLE IF EXISTS `works_with`;


--
-- Table structure for table `faculty_type`
--
CREATE TABLE `faculty_type` (
  `facultyTypeID` INTEGER NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
  `facultyType` varchar(12) DEFAULT NULL
);

--
-- Table structure for table `payment_system`
--
CREATE TABLE `payment_system` (
  `paymentID` INTEGER NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
  `price` decimal(5, 2) NOT NULL,
  `tax` decimal(5, 2) NOT NULL
);

--
-- Table structure for table `medication`
--
CREATE TABLE `medication` (
  `medicationID` INTEGER NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
  `medicationType` varchar(20) DEFAULT NULL,
  `paymentID` INTEGER NOT NULL,
  CONSTRAINT `medication_idfk_1` FOREIGN KEY (`paymentID`) REFERENCES `payment_system` (`paymentID`)
);

--
-- Table structure for table `phone_number`
--
CREATE TABLE `phone_number` (
  `numberID` INTEGER NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
  `phoneNumber` varchar(12) DEFAULT NULL
);

--
-- Table structure for table `faculty`
--
CREATE TABLE `faculty` (
  `facultyID` INTEGER NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
  `facultyLastName` varchar(20) DEFAULT NULL,
  `facultyTypeID` INTEGER NOT NULL,
  CONSTRAINT `faculty_ibfk_1` FOREIGN KEY (`facultyTypeID`) REFERENCES `faculty_type` (`facultyTypeID`)
);

--
-- Table structure for table `trusted_family`
--
CREATE TABLE `trusted_family` (
  `familyID` INTEGER NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
  `familyLastName` varchar(20) DEFAULT NULL,
  `phoneNumberID` INTEGER DEFAULT NULL,
  CONSTRAINT `trusted_family_ibfk_1` FOREIGN KEY (`phoneNumberID`) REFERENCES `phone_number` (`numberID`)
);

--
-- Table structure for table `patient`
--
CREATE TABLE `patient` (
  `patientID` INTEGER NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
  `firstName` varchar(20) DEFAULT NULL,
  `lastName` varchar(20) DEFAULT NULL,
  `patientPriority` INTEGER DEFAULT NULL,
  `conditionDesc` varchar(100) DEFAULT NULL,
  `familyID` INTEGER DEFAULT NULL,
  CONSTRAINT `patient_ibfk_1` FOREIGN KEY (`familyID`) REFERENCES `trusted_family` (`familyID`),
  CONSTRAINT `patient_chk_1` CHECK (((`patientPriority` > 0) AND (`patientPriority` <= 5)))
);

--
-- Table structure for table `patient_room`
--
CREATE TABLE `patient_room` (
  `patientRoomID` INTEGER NOT NULL UNIQUE AUTO_INCREMENT,
  `patientRoomNumber` INTEGER NOT NULL,
  `patientID` INTEGER NOT NULL UNIQUE,
  PRIMARY KEY (`patientRoomID`,`patientID`),
  CONSTRAINT `patient_room_ibfk_1` FOREIGN KEY (`patientID`) REFERENCES `patient` (`patientID`),
  CONSTRAINT `patient_room_chk_1` CHECK ((`patientRoomNumber` > 0) AND (`patientRoomNumber` < 4000))
);

--
-- Table structure for table `patient_med`
--
CREATE TABLE `patient_med` (
  `patientMedID` INTEGER NOT NULL UNIQUE AUTO_INCREMENT,
  `patientID` INTEGER NOT NULL,
  `medicationID` INTEGER NOT NULL,
  PRIMARY KEY (`medicationID`,`patientID`),
  CONSTRAINT `patient_med_ibfk_1` FOREIGN KEY (`medicationID`) REFERENCES `medication` (`medicationID`),
  CONSTRAINT `patient_med_ibfk_2` FOREIGN KEY (`patientID`) REFERENCES `patient` (`patientID`)
);

--
-- Table structure for table `payment_summary`
--
CREATE TABLE `payment_summary` (
  `paymentSumID` INTEGER NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
  `netPayment` decimal(5, 2) DEFAULT NULL,
  `patientID` INTEGER NOT NULL,
  `paymentID` INTEGER NOT NULL,
  CONSTRAINT `payment_summary_ibfk_2` FOREIGN KEY (`patientID`) REFERENCES `patient` (`patientID`),
  CONSTRAINT `payment_summary_ibfk_1` FOREIGN KEY (`paymentID`) REFERENCES `payment_system` (`paymentID`)
);

--
-- Table structure for table `assigned_room`
--
CREATE TABLE `assigned_room` (
  `assignedRoomID` INTEGER NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
  `patientRoomID` INTEGER NOT NULL UNIQUE,
  `facultyID` INTEGER NOT NULL,
  `floorNumber` INTEGER,
  CONSTRAINT `assigned_room_ibfk_1` FOREIGN KEY (`patientRoomID`) REFERENCES `patient_room` (`patientroomID`),
  CONSTRAINT `assigned_room_chk_1` CHECK (((`floorNumber` > 0) and (`floorNumber` < 4)))
);

--
-- Table structure for table `works_with`
--
CREATE TABLE `works_with` (
  `familyID` INTEGER NOT NULL,
  `facultyID` INTEGER NOT NULL,
  `paymentSumID` INTEGER NOT NULL,
  PRIMARY KEY (`facultyID`, `familyID`),
  CONSTRAINT `works_with_ibfk_1` FOREIGN KEY (`familyID`) REFERENCES `trusted_family` (`familyID`),
  CONSTRAINT `works_with_ibfk_2` FOREIGN KEY (`facultyID`) REFERENCES `faculty` (`facultyID`),
  CONSTRAINT `works_with_ibfk_3` FOREIGN KEY (`paymentSumID`) REFERENCES `payment_summary` (`paymentSumID`)
);

-- NOTE:
-- The Auto_Increment indices start at 1...retarded, I know
-- Any attribute listed in parenthesis that contains "ID" in its name should be a selection box in the home.ejs

-- Inserting into faculty_type is for the staff included in a nursing home, so only one insert option should be available
INSERT INTO faculty_type (facultyType) 
  VALUES ('Doctor'), 
      ('Nurse');

-- Two insertions: price and tax, index will be auto
INSERT INTO payment_system (price, tax) 
  VALUES (8.51, 2.7), 
  (10.50, 1.0), 
  (4.26, 3.8), 
  (18.75, 4.2);

-- Only a new medication should be written, a selection box should be used for the paymentID
--    Many medications can have similar prices
INSERT INTO medication (medicationType, paymentID) 
  VALUES ("Advil", 1), 
  ("Metformin", 2);

-- The employees should only insert the last names... I honestly do not know if the staff a real nursing home know each other's first name
--  It's us... and definitely not because I'm uncreative
INSERT INTO faculty (facultyLastName, facultyTypeID) 
  VALUES ('Roe', 2), 
  ('Oropesa', 2), 
  ('Snyder', 2), 
  ('Ventura', 1);

-- What do the numbers mean, Mason?
INSERT INTO phone_number (phoneNumber) 
  VALUES ("912-222-2500"),
  ("777-234-9090"),
  ("912-232-6605"),
  ("658-120-0420");

-- Some families will be related to patients with different names
INSERT INTO trusted_family (familyLastName, phoneNumberID) 
  VALUES ("None", NULL),
  ("Bowers", 1),
   ("Clints", 3),
   ("Stewart", 2),
   ("Howard", 4);

-- Just fucking kill me
INSERT INTO patient (firstName, lastName, patientPriority, conditionDesc, familyID) 
  VALUES ("Ronald", "Grace", 5, "Hernia", 2),
  ("Todd", "Howard", 5, "Migraine", 3),
  ("Will", "Bowers", 3, "Dimentia", 1),
  ("Bill", "Shatner", 1, "Dimentia", 4);
  ("Lorenzo", "Ventura", 5, "Ass Infection");

-- PatientRoom to Patient is 1:1
INSERT INTO patient_room (patientRoomNumber, patientID) 
  VALUES (1132, 2),
  (2002, 1);

-- Faculty can be assigned to multiple patient rooms (ergo many patients) which will be a M:N
INSERT INTO assigned_room (patientRoomID, facultyID) 
  VALUES (2, 1),
  (1, 4);

-- This looks awful: it can lead to some repetition, therefore, the query had to be very specific
INSERT INTO patient_med (patientID, medicationID) 
  VALUES (1, 1),
   (2, 1),
   (2, 2);

-- Give me all your money
INSERT INTO payment_summary (netPayment, patientID, paymentID) 
  VALUES (0, 1, 1),
  (0, 2, 1),
  (0, 2, 2);

-- For ease, the faculty should be able to reach a trusted family of the patient
-- Although, I believe that this is worthless because you can already reach the family via the patients table
-- Unless the faculty likes the family, but hates the patient, then sure...we can include it
INSERT INTO works_with (familyID, facultyID, paymentSumID) 
  VALUES (2, 1, 2),
  (2, 2, 2),
  (1, 3, 1);