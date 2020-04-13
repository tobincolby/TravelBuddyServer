CREATE DATABASE  IF NOT EXISTS `TravelBuddyLocal` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `TravelBuddyLocal`;
-- MySQL dump 10.13  Distrib 8.0.18, for macos10.14 (x86_64)
--
-- Host: localhost    Database: TravelBuddyLocal
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `flights`
--

DROP TABLE IF EXISTS `flights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flights` (
  `flight_id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `flight_info` text NOT NULL,
  `start_date` date NOT NULL,
  PRIMARY KEY (`flight_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flights`
--

LOCK TABLES `flights` WRITE;
/*!40000 ALTER TABLE `flights` DISABLE KEYS */;
INSERT INTO `flights` VALUES (6,'tobincolby@gmail.com','\"flights\": [{\"airline\": \"Alaska Airlines\", \"departure_date\": \"2020-04-16\", \"destination\": \"Chicago O\'Hare International\", \"destination_city\": \"Chicago\", \"destination_code\": \"ORD\", \"origin\": \"Atlanta Hartsfield-Jackson\", \"origin_city\": \"Atlanta\", \"origin_code\": \"ATL\", \"price\": 61}, {\"airline\": \"Alaska Airlines\", \"departure_date\": \"2020-04-19\", \"destination\": \"Seattle / Tacoma International\", \"destination_city\": \"Seattle\", \"destination_code\": \"SEA\", \"origin\": \"Chicago O\'Hare International\", \"origin_city\": \"Chicago\", \"origin_code\": \"ORD\", \"price\": 120}, {\"airline\": \"Aeromexico (aerm)\", \"departure_date\": \"2020-04-22\", \"destination\": \"Los Angeles International\", \"destination_city\": \"Los Angeles\", \"destination_code\": \"LAX\", \"origin\": \"Seattle / Tacoma International\", \"origin_city\": \"Seattle\", \"origin_code\": \"SEA\", \"price\": 149}, {\"airline\": \"Air France\", \"departure_date\": \"2020-04-25\", \"destination\": \"Atlanta Hartsfield-Jackson\", \"destination_city\": \"Atlanta\", \"destination_code\": \"ATL\", \"origin\": \"Los Angeles International\", \"origin_city\": \"Los Angeles\", \"origin_code\": \"LAX\", \"price\": 149}], \"price\": 479, \"success\": 1','2020-04-16'),(7,'tobincolby@gmail.com','\"flights\": [{\"airline\": \"British Airways\", \"departure_date\": \"2020-04-16\", \"destination\": \"Philadelphia International\", \"destination_city\": \"Philadelphia\", \"destination_code\": \"PHL\", \"origin\": \"Atlanta Hartsfield-Jackson\", \"origin_city\": \"Atlanta\", \"origin_code\": \"ATL\", \"price\": 78}, {\"airline\": \"Alaska Airlines\", \"departure_date\": \"2020-04-19\", \"destination\": \"Seattle / Tacoma International\", \"destination_city\": \"Seattle\", \"destination_code\": \"SEA\", \"origin\": \"Philadelphia International\", \"origin_city\": \"Philadelphia\", \"origin_code\": \"PHL\", \"price\": 191}, {\"airline\": \"British Airways\", \"departure_date\": \"2020-04-22\", \"destination\": \"Dallas Fort Worth International\", \"destination_city\": \"Dallas\", \"destination_code\": \"DFW\", \"origin\": \"Seattle / Tacoma International\", \"origin_city\": \"Seattle\", \"origin_code\": \"SEA\", \"price\": 204}, {\"airline\": \"Alaska Airlines\", \"departure_date\": \"2020-04-25\", \"destination\": \"Atlanta Hartsfield-Jackson\", \"destination_city\": \"Atlanta\", \"destination_code\": \"ATL\", \"origin\": \"Dallas Fort Worth International\", \"origin_city\": \"Dallas\", \"origin_code\": \"DFW\", \"price\": 54}], \"price\": 527, \"success\": 1','2020-04-16');
/*!40000 ALTER TABLE `flights` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-12 23:30:30
