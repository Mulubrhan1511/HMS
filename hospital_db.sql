-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: localhost    Database: hospital_db
-- ------------------------------------------------------
-- Server version	8.0.33-0ubuntu0.22.10.2

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
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int DEFAULT NULL,
  `doctor_id` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  `time` time DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`id`),
  CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment`
--

LOCK TABLES `appointment` WRITE;
/*!40000 ALTER TABLE `appointment` DISABLE KEYS */;
INSERT INTO `appointment` VALUES (1,3,14,'2023-07-08','16:43:00');
/*!40000 ALTER TABLE `appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `laboratory_test`
--

DROP TABLE IF EXISTS `laboratory_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `laboratory_test` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data` varchar(10000) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `patient_id` int DEFAULT NULL,
  `paid` int DEFAULT NULL,
  `test` int DEFAULT NULL,
  `price` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `laboratory_test_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `laboratory_test`
--

LOCK TABLES `laboratory_test` WRITE;
/*!40000 ALTER TABLE `laboratory_test` DISABLE KEYS */;
INSERT INTO `laboratory_test` VALUES (1,'Patient Information:\r\n            Lab Report for Patient ID : 2 Patient Name :Tsion Patient Gender : Female Patient Age : 26 \r\n\r\nSelected Lab Types:\r\n- Complete Blood Count (CBC)\r\n\r\njb vhbmb<vjb<m.kbmk vbnl,n <vnjnsd\r\n- Basic Metabolic Panel (BMP)\r\nvjbm jbmmnjb.mk\r\n\r\n- Comprehensive Metabolic Panel (CMP)\r\njknjb < bn sdb<mnb\r\n\r\n\r\n          ','2023-07-02 15:19:30',2,1,1,225),(2,'Patient Information:\r\n            Lab Report for Patient ID : 2 Patient Name :Tsion Patient Gender : Female Patient Age : 26 \r\n\r\nSelected Lab Types:\r\n- Complete Blood Count (CBC)\r\n\r\nqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq\r\n- Comprehensive Metabolic Panel (CMP)\r\n\r\nqqqqqqqqqqqqqqqqqqqqqqqqq\r\n\r\n          ','2023-07-02 15:21:18',2,1,1,150),(3,'Patient Information:\r\n            Lab Report for Patient ID : 3 Patient Name :Mulubrhan Patient Gender : Male Patient Age : 32 \r\n\r\nSelected Lab Types:\r\n- Complete Blood Count (CBC)\r\nhve vj<kbv <b s\r\n\r\n- Lipid Panel\r\n\r\n\r\nj jb  n<j\r\n          ','2023-07-05 14:42:28',3,1,1,125),(4,'Patient Information:\r\n            Lab Report for Patient ID : 3 Patient Name :Mulubrhan Patient Gender : Male Patient Age : 32 \r\n\r\nSelected Lab Types:\r\n- Basic Metabolic Panel (BMP)\r\nv hvbn vwk\r\n\r\n- Comprehensive Metabolic Panel (CMP)\r\nb bjb \r\n\r\n- Lipid Panel\r\n\r\nsdddddddddds\r\n\r\n          ','2023-07-06 15:10:27',3,1,1,250),(5,'Patient Information:\r\n            Lab Report for Patient ID : 5 Patient Name :Tsion Patient Gender : Female Patient Age : 24 \r\n\r\nSelected Lab Types:\r\n- Complete Blood Count (CBC)\r\n\r\n\r\n- Comprehensive Metabolic Panel (CMP)\r\n\r\n\r\n\r\n          ','2023-07-07 16:35:32',5,1,1,150);
/*!40000 ALTER TABLE `laboratory_test` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `laboratory_type`
--

DROP TABLE IF EXISTS `laboratory_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `laboratory_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `price` int DEFAULT NULL,
  `Active` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `laboratory_type`
--

LOCK TABLES `laboratory_type` WRITE;
/*!40000 ALTER TABLE `laboratory_type` DISABLE KEYS */;
INSERT INTO `laboratory_type` VALUES (1,'Complete Blood Count (CBC)',50,1),(2,'Basic Metabolic Panel (BMP)',75,1),(3,'Comprehensive Metabolic Panel (CMP)',100,1),(4,'Lipid Panel',75,1),(5,'Hapataytes',150,0);
/*!40000 ALTER TABLE `laboratory_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medication_report`
--

DROP TABLE IF EXISTS `medication_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medication_report` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data` varchar(10000) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `patient_id` int DEFAULT NULL,
  `paid` int DEFAULT NULL,
  `test` int DEFAULT NULL,
  `price` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `medication_report_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medication_report`
--

LOCK TABLES `medication_report` WRITE;
/*!40000 ALTER TABLE `medication_report` DISABLE KEYS */;
INSERT INTO `medication_report` VALUES (1,'Medicine Report for Patient ID : 2 Patient Name :Tsion Patient Gender : Female Patient Age : 26 \n\nSelected Medicine Types:\n- id           Name                Quaty\n\n\n- 4         Lisinopril              10\n\n\n','2023-07-02 15:42:41',2,1,1,100),(2,'Medicine Report for Patient ID : 3 Patient Name :Mulubrhan Patient Gender : Male Patient Age : 32 \n\nSelected Medicine Types:\n- id           Name                Quaty\n\n\n- 4         Lisinopril              2\n\n\n','2023-07-05 15:14:09',3,1,1,20),(3,'Medicine Report for Patient ID : 3 Patient Name :Mulubrhan Patient Gender : Male Patient Age : 32 \n\nSelected Medicine Types:\n- id           Name                Quaty\n\n\n- 4         Lisinopril              11\n\n\n','2023-07-06 15:12:56',3,1,1,110),(4,'Medicine Report for Patient ID : 5 Patient Name :Tsion Patient Gender : Female Patient Age : 24 \n\nSelected Medicine Types:\n- id           Name                Quaty\n\n\n- 4         Lisinopril              2\n\n\n','2023-07-07 16:38:14',5,1,1,20);
/*!40000 ALTER TABLE `medication_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicine`
--

DROP TABLE IF EXISTS `medicine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicine` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `total` int DEFAULT NULL,
  `price` int DEFAULT NULL,
  `expired_date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicine`
--

LOCK TABLES `medicine` WRITE;
/*!40000 ALTER TABLE `medicine` DISABLE KEYS */;
INSERT INTO `medicine` VALUES (4,'Lisinopril',175,10,'2050-12-10');
/*!40000 ALTER TABLE `medicine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) DEFAULT NULL,
  `second_name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `doctor_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `patient_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES (1,'Mulubrhan','Geberkidan','muleP@gmail.com',NULL,'sha256$TADmpBRmsVaMKd23$dfb82ec07ea829d414ae6cf077328627119805ca6c4ee12496651cfeb82cd328','1996-12-07','Male','Bole','Bulubula',NULL),(2,'Tsion','Assefa','tsionP@gmail.com','0919151121','sha256$KJsLf74TL6uVDwj9$672f9b9ef0899c942ef5f921bdc028b299f66956f26566f2588d3e985e1ddd68','1996-07-11','Female','Bole','Bulubula',NULL),(3,'Mulubrhan','Geberkidan','MulubrhanP@gmail.com','0919151121','sha256$8uFyF78fKLfUh3MN$704ab84612a69bb894f747e1d74faca7b9e8c7df9742f5d878090b01940f9fda','1990-12-11','Male','Addis ababa','Bole',14),(4,'Mulubrhan','Geberkidan','muleP2@gmail.com','0919151121','sha256$QDi0xooK7XS3iQcX$b7832db8d8de9baafcab77f398cc2567fd89f49b1b0f19227f4bfd5f6cacd6d4','1999-11-11','Male','Addis Abeba','Bole',16),(5,'Tsion','Assefa','TsionP2@gmail.com','0978564323','sha256$6rm8xG848CqIEftL$bea847ea43e271777d5aaea3d606e61928441f1e1734e08119a74af081144edf','1998-12-11','Female','Bahidar','Abay mado',14);
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data` varchar(10000) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `patient_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `report_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report`
--

LOCK TABLES `report` WRITE;
/*!40000 ALTER TABLE `report` DISABLE KEYS */;
INSERT INTO `report` VALUES (1,'Patient Information:\r\nName:   Tsion   Assefa\r\nAge:   26\r\nGender:   Female\r\nAddress:   Bole   Bulubula\r\nPhone:   0919151121\r\n\r\nMedical History:\r\ngvf a shvb vnmb<hvbwm<hkb  bj <b ws\r\nDiagnosis:\r\nbhbejbhvbwbn<jkbWMBJK\r\nTreatment Plan:\r\nBJKBFJKVBl<jbjb,anjb\r\nFollow-up:\r\n   hjnfjljvN   ','2023-07-02 15:15:39',2),(2,'Patient Information:\r\n  Name:   Mulubrhan   Geberkidan\r\n  Age:   32\r\n  Gender:   Male\r\n  Address:   Addis ababa   Bole\r\n  Phone:   0919151121\r\n\r\n  Medical History:\r\nyes\r\n  Diagnosis:\r\n\r\n  Treatment Plan:\r\n\r\n  Follow-up:\r\n  ','2023-07-05 14:06:33',3),(3,'Patient Information:\r\n  Name:   Mulubrhan   Geberkidan\r\n  Age:   32\r\n  Gender:   Male\r\n  Address:   Addis ababa   Bole\r\n  Phone:   0919151121\r\n\r\n  Medical History:\r\n\r\n  Diagnosis:\r\n\r\n  Treatment Plan:\r\n\r\n  Follow-up:\r\n  ','2023-07-05 14:06:43',3),(4,'Patient Information:\r\n  Name:   Tsion   Assefa\r\n  Age:   24\r\n  Gender:   Female\r\n  Address:   Bahidar   Abay mado\r\n  Phone:   0978564323\r\n\r\n  Medical History:\r\n check\r\n  Diagnosis:\r\n\r\n  Treatment Plan:\r\n\r\n  Follow-up:\r\n  ','2023-07-07 16:34:32',5);
/*!40000 ALTER TABLE `report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) DEFAULT NULL,
  `second_name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `online` int NOT NULL DEFAULT '0',
  `last_seen` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `image` longblob,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (13,'Mulubrhan','Geberkidan','tsionD2@gmail.com','0919151121','sha256$SbQq3sFhM0s9Dh5K$2b58a9d61807dbae495017bbee9ff3efec8c39e48b8289d54f8b0d4d56afe5f8','1996-12-14','Male','Addis ababa','Bole','pharmacist',0,'2023-07-07 13:40:27',_binary 'tsion.jpg'),(14,'Tsion','Assefa','tsionD11@gmail.com','0919151121','sha256$mklI7KwZcB0tvIde$71e5dca2a99e4815baaafd4dfa4f3e5ca94664577f64d0ae2f03a477c6ee4e28','1996-12-14','Male','Addis ababa','Bole','doctor',0,'2023-07-07 13:41:10',_binary 'Doctor_tsion.jpeg'),(15,'Mulubrhan','Geberkidan','muleA@gmail.com','0919151121','sha256$18kaxu7lRQNwnXer$5ea8205286c7166cb2fdc0d741aa82aec801259981a36b50d78508263a66d41c','1996-12-04','Male','Addis ababa','Bole','admin',0,'2023-07-07 13:39:54',_binary 'photo_2023-05-09_23-02-19.jpg'),(16,'Brkity','Geberkidan','BrkityD@gmail.com','0919151121','sha256$qyyxPPLUgZMcKUFN$febf39b85a889c66892f27e3d58582b51648aefe718e1b4288217c1fd0340d8f','1990-11-11','Female','Addis ababa','Bole','doctor',0,'2023-07-04 20:15:23',_binary 'download.jpeg'),(17,'Tsion','Assefa','TsionR@gmail.com','0978564323','sha256$u10nv4uX0HqAu2qV$42c691ebfc8582468f84736cba69dca228d57499f3033792b377159ab594c593','2000-11-21','Male','Addis ababa','Bole','reception',0,'2023-07-07 13:39:01',_binary 'newprofilepic-mod-apk.png'),(18,'Mulubrhan','Geberkidan','muleL@gmail.com','0919151121','sha256$Oq3AwEy2pKAxFW4j$ca933df221b03ba36e7c0c95bd083ccbfae477793dfb807ba615a971d2c74c5c','1999-11-12','Male','Addis Abeba','Bole','laboratory',0,'2023-07-07 13:36:50',_binary 'mulelab.jpeg');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-07 18:24:00
