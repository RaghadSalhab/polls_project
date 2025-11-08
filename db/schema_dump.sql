-- MySQL dump 10.13  Distrib 8.0.44, for Linux (x86_64)
--
-- Host: localhost    Database: dev_db
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `addresses`
--

DROP TABLE IF EXISTS `addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addresses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `street` varchar(100) DEFAULT NULL,
  `city_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `city_id` (`city_id`),
  CONSTRAINT `addresses_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `cities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cars`
--

DROP TABLE IF EXISTS `cars`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cars` (
  `id` int NOT NULL AUTO_INCREMENT,
  `model` varchar(100) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cities`
--

DROP TABLE IF EXISTS `cities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `population` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `companies`
--

DROP TABLE IF EXISTS `companies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `companies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `founded_year` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `salary` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `flight_passengers`
--

DROP TABLE IF EXISTS `flight_passengers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight_passengers` (
  `flight_id` int NOT NULL,
  `passenger_id` int NOT NULL,
  PRIMARY KEY (`flight_id`,`passenger_id`),
  KEY `passenger_id` (`passenger_id`),
  CONSTRAINT `flight_passengers_ibfk_1` FOREIGN KEY (`flight_id`) REFERENCES `flights` (`id`),
  CONSTRAINT `flight_passengers_ibfk_2` FOREIGN KEY (`passenger_id`) REFERENCES `passengers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `flights`
--

DROP TABLE IF EXISTS `flights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flights` (
  `id` int NOT NULL AUTO_INCREMENT,
  `flight_no` varchar(20) DEFAULT NULL,
  `origin` varchar(100) DEFAULT NULL,
  `destination` varchar(100) DEFAULT NULL,
  `departure_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int DEFAULT NULL,
  `order_date` date DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `owners`
--

DROP TABLE IF EXISTS `owners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `owners` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `car_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `car_id` (`car_id`),
  CONSTRAINT `owners_ibfk_1` FOREIGN KEY (`car_id`) REFERENCES `cars` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `passengers`
--

DROP TABLE IF EXISTS `passengers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passengers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `passport_no` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `stock` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `company_id` int DEFAULT NULL,
  `budget` decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `company_id` (`company_id`),
  CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `university_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `university_id` (`university_id`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_1`
--

DROP TABLE IF EXISTS `table_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_10`
--

DROP TABLE IF EXISTS `table_10`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_10` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_100`
--

DROP TABLE IF EXISTS `table_100`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_100` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_11`
--

DROP TABLE IF EXISTS `table_11`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_11` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_12`
--

DROP TABLE IF EXISTS `table_12`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_12` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_13`
--

DROP TABLE IF EXISTS `table_13`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_13` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_14`
--

DROP TABLE IF EXISTS `table_14`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_14` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_15`
--

DROP TABLE IF EXISTS `table_15`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_15` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_16`
--

DROP TABLE IF EXISTS `table_16`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_16` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_17`
--

DROP TABLE IF EXISTS `table_17`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_17` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_18`
--

DROP TABLE IF EXISTS `table_18`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_18` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_19`
--

DROP TABLE IF EXISTS `table_19`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_19` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_2`
--

DROP TABLE IF EXISTS `table_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_2` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_20`
--

DROP TABLE IF EXISTS `table_20`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_20` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_21`
--

DROP TABLE IF EXISTS `table_21`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_21` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_22`
--

DROP TABLE IF EXISTS `table_22`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_22` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_23`
--

DROP TABLE IF EXISTS `table_23`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_23` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_24`
--

DROP TABLE IF EXISTS `table_24`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_24` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_25`
--

DROP TABLE IF EXISTS `table_25`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_25` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_26`
--

DROP TABLE IF EXISTS `table_26`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_26` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_27`
--

DROP TABLE IF EXISTS `table_27`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_27` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_28`
--

DROP TABLE IF EXISTS `table_28`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_28` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_29`
--

DROP TABLE IF EXISTS `table_29`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_29` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_3`
--

DROP TABLE IF EXISTS `table_3`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_3` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_30`
--

DROP TABLE IF EXISTS `table_30`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_30` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_31`
--

DROP TABLE IF EXISTS `table_31`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_31` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_32`
--

DROP TABLE IF EXISTS `table_32`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_32` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_33`
--

DROP TABLE IF EXISTS `table_33`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_33` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_34`
--

DROP TABLE IF EXISTS `table_34`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_34` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_35`
--

DROP TABLE IF EXISTS `table_35`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_35` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_36`
--

DROP TABLE IF EXISTS `table_36`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_36` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_37`
--

DROP TABLE IF EXISTS `table_37`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_37` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_38`
--

DROP TABLE IF EXISTS `table_38`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_38` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_39`
--

DROP TABLE IF EXISTS `table_39`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_39` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_4`
--

DROP TABLE IF EXISTS `table_4`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_4` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_40`
--

DROP TABLE IF EXISTS `table_40`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_40` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_41`
--

DROP TABLE IF EXISTS `table_41`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_41` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_42`
--

DROP TABLE IF EXISTS `table_42`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_42` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_43`
--

DROP TABLE IF EXISTS `table_43`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_43` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_44`
--

DROP TABLE IF EXISTS `table_44`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_44` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_45`
--

DROP TABLE IF EXISTS `table_45`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_45` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_46`
--

DROP TABLE IF EXISTS `table_46`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_46` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_47`
--

DROP TABLE IF EXISTS `table_47`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_47` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_48`
--

DROP TABLE IF EXISTS `table_48`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_48` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_49`
--

DROP TABLE IF EXISTS `table_49`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_49` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_5`
--

DROP TABLE IF EXISTS `table_5`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_5` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_50`
--

DROP TABLE IF EXISTS `table_50`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_50` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_51`
--

DROP TABLE IF EXISTS `table_51`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_51` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_52`
--

DROP TABLE IF EXISTS `table_52`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_52` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_53`
--

DROP TABLE IF EXISTS `table_53`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_53` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_54`
--

DROP TABLE IF EXISTS `table_54`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_54` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_55`
--

DROP TABLE IF EXISTS `table_55`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_55` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_56`
--

DROP TABLE IF EXISTS `table_56`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_56` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_57`
--

DROP TABLE IF EXISTS `table_57`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_57` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_58`
--

DROP TABLE IF EXISTS `table_58`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_58` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_59`
--

DROP TABLE IF EXISTS `table_59`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_59` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_6`
--

DROP TABLE IF EXISTS `table_6`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_6` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_60`
--

DROP TABLE IF EXISTS `table_60`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_60` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_61`
--

DROP TABLE IF EXISTS `table_61`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_61` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_62`
--

DROP TABLE IF EXISTS `table_62`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_62` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_63`
--

DROP TABLE IF EXISTS `table_63`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_63` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_64`
--

DROP TABLE IF EXISTS `table_64`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_64` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_65`
--

DROP TABLE IF EXISTS `table_65`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_65` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_66`
--

DROP TABLE IF EXISTS `table_66`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_66` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_67`
--

DROP TABLE IF EXISTS `table_67`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_67` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_68`
--

DROP TABLE IF EXISTS `table_68`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_68` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_69`
--

DROP TABLE IF EXISTS `table_69`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_69` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_7`
--

DROP TABLE IF EXISTS `table_7`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_7` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_70`
--

DROP TABLE IF EXISTS `table_70`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_70` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_71`
--

DROP TABLE IF EXISTS `table_71`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_71` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_72`
--

DROP TABLE IF EXISTS `table_72`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_72` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_73`
--

DROP TABLE IF EXISTS `table_73`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_73` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_74`
--

DROP TABLE IF EXISTS `table_74`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_74` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_75`
--

DROP TABLE IF EXISTS `table_75`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_75` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_76`
--

DROP TABLE IF EXISTS `table_76`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_76` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_77`
--

DROP TABLE IF EXISTS `table_77`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_77` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_78`
--

DROP TABLE IF EXISTS `table_78`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_78` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_79`
--

DROP TABLE IF EXISTS `table_79`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_79` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_8`
--

DROP TABLE IF EXISTS `table_8`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_8` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_80`
--

DROP TABLE IF EXISTS `table_80`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_80` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_81`
--

DROP TABLE IF EXISTS `table_81`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_81` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_82`
--

DROP TABLE IF EXISTS `table_82`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_82` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_83`
--

DROP TABLE IF EXISTS `table_83`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_83` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_84`
--

DROP TABLE IF EXISTS `table_84`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_84` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_85`
--

DROP TABLE IF EXISTS `table_85`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_85` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_86`
--

DROP TABLE IF EXISTS `table_86`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_86` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_87`
--

DROP TABLE IF EXISTS `table_87`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_87` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_88`
--

DROP TABLE IF EXISTS `table_88`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_88` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_89`
--

DROP TABLE IF EXISTS `table_89`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_89` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_9`
--

DROP TABLE IF EXISTS `table_9`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_9` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_90`
--

DROP TABLE IF EXISTS `table_90`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_90` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_91`
--

DROP TABLE IF EXISTS `table_91`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_91` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_92`
--

DROP TABLE IF EXISTS `table_92`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_92` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_93`
--

DROP TABLE IF EXISTS `table_93`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_93` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_94`
--

DROP TABLE IF EXISTS `table_94`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_94` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_95`
--

DROP TABLE IF EXISTS `table_95`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_95` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_96`
--

DROP TABLE IF EXISTS `table_96`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_96` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_97`
--

DROP TABLE IF EXISTS `table_97`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_97` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_98`
--

DROP TABLE IF EXISTS `table_98`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_98` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `table_99`
--

DROP TABLE IF EXISTS `table_99`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `table_99` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col_1` varchar(100) DEFAULT NULL,
  `col_2` varchar(100) DEFAULT NULL,
  `col_3` varchar(100) DEFAULT NULL,
  `col_4` varchar(100) DEFAULT NULL,
  `col_5` varchar(100) DEFAULT NULL,
  `col_6` varchar(100) DEFAULT NULL,
  `col_7` varchar(100) DEFAULT NULL,
  `col_8` varchar(100) DEFAULT NULL,
  `col_9` varchar(100) DEFAULT NULL,
  `col_10` varchar(100) DEFAULT NULL,
  `col_11` varchar(100) DEFAULT NULL,
  `col_12` varchar(100) DEFAULT NULL,
  `col_13` varchar(100) DEFAULT NULL,
  `col_14` varchar(100) DEFAULT NULL,
  `col_15` varchar(100) DEFAULT NULL,
  `col_16` varchar(100) DEFAULT NULL,
  `col_17` varchar(100) DEFAULT NULL,
  `col_18` varchar(100) DEFAULT NULL,
  `col_19` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `subject` varchar(100) DEFAULT NULL,
  `university_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `university_id` (`university_id`),
  CONSTRAINT `teachers_ibfk_1` FOREIGN KEY (`university_id`) REFERENCES `universities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `universities`
--

DROP TABLE IF EXISTS `universities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `universities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-07 20:58:28
