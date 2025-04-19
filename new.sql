-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: railway_reservation
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking` (
  `booking_id` int NOT NULL AUTO_INCREMENT,
  `booking_date` datetime NOT NULL,
  `booking_type` enum('Online','Counter') NOT NULL,
  `booking_status` enum('Confirmed','RAC','Waitlist') NOT NULL,
  PRIMARY KEY (`booking_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking`
--

LOCK TABLES `booking` WRITE;
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
INSERT INTO `booking` VALUES (1,'2023-05-15 10:30:00','Online','Confirmed'),(2,'2023-05-16 11:45:00','Counter','Confirmed'),(3,'2023-05-17 09:15:00','Online','RAC'),(4,'2023-05-18 14:20:00','Online','Waitlist'),(5,'2023-05-19 16:00:00','Counter','Confirmed'),(6,'2023-05-20 12:30:00','Online','Confirmed'),(7,'2023-05-21 08:45:00','Counter','Confirmed'),(8,'2023-05-22 15:15:00','Online','RAC'),(9,'2023-05-23 11:00:00','Counter','Waitlist'),(10,'2023-05-24 14:45:00','Online','Confirmed'),(11,'2023-05-25 10:20:00','Online','Confirmed'),(12,'2023-05-26 16:30:00','Counter','Confirmed'),(13,'2023-05-27 09:45:00','Online','RAC'),(14,'2023-05-28 13:20:00','Counter','Waitlist'),(15,'2023-05-29 17:00:00','Online','Confirmed'),(16,'2023-05-30 08:15:00','Counter','Confirmed'),(17,'2023-05-31 14:50:00','Online','Confirmed'),(18,'2023-06-01 11:25:00','Counter','RAC'),(19,'2023-06-02 15:40:00','Online','Waitlist'),(20,'2023-06-03 10:10:00','Counter','Confirmed');
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cancellation`
--

DROP TABLE IF EXISTS `cancellation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cancellation` (
  `cancellation_id` int NOT NULL AUTO_INCREMENT,
  `ticket_id` int DEFAULT NULL,
  `cancellation_date` datetime NOT NULL,
  `refund_amount` decimal(10,2) NOT NULL,
  `refund_status` enum('Processed','Pending','Rejected') NOT NULL,
  PRIMARY KEY (`cancellation_id`),
  KEY `ticket_id` (`ticket_id`),
  CONSTRAINT `cancellation_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`ticket_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cancellation`
--

LOCK TABLES `cancellation` WRITE;
/*!40000 ALTER TABLE `cancellation` DISABLE KEYS */;
INSERT INTO `cancellation` VALUES (1,1,'2023-05-20 12:00:00',3360.00,'Processed'),(2,3,'2023-05-21 14:30:00',1152.00,'Pending'),(3,6,'2023-05-25 15:45:00',1800.00,'Processed'),(4,8,'2023-05-28 10:20:00',768.00,'Pending'),(5,13,'2023-06-02 09:15:00',1800.00,'Processed'),(6,18,'2023-06-05 16:30:00',1040.00,'Pending');
/*!40000 ALTER TABLE `cancellation` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_cancellation` AFTER INSERT ON `cancellation` FOR EACH ROW BEGIN
    DECLARE v_train_id INT;
    DECLARE v_class_id INT;
    DECLARE v_journey_date DATE;
    DECLARE v_seat_number VARCHAR(10);
    DECLARE v_status VARCHAR(20);
    
    
    SELECT train_id, class_id, journey_date, seat_number, status
    INTO v_train_id, v_class_id, v_journey_date, v_seat_number, v_status
    FROM Ticket
    WHERE ticket_id = NEW.ticket_id;
    
    
    UPDATE Ticket
    SET status = 'Cancelled'
    WHERE ticket_id = NEW.ticket_id;
    
    
    IF v_status = 'Confirmed' AND v_seat_number IS NOT NULL THEN
        UPDATE Seat
        SET status = 'Available'
        WHERE train_id = v_train_id
          AND class_id = v_class_id
          AND journey_date = v_journey_date
          AND seat_number = v_seat_number;
          
        
        UPDATE Train_Class
        SET available_seats = available_seats + 1
        WHERE train_id = v_train_id AND class_id = v_class_id;
    END IF;
    
    
    
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class` (
  `class_id` int NOT NULL AUTO_INCREMENT,
  `class_name` varchar(50) NOT NULL,
  `base_fare_per_km` decimal(10,2) NOT NULL,
  PRIMARY KEY (`class_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT INTO `class` VALUES (1,'Sleeper',1.00),(2,'AC 3-tier',2.50),(3,'AC 2-tier',3.50),(4,'First Class',5.00),(5,'Second Sitting',0.75),(6,'AC Chair Car',2.00),(7,'Executive Class',6.00);
/*!40000 ALTER TABLE `class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `concession`
--

DROP TABLE IF EXISTS `concession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `concession` (
  `concession_id` int NOT NULL AUTO_INCREMENT,
  `concession_type` varchar(50) NOT NULL,
  `discount_percentage` decimal(5,2) NOT NULL,
  `description` text,
  PRIMARY KEY (`concession_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `concession`
--

LOCK TABLES `concession` WRITE;
/*!40000 ALTER TABLE `concession` DISABLE KEYS */;
INSERT INTO `concession` VALUES (1,'Senior Citizen (Male)',40.00,'For male passengers aged 60 and above\r'),(2,'Senior Citizen (Female)',50.00,'For female passengers aged 58 and above\r'),(3,'Student',25.00,'For students with valid ID\r'),(4,'Disabled',50.00,'For passengers with disability\r'),(5,'Armed Forces',30.00,'For armed forces personnel\r'),(6,'War Widow',75.00,'For war widows with valid proof\r'),(7,'Paramilitary Forces',30.00,'For paramilitary forces personnel\r'),(8,'Physically Challenged',50.00,'For physically challenged passengers\r'),(9,'Patients',50.00,'For patients traveling for medical treatment\r'),(10,'Press Correspondents',50.00,'For accredited press correspondents');
/*!40000 ALTER TABLE `concession` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `passenger`
--

DROP TABLE IF EXISTS `passenger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passenger` (
  `passenger_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `age` int DEFAULT NULL,
  `gender` enum('Male','Female','Other') DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `proof_type` varchar(50) DEFAULT NULL,
  `proof_number` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`passenger_id`),
  KEY `idx_passenger_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passenger`
--

LOCK TABLES `passenger` WRITE;
/*!40000 ALTER TABLE `passenger` DISABLE KEYS */;
INSERT INTO `passenger` VALUES (1,'Rahul Sharma',35,'Male','9876543210','rahul@gmail.com','Aadhar','123456789012\r'),(2,'Priya Patel',28,'Female','8765432109','priya@gmail.com','PAN','ABCDE1234F\r'),(3,'Amit Singh',65,'Male','7654321098','amit@gmail.com','Aadhar','234567890123\r'),(4,'Neha Gupta',60,'Female','6543210987','neha@gmail.com','Aadhar','345678901234\r'),(5,'Vijay Kumar',22,'Male','9432109876','vijay@gmail.com','Student ID','STU2023001\r'),(6,'Ananya Desai',45,'Female','8321098765','ananya@yahoo.com','Aadhar','456789012345\r'),(7,'Rajesh Khanna',70,'Male','7210987654','rajesh@hotmail.com','PAN','BCDEF2345G\r'),(8,'Sunita Reddy',58,'Female','6109876543','sunita@gmail.com','Aadhar','567890123456\r'),(9,'Arjun Mehta',19,'Male','5998765432','arjun@outlook.com','Student ID','STU2023002\r'),(10,'Divya Iyer',62,'Female','4887654321','divya@gmail.com','Aadhar','678901234567\r'),(11,'Karan Malhotra',40,'Male','3776543210','karan@yahoo.com','Driving License','DL0420111234567\r'),(12,'Shweta Joshi',27,'Female','2665432109','shweta@gmail.com','Aadhar','789012345678\r'),(13,'Vikram Bhat',55,'Male','1554321098','vikram@hotmail.com','PAN','CDEFG3456H\r'),(14,'Pooja Shah',63,'Female','0443210987','pooja@gmail.com','Aadhar','890123456789\r'),(15,'Rohit Verma',24,'Male','9332109876','rohit@outlook.com','Student ID','STU2023003\r'),(16,'Anjali Kapoor',59,'Female','8221098765','anjali@yahoo.com','Aadhar','901234567890\r'),(17,'Suresh Nair',68,'Male','7110987654','suresh@gmail.com','PAN','DEFGH4567I\r'),(18,'Meena Choudhary',57,'Female','6009876543','meena@hotmail.com','Aadhar','012345678901\r'),(19,'Aakash Deshmukh',21,'Male','5898765432','aakash@gmail.com','Student ID','STU2023004\r'),(20,'Kavita Srinivasan',64,'Female','4787654321','kavita@yahoo.com','Aadhar','123456789012');
/*!40000 ALTER TABLE `passenger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `passenger_concession`
--

DROP TABLE IF EXISTS `passenger_concession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passenger_concession` (
  `passenger_id` int NOT NULL,
  `concession_id` int NOT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`passenger_id`,`concession_id`),
  KEY `concession_id` (`concession_id`),
  CONSTRAINT `passenger_concession_ibfk_1` FOREIGN KEY (`passenger_id`) REFERENCES `passenger` (`passenger_id`),
  CONSTRAINT `passenger_concession_ibfk_2` FOREIGN KEY (`concession_id`) REFERENCES `concession` (`concession_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passenger_concession`
--

LOCK TABLES `passenger_concession` WRITE;
/*!40000 ALTER TABLE `passenger_concession` DISABLE KEYS */;
INSERT INTO `passenger_concession` VALUES (3,1,'2025-12-31'),(4,2,'2025-12-31'),(5,3,'2024-06-30'),(7,1,'2024-12-31'),(8,2,'2024-12-31'),(9,3,'2024-05-31'),(10,2,'2025-06-30'),(13,1,'2024-11-30'),(14,2,'2025-03-31'),(15,3,'2024-07-31'),(16,2,'2025-01-31'),(17,1,'2024-09-30'),(18,2,'2024-08-31'),(19,3,'2024-04-30'),(20,2,'2025-05-31');
/*!40000 ALTER TABLE `passenger_concession` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `ticket_id` int DEFAULT NULL,
  `payment_mode` enum('Credit Card','Debit Card','Net Banking','UPI','Cash') NOT NULL,
  `payment_amount` decimal(10,2) NOT NULL,
  `payment_date` datetime NOT NULL,
  `payment_status` enum('Success','Failed','Pending') NOT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `idx_payment_ticket` (`ticket_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`ticket_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (1,1,'Credit Card',2500.00,'2023-05-15 10:35:00','Success'),(2,2,'Cash',3500.00,'2023-05-16 11:50:00','Success'),(3,3,'Net Banking',1800.00,'2023-05-17 09:20:00','Success'),(4,4,'UPI',1200.00,'2023-05-18 14:25:00','Success'),(5,5,'Debit Card',2800.00,'2023-05-19 16:05:00','Success');
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `route`
--

DROP TABLE IF EXISTS `route`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `route` (
  `route_id` int NOT NULL AUTO_INCREMENT,
  `train_id` int DEFAULT NULL,
  `sequence_number` int NOT NULL,
  `station_id` int DEFAULT NULL,
  `arrival_time` time DEFAULT NULL,
  `departure_time` time DEFAULT NULL,
  `distance_from_source` decimal(10,2) NOT NULL,
  PRIMARY KEY (`route_id`),
  UNIQUE KEY `train_id` (`train_id`,`sequence_number`),
  KEY `station_id` (`station_id`),
  KEY `idx_route_train` (`train_id`),
  CONSTRAINT `route_ibfk_1` FOREIGN KEY (`train_id`) REFERENCES `train` (`train_id`),
  CONSTRAINT `route_ibfk_2` FOREIGN KEY (`station_id`) REFERENCES `station` (`station_id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `route`
--

LOCK TABLES `route` WRITE;
/*!40000 ALTER TABLE `route` DISABLE KEYS */;
INSERT INTO `route` VALUES (1,1,1,1,NULL,'16:00:00',0.00),(2,1,2,7,'19:30:00','19:35:00',180.00),(3,1,3,9,'05:30:00','05:35:00',800.00),(4,1,4,2,'08:30:00',NULL,1200.00),(5,2,1,2,NULL,'06:00:00',0.00),(6,2,2,16,'09:30:00','09:35:00',240.00),(7,2,3,1,'13:00:00',NULL,440.00),(8,3,1,3,NULL,'20:00:00',0.00),(9,3,2,10,'04:30:00','04:35:00',520.00),(10,3,3,4,'10:00:00',NULL,1300.00),(11,4,1,5,NULL,'08:00:00',0.00),(12,4,2,7,'12:30:00','12:35:00',350.00),(13,4,3,6,'16:00:00',NULL,560.00),(14,5,1,7,NULL,'07:00:00',0.00),(15,5,2,9,'12:00:00','12:05:00',400.00),(16,5,3,8,'16:30:00',NULL,650.00),(17,6,1,9,NULL,'09:00:00',0.00),(18,6,2,10,'14:00:00',NULL,500.00),(19,7,1,4,NULL,'15:00:00',0.00),(20,7,2,3,'22:00:00',NULL,1300.00),(21,8,1,6,NULL,'11:00:00',0.00),(22,8,2,5,'16:00:00',NULL,560.00),(23,9,1,8,NULL,'10:00:00',0.00),(24,9,2,7,'15:30:00',NULL,650.00),(25,10,1,10,NULL,'12:00:00',0.00),(26,10,2,9,'19:00:00',NULL,500.00),(27,11,1,2,NULL,'08:30:00',0.00),(28,11,2,16,'11:00:00','11:05:00',240.00),(29,11,3,8,'15:30:00',NULL,450.00),(30,12,1,2,NULL,'19:00:00',0.00),(31,12,2,9,'03:00:00','03:05:00',800.00),(32,12,3,5,'10:00:00',NULL,1500.00),(33,13,1,2,NULL,'20:00:00',0.00),(34,13,2,5,'05:00:00','05:05:00',1500.00),(35,13,3,14,'14:00:00',NULL,3000.00),(36,14,1,8,NULL,'09:00:00',0.00),(37,14,2,1,'20:00:00','20:05:00',1100.00),(38,14,3,15,'06:00:00',NULL,1800.00),(39,15,1,2,NULL,'17:00:00',0.00),(40,15,2,16,'20:30:00','20:35:00',240.00),(41,15,3,17,'23:00:00','23:05:00',400.00),(42,15,4,12,'06:00:00',NULL,1000.00),(43,16,1,7,NULL,'23:00:00',0.00),(44,16,2,1,'06:00:00',NULL,180.00),(45,17,1,4,NULL,'21:00:00',0.00),(46,17,2,18,'01:00:00','01:05:00',300.00),(47,17,3,2,'08:00:00',NULL,1300.00),(48,18,1,1,NULL,'22:00:00',0.00),(49,18,2,4,'08:00:00',NULL,1300.00),(50,19,1,7,NULL,'07:15:00',0.00),(51,19,2,1,'10:45:00',NULL,180.00),(52,20,1,6,NULL,'18:00:00',0.00),(53,20,2,1,'08:00:00',NULL,560.00);
/*!40000 ALTER TABLE `route` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule`
--

DROP TABLE IF EXISTS `schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedule` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `train_id` int DEFAULT NULL,
  `running_days` varchar(20) NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `train_id` (`train_id`),
  CONSTRAINT `schedule_ibfk_1` FOREIGN KEY (`train_id`) REFERENCES `train` (`train_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule`
--

LOCK TABLES `schedule` WRITE;
/*!40000 ALTER TABLE `schedule` DISABLE KEYS */;
INSERT INTO `schedule` VALUES (1,1,'1111111','2023-01-01','2023-12-31'),(2,2,'0111110','2023-01-01','2023-12-31'),(3,3,'1010101','2023-01-01','2023-12-31'),(4,4,'1111111','2023-01-01','2023-12-31'),(5,5,'0011001','2023-01-01','2023-12-31'),(6,6,'1111111','2023-01-01','2023-12-31'),(7,7,'1111111','2023-01-01','2023-12-31'),(8,8,'0111110','2023-01-01','2023-12-31'),(9,9,'1010101','2023-01-01','2023-12-31'),(10,10,'1111111','2023-01-01','2023-12-31'),(11,11,'1111100','2023-01-01','2023-12-31'),(12,12,'1111111','2023-01-01','2023-12-31'),(13,13,'1111111','2023-01-01','2023-12-31'),(14,14,'1111111','2023-01-01','2023-12-31'),(15,15,'1111111','2023-01-01','2023-12-31'),(16,16,'1111111','2023-01-01','2023-12-31'),(17,17,'1111111','2023-01-01','2023-12-31'),(18,18,'1111111','2023-01-01','2023-12-31'),(19,19,'1111111','2023-01-01','2023-12-31'),(20,20,'1111111','2023-01-01','2023-12-31');
/*!40000 ALTER TABLE `schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seat`
--

DROP TABLE IF EXISTS `seat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seat` (
  `seat_id` int NOT NULL AUTO_INCREMENT,
  `train_id` int DEFAULT NULL,
  `class_id` int DEFAULT NULL,
  `seat_number` varchar(10) NOT NULL,
  `journey_date` date NOT NULL,
  `status` enum('Available','Booked','RAC') NOT NULL,
  PRIMARY KEY (`seat_id`),
  UNIQUE KEY `train_id` (`train_id`,`class_id`,`seat_number`,`journey_date`),
  KEY `class_id` (`class_id`),
  KEY `idx_seat_train_class_date` (`train_id`,`class_id`,`journey_date`),
  CONSTRAINT `seat_ibfk_1` FOREIGN KEY (`train_id`) REFERENCES `train` (`train_id`),
  CONSTRAINT `seat_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `class` (`class_id`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seat`
--

LOCK TABLES `seat` WRITE;
/*!40000 ALTER TABLE `seat` DISABLE KEYS */;
INSERT INTO `seat` VALUES (1,1,3,'B2-45','2023-06-01','Booked'),(2,2,4,'A1-12','2023-06-02','Booked'),(3,5,3,'C3-22','2023-06-05','Booked'),(4,6,2,'B1-18','2023-06-06','Booked'),(5,7,4,'A2-05','2023-06-07','Booked'),(6,10,3,'C1-15','2023-06-10','Booked'),(7,11,6,'D3-22','2023-06-11','Booked'),(8,12,3,'B2-28','2023-06-12','Booked'),(9,15,3,'A1-08','2023-06-15','Booked'),(10,16,2,'B3-17','2023-06-16','Booked'),(11,17,1,'S5-42','2023-06-17','Booked'),(12,19,6,'D2-11','2023-06-19','Booked'),(13,20,1,'S7-35','2023-06-20','Booked'),(14,1,3,'B2-46','2023-06-01','Available'),(15,2,4,'A1-13','2023-06-02','Available'),(16,5,3,'C3-23','2023-06-05','Available'),(17,6,2,'B1-19','2023-06-06','Available'),(18,7,4,'A2-06','2023-06-07','Available'),(19,10,3,'C1-16','2023-06-10','Available'),(20,11,6,'D3-23','2023-06-11','Available'),(21,12,3,'B2-29','2023-06-12','Available'),(22,15,3,'A1-09','2023-06-15','Available'),(23,16,2,'B3-18','2023-06-16','Available'),(24,17,1,'S5-43','2023-06-17','Available'),(25,19,6,'D2-12','2023-06-19','Available'),(26,1,3,'B1-01','2023-06-01','Booked'),(27,1,3,'B1-02','2023-06-01','Available'),(28,1,3,'B1-03','2023-06-01','Available'),(29,1,3,'B1-04','2023-06-01','Available'),(30,1,3,'B1-05','2023-06-01','Available'),(31,1,3,'B1-06','2023-06-01','Available'),(32,1,3,'B1-07','2023-06-01','Available'),(33,1,3,'B1-08','2023-06-01','Available'),(34,1,3,'B1-09','2023-06-01','Available'),(35,1,3,'B1-10','2023-06-01','Available'),(36,1,3,'B1-11','2023-06-01','Available'),(37,1,3,'B1-12','2023-06-01','Available'),(38,1,3,'B1-13','2023-06-01','Available'),(39,1,3,'B1-14','2023-06-01','Available'),(40,1,3,'B1-15','2023-06-01','Available'),(41,1,3,'B1-16','2023-06-01','Available'),(42,1,3,'B1-17','2023-06-01','Available'),(43,1,3,'B1-18','2023-06-01','Available'),(44,1,3,'B1-19','2023-06-01','Available'),(45,1,3,'B1-20','2023-06-01','Available'),(46,1,3,'B1-21','2023-06-01','Available'),(47,1,3,'B1-22','2023-06-01','Available'),(48,1,3,'B1-23','2023-06-01','Available'),(49,1,3,'B1-24','2023-06-01','Available'),(50,1,3,'B1-25','2023-06-01','Available'),(51,1,3,'B1-26','2023-06-01','Available'),(52,1,3,'B1-27','2023-06-01','Available'),(53,1,3,'B1-28','2023-06-01','Available'),(54,1,3,'B1-29','2023-06-01','Available'),(55,1,3,'B1-30','2023-06-01','Available');
/*!40000 ALTER TABLE `seat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `station`
--

DROP TABLE IF EXISTS `station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `station` (
  `station_id` int NOT NULL AUTO_INCREMENT,
  `station_name` varchar(100) NOT NULL,
  `station_code` varchar(10) NOT NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  PRIMARY KEY (`station_id`),
  UNIQUE KEY `station_code` (`station_code`),
  KEY `idx_station_code` (`station_code`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `station`
--

LOCK TABLES `station` WRITE;
/*!40000 ALTER TABLE `station` DISABLE KEYS */;
INSERT INTO `station` VALUES (1,'Mumbai Central','MMCT','Mumbai','Maharashtra\r'),(2,'Delhi Junction','DLI','Delhi','Delhi\r'),(3,'Chennai Central','MAS','Chennai','Tamil Nadu\r'),(4,'Howrah Junction','HWH','Kolkata','West Bengal\r'),(5,'Bangalore City','SBC','Bangalore','Karnataka\r'),(6,'Ahmedabad Junction','ADI','Ahmedabad','Gujarat\r'),(7,'Pune Junction','PUNE','Pune','Maharashtra\r'),(8,'Jaipur Junction','JP','Jaipur','Rajasthan\r'),(9,'Lucknow Junction','LJN','Lucknow','Uttar Pradesh\r'),(10,'Hyderabad Deccan','HYB','Hyderabad','Telangana\r'),(11,'Secunderabad Junction','SC','Hyderabad','Telangana\r'),(12,'Patna Junction','PNBE','Patna','Bihar\r'),(13,'Guwahati','GHY','Guwahati','Assam\r'),(14,'Thiruvananthapuram Central','TVC','Thiruvananthapuram','Kerala\r'),(15,'Chhatrapati Shivaji Terminus','CSTM','Mumbai','Maharashtra\r'),(16,'Kanpur Central','CNB','Kanpur','Uttar Pradesh\r'),(17,'Allahabad Junction','ALD','Allahabad','Uttar Pradesh\r'),(18,'Varanasi Junction','BSB','Varanasi','Uttar Pradesh\r'),(19,'Bhopal Junction','BPL','Bhopal','Madhya Pradesh\r'),(20,'Indore Junction INDB','INDB','Indore','Madhya Pradesh');
/*!40000 ALTER TABLE `station` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket` (
  `ticket_id` int NOT NULL AUTO_INCREMENT,
  `pnr_number` varchar(10) NOT NULL,
  `booking_id` int DEFAULT NULL,
  `passenger_id` int DEFAULT NULL,
  `train_id` int DEFAULT NULL,
  `class_id` int DEFAULT NULL,
  `journey_date` date NOT NULL,
  `from_station_id` int DEFAULT NULL,
  `to_station_id` int DEFAULT NULL,
  `seat_number` varchar(10) DEFAULT NULL,
  `status` enum('Confirmed','RAC','Waitlist','Cancelled') NOT NULL,
  `fare` decimal(10,2) DEFAULT NULL,
  `concession_applied` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`ticket_id`),
  UNIQUE KEY `pnr_number` (`pnr_number`),
  KEY `booking_id` (`booking_id`),
  KEY `passenger_id` (`passenger_id`),
  KEY `class_id` (`class_id`),
  KEY `from_station_id` (`from_station_id`),
  KEY `to_station_id` (`to_station_id`),
  KEY `idx_ticket_pnr` (`pnr_number`),
  KEY `idx_ticket_train_journey` (`train_id`,`journey_date`),
  KEY `idx_ticket_status` (`status`),
  CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `booking` (`booking_id`),
  CONSTRAINT `ticket_ibfk_2` FOREIGN KEY (`passenger_id`) REFERENCES `passenger` (`passenger_id`),
  CONSTRAINT `ticket_ibfk_3` FOREIGN KEY (`train_id`) REFERENCES `train` (`train_id`),
  CONSTRAINT `ticket_ibfk_4` FOREIGN KEY (`class_id`) REFERENCES `class` (`class_id`),
  CONSTRAINT `ticket_ibfk_5` FOREIGN KEY (`from_station_id`) REFERENCES `station` (`station_id`),
  CONSTRAINT `ticket_ibfk_6` FOREIGN KEY (`to_station_id`) REFERENCES `station` (`station_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
INSERT INTO `ticket` VALUES (1,'PNR100001',1,1,1,3,'2023-06-01',1,2,'B2-45','Confirmed',4200.00,0.00),(2,'PNR100002',2,2,2,4,'2023-06-02',2,1,'A1-12','Confirmed',3850.00,0.00),(3,'PNR100003',3,3,3,2,'2023-06-03',3,4,NULL,'RAC',2520.00,1080.00),(4,'PNR100004',4,4,4,1,'2023-06-04',5,6,NULL,'Waitlist',840.00,560.00),(5,'PNR100005',5,5,5,3,'2023-06-05',7,8,'C3-22','Confirmed',3150.00,0.00),(6,'PNR100006',6,6,6,2,'2023-06-06',9,10,'B1-18','Confirmed',2250.00,0.00),(7,'PNR100007',7,7,7,4,'2023-06-07',4,3,'A2-05','Confirmed',4550.00,1950.00),(8,'PNR100008',8,8,8,2,'2023-06-08',6,5,NULL,'RAC',1680.00,720.00),(9,'PNR100009',9,9,9,1,'2023-06-09',8,7,NULL,'Waitlist',650.00,0.00),(10,'PNR100010',10,10,10,3,'2023-06-10',10,9,'C1-15','Confirmed',2625.00,875.00),(11,'PNR100011',11,11,11,6,'2023-06-11',2,8,'D3-22','Confirmed',1440.00,0.00),(12,'PNR100012',12,12,12,3,'2023-06-12',2,5,'B2-28','Confirmed',5250.00,0.00),(13,'PNR100013',13,13,13,2,'2023-06-13',2,14,NULL,'RAC',3750.00,1500.00),(14,'PNR100014',14,14,14,1,'2023-06-14',8,15,NULL,'Waitlist',1100.00,0.00),(15,'PNR100015',15,15,15,3,'2023-06-15',2,12,'A1-08','Confirmed',2800.00,0.00),(16,'PNR100016',16,16,16,2,'2023-06-16',7,2,'B3-17','Confirmed',1260.00,540.00),(17,'PNR100017',17,17,17,1,'2023-06-17',4,2,'S5-42','Confirmed',1300.00,0.00),(18,'PNR100018',18,18,18,1,'2023-06-18',1,4,NULL,'RAC',1300.00,0.00),(19,'PNR100019',19,19,19,6,'2023-06-19',7,1,'D2-11','Confirmed',360.00,0.00),(20,'PNR100020',20,20,20,1,'2023-06-20',6,1,'S7-35','Confirmed',560.00,0.00);
/*!40000 ALTER TABLE `ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `train`
--

DROP TABLE IF EXISTS `train`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `train` (
  `train_id` int NOT NULL AUTO_INCREMENT,
  `train_name` varchar(100) NOT NULL,
  `train_type` varchar(50) DEFAULT NULL,
  `total_seats` int DEFAULT NULL,
  `source_station_id` int DEFAULT NULL,
  `destination_station_id` int DEFAULT NULL,
  PRIMARY KEY (`train_id`),
  KEY `source_station_id` (`source_station_id`),
  KEY `destination_station_id` (`destination_station_id`),
  CONSTRAINT `train_ibfk_1` FOREIGN KEY (`source_station_id`) REFERENCES `station` (`station_id`),
  CONSTRAINT `train_ibfk_2` FOREIGN KEY (`destination_station_id`) REFERENCES `station` (`station_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `train`
--

LOCK TABLES `train` WRITE;
/*!40000 ALTER TABLE `train` DISABLE KEYS */;
INSERT INTO `train` VALUES (1,'Rajdhani Express','Superfast',500,1,2),(2,'Shatabdi Express','Superfast',400,2,1),(3,'Duronto Express','Superfast',450,3,4),(4,'Garib Rath','Express',600,5,6),(5,'Sampark Kranti','Express',550,7,8),(6,'Jan Shatabdi','Superfast',480,9,10),(7,'Vande Bharat','Superfast',300,4,3),(8,'Tejas Express','Superfast',350,6,5),(9,'Double Decker','Express',400,8,7),(10,'Humsafar Express','Superfast',500,10,9),(11,'Gatimaan Express','Superfast',250,2,8),(12,'Karnataka Express','Express',520,2,5),(13,'Kerala Express','Express',500,2,14),(14,'Goa Express','Express',480,8,15),(15,'Bhubaneswar Rajdhani','Superfast',500,2,16),(16,'Pune Duronto','Superfast',450,7,2),(17,'Howrah Mail','Express',550,4,2),(18,'Mumbai Mail','Express',550,1,4),(19,'Deccan Queen','Superfast',400,7,1),(20,'Gujarat Mail','Express',500,6,1);
/*!40000 ALTER TABLE `train` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `train_class`
--

DROP TABLE IF EXISTS `train_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `train_class` (
  `train_id` int NOT NULL,
  `class_id` int NOT NULL,
  `total_seats` int NOT NULL,
  `available_seats` int NOT NULL,
  PRIMARY KEY (`train_id`,`class_id`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `train_class_ibfk_1` FOREIGN KEY (`train_id`) REFERENCES `train` (`train_id`),
  CONSTRAINT `train_class_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `class` (`class_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `train_class`
--

LOCK TABLES `train_class` WRITE;
/*!40000 ALTER TABLE `train_class` DISABLE KEYS */;
INSERT INTO `train_class` VALUES (1,2,150,50),(1,3,100,30),(1,4,50,10),(2,3,120,40),(2,4,80,20),(3,1,200,100),(3,2,150,75),(4,1,250,150),(4,2,150,50),(5,1,200,100),(5,3,100,30),(6,2,180,90),(6,5,200,150),(7,3,100,20),(7,4,50,10),(8,2,150,50),(8,3,100,30),(9,1,200,100),(9,5,200,150),(10,2,200,100),(10,3,150,50),(11,6,150,75),(11,7,50,15),(12,1,200,120),(12,2,150,80),(12,3,100,40),(13,1,200,100),(13,2,150,75),(13,3,100,50),(14,1,200,150),(14,2,150,100),(15,2,150,60),(15,3,100,30),(15,4,50,10),(16,2,150,70),(16,3,100,40),(17,1,250,150),(17,2,150,80),(18,1,250,120),(18,2,150,90),(19,6,200,100),(20,1,250,150),(20,2,150,100);
/*!40000 ALTER TABLE `train_class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'railway_reservation'
--
/*!50003 DROP FUNCTION IF EXISTS `CalculateFare` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `CalculateFare`(
    p_passenger_id INT,
    p_train_id INT,
    p_class_id INT,
    p_from_station_id INT,
    p_to_station_id INT
) RETURNS decimal(10,2)
    DETERMINISTIC
BEGIN
    DECLARE v_distance DECIMAL(10,2);
    DECLARE v_base_fare DECIMAL(10,2);
    DECLARE v_concession DECIMAL(10,2) DEFAULT 0;
    DECLARE v_total_fare DECIMAL(10,2);
    
    
    SELECT (r2.distance_from_source - r1.distance_from_source) INTO v_distance
    FROM Route r1
    JOIN Route r2 ON r1.train_id = r2.train_id
    WHERE r1.train_id = p_train_id 
      AND r1.station_id = p_from_station_id
      AND r2.station_id = p_to_station_id;
    
    
    SELECT base_fare_per_km * v_distance INTO v_base_fare
    FROM Class
    WHERE class_id = p_class_id;
    
    
    SELECT SUM(c.discount_percentage * v_base_fare / 100) INTO v_concession
    FROM Passenger_Concession pc
    JOIN Concession c ON pc.concession_id = c.concession_id
    WHERE pc.passenger_id = p_passenger_id
      AND pc.valid_until >= CURDATE();
    
    SET v_total_fare = v_base_fare - IFNULL(v_concession, 0);
    
    RETURN v_total_fare;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `BookTicket` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `BookTicket`(
    IN p_passenger_id INT,
    IN p_train_id INT,
    IN p_class_id INT,
    IN p_journey_date DATE,
    IN p_from_station_id INT,
    IN p_to_station_id INT,
    IN p_booking_type ENUM('Online', 'Counter'),
    IN p_payment_mode ENUM('Credit Card', 'Debit Card', 'Net Banking', 'UPI', 'Cash')
)
BEGIN
    DECLARE v_fare DECIMAL(10,2);
    DECLARE v_distance DECIMAL(10,2);
    DECLARE v_available_seats INT;
    DECLARE v_booking_id INT;
    DECLARE v_pnr_number VARCHAR(10);
    DECLARE v_ticket_id INT;
    DECLARE v_seat_number VARCHAR(10);
    DECLARE v_status ENUM('Confirmed', 'RAC', 'Waitlist');
    DECLARE v_concession DECIMAL(10,2) DEFAULT 0;
    
    
    SELECT (r2.distance_from_source - r1.distance_from_source) INTO v_distance
    FROM Route r1
    JOIN Route r2 ON r1.train_id = r2.train_id
    WHERE r1.train_id = p_train_id 
      AND r1.station_id = p_from_station_id
      AND r2.station_id = p_to_station_id;
    
    
    SELECT base_fare_per_km * v_distance INTO v_fare
    FROM Class
    WHERE class_id = p_class_id;
    
    
    SELECT SUM(c.discount_percentage * v_fare / 100) INTO v_concession
    FROM Passenger_Concession pc
    JOIN Concession c ON pc.concession_id = c.concession_id
    WHERE pc.passenger_id = p_passenger_id
      AND pc.valid_until >= CURDATE();
    
    SET v_fare = v_fare - IFNULL(v_concession, 0);
    
    
    SELECT available_seats INTO v_available_seats
    FROM Train_Class
    WHERE train_id = p_train_id AND class_id = p_class_id;
    
    
    IF v_available_seats > 0 THEN
        SET v_status = 'Confirmed';
        
        
        SELECT seat_number INTO v_seat_number
        FROM Seat
        WHERE train_id = p_train_id 
          AND class_id = p_class_id
          AND journey_date = p_journey_date
          AND status = 'Available'
        LIMIT 1;
        
        
        UPDATE Seat
        SET status = 'Booked'
        WHERE train_id = p_train_id 
          AND class_id = p_class_id
          AND journey_date = p_journey_date
          AND seat_number = v_seat_number;
    ELSE
        
        SET v_status = 'RAC';
        SET v_seat_number = NULL;
    END IF;
    
    
    SET v_pnr_number = CONCAT('PNR', FLOOR(RAND() * 900000 + 100000));
    
    
    INSERT INTO Booking (booking_date, booking_type, booking_status)
    VALUES (NOW(), p_booking_type, v_status);
    
    SET v_booking_id = LAST_INSERT_ID();
    
    
    INSERT INTO Ticket (pnr_number, booking_id, passenger_id, train_id, class_id, 
                        journey_date, from_station_id, to_station_id, 
                        seat_number, status, fare, concession_applied)
    VALUES (v_pnr_number, v_booking_id, p_passenger_id, p_train_id, p_class_id,
            p_journey_date, p_from_station_id, p_to_station_id,
            v_seat_number, v_status, v_fare + IFNULL(v_concession, 0), IFNULL(v_concession, 0));
    
    SET v_ticket_id = LAST_INSERT_ID();
    
    
    INSERT INTO Payment (ticket_id, payment_mode, payment_amount, payment_date, payment_status)
    VALUES (v_ticket_id, p_payment_mode, v_fare, NOW(), 'Success');
    
    
    IF v_status = 'Confirmed' THEN
        UPDATE Train_Class
        SET available_seats = available_seats - 1
        WHERE train_id = p_train_id AND class_id = p_class_id;
    END IF;
    
    
    SELECT v_pnr_number AS pnr_number, v_status AS status;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `CalculateCancellationRefund` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `CalculateCancellationRefund`(
    IN p_train_id INT,
    IN p_cancellation_date DATE
)
BEGIN
    SELECT SUM(c.refund_amount) AS total_refund_amount
    FROM Cancellation c
    JOIN Ticket t ON c.ticket_id = t.ticket_id
    WHERE t.train_id = p_train_id 
      AND DATE(c.cancellation_date) = p_cancellation_date;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `CheckPNRStatus` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `CheckPNRStatus`(IN p_pnr_number VARCHAR(10))
BEGIN
    SELECT t.pnr_number, t.status, 
           p.name AS passenger_name, tr.train_name, 
           c.class_name, t.journey_date,
           s1.station_name AS from_station, 
           s2.station_name AS to_station,
           t.seat_number
    FROM Ticket t
    JOIN Passenger p ON t.passenger_id = p.passenger_id
    JOIN Train tr ON t.train_id = tr.train_id
    JOIN Class c ON t.class_id = c.class_id
    JOIN Station s1 ON t.from_station_id = s1.station_id
    JOIN Station s2 ON t.to_station_id = s2.station_id
    WHERE t.pnr_number = p_pnr_number;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `CheckSeatAvailability` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `CheckSeatAvailability`(
    IN p_train_id INT,
    IN p_class_id INT,
    IN p_journey_date DATE
)
BEGIN
    
    SELECT tc.available_seats AS total_available_seats
    FROM Train_Class tc
    WHERE tc.train_id = p_train_id AND tc.class_id = p_class_id;
    
    
    SELECT seat_number
    FROM Seat
    WHERE train_id = p_train_id 
      AND class_id = p_class_id 
      AND journey_date = p_journey_date
      AND status = 'Available';
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `FindBusiestRoutes` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `FindBusiestRoutes`(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    SELECT s1.station_name AS source, 
           s2.station_name AS destination,
           COUNT(*) AS passenger_count
    FROM Ticket t
    JOIN Station s1 ON t.from_station_id = s1.station_id
    JOIN Station s2 ON t.to_station_id = s2.station_id
    WHERE t.journey_date BETWEEN p_start_date AND p_end_date
      AND t.status = 'Confirmed'
    GROUP BY t.from_station_id, t.to_station_id
    ORDER BY passenger_count DESC
    LIMIT 5;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `FindTrainsBetweenStations` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `FindTrainsBetweenStations`(
    IN p_from_station_id INT,
    IN p_to_station_id INT,
    IN p_journey_date DATE
)
BEGIN
    SELECT DISTINCT t.train_id, t.train_name, t.train_type,
           (SELECT departure_time FROM Route WHERE train_id = t.train_id AND station_id = p_from_station_id) AS departure_time,
           (SELECT arrival_time FROM Route WHERE train_id = t.train_id AND station_id = p_to_station_id) AS arrival_time,
           tc.class_id, c.class_name, tc.available_seats
    FROM Train t
    JOIN Route r1 ON t.train_id = r1.train_id
    JOIN Route r2 ON t.train_id = r2.train_id
    JOIN Train_Class tc ON t.train_id = tc.train_id
    JOIN Class c ON tc.class_id = c.class_id
    WHERE r1.station_id = p_from_station_id
      AND r2.station_id = p_to_station_id
      AND r1.sequence_number < r2.sequence_number
      AND EXISTS (
          SELECT 1 FROM Schedule 
          WHERE train_id = t.train_id 
            AND (running_days LIKE CONCAT('%', DAYOFWEEK(p_journey_date)-1, '%') OR running_days = '1111111')
            AND start_date <= p_journey_date
            AND (end_date IS NULL OR end_date >= p_journey_date)
      )
    ORDER BY departure_time;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GenerateRevenueReport` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GenerateRevenueReport`(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    
    SELECT SUM(p.payment_amount) AS total_revenue
    FROM Payment p
    WHERE p.payment_date BETWEEN p_start_date AND p_end_date
      AND p.payment_status = 'Success';
    
    
    SELECT payment_mode, SUM(payment_amount) AS mode_revenue
    FROM Payment
    WHERE payment_date BETWEEN p_start_date AND p_end_date
      AND payment_status = 'Success'
    GROUP BY payment_mode;
    
    
    SELECT t.train_name, SUM(py.payment_amount) AS train_revenue
    FROM Payment py
    JOIN Ticket tk ON py.ticket_id = tk.ticket_id
    JOIN Train t ON tk.train_id = t.train_id
    WHERE py.payment_date BETWEEN p_start_date AND p_end_date
      AND py.payment_status = 'Success'
    GROUP BY t.train_id, t.train_name;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GenerateTicketBill` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GenerateTicketBill`(IN p_pnr_number VARCHAR(10))
BEGIN
    SELECT t.pnr_number, p.name AS passenger_name,
           tr.train_name, c.class_name,
           t.journey_date,
           s1.station_name AS from_station,
           s2.station_name AS to_station,
           t.fare AS base_fare,
           t.concession_applied,
           (t.fare - t.concession_applied) AS net_fare,
           py.payment_mode,
           py.payment_amount,
           py.payment_date,
           CASE 
               WHEN t.concession_applied > 0 THEN 'Yes'
               ELSE 'No'
           END AS concession_used
    FROM Ticket t
    JOIN Passenger p ON t.passenger_id = p.passenger_id
    JOIN Train tr ON t.train_id = tr.train_id
    JOIN Class c ON t.class_id = c.class_id
    JOIN Station s1 ON t.from_station_id = s1.station_id
    JOIN Station s2 ON t.to_station_id = s2.station_id
    JOIN Payment py ON t.ticket_id = py.ticket_id
    WHERE t.pnr_number = p_pnr_number;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetAverageAgePerClass` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetAverageAgePerClass`()
BEGIN
    SELECT c.class_name, AVG(p.age) AS average_age
    FROM Ticket t
    JOIN Passenger p ON t.passenger_id = p.passenger_id
    JOIN Class c ON t.class_id = c.class_id
    GROUP BY c.class_id
    ORDER BY average_age DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetCancellationRecords` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetCancellationRecords`(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    SELECT t.pnr_number, p.name AS passenger_name,
           c.cancellation_date, c.refund_amount,
           c.refund_status, tr.train_name
    FROM Cancellation c
    JOIN Ticket t ON c.ticket_id = t.ticket_id
    JOIN Passenger p ON t.passenger_id = p.passenger_id
    JOIN Train tr ON t.train_id = tr.train_id
    WHERE c.cancellation_date BETWEEN p_start_date AND p_end_date
    ORDER BY c.cancellation_date DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetConcessionEligibleWithoutApplication` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetConcessionEligibleWithoutApplication`()
BEGIN
    SELECT p.name, p.age, pc.concession_type
    FROM Passenger p
    JOIN Passenger_Concession pc ON p.passenger_id = pc.passenger_id
    LEFT JOIN Ticket t ON p.passenger_id = t.passenger_id AND t.concession_applied > 0
    WHERE t.ticket_id IS NULL;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetMostBookedClass` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetMostBookedClass`()
BEGIN
    SELECT c.class_name, COUNT(*) AS ticket_count
    FROM Ticket t
    JOIN Class c ON t.class_id = c.class_id
    WHERE t.status = 'Confirmed'
    GROUP BY c.class_id
    ORDER BY ticket_count DESC
    LIMIT 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetPassengersByTrain` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetPassengersByTrain`(
    IN p_train_id INT,
    IN p_journey_date DATE
)
BEGIN
    SELECT p.name, p.age, p.gender, 
           c.class_name, t.seat_number,
           s1.station_name AS from_station,
           s2.station_name AS to_station
    FROM Ticket t
    JOIN Passenger p ON t.passenger_id = p.passenger_id
    JOIN Class c ON t.class_id = c.class_id
    JOIN Station s1 ON t.from_station_id = s1.station_id
    JOIN Station s2 ON t.to_station_id = s2.station_id
    WHERE t.train_id = p_train_id 
      AND t.journey_date = p_journey_date
      AND t.status = 'Confirmed';
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetRevenueByPaymentMode` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetRevenueByPaymentMode`()
BEGIN
    SELECT payment_mode, SUM(payment_amount) AS total_revenue
    FROM Payment
    WHERE payment_status = 'Success'
    GROUP BY payment_mode
    ORDER BY total_revenue DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetTicketDetails` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetTicketDetails`(IN p_pnr_number VARCHAR(10))
BEGIN
    SELECT t.pnr_number, t.status, 
           p.name AS passenger_name, tr.train_name, 
           c.class_name, t.journey_date,
           s1.station_name AS from_station, 
           s2.station_name AS to_station,
           t.seat_number
    FROM Ticket t
    JOIN Passenger p ON t.passenger_id = p.passenger_id
    JOIN Train tr ON t.train_id = tr.train_id
    JOIN Class c ON t.class_id = c.class_id
    JOIN Station s1 ON t.from_station_id = s1.station_id
    JOIN Station s2 ON t.to_station_id = s2.station_id
    WHERE t.pnr_number = p_pnr_number;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetTrainCancellations` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetTrainCancellations`()
BEGIN
    SELECT t.train_name, COUNT(*) AS cancellation_count
    FROM Cancellation c
    JOIN Ticket tk ON c.ticket_id = tk.ticket_id
    JOIN Train t ON tk.train_id = t.train_id
    GROUP BY tk.train_id
    ORDER BY cancellation_count DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetTrainSchedule` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetTrainSchedule`(IN p_train_id INT)
BEGIN
    SELECT t.train_name, 
           s.station_name, 
           r.arrival_time, 
           r.departure_time, 
           r.distance_from_source
    FROM Route r
    JOIN Train t ON r.train_id = t.train_id
    JOIN Station s ON r.station_id = s.station_id
    WHERE t.train_id = p_train_id
    ORDER BY r.sequence_number;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetWaitlistedPassengers` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetWaitlistedPassengers`(
    IN p_train_id INT,
    IN p_journey_date DATE
)
BEGIN
    SELECT p.name, t.pnr_number, t.journey_date,
           s1.station_name AS from_station,
           s2.station_name AS to_station,
           b.booking_date
    FROM Ticket t
    JOIN Passenger p ON t.passenger_id = p.passenger_id
    JOIN Booking b ON t.booking_id = b.booking_id
    JOIN Station s1 ON t.from_station_id = s1.station_id
    JOIN Station s2 ON t.to_station_id = s2.station_id
    WHERE t.train_id = p_train_id 
      AND t.journey_date = p_journey_date
      AND t.status = 'Waitlist'
    ORDER BY b.booking_date;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `k` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `k`()
BEGIN
    SELECT SUM(fare) AS revenue
    FROM ticket;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `k1` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `k1`()
BEGIN
    SELECT SUM(p.payment_amount) AS revenue, p.payment_mode
    FROM payment p
    GROUP BY p.payment_mode
    ORDER BY SUM(p.payment_amount);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `p` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `p`(IN n VARCHAR(20))
BEGIN
    SELECT 
        t.pnr_number,
        t.status,
        p.name,
        tr.train_name,
        c.class_name,
        t.journey_date,
        s.station_name AS source_station,
        s1.station_name AS destination_station,
        t.seat_number
    FROM ticket t
    JOIN passenger p ON t.passenger_id = p.passenger_id
    JOIN train tr ON tr.train_id = t.train_id
    JOIN class c ON c.class_id = t.class_id
    JOIN station s ON s.station_id = t.from_station_id
    JOIN station s1 ON s1.station_id = t.to_station_id
    WHERE t.pnr_number = n;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-19 18:16:25
