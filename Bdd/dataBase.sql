-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: assessment
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `annotations`
--

DROP TABLE IF EXISTS `annotations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `annotations` (
  `id` int NOT NULL,
  `id_case` int NOT NULL,
  `version` int NOT NULL,
  `category` int NOT NULL,
  `log_prob` float NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_cases_fk_idx` (`id_case`),
  CONSTRAINT `id_cases_fk` FOREIGN KEY (`id_case`) REFERENCES `cases` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `annotations`
--

LOCK TABLES `annotations` WRITE;
/*!40000 ALTER TABLE `annotations` DISABLE KEYS */;
INSERT INTO `annotations` VALUES (1,1,1,0,-0.002883,1),(2,1,1,1,-0.002197,1),(3,1,1,2,-0.000612,1),(4,1,1,3,-0.275832,1),(5,1,1,4,-0.07097,1),(6,1,1,5,-0.000012,1),(7,1,1,6,-0.000001,1),(8,1,1,7,0,1),(9,1,1,8,-0.000173,1),(10,1,1,9,-0.006758,1),(11,1,1,10,-0.000007,1),(12,1,1,11,-0.000008,1),(13,1,1,12,-0.000019,1),(14,1,1,13,0,1),(15,1,1,14,0,1),(16,1,1,15,-0.000001,1),(17,1,1,16,0,1),(18,1,1,17,0,1),(19,1,1,18,-0.000152,1),(20,1,1,19,-0.00076,1),(21,1,1,20,-0.000002,1),(22,1,1,21,-0.000002,1),(23,1,1,22,0,1),(24,2,1,0,-54.3053,1),(25,2,1,1,-0.162349,1),(26,2,1,2,-54.3053,1),(27,2,1,3,-54.3053,1),(28,2,1,4,-54.3053,1),(29,2,1,5,-0.028108,1),(30,2,1,6,-54.3053,1),(31,2,1,7,-0.251992,1),(32,2,1,8,-54.3053,1),(33,2,1,9,-54.3053,1),(34,2,1,10,-1.0043,1),(35,2,1,11,-54.3053,1),(36,2,1,12,-54.3053,1),(37,2,1,13,-54.3053,1),(38,2,1,14,-54.3053,1),(39,2,1,15,-0.73733,1),(40,2,1,16,-0.000183,1),(41,2,1,17,-0.000939,1),(42,2,1,18,-0.000013,1),(43,2,1,19,-54.3053,1),(44,2,1,20,-54.3053,1),(45,2,1,21,-0.000808,1),(46,2,1,22,0,1),(47,3,1,0,-0.305639,1),(48,3,1,1,-0.000139,1),(49,3,1,2,-0.315314,1),(50,3,1,3,-1.3,1),(51,3,1,4,-0.269813,1),(52,3,1,5,-0.000059,1),(53,3,1,6,-0.000001,1),(54,3,1,7,-0.000004,1),(55,3,1,8,-72.1618,1),(56,3,1,9,-0.64332,1),(57,3,1,10,-0.002333,1),(58,3,1,11,-0.026702,1),(59,3,1,12,-0.000553,1),(60,3,1,13,-0.000001,1),(61,3,1,14,-0.000032,1),(62,3,1,15,-0.000001,1),(63,3,1,16,-0.000038,1),(64,3,1,17,-0.000002,1),(65,3,1,18,-0.000139,1),(66,3,1,19,-72.1618,1),(67,3,1,20,-72.1618,1),(68,3,1,21,-0.603309,1),(69,3,1,22,0,1),(70,4,1,0,-63.7406,1),(71,4,1,1,-0.252886,1),(72,4,1,2,-63.7406,1),(73,4,1,3,-63.7406,1),(74,4,1,4,-63.7406,1),(75,4,1,5,-63.7406,1),(76,4,1,6,-63.7406,1),(77,4,1,7,-0.344583,1),(78,4,1,8,-63.7406,1),(79,4,1,9,-63.7406,1),(80,4,1,10,-63.7406,1),(81,4,1,11,-63.7406,1),(82,4,1,12,-63.7406,1),(83,4,1,13,-1.36679,1),(84,4,1,14,-63.7406,1),(85,4,1,15,-0.43015,1),(86,4,1,16,-0.002976,1),(87,4,1,17,-0.037962,1),(88,4,1,18,-0.040245,1),(89,4,1,19,-0.001996,1),(90,4,1,20,-63.7406,1),(91,4,1,21,-0.045964,1),(92,4,1,22,0,1),(93,5,1,0,-88.4123,1),(94,5,1,1,-0.581875,1),(95,5,1,2,-88.4123,1),(96,5,1,3,-88.4123,1),(97,5,1,4,-88.4123,1),(98,5,1,5,-88.4123,1),(99,5,1,6,-88.4123,1),(100,5,1,7,-88.4123,1),(101,5,1,8,-88.4123,1),(102,5,1,9,-88.4123,1),(103,5,1,10,-88.4123,1),(104,5,1,11,-88.4123,1),(105,5,1,12,-88.4123,1),(106,5,1,13,-88.4123,1),(107,5,1,14,-88.4123,1),(108,5,1,15,-0.783474,1),(109,5,1,16,-0.000059,1),(110,5,1,17,-0.00025,1),(111,5,1,18,-0.106966,1),(112,5,1,19,-0.205546,1),(113,5,1,20,-88.4123,1),(114,5,1,21,-88.4123,1),(115,5,1,22,-0.576786,1),(116,6,1,0,-99.145,1),(117,6,1,1,-99.145,1),(118,6,1,2,-99.145,1),(119,6,1,3,-1.18158,1),(120,6,1,4,-99.145,1),(121,6,1,5,-0.86881,1),(122,6,1,6,-0.00111,1),(123,6,1,7,-0.053167,1),(124,6,1,8,-99.145,1),(125,6,1,9,-99.145,1),(126,6,1,10,-0.484032,1),(127,6,1,11,-0.000001,1),(128,6,1,12,-0.038186,1),(129,6,1,13,-0.000013,1),(130,6,1,14,-0.000005,1),(131,6,1,15,-0.000217,1),(132,6,1,16,-0.001548,1),(133,6,1,17,-0.000263,1),(134,6,1,18,-0.000092,1),(135,6,1,19,-0.181811,1),(136,6,1,20,-0.003097,1),(137,6,1,21,-0.000001,1),(138,6,1,22,0,1),(139,7,1,0,-29.3681,1),(140,7,1,1,-0.57773,1),(141,7,1,2,-0.409912,1),(142,7,1,3,-0.588861,1),(143,7,1,4,-0.281722,1),(144,7,1,5,-0.000181,1),(145,7,1,6,0,1),(146,7,1,7,-0.000001,1),(147,7,1,8,-0.000558,1),(148,7,1,9,-29.3681,1),(149,7,1,10,-0.313326,1),(150,7,1,11,0,1),(151,7,1,12,-0.062106,1),(152,7,1,13,-0.000003,1),(153,7,1,14,0,1),(154,7,1,15,-0.000002,1),(155,7,1,16,0,1),(156,7,1,17,-0.000005,1),(157,7,1,18,-0.000003,1),(158,7,1,19,-0.000065,1),(159,7,1,20,-0.127107,1),(160,7,1,21,0,1),(161,7,1,22,0,1),(162,8,1,0,-77.2344,1),(163,8,1,1,-0.163613,1),(164,8,1,2,-77.2344,1),(165,8,1,3,-77.2344,1),(166,8,1,4,-77.2344,1),(167,8,1,5,-77.2344,1),(168,8,1,6,-77.2344,1),(169,8,1,7,-77.2344,1),(170,8,1,8,-77.2344,1),(171,8,1,9,-77.2344,1),(172,8,1,10,-77.2344,1),(173,8,1,11,-77.2344,1),(174,8,1,12,-77.2344,1),(175,8,1,13,-77.2344,1),(176,8,1,14,-77.2344,1),(177,8,1,15,-1.1051,1),(178,8,1,16,-77.2344,1),(179,8,1,17,-77.2344,1),(180,8,1,18,-77.2344,1),(181,8,1,19,-77.2344,1),(182,8,1,20,-77.2344,1),(183,8,1,21,-0.561796,1),(184,8,1,22,0,1),(185,9,1,0,-32.7339,1),(186,9,1,1,-0.43256,1),(187,9,1,2,-32.7339,1),(188,9,1,3,-32.7339,1),(189,9,1,4,-32.7339,1),(190,9,1,5,-0.00742,1),(191,9,1,6,-0.00096,1),(192,9,1,7,-0.530123,1),(193,9,1,8,-32.7339,1),(194,9,1,9,-32.7339,1),(195,9,1,10,-0.950831,1),(196,9,1,11,0,1),(197,9,1,12,-32.7339,1),(198,9,1,13,-0.029753,1),(199,9,1,14,-0.000002,1),(200,9,1,15,-0.000435,1),(201,9,1,16,-0.061839,1),(202,9,1,17,-0.000239,1),(203,9,1,18,-0.05708,1),(204,9,1,19,-32.7339,1),(205,9,1,20,-32.7339,1),(206,9,1,21,-0.075767,1),(207,9,1,22,-0.000002,1),(208,10,1,0,-40.9941,1),(209,10,1,1,-0.481465,1),(210,10,1,2,-0.064714,1),(211,10,1,3,-40.9941,1),(212,10,1,4,-40.9941,1),(213,10,1,5,-1.08363,1),(214,10,1,6,-40.9941,1),(215,10,1,7,-40.9941,1),(216,10,1,8,-40.9941,1),(217,10,1,9,-40.9941,1),(218,10,1,10,-40.9941,1),(219,10,1,11,-40.9941,1),(220,10,1,12,-40.9941,1),(221,10,1,13,-0.259865,1),(222,10,1,14,-0.005245,1),(223,10,1,15,-0.00013,1),(224,10,1,16,-40.9941,1),(225,10,1,17,-40.9941,1),(226,10,1,18,-40.9941,1),(227,10,1,19,-40.9941,1),(228,10,1,20,-40.9941,1),(229,10,1,21,-40.9941,1),(230,10,1,22,-0.285596,1),(231,11,1,0,-72.8264,1),(232,11,1,1,-0.184237,1),(233,11,1,2,-0.418761,1),(234,11,1,3,-0.631732,1),(235,11,1,4,-0.528935,1),(236,11,1,5,-0.014177,1),(237,11,1,6,-0.000004,1),(238,11,1,7,-0.000285,1),(239,11,1,8,-72.8264,1),(240,11,1,9,-0.669152,1),(241,11,1,10,-0.00001,1),(242,11,1,11,0,1),(243,11,1,12,-0.000029,1),(244,11,1,13,0,1),(245,11,1,14,0,1),(246,11,1,15,0,1),(247,11,1,16,-0.000011,1),(248,11,1,17,-0.000009,1),(249,11,1,18,-0.000053,1),(250,11,1,19,-0.022685,1),(251,11,1,20,-0.005999,1),(252,11,1,21,-0.000002,1),(253,11,1,22,0,1);
/*!40000 ALTER TABLE `annotations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cases`
--

DROP TABLE IF EXISTS `cases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cases` (
  `id` int NOT NULL,
  `id_normative` int NOT NULL,
  `id_law` int NOT NULL,
  `name` varchar(500) NOT NULL,
  `alias` varchar(500) NOT NULL,
  `description` varchar(5000) NOT NULL,
  `version` int NOT NULL,
  `version_cs` int NOT NULL,
  `version_ncs` int NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_normatives_idx` (`id_normative`),
  KEY `fk_laws_idx` (`id_law`),
  CONSTRAINT `fk_laws` FOREIGN KEY (`id_law`) REFERENCES `laws` (`id`),
  CONSTRAINT `fk_norms` FOREIGN KEY (`id_normative`) REFERENCES `normatives` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cases`
--

LOCK TABLES `cases` WRITE;
/*!40000 ALTER TABLE `cases` DISABLE KEYS */;
INSERT INTO `cases` VALUES (1,1,1,'ISO and GDPR','GDPR (Europe)','This case study defines how well the GDPR is aligned with the ISO/IEC 27701:2025 standard. This serves as a baseline for the study.',1,1,1,1),(2,1,2,'ISO and Law 7593/25','Law 7593/25 (Paraguay)','This case study establishes the mapping between the ISO/IEC 27701:2025 and the Law 7593/25 of Paraguay, in order to unveil how well this privacy legal framework is aligned with the standard.',1,1,1,1),(3,1,3,'ISO and Law 21719','Law 21719 (Chile)','This study defines how well the ISO/IEC 27701:2019 standard is aligned with Law 21719 of Chile, allowing to unveils critical maps.',1,1,1,1),(4,1,4,'ISO and LOPDP','LOPDP (Ecuador)','This case study is oriented to establish how well the LOPDP of Ecuador is aligned with the ISO/IEC 27701:2025 standard.',1,1,1,1),(5,1,5,'ISO and RLOPDP','RLOPDP (Ecuador)','In order to determine how well thr RLOPDP of Ecuador is aligned with ISO/IEC 27701:2019, this case study analyzes this regulation through GPT.',1,1,1,1),(6,1,6,'ISO and LFPDPPP','LFPDPPP (México)','This case study analyzes the alignment between the ISO/IEC 27701:2025 and the LFPDPPP, in order to unveil critical gaps that this privacy legal framework could have.',1,1,1,1),(7,1,7,'ISO and LOPDPPSO','LOPDPPSO (México)','This case study analyzes the level of alignment between the ISO/IEC 27701:2025 and LGPDPPSO, in order to be analyzed with GPT some pros and cons.',1,1,1,1),(8,1,8,'ISO and Law 1581','Law 1581 (Colombia)','This case study maps the ISO/IEC 27701:2025 and the Law 1581 of Colombia, in order to analyze current gaps and opportunities for improvement.',1,1,1,1),(9,1,9,'ISO and Decree 1733','Decree 1377 (Colombia)','This case study maps the ISO/IEC 27701:2025 and the Decree 1377 of Colombia, in order to analyze current gaps and opportunities for improvement.',1,1,1,1),(10,1,10,'ISO and Law 29733','Law 29733 (Perú)','Mapping between the ISO/IEC 27701 and the Law 29733 of Perú for analysis purposes.',1,1,1,1),(11,1,11,'ISO and Supreme Decree 016-2024-JUS','Supreme Decree 016-2024-JUS (Perú)','Case study for analyzing the ISO/IEC 27701:2025 and Supreme Decree 016-2024-JUS of Perú.',1,1,1,1);
/*!40000 ALTER TABLE `cases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `laws`
--

DROP TABLE IF EXISTS `laws`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `laws` (
  `id` int NOT NULL,
  `name` varchar(500) NOT NULL,
  `alias` varchar(500) NOT NULL,
  `description` varchar(5000) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `laws`
--

LOCK TABLES `laws` WRITE;
/*!40000 ALTER TABLE `laws` DISABLE KEYS */;
INSERT INTO `laws` VALUES (1,'General Data Protection Regulation','GDPR','The GDPR (General Data Protection Regulation) is a European Union regulation designed to protect individuals’ personal data. It sets rules for how organizations collect, process, store, and share personal information, and gives people greater control over their privacy and data rights.',1),(2,'Law 7593/25 Paraguay','Law 7593 25','Law 7593/25 (Paraguay) is Paraguay’s new Personal Data Protection Law, enacted on 27 November 2025, that establishes the country’s first modern, comprehensive legal framework for how personal data must be handled by public and private organizations.',1),(3,'Law 21719 Chile','Law 21719','Law 21719 (Chile) is Chile’s new Personal Data Protection Law (officially Law 21.719), published on December 13, 2024, that regulates how personal data is collected, processed, stored, and shared by public and private organizations and creates the Personal Data Protection Agency as an independent authority to supervise compliance.',1),(4,'Ley Orgánica de Protección de Datos Personales','LOPDP','The Ley Orgánica de Protección de Datos Personales, enacted in May 2021, regulates the collection and use of personal data, protects individuals’ privacy rights, and sets obligations for organizations that process such data.',1),(5,'Reglamento a la Ley Orgánica de Protección de Datos Personales','RLOPDP','The Reglamento a la Ley Orgánica de Protección de Datos Personales de Ecuador (RLOPDP) is the implementing regulation that details and clarifies how the LOPDP must be applied, specifying procedures and obligations.',1),(6,'Ley Federal de Protección de Datos Personales en Posesión de Particulares','LFPDPPP','The LFPDPPP is Mexico’s main data protection law, regulating how private organizations collect, use, store, and protect personal data, and granting individuals rights over their personal information.',1),(7,'Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados','LGPDPPSO','The LGPDPPSO is Mexico’s data protection law that regulates how public authorities and government entities process and protect personal data, ensuring individuals’ privacy rights.',1),(8,'Law 1581 Colombia','Law 1581','Law 1581 of Colombia is the country’s personal data protection law that regulates how personal data is collected, used, stored, and shared, and guarantees individuals’ rights over their personal information, such as access, correction, and deletion.',1),(9,'Decree 1377 Colombia','Decree 1377','Decree 1377 of Colombia is a regulatory decree that implements Law 1581, establishing procedures and requirements for the authorization, processing, and protection of personal data by organizations.',1),(10,'Law 29733 Perú','Law 29733','Law 29733 of Perú is the Personal Data Protection Law that regulates the collection, processing, and protection of personal data, and guarantees individuals’ rights over their personal information.',1),(11,'Supreme Decree 016-2024-JUS Perú','Supreme Decree 016-2024-JUS','Supreme Decree 016‑2024‑JUS (Peru) is the regulation that implements Law 29733, the Personal Data Protection Law in Peru. Published on November 30 2024 and in force from March 31 2025, it updates and replaces the previous regulation, modernizing the data protection framework.',1);
/*!40000 ALTER TABLE `laws` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `normatives`
--

DROP TABLE IF EXISTS `normatives`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `normatives` (
  `id` int NOT NULL,
  `name` varchar(500) NOT NULL,
  `alias` varchar(500) NOT NULL,
  `description` varchar(5000) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `normatives`
--

LOCK TABLES `normatives` WRITE;
/*!40000 ALTER TABLE `normatives` DISABLE KEYS */;
INSERT INTO `normatives` VALUES (1,'ISO/IEC 27701:2025 Standard','ISO IEC 27701','Information security, cybersecurity and privacy protection - Privacy information management systems - Requirements and guidance',1);
/*!40000 ALTER TABLE `normatives` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `principles`
--

DROP TABLE IF EXISTS `principles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `principles` (
  `id` int NOT NULL,
  `id_normative` int NOT NULL,
  `principle` int NOT NULL,
  `category_from` int NOT NULL,
  `category_to` int NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk1_idx` (`id_normative`),
  CONSTRAINT `fk_normatives` FOREIGN KEY (`id_normative`) REFERENCES `normatives` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `principles`
--

LOCK TABLES `principles` WRITE;
/*!40000 ALTER TABLE `principles` DISABLE KEYS */;
INSERT INTO `principles` VALUES (1,1,1,0,3,1),(2,1,2,4,6,1),(3,1,3,7,9,1),(4,1,4,10,14,1),(5,1,5,15,17,1),(6,1,6,18,20,1),(7,1,7,21,22,1);
/*!40000 ALTER TABLE `principles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-14 20:01:08
