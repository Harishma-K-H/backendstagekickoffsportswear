-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: KICKOFF
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add branch',6,'add_branch'),(22,'Can change branch',6,'change_branch'),(23,'Can delete branch',6,'delete_branch'),(24,'Can view branch',6,'view_branch'),(25,'Can add user role',7,'add_userrole'),(26,'Can change user role',7,'change_userrole'),(27,'Can delete user role',7,'delete_userrole'),(28,'Can view user role',7,'view_userrole'),(29,'Can add user',8,'add_user'),(30,'Can change user',8,'change_user'),(31,'Can delete user',8,'delete_user'),(32,'Can view user',8,'view_user'),(33,'Can add customer',9,'add_customer'),(34,'Can change customer',9,'change_customer'),(35,'Can delete customer',9,'delete_customer'),(36,'Can view customer',9,'view_customer'),(37,'Can add material',10,'add_material'),(38,'Can change material',10,'change_material'),(39,'Can delete material',10,'delete_material'),(40,'Can view material',10,'view_material'),(41,'Can add print type',11,'add_printtype'),(42,'Can change print type',11,'change_printtype'),(43,'Can delete print type',11,'delete_printtype'),(44,'Can view print type',11,'view_printtype'),(45,'Can add item',12,'add_item'),(46,'Can change item',12,'change_item'),(47,'Can delete item',12,'delete_item'),(48,'Can view item',12,'view_item'),(49,'Can add Menu',13,'add_menu'),(50,'Can change Menu',13,'change_menu'),(51,'Can delete Menu',13,'delete_menu'),(52,'Can view Menu',13,'view_menu'),(53,'Can add Menu access',14,'add_menuaccess'),(54,'Can change Menu access',14,'change_menuaccess'),(55,'Can delete Menu access',14,'delete_menuaccess'),(56,'Can view Menu access',14,'view_menuaccess'),(57,'Can add orderdata',15,'add_orderdata'),(58,'Can change orderdata',15,'change_orderdata'),(59,'Can delete orderdata',15,'delete_orderdata'),(60,'Can view orderdata',15,'view_orderdata'),(61,'Can add order item',16,'add_orderitem'),(62,'Can change order item',16,'change_orderitem'),(63,'Can delete order item',16,'delete_orderitem'),(64,'Can view order item',16,'view_orderitem'),(65,'Can add model_data',17,'add_model_data'),(66,'Can change model_data',17,'change_model_data'),(67,'Can delete model_data',17,'delete_model_data'),(68,'Can view model_data',17,'view_model_data'),(69,'Can add invoice',18,'add_invoice'),(70,'Can change invoice',18,'change_invoice'),(71,'Can delete invoice',18,'delete_invoice'),(72,'Can view invoice',18,'view_invoice'),(73,'Can add invoice item',19,'add_invoiceitem'),(74,'Can change invoice item',19,'change_invoiceitem'),(75,'Can delete invoice item',19,'delete_invoiceitem'),(76,'Can view invoice item',19,'view_invoiceitem'),(77,'VIEW_CUSTOMERS',20,'VIEW_CUSTOMERS'),(78,'Can add material data',21,'add_materialdata'),(79,'Can change material data',21,'change_materialdata'),(80,'Can delete material data',21,'delete_materialdata'),(81,'Can view material data',21,'view_materialdata'),(82,'Can add order payment',22,'add_orderpayment'),(83,'Can change order payment',22,'change_orderpayment'),(84,'Can delete order payment',22,'delete_orderpayment'),(85,'Can view order payment',22,'view_orderpayment'),(86,'Can add district',23,'add_district'),(87,'Can change district',23,'change_district'),(88,'Can delete district',23,'delete_district'),(89,'Can view district',23,'view_district');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_user_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_user_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=183 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-03-13 05:22:00.261096','2','User',1,'[{\"added\": {}}]',7,1),(2,'2025-03-13 05:33:19.305824','2','branch2',2,'[{\"changed\": {\"fields\": [\"Name\"]}}]',6,1),(3,'2025-03-13 06:51:38.819314','1','Model_data object (1)',1,'[{\"added\": {}}]',17,1),(4,'2025-03-13 06:52:18.647456','2','T SHIRT',1,'[{\"added\": {}}]',17,1),(5,'2025-03-13 06:52:33.858203','3','SHIRT',1,'[{\"added\": {}}]',17,1),(6,'2025-03-13 06:52:44.678881','4','CLUB JERSEY - JR',1,'[{\"added\": {}}]',17,1),(7,'2025-03-13 06:52:53.148149','5','CLUB JERSEY - SR',1,'[{\"added\": {}}]',17,1),(8,'2025-03-13 06:53:08.195509','6','SHORTS',1,'[{\"added\": {}}]',17,1),(9,'2025-03-13 06:53:25.766118','7','LOWER',1,'[{\"added\": {}}]',17,1),(10,'2025-03-13 06:54:41.360643','1','Material object (1)',1,'[{\"added\": {}}]',10,1),(11,'2025-03-13 06:57:46.855126','2','DOT KNIT (JERSEY)',1,'[{\"added\": {}}]',10,1),(12,'2025-03-13 06:57:59.603115','3','HONEYCOMB (JERSEY)',1,'[{\"added\": {}}]',10,1),(13,'2025-03-13 06:58:20.945988','4','HONEYCOMB (T SHIRT)',1,'[{\"added\": {}}]',10,1),(14,'2025-03-13 06:58:32.956167','5','DOT KNIT (T SHIRT)',1,'[{\"added\": {}}]',10,1),(15,'2025-03-13 06:58:45.805988','6','SALINA (T SHIRT)',1,'[{\"added\": {}}]',10,1),(16,'2025-03-13 06:59:01.833504','7','SALINA (SHIRT)',1,'[{\"added\": {}}]',10,1),(17,'2025-03-13 06:59:13.328855','8','DOT KNIT (SHIRT)',1,'[{\"added\": {}}]',10,1),(18,'2025-03-13 06:59:24.745120','9','HONEYCOMB (SHIRT)',1,'[{\"added\": {}}]',10,1),(19,'2025-03-13 06:59:51.945819','10','SALINA (CLUB JERSEY - JR)',1,'[{\"added\": {}}]',10,1),(20,'2025-03-13 07:00:02.830274','11','DOT KNIT (CLUB JERSEY - JR)',1,'[{\"added\": {}}]',10,1),(21,'2025-03-13 07:00:18.807325','12','HONEYCOMB (CLUB JERSEY - JR)',1,'[{\"added\": {}}]',10,1),(22,'2025-03-13 07:00:36.049509','13','SALINA (CLUB JERSEY - SR)',1,'[{\"added\": {}}]',10,1),(23,'2025-03-13 07:00:44.868921','14','DOT KNIT (CLUB JERSEY - SR)',1,'[{\"added\": {}}]',10,1),(24,'2025-03-13 07:00:53.540568','15','HONEYCOMB (CLUB JERSEY - SR)',1,'[{\"added\": {}}]',10,1),(25,'2025-03-13 07:01:04.433796','16','Super Poly (SHORTS)',1,'[{\"added\": {}}]',10,1),(26,'2025-03-13 07:01:17.191570','17','Honeycomb (SHORTS)',1,'[{\"added\": {}}]',10,1),(27,'2025-03-13 07:01:28.634633','18','2 Way Lycra (SHORTS)',1,'[{\"added\": {}}]',10,1),(28,'2025-03-13 07:01:38.587871','19','4 Way Lycra (SHORTS)',1,'[{\"added\": {}}]',10,1),(29,'2025-03-13 07:01:48.460707','20','Ns Lycra (SHORTS)',1,'[{\"added\": {}}]',10,1),(30,'2025-03-13 07:02:15.198113','21','PP (SHORTS)',1,'[{\"added\": {}}]',10,1),(31,'2025-03-13 07:02:36.923123','22','Dot Knit (SHORTS)',1,'[{\"added\": {}}]',10,1),(32,'2025-03-13 07:02:49.507134','23','Super Poly (LOWER)',1,'[{\"added\": {}}]',10,1),(33,'2025-03-13 07:02:59.214868','24','Honeycomb (LOWER)',1,'[{\"added\": {}}]',10,1),(34,'2025-03-13 07:03:07.800906','25','2 Way Lycra (LOWER)',1,'[{\"added\": {}}]',10,1),(35,'2025-03-13 07:03:16.377902','26','4 Way Lycra (LOWER)',1,'[{\"added\": {}}]',10,1),(36,'2025-03-13 07:03:28.772513','27','Ns Lycra (LOWER)',1,'[{\"added\": {}}]',10,1),(37,'2025-03-13 07:03:36.905833','28','PP (LOWER)',1,'[{\"added\": {}}]',10,1),(38,'2025-03-13 07:03:45.446205','29','Dot Knit (LOWER)',1,'[{\"added\": {}}]',10,1),(39,'2025-03-13 07:04:45.134593','1','PrintType object (1)',1,'[{\"added\": {}}]',11,1),(40,'2025-03-13 07:04:52.320662','2','PrintType object (2)',1,'[{\"added\": {}}]',11,1),(41,'2025-03-13 08:51:59.800847','1','HARISHMA',1,'[{\"added\": {}}]',9,1),(42,'2025-03-13 08:56:29.546698','1','JERSEY (Half Sleeve)',1,'[{\"added\": {}}]',12,1),(43,'2025-03-13 08:57:47.418363','2','JERSEY (Full Sleeve)',1,'[{\"added\": {}}]',12,1),(44,'2025-03-13 09:25:51.901410','1','Orderdata object (1)',3,'',15,1),(45,'2025-03-13 09:26:13.698114','3','Orderdata object (3)',3,'',15,1),(46,'2025-03-13 09:31:47.415627','4','Orderdata object (4)',3,'',15,1),(47,'2025-03-13 09:33:31.782256','5','Orderdata object (5)',3,'',15,1),(48,'2025-03-13 09:34:47.620840','7','Orderdata object (7)',3,'',15,1),(49,'2025-03-13 09:36:14.390408','9','Orderdata object (9)',3,'',15,1),(50,'2025-03-13 09:41:14.773355','10','Orderdata object (10)',3,'',15,1),(51,'2025-03-13 09:42:16.241576','12','Orderdata object (12)',3,'',15,1),(52,'2025-03-13 09:42:35.201011','14','Orderdata object (14)',3,'',15,1),(53,'2025-03-13 09:42:50.790786','15','Orderdata object (15)',3,'',15,1),(54,'2025-03-13 09:43:17.545032','17','Orderdata object (17)',3,'',15,1),(55,'2025-03-13 09:43:30.419526','18','Orderdata object (18)',3,'',15,1),(56,'2025-03-13 09:44:42.567361','20','Orderdata object (20)',3,'',15,1),(57,'2025-03-13 10:01:38.677549','13','OrderItem object (13)',3,'',16,1),(58,'2025-03-13 10:01:38.677594','12','OrderItem object (12)',3,'',16,1),(59,'2025-03-13 10:01:38.677617','11','OrderItem object (11)',3,'',16,1),(60,'2025-03-13 10:01:38.677637','10','OrderItem object (10)',3,'',16,1),(61,'2025-03-13 10:01:38.677654','9','OrderItem object (9)',3,'',16,1),(62,'2025-03-13 10:01:38.677671','8','OrderItem object (8)',3,'',16,1),(63,'2025-03-13 10:01:38.677687','7','OrderItem object (7)',3,'',16,1),(64,'2025-03-13 10:01:38.677703','6','OrderItem object (6)',3,'',16,1),(65,'2025-03-13 10:01:38.677718','5','OrderItem object (5)',3,'',16,1),(66,'2025-03-13 10:01:38.677733','4','OrderItem object (4)',3,'',16,1),(67,'2025-03-13 10:01:38.677748','3','OrderItem object (3)',3,'',16,1),(68,'2025-03-13 10:01:38.677762','2','OrderItem object (2)',3,'',16,1),(69,'2025-03-13 10:01:38.677776','1','OrderItem object (1)',3,'',16,1),(70,'2025-03-13 10:01:55.429834','43','Orderdata object (43)',3,'',15,1),(71,'2025-03-13 10:01:55.429939','41','Orderdata object (41)',3,'',15,1),(72,'2025-03-13 10:01:55.430018','40','Orderdata object (40)',3,'',15,1),(73,'2025-03-13 10:01:55.430051','39','Orderdata object (39)',3,'',15,1),(74,'2025-03-13 10:01:55.430122','38','Orderdata object (38)',3,'',15,1),(75,'2025-03-13 10:01:55.430146','36','Orderdata object (36)',3,'',15,1),(76,'2025-03-13 10:01:55.430161','34','Orderdata object (34)',3,'',15,1),(77,'2025-03-13 10:01:55.430174','32','Orderdata object (32)',3,'',15,1),(78,'2025-03-13 10:01:55.430189','31','Orderdata object (31)',3,'',15,1),(79,'2025-03-13 10:01:55.430203','30','Orderdata object (30)',3,'',15,1),(80,'2025-03-13 10:01:55.430215','29','Orderdata object (29)',3,'',15,1),(81,'2025-03-13 10:01:55.430228','27','Orderdata object (27)',3,'',15,1),(82,'2025-03-13 10:01:55.430241','26','Orderdata object (26)',3,'',15,1),(83,'2025-03-13 10:01:55.430254','25','Orderdata object (25)',3,'',15,1),(84,'2025-03-13 10:01:55.430266','24','Orderdata object (24)',3,'',15,1),(85,'2025-03-13 10:01:55.430278','23','Orderdata object (23)',3,'',15,1),(86,'2025-03-13 10:01:55.430290','21','Orderdata object (21)',3,'',15,1),(87,'2025-03-13 10:07:21.339059','44','Orderdata object (44)',3,'',15,1),(88,'2025-03-14 06:10:32.771197','1','Customer',1,'[{\"added\": {}}]',13,1),(89,'2025-03-14 06:23:48.565414','1','Customer',3,'',13,1),(90,'2025-03-14 06:36:18.225649','20','Customer',1,'[{\"added\": {}}]',4,1),(91,'2025-03-14 06:36:57.121824','77','Customer | VIEW_CUSTOMERS',1,'[{\"added\": {}}]',2,1),(92,'2025-03-14 06:39:52.435618','4','Customer',1,'[{\"added\": {}}]',13,1),(93,'2025-03-14 06:41:33.970616','5','View_customer_list',1,'[{\"added\": {}}]',13,1),(94,'2025-03-14 06:42:38.375957','6','Create_customer',1,'[{\"added\": {}}]',13,1),(95,'2025-03-14 06:43:34.319361','3','test1@example.com',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',8,1),(96,'2025-03-14 07:02:36.265294','2','User',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',7,1),(97,'2025-03-14 07:04:42.140374','2','User',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',7,1),(98,'2025-03-14 07:17:21.993296','2','User',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',7,1),(99,'2025-03-14 07:39:55.556601','2','User',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',7,1),(100,'2025-03-15 06:52:04.832716','1','SALINA',1,'[{\"added\": {}}]',21,1),(101,'2025-03-15 06:52:16.165875','2','DOT KNIT',1,'[{\"added\": {}}]',21,1),(102,'2025-03-15 06:52:37.442496','3','HONEYCOMB',1,'[{\"added\": {}}]',21,1),(103,'2025-03-15 06:52:51.484232','4','Super Poly',1,'[{\"added\": {}}]',21,1),(104,'2025-03-15 06:53:08.406858','5','Honeycomb',1,'[{\"added\": {}}]',21,1),(105,'2025-03-15 06:53:19.919129','6','2 Way Lycra',1,'[{\"added\": {}}]',21,1),(106,'2025-03-15 06:53:31.548014','7','4 Way Lycra',1,'[{\"added\": {}}]',21,1),(107,'2025-03-15 06:53:42.527568','8','Ns Lycra',1,'[{\"added\": {}}]',21,1),(108,'2025-03-15 06:53:51.891297','9','PP',1,'[{\"added\": {}}]',21,1),(109,'2025-03-15 07:48:21.333337','2','JERSEY (Full Sleeve)',3,'',12,1),(110,'2025-03-15 07:48:21.333390','1','JERSEY (Half Sleeve)',3,'',12,1),(111,'2025-03-17 04:54:19.920870','45','Orderdata object (45)',3,'',15,1),(112,'2025-03-17 05:21:36.160409','47','Orderdata object (47)',3,'',15,1),(113,'2025-03-17 05:23:32.243718','48','Orderdata object (48)',3,'',15,1),(114,'2025-03-17 06:18:55.456418','17','OrderItem object (17)',3,'',16,1),(115,'2025-03-17 06:18:55.456480','16','OrderItem object (16)',3,'',16,1),(116,'2025-03-17 06:19:00.037035','50','Orderdata object (50)',3,'',15,1),(117,'2025-03-18 04:17:55.046957','19','OrderItem object (19)',3,'',16,1),(118,'2025-03-18 04:17:55.046999','18','OrderItem object (18)',3,'',16,1),(119,'2025-03-18 04:17:59.917768','52','Orderdata object (52)',3,'',15,1),(120,'2025-03-18 04:30:52.127855','53','Orderdata object (53)',3,'',15,1),(121,'2025-03-18 05:04:38.264743','23','OrderItem object (23)',2,'[{\"changed\": {\"fields\": [\"Discount\", \"Total item cost\"]}}]',16,1),(122,'2025-03-19 07:47:43.545416','1','Invoice 12345 for Order EKM/2625/0001',3,'',18,5),(123,'2025-03-19 07:49:10.747422','3','Invoice 12345 for Order EKM/2625/0001',3,'',18,5),(124,'2025-03-19 07:50:08.513538','4','Invoice 12345 for Order EKM/2625/0001',3,'',18,5),(125,'2025-03-19 08:29:43.509620','5','Invoice 12345 for Order EKM/2625/0001',3,'',18,5),(126,'2025-03-19 08:30:15.571726','7','JERSEY (Full Sleeve)',3,'',12,5),(127,'2025-03-19 08:30:15.571923','6','JERSEY (Half Sleeve)',3,'',12,5),(128,'2025-03-19 08:37:26.443595','10','10 - JERSEY (Full Sleeve)',3,'',12,5),(129,'2025-03-19 08:38:59.380437','2','InvoiceItem: 18 - JERSEY (Half Sleeve) (26) - 7 in Invoice 12345',3,'',19,5),(130,'2025-03-19 08:38:59.380491','1','InvoiceItem: 16 - JERSEY (Full Sleeve) (25) - 0 in Invoice 12345',3,'',19,5),(131,'2025-03-19 08:39:09.439486','7','Invoice 12345 for Order EKM/2625/0001',3,'',18,5),(132,'2025-03-19 09:18:10.473667','57','Orderdata object (57)',3,'',15,5),(133,'2025-03-19 09:27:24.514995','6','InvoiceItem: 18 - JERSEY (Half Sleeve) (26) - 7 in Invoice 12345',3,'',19,5),(134,'2025-03-19 09:27:24.515042','5','InvoiceItem: 16 - JERSEY (Full Sleeve) (25) - 3 in Invoice 12345',3,'',19,5),(135,'2025-03-19 09:27:30.828132','11','Invoice 12345 for Order EKM/2625/0002',3,'',18,5),(136,'2025-03-19 09:28:58.484629','8','InvoiceItem: 18 - JERSEY (Half Sleeve) (26) - 7 in Invoice b327e84a-6e77-462b-9a09-6cca44351485',3,'',19,5),(137,'2025-03-19 09:28:58.484685','7','InvoiceItem: 16 - JERSEY (Full Sleeve) (25) - 3 in Invoice b327e84a-6e77-462b-9a09-6cca44351485',3,'',19,5),(138,'2025-03-19 09:29:02.879296','14','Invoice b327e84a-6e77-462b-9a09-6cca44351485 for Order EKM/2625/0003',3,'',18,5),(139,'2025-03-20 06:26:15.893087','8','EKM/2625/0002',1,'[{\"added\": {}}]',22,5),(140,'2025-03-20 06:27:07.482598','9','EKM/2625/0002',1,'[{\"added\": {}}]',22,5),(141,'2025-03-20 08:55:34.846555','16','Invoice INV81008 for Order EKM/2625/0002',2,'[{\"changed\": {\"fields\": [\"Total cost\", \"Gst\", \"Net cost\"]}}]',18,5),(142,'2025-03-22 07:21:34.548348','11','kh5417@example.com',2,'[{\"changed\": {\"fields\": [\"First name\", \"Middle name\", \"Last name\"]}}]',8,5),(143,'2025-03-22 07:24:10.581104','3','KICKOFF',2,'[{\"changed\": {\"fields\": [\"Name\", \"Code\", \"Location\", \"City\"]}}]',6,5),(144,'2025-03-22 09:25:57.003995','29','Dot Knit (LOWER)',3,'',10,5),(145,'2025-03-22 09:25:57.004041','28','PP (LOWER)',3,'',10,5),(146,'2025-03-22 09:25:57.004061','27','Ns Lycra (LOWER)',3,'',10,5),(147,'2025-03-22 09:25:57.004077','26','4 Way Lycra (LOWER)',3,'',10,5),(148,'2025-03-22 09:25:57.004092','25','2 Way Lycra (LOWER)',3,'',10,5),(149,'2025-03-22 09:25:57.004107','24','Honeycomb (LOWER)',3,'',10,5),(150,'2025-03-22 09:25:57.004120','23','Super Poly (LOWER)',3,'',10,5),(151,'2025-03-22 09:25:57.004133','22','Dot Knit (SHORTS)',3,'',10,5),(152,'2025-03-22 09:25:57.004146','21','PP (SHORTS)',3,'',10,5),(153,'2025-03-22 09:25:57.004159','20','Ns Lycra (SHORTS)',3,'',10,5),(154,'2025-03-22 09:25:57.004171','19','4 Way Lycra (SHORTS)',3,'',10,5),(155,'2025-03-22 09:25:57.004184','18','2 Way Lycra (SHORTS)',3,'',10,5),(156,'2025-03-22 09:25:57.004196','17','Honeycomb (SHORTS)',3,'',10,5),(157,'2025-03-22 09:25:57.004209','16','Super Poly (SHORTS)',3,'',10,5),(158,'2025-03-22 09:25:57.004221','15','HONEYCOMB (CLUB JERSEY - SR)',3,'',10,5),(159,'2025-03-22 09:25:57.004233','14','DOT KNIT (CLUB JERSEY - SR)',3,'',10,5),(160,'2025-03-22 09:25:57.004245','13','SALINA (CLUB JERSEY - SR)',3,'',10,5),(161,'2025-03-22 09:25:57.004258','12','HONEYCOMB (CLUB JERSEY - JR)',3,'',10,5),(162,'2025-03-22 09:25:57.004270','11','DOT KNIT (CLUB JERSEY - JR)',3,'',10,5),(163,'2025-03-22 09:25:57.004282','10','SALINA (CLUB JERSEY - JR)',3,'',10,5),(164,'2025-03-22 09:25:57.004294','9','HONEYCOMB (SHIRT)',3,'',10,5),(165,'2025-03-22 09:25:57.004307','8','DOT KNIT (SHIRT)',3,'',10,5),(166,'2025-03-22 09:25:57.004320','7','SALINA (SHIRT)',3,'',10,5),(167,'2025-03-22 09:25:57.004332','6','SALINA (T SHIRT)',3,'',10,5),(168,'2025-03-22 09:25:57.004344','5','DOT KNIT (T SHIRT)',3,'',10,5),(169,'2025-03-22 09:25:57.004356','4','HONEYCOMB (T SHIRT)',3,'',10,5),(170,'2025-03-22 09:25:57.004369','3','HONEYCOMB (JERSEY)',3,'',10,5),(171,'2025-03-22 09:25:57.004381','2','DOT KNIT (JERSEY)',3,'',10,5),(172,'2025-03-22 09:25:57.004393','1','SALINA (JERSEY)',3,'',10,5),(173,'2025-03-22 09:26:55.248312','30','SALINA (JERSEY)',1,'[{\"added\": {}}]',10,5),(174,'2025-03-22 09:27:30.829877','31','DOT KNIT (JERSEY)',1,'[{\"added\": {}}]',10,5),(175,'2025-03-22 09:28:07.327730','32','HONEYCOMB (JERSEY)',1,'[{\"added\": {}}]',10,5),(176,'2025-03-22 09:28:31.609588','33','SALINA (T SHIRT)',1,'[{\"added\": {}}]',10,5),(177,'2025-03-22 09:28:38.714907','34','DOT KNIT (T SHIRT)',1,'[{\"added\": {}}]',10,5),(178,'2025-03-22 09:28:45.642123','35','HONEYCOMB (T SHIRT)',1,'[{\"added\": {}}]',10,5),(179,'2025-03-24 04:20:25.910212','109','109 - SHORTS (None)',2,'[{\"changed\": {\"fields\": [\"Model\"]}}]',12,5),(180,'2025-03-24 04:35:05.625066','10','HARI',2,'[{\"changed\": {\"fields\": [\"Name\"]}}]',9,5),(181,'2025-03-24 04:37:46.142261','109','109 - SHORTS (Sleeveless)',2,'[{\"changed\": {\"fields\": [\"Is sleeve\"]}}]',12,5),(182,'2025-03-24 04:40:48.407227','8','8 - JERSEY (Sleeveless)',2,'[{\"changed\": {\"fields\": [\"Model\"]}}]',12,5);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(18,'Order','invoice'),(19,'Order','invoiceitem'),(15,'Order','orderdata'),(16,'Order','orderitem'),(22,'Order','orderpayment'),(5,'sessions','session'),(6,'user_auth','branch'),(9,'user_auth','customer'),(23,'user_auth','district'),(12,'user_auth','item'),(10,'user_auth','material'),(21,'user_auth','materialdata'),(13,'user_auth','menu'),(14,'user_auth','menuaccess'),(17,'user_auth','model_data'),(11,'user_auth','printtype'),(8,'user_auth','user'),(7,'user_auth','userrole'),(20,'VIEW_CUSTOMER','Customer');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-03-12 10:25:44.101662'),(2,'contenttypes','0002_remove_content_type_name','2025-03-12 10:25:44.215617'),(3,'auth','0001_initial','2025-03-12 10:25:44.698922'),(4,'auth','0002_alter_permission_name_max_length','2025-03-12 10:25:44.801829'),(5,'auth','0003_alter_user_email_max_length','2025-03-12 10:25:44.808570'),(6,'auth','0004_alter_user_username_opts','2025-03-12 10:25:44.824859'),(7,'auth','0005_alter_user_last_login_null','2025-03-12 10:25:44.841269'),(8,'auth','0006_require_contenttypes_0002','2025-03-12 10:25:44.845391'),(9,'auth','0007_alter_validators_add_error_messages','2025-03-12 10:25:44.855179'),(10,'auth','0008_alter_user_username_max_length','2025-03-12 10:25:44.862928'),(11,'auth','0009_alter_user_last_name_max_length','2025-03-12 10:25:44.874387'),(12,'auth','0010_alter_group_name_max_length','2025-03-12 10:25:44.896240'),(13,'auth','0011_update_proxy_permissions','2025-03-12 10:25:44.904545'),(14,'auth','0012_alter_user_first_name_max_length','2025-03-12 10:25:44.912352'),(15,'user_auth','0001_initial','2025-03-12 10:25:45.824471'),(16,'Order','0001_initial','2025-03-12 10:25:45.895497'),(17,'Order','0002_initial','2025-03-12 10:25:46.257811'),(18,'admin','0001_initial','2025-03-12 10:25:46.458867'),(19,'admin','0002_logentry_remove_auto_add','2025-03-12 10:25:46.468925'),(20,'admin','0003_logentry_add_action_flag_choices','2025-03-12 10:25:46.484576'),(21,'sessions','0001_initial','2025-03-12 10:25:46.538525'),(22,'user_auth','0002_material_printtype_alter_item_material_and_more','2025-03-12 11:13:48.476337'),(23,'user_auth','0003_menu_menuaccess','2025-03-13 05:10:46.710065'),(24,'Order','0003_orderdata_total_cost','2025-03-13 06:50:56.513342'),(25,'user_auth','0004_model_data_alter_user_groups_and_more','2025-03-13 06:50:56.586438'),(26,'user_auth','0005_material_model_id','2025-03-13 06:54:19.066275'),(27,'Order','0004_remove_orderdata_item','2025-03-13 09:05:45.802809'),(28,'user_auth','0006_customer_custom_id','2025-03-14 05:17:58.887867'),(29,'Order','0005_alter_orderitem_qty_invoice_invoiceitem','2025-03-14 05:17:59.541004'),(30,'user_auth','0007_alter_menu_options_alter_menuaccess_options_and_more','2025-03-14 06:09:19.476547'),(31,'user_auth','0008_remove_menuaccess_can_delete_and_more','2025-03-14 06:24:24.431412'),(32,'user_auth','0009_branch_permissions_alter_branch_location','2025-03-14 06:56:04.564827'),(33,'user_auth','0010_remove_branch_permissions_userrole_permissions','2025-03-14 07:02:01.383671'),(34,'user_auth','0011_materialdata','2025-03-15 06:51:06.582556'),(35,'user_auth','0012_alter_item_is_sleeve','2025-03-15 07:27:05.943606'),(36,'Order','0006_orderdata_gst_orderdata_net_cost_orderitem_discount_and_more','2025-03-17 04:53:48.145186'),(37,'user_auth','0013_customer_business_name','2025-03-17 04:53:48.205025'),(39,'user_auth','0014_alter_item_material','2025-03-18 07:03:53.146452'),(40,'user_auth','0015_alter_item_created_at','2025-03-18 07:03:53.353024'),(45,'Order','0007_alter_orderdata_customer_alter_orderitem_item_and_more','2025-03-19 06:43:51.138994'),(46,'Order','0008_orderdata_completed_payment','2025-03-19 06:44:12.649136'),(47,'Order','0009_orderdata_invoice_flag','2025-03-19 06:44:37.966374'),(48,'Order','0010_invoice_back_img_invoice_back_matter_and_more','2025-03-19 06:45:04.332917'),(49,'Order','0011_alter_invoice_invoice_id','2025-03-19 06:45:10.641538'),(50,'Order','0012_alter_invoice_delivery_date','2025-03-19 06:59:05.673390'),(51,'Order','0002_invoice_created_by','2025-03-20 07:09:26.486215'),(52,'user_auth','0016_district_branch_city_branch_district','2025-03-20 10:04:34.795365'),(53,'Order','0003_orderdata_status','2025-03-20 11:03:27.823313'),(54,'user_auth','0017_item_model_alter_item_name','2025-03-24 04:20:03.278813');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('9ac2hll4tkxk6pm6b6rg8kqk5s9p0s83','.eJxVjEEOwiAQRe_C2hCgztC6dN8zkBlgpGpoUtqV8e7apAvd_vfef6lA21rC1vISpqQuCtTpd2OKj1x3kO5Ub7OOc12XifWu6IM2Pc4pP6-H-3dQqJVvzU4YAIWzDABiHUTw2In1FNFw5I7IAhkcenGmPwOST9bbiJQQxav3B_VqOAY:1tuUlX:0dgaHt6jH4qDMeuITR-Rojjz5L3Eqp3gsBbEEPbHiR8','2025-04-01 11:05:47.625518');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_invoice`
--

DROP TABLE IF EXISTS `order_invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_invoice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `invoice_id` varchar(100) NOT NULL,
  `total_cost` decimal(10,2) DEFAULT NULL,
  `discount` decimal(5,2) NOT NULL,
  `gst` decimal(5,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `order_id` bigint DEFAULT NULL,
  `order_item_id_id` bigint DEFAULT NULL,
  `back_img` varchar(100) DEFAULT NULL,
  `back_matter` varchar(255) DEFAULT NULL,
  `customer_id` bigint DEFAULT NULL,
  `net_cost` varchar(30) DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `front_matter` varchar(255) DEFAULT NULL,
  `front_img` varchar(255) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `invoice_id` (`invoice_id`),
  KEY `Order_invoice_order_id_680a7e10_fk_Order_orderdata_id` (`order_id`),
  KEY `Order_invoice_order_item_id_id_53d03ba5_fk_Order_orderitem_id` (`order_item_id_id`),
  KEY `Order_invoice_customer_id_574d60c9_fk_user_auth_customer_id` (`customer_id`),
  KEY `Order_invoice_created_by_id_64e71d06_fk_user_auth_user_id` (`created_by_id`),
  CONSTRAINT `Order_invoice_created_by_id_64e71d06_fk_user_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `user_auth_user` (`id`),
  CONSTRAINT `Order_invoice_customer_id_574d60c9_fk_user_auth_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `user_auth_customer` (`id`),
  CONSTRAINT `Order_invoice_order_id_680a7e10_fk_Order_orderdata_id` FOREIGN KEY (`order_id`) REFERENCES `order_orderdata` (`id`),
  CONSTRAINT `Order_invoice_order_item_id_id_53d03ba5_fk_Order_orderitem_id` FOREIGN KEY (`order_item_id_id`) REFERENCES `order_orderitem` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_invoice`
--

LOCK TABLES `order_invoice` WRITE;
/*!40000 ALTER TABLE `order_invoice` DISABLE KEYS */;
INSERT INTO `order_invoice` VALUES (15,'INV22456',735.00,0.00,35.00,'2025-03-19 09:30:53.493021',59,NULL,'back_images/11_tk53_QhrxfBB.jpg','back2',1,'700','2025-03-18','logos/19-5-3-min_mBp6r1v.jpg','text1','',NULL),(16,'INV81008',1575.00,0.00,75.00,'2025-03-19 09:31:19.432818',58,NULL,'back_images/11_tk53_8JVP2cX.jpg','back2',1,'1500','2025-03-18','logos/19-5-3-min_d7kT9hK.jpg','text1','',NULL),(17,'INV21097',735.00,0.00,35.00,'2025-03-22 07:10:00.273496',60,NULL,'back_images/11_tk53_yMZdWR8.jpg','back2',1,'700','2025-03-18','logos/19-5-3-min_9TAttSd.jpg','text1','',11);
/*!40000 ALTER TABLE `order_invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_invoiceitem`
--

DROP TABLE IF EXISTS `order_invoiceitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_invoiceitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `size` varchar(50) DEFAULT NULL,
  `qty` int unsigned DEFAULT NULL,
  `sleeve_case` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `invoice_id` bigint DEFAULT NULL,
  `item_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Order_invoiceitem_invoice_id_cfcb0070_fk_Order_invoice_id` (`invoice_id`),
  KEY `Order_invoiceitem_item_id_0319e021_fk_user_auth_item_id` (`item_id`),
  CONSTRAINT `Order_invoiceitem_invoice_id_cfcb0070_fk_Order_invoice_id` FOREIGN KEY (`invoice_id`) REFERENCES `order_invoice` (`id`),
  CONSTRAINT `Order_invoiceitem_item_id_0319e021_fk_user_auth_item_id` FOREIGN KEY (`item_id`) REFERENCES `user_auth_item` (`id`),
  CONSTRAINT `order_invoiceitem_chk_1` CHECK ((`qty` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_invoiceitem`
--

LOCK TABLES `order_invoiceitem` WRITE;
/*!40000 ALTER TABLE `order_invoiceitem` DISABLE KEYS */;
INSERT INTO `order_invoiceitem` VALUES (9,'25',3,'full','2025-03-19 09:30:53.500557',NULL,1,15,16),(10,'26',7,'half','2025-03-19 09:30:53.507104',NULL,1,15,18),(11,'25',3,'full','2025-03-19 09:31:19.440059',NULL,1,16,16),(12,'26',7,'half','2025-03-19 09:31:19.446688',NULL,1,16,18),(13,'25',3,'full','2025-03-22 07:10:00.296786',NULL,1,17,16),(14,'26',7,'half','2025-03-22 07:10:00.304650',NULL,1,17,18);
/*!40000 ALTER TABLE `order_invoiceitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_orderdata`
--

DROP TABLE IF EXISTS `order_orderdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_orderdata` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `orderID` varchar(100) NOT NULL,
  `order_date` datetime(6) NOT NULL,
  `delivery_date` date NOT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `front_matter` varchar(255) DEFAULT NULL,
  `front_img` varchar(100) DEFAULT NULL,
  `back_matter` varchar(255) DEFAULT NULL,
  `back_img` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `customer_id` bigint DEFAULT NULL,
  `total_cost` varchar(30) DEFAULT NULL,
  `gst` varchar(30) DEFAULT NULL,
  `net_cost` varchar(30) DEFAULT NULL,
  `Completed_payment` tinyint(1) NOT NULL,
  `invoice_flag` tinyint(1) NOT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `orderID` (`orderID`),
  KEY `Order_orderdata_customer_id_d39dc04c_fk_user_auth_customer_id` (`customer_id`),
  CONSTRAINT `Order_orderdata_customer_id_d39dc04c_fk_user_auth_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `user_auth_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_orderdata`
--

LOCK TABLES `order_orderdata` WRITE;
/*!40000 ALTER TABLE `order_orderdata` DISABLE KEYS */;
INSERT INTO `order_orderdata` VALUES (58,'EKM/2625/0002','2025-03-19 09:18:13.297569','2025-03-18','logos/19-5-3-min_dsPfgLC.jpg','text1','','back2','back_images/11_tk53_KZqk8Zi.jpg','2025-03-19 09:18:13.301426',NULL,1,1,'735.00','35.00','700',0,0,'Pending'),(59,'EKM/2625/0003','2025-03-19 09:18:21.616571','2025-03-18','logos/19-5-3-min_5lOphuC.jpg','text1','','back2','back_images/11_tk53_3Z3siWj.jpg','2025-03-19 09:18:21.620095',NULL,1,1,'735.00','35.00','700',0,0,'Pending'),(60,'EKM/2625/0004','2025-03-19 09:18:29.186227','2025-03-18','logos/19-5-3-min_FqmlhBR.jpg','text1','','back2','back_images/11_tk53_GLiU57O.jpg','2025-03-19 09:18:29.189519',NULL,1,1,'735.00','35.00','700',0,0,'Pending'),(61,'60','2025-03-22 08:31:16.632401','2025-03-18','logos/19-5-3-min_BQxTDAR.jpg','text1','','back2','back_images/11_tk53_twfDFOW.jpg','2025-03-22 08:31:16.655784',NULL,1,1,'735.00','35.00','700',0,0,'Pending'),(63,'656677887','2025-03-22 08:31:58.393749','2025-03-18','logos/19-5-3-min_5oczf8k.jpg','text1','','back2','back_images/11_tk53_n1wQ9WJ.jpg','2025-03-22 08:31:58.397607',NULL,1,1,'735.00','35.00','700',0,0,'Pending');
/*!40000 ALTER TABLE `order_orderdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_orderitem`
--

DROP TABLE IF EXISTS `order_orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_orderitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `size` varchar(50) NOT NULL,
  `qty` int unsigned DEFAULT NULL,
  `sleeve_case` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `item_id` bigint DEFAULT NULL,
  `order_id` bigint DEFAULT NULL,
  `discount` varchar(50) DEFAULT NULL,
  `total_item_cost` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Order_orderitem_item_id_78bc8882_fk_user_auth_item_id` (`item_id`),
  KEY `Order_orderitem_order_id_a5a99dec_fk_Order_orderdata_id` (`order_id`),
  CONSTRAINT `Order_orderitem_item_id_78bc8882_fk_user_auth_item_id` FOREIGN KEY (`item_id`) REFERENCES `user_auth_item` (`id`),
  CONSTRAINT `Order_orderitem_order_id_a5a99dec_fk_Order_orderdata_id` FOREIGN KEY (`order_id`) REFERENCES `order_orderdata` (`id`),
  CONSTRAINT `order_orderitem_chk_1` CHECK ((`qty` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_orderitem`
--

LOCK TABLES `order_orderitem` WRITE;
/*!40000 ALTER TABLE `order_orderitem` DISABLE KEYS */;
INSERT INTO `order_orderitem` VALUES (24,'25',3,'full','2025-03-19 09:18:13.302955',NULL,1,16,58,NULL,NULL),(25,'26',7,'half','2025-03-19 09:18:13.309714',NULL,1,18,58,NULL,NULL),(26,'25',3,'full','2025-03-19 09:18:21.621946',NULL,1,16,59,NULL,NULL),(27,'26',7,'half','2025-03-19 09:18:21.630653',NULL,1,18,59,NULL,NULL),(28,'25',3,'full','2025-03-19 09:18:29.190994',NULL,1,16,60,NULL,NULL),(29,'26',7,'half','2025-03-19 09:18:29.199107',NULL,1,18,60,NULL,NULL),(30,'25',3,'full','2025-03-22 08:31:16.675026',NULL,1,16,61,NULL,NULL),(31,'26',7,'half','2025-03-22 08:31:16.687014',NULL,1,18,61,NULL,NULL),(32,'25',3,'full','2025-03-22 08:31:58.399523',NULL,1,16,63,NULL,NULL),(33,'26',7,'half','2025-03-22 08:31:58.411205',NULL,1,18,63,NULL,NULL);
/*!40000 ALTER TABLE `order_orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_orderpayment`
--

DROP TABLE IF EXISTS `order_orderpayment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_orderpayment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `total_amount` varchar(100) DEFAULT NULL,
  `balance_amount` varchar(100) DEFAULT NULL,
  `paid_amount` varchar(100) DEFAULT NULL,
  `payment_method` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `order_id_id` bigint DEFAULT NULL,
  `customer_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Order_orderpayment_created_by_id_090e7af3_fk_user_auth_user_id` (`created_by_id`),
  KEY `Order_orderpayment_order_id_id_7f80068c_fk_Order_orderdata_id` (`order_id_id`),
  KEY `fk_orderpayment_customer` (`customer_id`),
  CONSTRAINT `fk_orderpayment_customer` FOREIGN KEY (`customer_id`) REFERENCES `user_auth_customer` (`id`) ON DELETE CASCADE,
  CONSTRAINT `Order_orderpayment_created_by_id_090e7af3_fk_user_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `user_auth_user` (`id`),
  CONSTRAINT `Order_orderpayment_order_id_id_7f80068c_fk_Order_orderdata_id` FOREIGN KEY (`order_id_id`) REFERENCES `order_orderdata` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_orderpayment`
--

LOCK TABLES `order_orderpayment` WRITE;
/*!40000 ALTER TABLE `order_orderpayment` DISABLE KEYS */;
INSERT INTO `order_orderpayment` VALUES (8,'735','700','35','Cash','2025-03-20 06:26:15.871650',1,58,1),(9,'735','700','100','Cash','2025-03-20 06:27:07.479760',1,58,1);
/*!40000 ALTER TABLE `order_orderpayment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth_branch`
--

DROP TABLE IF EXISTS `user_auth_branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth_branch` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `code` varchar(255) NOT NULL,
  `location` longtext,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `city` varchar(255) DEFAULT NULL,
  `district` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth_branch`
--

LOCK TABLES `user_auth_branch` WRITE;
/*!40000 ALTER TABLE `user_auth_branch` DISABLE KEYS */;
INSERT INTO `user_auth_branch` VALUES (1,'branch1','EKM','Ernamkulamm','2025-03-13 05:14:54.780613','2025-03-13 05:19:47.171040',0,NULL,NULL),(2,'branch2','CKM','Ernamkulamm','2025-03-13 05:19:05.585994',NULL,1,NULL,NULL),(3,'KICKOFF','TSR0001','PERUMBILAVU BUS STOP,NEAREST TO ANSAR COLLEGE','2025-03-21 07:34:20.309118',NULL,1,'PERUMBILAVU','Thrissur'),(4,'test2','brs009','testy2loc','2025-03-21 08:50:56.933740',NULL,1,'twesrt4','Thrissur'),(5,'test334','jgh89r7','gh7567','2025-03-21 08:54:07.642800',NULL,1,'787','Thrissur');
/*!40000 ALTER TABLE `user_auth_branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth_customer`
--

DROP TABLE IF EXISTS `user_auth_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth_customer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `address1` longtext NOT NULL,
  `address2` longtext,
  `mobile_number1` varchar(15) NOT NULL,
  `mobile_number2` varchar(15) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `gst_no` varchar(15) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `custom_id` varchar(100) NOT NULL,
  `business_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobile_number1` (`mobile_number1`),
  UNIQUE KEY `custom_id` (`custom_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth_customer`
--

LOCK TABLES `user_auth_customer` WRITE;
/*!40000 ALTER TABLE `user_auth_customer` DISABLE KEYS */;
INSERT INTO `user_auth_customer` VALUES (1,'HARISHMA','ADDRESS HOUSE','','953926379',NULL,'hari@gmail.com','09090','2025-03-13 08:51:59.799527','2025-03-14 05:23:45.243618',0,'1',NULL),(2,'John Doe','123 Main Street','Apartment 4B','9876543210',NULL,'johndoe@example.com','22ABCDE1234F1Z5','2025-03-14 05:19:47.583265',NULL,1,'CUSM001',NULL),(3,'John Doe','123 Main Street','Apartment 4B','9876543211',NULL,'johndoee@example.com','22ABCDE1234F1Z5','2025-03-14 05:22:39.380525',NULL,1,'CUSM002',NULL),(4,'John Doe','123 Main Street','Apartment 4B','9876543216',NULL,'johndee@example.com','22ABCDE1234F1Z5','2025-03-14 07:06:23.293538',NULL,1,'CUSM003',NULL),(5,'John Doe','123 Main Street','Apartment 4B','9876543219',NULL,'johndeed@example.com','22ABCDE1234F1Z5','2025-03-14 07:17:37.548591',NULL,1,'CUSM004',NULL),(6,'John Doe','123 Main Street','Apartment 4B','9876543719',NULL,'johndeeSd@example.com','22ABCDE1234F1Z5','2025-03-14 07:26:15.601703',NULL,1,'CUSM005',NULL),(7,'John Doe','123 Main Street','Apartment 4B','9873543719',NULL,'johndejsd@example.com','22ABCDE1234F1Z5','2025-03-14 07:26:59.722178',NULL,1,'CUSM006',NULL),(8,'John Doe','123 Main Street','Apartment 4B','9873743719',NULL,'johnndejsd@example.com','22ABCDE1234F1Z5','2025-03-14 07:34:53.973784',NULL,1,'CUSM007',NULL),(9,'John Doe','123 Main Street','Apartment 4B','9873748719',NULL,'johnndejsd@exxample.com','22ABCDE1234F1Z5','2025-03-14 07:36:53.195293',NULL,1,'CUSM008',NULL),(10,'HARI','123 Main Street','Apartment 4B','9872748719',NULL,'johnndejsd@exple.com','22ABCDE1234F1Z5','2025-03-14 07:38:53.606400',NULL,1,'CUSM009',NULL);
/*!40000 ALTER TABLE `user_auth_customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth_district`
--

DROP TABLE IF EXISTS `user_auth_district`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth_district` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth_district`
--

LOCK TABLES `user_auth_district` WRITE;
/*!40000 ALTER TABLE `user_auth_district` DISABLE KEYS */;
INSERT INTO `user_auth_district` VALUES (4,'Alappuzha\r'),(7,'Ernakulam\r'),(6,'Idukki\r'),(13,'Kannur\r'),(14,'Kasaragode\r'),(2,'Kollam\r'),(5,'Kottayam\r'),(11,'Kozhikode\r'),(10,'Malappuram\r'),(9,'Palakkad\r'),(3,'Pathanamthitta\r'),(1,'Thiruvananthapuram\r'),(8,'Thrissur\r'),(12,'Wayanad\r');
/*!40000 ALTER TABLE `user_auth_district` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth_item`
--

DROP TABLE IF EXISTS `user_auth_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth_item` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `item_code` varchar(100) NOT NULL,
  `item_cost` decimal(10,2) NOT NULL,
  `item_alert` int DEFAULT '0',
  `material_id` bigint DEFAULT NULL,
  `gst` decimal(5,2) DEFAULT NULL,
  `tax` decimal(5,2) DEFAULT NULL,
  `print_type_id` bigint DEFAULT NULL,
  `size` varchar(50) DEFAULT NULL,
  `is_sleeve` varchar(20) DEFAULT NULL,
  `item_description` longtext NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `model_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `item_code` (`item_code`),
  KEY `user_auth_item_material_id_f684c3e2` (`material_id`),
  KEY `user_auth_item_print_type_id_91b04a67` (`print_type_id`),
  KEY `user_auth_item_model_id_51615fc1_fk_user_auth_model_data_id` (`model_id`),
  CONSTRAINT `user_auth_item_model_id_51615fc1_fk_user_auth_model_data_id` FOREIGN KEY (`model_id`) REFERENCES `user_auth_model_data` (`id`),
  CONSTRAINT `user_auth_item_print_type_id_91b04a67_fk_user_auth_printtype_id` FOREIGN KEY (`print_type_id`) REFERENCES `user_auth_printtype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth_item`
--

LOCK TABLES `user_auth_item` WRITE;
/*!40000 ALTER TABLE `user_auth_item` DISABLE KEYS */;
INSERT INTO `user_auth_item` VALUES (8,'JERSEY','JS003',150.00,NULL,1,0.00,0.00,1,NULL,'sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,1),(9,'JERSEY','JS004',150.00,NULL,1,0.00,0.00,2,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(11,'JERSEY','JS006',150.00,NULL,1,0.00,0.00,2,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(12,'JERSEY','JD007',150.00,NULL,2,0.00,0.00,1,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(13,'JERSEY','JD008',150.00,NULL,2,0.00,0.00,1,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(14,'JERSEY','JD009',150.00,NULL,2,0.00,0.00,1,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(15,'JERSEY','JD010',150.00,NULL,2,0.00,0.00,2,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(16,'JERSEY','JD011',150.00,NULL,1,0.00,0.00,2,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(17,'JERSEY','JD012',150.00,NULL,2,0.00,0.00,2,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(18,'JERSEY','JH013',150.00,NULL,3,0.00,0.00,1,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(19,'JERSEY','JH014',150.00,NULL,3,0.00,0.00,1,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(20,'JERSEY','JH015',150.00,NULL,3,0.00,0.00,1,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(21,'JERSEY','JH016',150.00,NULL,3,0.00,0.00,2,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(22,'JERSEY','JH017',150.00,NULL,3,0.00,0.00,2,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(23,'JERSEY','JH018',150.00,NULL,3,0.00,0.00,2,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(24,'T SHIRT','TS019',150.00,NULL,1,0.00,0.00,1,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(25,'T SHIRT','TS020',150.00,NULL,1,0.00,0.00,1,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(26,'T SHIRT','TS021',150.00,NULL,1,0.00,0.00,1,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(27,'T SHIRT','TS022',150.00,NULL,1,0.00,0.00,2,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(28,'T SHIRT','TS023',150.00,NULL,1,0.00,0.00,2,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(29,'T SHIRT','TS024',150.00,NULL,1,0.00,0.00,2,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(30,'T SHIRT','TD025',150.00,NULL,2,0.00,0.00,1,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(31,'T SHIRT','TD026',150.00,NULL,2,0.00,0.00,1,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(32,'T SHIRT','TD027',150.00,NULL,2,0.00,0.00,1,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(33,'T SHIRT','TD028',150.00,NULL,2,0.00,0.00,2,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(34,'T SHIRT','TD029',150.00,NULL,2,0.00,0.00,2,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(35,'T SHIRT','TD030',150.00,NULL,2,0.00,0.00,2,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(36,'T SHIRT','TH031',150.00,NULL,3,0.00,0.00,1,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(37,'T SHIRT','TH032',150.00,NULL,3,0.00,0.00,1,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(38,'T SHIRT','TH033',150.00,NULL,3,0.00,0.00,1,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(39,'T SHIRT','TH034',150.00,NULL,3,0.00,0.00,2,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(40,'T SHIRT','TH035',150.00,NULL,3,0.00,0.00,2,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(41,'T SHIRT','TH036',150.00,NULL,3,0.00,0.00,2,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(42,'SHIRT','SS037',150.00,NULL,1,0.00,0.00,1,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(43,'SHIRT','SS038',150.00,NULL,1,0.00,0.00,1,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(44,'SHIRT','SS039',150.00,NULL,1,0.00,0.00,1,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(45,'SHIRT','SS040',150.00,NULL,1,0.00,0.00,2,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(46,'SHIRT','SS041',150.00,NULL,1,0.00,0.00,2,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(47,'SHIRT','SS042',150.00,NULL,1,0.00,0.00,2,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(48,'SHIRT','SD043',150.00,NULL,2,0.00,0.00,1,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(49,'SHIRT','SD044',150.00,NULL,2,0.00,0.00,1,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(50,'SHIRT','SD045',150.00,NULL,2,0.00,0.00,1,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(51,'SHIRT','SD046',150.00,NULL,2,0.00,0.00,2,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(52,'SHIRT','SD047',150.00,NULL,2,0.00,0.00,2,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(53,'SHIRT','SD048',150.00,NULL,2,0.00,0.00,2,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(54,'SHIRT','SH049',150.00,NULL,3,0.00,0.00,1,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(55,'SHIRT','SH050',150.00,NULL,3,0.00,0.00,1,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(56,'SHIRT','SH051',150.00,NULL,3,0.00,0.00,1,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(57,'SHIRT','SH052',150.00,NULL,3,0.00,0.00,2,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(58,'SHIRT','SH053',150.00,NULL,3,0.00,0.00,2,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(59,'SHIRT','SH054',150.00,NULL,3,0.00,0.00,2,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(60,'CLUB JERSEY - JR','JJS056',150.00,NULL,1,0.00,0.00,1,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(61,'CLUB JERSEY - JR','JJS057',150.00,NULL,1,0.00,0.00,1,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(62,'CLUB JERSEY - JR','JJS058',150.00,NULL,1,0.00,0.00,1,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(63,'CLUB JERSEY - JR','JJS059',150.00,NULL,1,0.00,0.00,2,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(64,'CLUB JERSEY - JR','JJS060',150.00,NULL,1,0.00,0.00,2,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(65,'CLUB JERSEY - JR','JJS061',150.00,NULL,1,0.00,0.00,2,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(66,'CLUB JERSEY - JR','JJD062',150.00,NULL,2,0.00,0.00,1,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(67,'CLUB JERSEY - JR','JJD063',150.00,NULL,2,0.00,0.00,1,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(68,'CLUB JERSEY - JR','JJD064',150.00,NULL,2,0.00,0.00,1,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(69,'CLUB JERSEY - JR','JJD065',150.00,NULL,2,0.00,0.00,2,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(70,'CLUB JERSEY - JR','JJD066',150.00,NULL,2,0.00,0.00,2,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(71,'CLUB JERSEY - JR','JJD067',150.00,NULL,2,0.00,0.00,2,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(72,'CLUB JERSEY - JR','JJH068',150.00,NULL,3,0.00,0.00,1,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(73,'CLUB JERSEY - JR','JJH069',150.00,NULL,3,0.00,0.00,1,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(74,'CLUB JERSEY - JR','JJH070',150.00,NULL,3,0.00,0.00,1,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(75,'CLUB JERSEY - JR','JJH071',150.00,NULL,3,0.00,0.00,2,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(76,'CLUB JERSEY - JR','JJH072',150.00,NULL,3,0.00,0.00,2,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(77,'CLUB JERSEY - JR','JJH073',150.00,NULL,3,0.00,0.00,2,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(78,'CLUB JERSEY - SR','JSS074',150.00,NULL,1,0.00,0.00,1,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(79,'CLUB JERSEY - SR','JSS075',150.00,NULL,1,0.00,0.00,1,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(80,'CLUB JERSEY - SR','JSS076',150.00,NULL,1,0.00,0.00,1,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(81,'CLUB JERSEY - SR','JSS077',150.00,NULL,1,0.00,0.00,2,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(82,'CLUB JERSEY - SR','JSS078',150.00,NULL,1,0.00,0.00,2,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(83,'CLUB JERSEY - SR','JSS079',150.00,NULL,1,0.00,0.00,2,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(84,'CLUB JERSEY - SR','JSD080',150.00,NULL,2,0.00,0.00,1,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(85,'CLUB JERSEY - SR','JSD081',150.00,NULL,2,0.00,0.00,1,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(86,'CLUB JERSEY - SR','JSD082',150.00,NULL,2,0.00,0.00,1,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(87,'CLUB JERSEY - SR','JSD083',150.00,NULL,2,0.00,0.00,2,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(88,'CLUB JERSEY - SR','JSD084',150.00,NULL,2,0.00,0.00,2,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(89,'CLUB JERSEY - SR','JSD085',150.00,NULL,2,0.00,0.00,2,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(90,'CLUB JERSEY - SR','JSH086',150.00,NULL,3,0.00,0.00,1,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(91,'CLUB JERSEY - SR','JSH087',150.00,NULL,3,0.00,0.00,1,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(92,'CLUB JERSEY - SR','JSH088',150.00,NULL,3,0.00,0.00,1,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(93,'CLUB JERSEY - SR','JSH089',150.00,NULL,3,0.00,0.00,2,'','half','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(94,'CLUB JERSEY - SR','JSH090',150.00,NULL,3,0.00,0.00,2,'','full','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(95,'CLUB JERSEY - SR','JSH091',150.00,NULL,3,0.00,0.00,2,'','sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(96,'SHORTS','SSP092',150.00,NULL,4,0.00,0.00,1,'','','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(97,'SHORTS','SSP093',150.00,NULL,4,0.00,0.00,2,'','','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(98,'SHORTS','SSH094',150.00,NULL,5,0.00,0.00,1,'','','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(99,'SHORTS','SSH095',150.00,NULL,5,0.00,0.00,2,'','','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(100,'SHORTS','S2WL096',150.00,NULL,6,0.00,0.00,1,'','','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(101,'SHORTS','S2WL097',150.00,NULL,6,0.00,0.00,2,'','','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(102,'SHORTS','S4WL098',150.00,NULL,7,0.00,0.00,1,'','','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(103,'SHORTS','S4WL099',150.00,NULL,7,0.00,0.00,2,'','','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(104,'SHORTS','SNL100',150.00,NULL,8,0.00,0.00,1,'','','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(105,'SHORTS','SNL101',150.00,NULL,8,0.00,0.00,2,'','','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(106,'SHORTS','SP102',150.00,NULL,9,0.00,0.00,1,'','','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(107,'SHORTS','SP103',150.00,NULL,9,0.00,0.00,2,'','','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(108,'SHORTS','SD104',150.00,NULL,2,0.00,0.00,1,'','','for test','2025-03-24 09:49:26.000000',NULL,1,NULL),(109,'SHORTS','SD105',150.00,NULL,2,0.00,0.00,2,NULL,'sleeveless','for test','2025-03-24 09:49:26.000000',NULL,1,6);
/*!40000 ALTER TABLE `user_auth_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth_material`
--

DROP TABLE IF EXISTS `user_auth_material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth_material` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `model_id_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_auth_material_model_id_id_ace1236e_fk_user_auth` (`model_id_id`),
  CONSTRAINT `user_auth_material_model_id_id_ace1236e_fk_user_auth` FOREIGN KEY (`model_id_id`) REFERENCES `user_auth_model_data` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth_material`
--

LOCK TABLES `user_auth_material` WRITE;
/*!40000 ALTER TABLE `user_auth_material` DISABLE KEYS */;
INSERT INTO `user_auth_material` VALUES (30,'SALINA','2025-03-22 09:26:55.245459',NULL,1,1),(31,'DOT KNIT','2025-03-22 09:27:30.827721',NULL,1,1),(32,'HONEYCOMB','2025-03-22 09:28:07.325866',NULL,1,1),(33,'SALINA','2025-03-22 09:28:31.608128',NULL,1,2),(34,'DOT KNIT','2025-03-22 09:28:38.712381',NULL,1,2),(35,'HONEYCOMB','2025-03-22 09:28:45.641246',NULL,1,2);
/*!40000 ALTER TABLE `user_auth_material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth_materialdata`
--

DROP TABLE IF EXISTS `user_auth_materialdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth_materialdata` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth_materialdata`
--

LOCK TABLES `user_auth_materialdata` WRITE;
/*!40000 ALTER TABLE `user_auth_materialdata` DISABLE KEYS */;
INSERT INTO `user_auth_materialdata` VALUES (1,'SALINA','2025-03-15 06:52:04.831889',NULL,1),(2,'DOT KNIT','2025-03-15 06:52:16.165027',NULL,1),(3,'HONEYCOMB','2025-03-15 06:52:37.441773',NULL,1),(4,'Super Poly','2025-03-15 06:52:51.483310',NULL,1),(5,'Honeycomb','2025-03-15 06:53:08.405787',NULL,1),(6,'2 Way Lycra','2025-03-15 06:53:19.918222',NULL,1),(7,'4 Way Lycra','2025-03-15 06:53:31.546053',NULL,1),(8,'Ns Lycra','2025-03-15 06:53:42.526451',NULL,1),(9,'PP','2025-03-15 06:53:51.890224',NULL,1);
/*!40000 ALTER TABLE `user_auth_materialdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth_menu`
--

DROP TABLE IF EXISTS `user_auth_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth_menu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `level` varchar(50) DEFAULT NULL,
  `icon` varchar(255) DEFAULT NULL,
  `order` int DEFAULT NULL,
  `parent_id` bigint DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_auth_menu_parent_id_ea44a916_fk_user_auth_menu_id` (`parent_id`),
  CONSTRAINT `user_auth_menu_parent_id_ea44a916_fk_user_auth_menu_id` FOREIGN KEY (`parent_id`) REFERENCES `user_auth_menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth_menu`
--

LOCK TABLES `user_auth_menu` WRITE;
/*!40000 ALTER TABLE `user_auth_menu` DISABLE KEYS */;
INSERT INTO `user_auth_menu` VALUES (4,'Customer','1',NULL,1,NULL,'/'),(5,'View_customer_list','2',NULL,1,4,'customer_list'),(6,'Create_customer','2',NULL,1,4,'/create_customer');
/*!40000 ALTER TABLE `user_auth_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth_menu_permissions`
--

DROP TABLE IF EXISTS `user_auth_menu_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth_menu_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `menu_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_auth_menu_permissions_menu_id_permission_id_3a0ae2ca_uniq` (`menu_id`,`permission_id`),
  KEY `user_auth_menu_permi_permission_id_671f54b0_fk_auth_perm` (`permission_id`),
  CONSTRAINT `user_auth_menu_permi_permission_id_671f54b0_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_auth_menu_permissions_menu_id_ec14c497_fk_user_auth_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `user_auth_menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth_menu_permissions`
--

LOCK TABLES `user_auth_menu_permissions` WRITE;
/*!40000 ALTER TABLE `user_auth_menu_permissions` DISABLE KEYS */;
INSERT INTO `user_auth_menu_permissions` VALUES (7,4,77),(8,5,34),(9,5,35),(10,5,36),(11,6,33);
/*!40000 ALTER TABLE `user_auth_menu_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth_menuaccess`
--

DROP TABLE IF EXISTS `user_auth_menuaccess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth_menuaccess` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `menu_id` bigint DEFAULT NULL,
  `icon` varchar(255) DEFAULT NULL,
  `level` varchar(50) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `order` int DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_auth_menuaccess_menu_id_655ba620_fk_user_auth_menu_id` (`menu_id`),
  CONSTRAINT `user_auth_menuaccess_menu_id_655ba620_fk_user_auth_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `user_auth_menu` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth_menuaccess`
--

LOCK TABLES `user_auth_menuaccess` WRITE;
/*!40000 ALTER TABLE `user_auth_menuaccess` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_auth_menuaccess` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth_menuaccess_permissions`
--

DROP TABLE IF EXISTS `user_auth_menuaccess_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth_menuaccess_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `menuaccess_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_auth_menuaccess_per_menuaccess_id_permission_720a28fa_uniq` (`menuaccess_id`,`permission_id`),
  KEY `user_auth_menuaccess_permission_id_c82c1f63_fk_auth_perm` (`permission_id`),
  CONSTRAINT `user_auth_menuaccess_menuaccess_id_82ab880f_fk_user_auth` FOREIGN KEY (`menuaccess_id`) REFERENCES `user_auth_menuaccess` (`id`),
  CONSTRAINT `user_auth_menuaccess_permission_id_c82c1f63_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth_menuaccess_permissions`
--

LOCK TABLES `user_auth_menuaccess_permissions` WRITE;
/*!40000 ALTER TABLE `user_auth_menuaccess_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_auth_menuaccess_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth_model_data`
--

DROP TABLE IF EXISTS `user_auth_model_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth_model_data` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth_model_data`
--

LOCK TABLES `user_auth_model_data` WRITE;
/*!40000 ALTER TABLE `user_auth_model_data` DISABLE KEYS */;
INSERT INTO `user_auth_model_data` VALUES (1,'JERSEY','2025-03-13 06:51:38.818402',NULL,1),(2,'T SHIRT','2025-03-13 06:52:18.646507',NULL,1),(3,'SHIRT','2025-03-13 06:52:33.857464',NULL,1),(4,'CLUB JERSEY - JR','2025-03-13 06:52:44.677700',NULL,1),(5,'CLUB JERSEY - SR','2025-03-13 06:52:53.147308',NULL,1),(6,'SHORTS','2025-03-13 06:53:08.194609',NULL,1),(7,'LOWER','2025-03-13 06:53:25.765272',NULL,1);
/*!40000 ALTER TABLE `user_auth_model_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth_printtype`
--

DROP TABLE IF EXISTS `user_auth_printtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth_printtype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth_printtype`
--

LOCK TABLES `user_auth_printtype` WRITE;
/*!40000 ALTER TABLE `user_auth_printtype` DISABLE KEYS */;
INSERT INTO `user_auth_printtype` VALUES (1,'SUBLIMATION','2025-03-13 07:04:45.133864',NULL,1),(2,'PLAIN','2025-03-13 07:04:52.319720',NULL,1);
/*!40000 ALTER TABLE `user_auth_printtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth_user`
--

DROP TABLE IF EXISTS `user_auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `emp_code` varchar(25) DEFAULT NULL,
  `first_name` varchar(35) NOT NULL,
  `middle_name` varchar(35) DEFAULT NULL,
  `last_name` varchar(35) NOT NULL,
  `dob` date DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `age` varchar(35) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `mobile_number` varchar(15) DEFAULT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `pro_pic` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `branch_id` bigint DEFAULT NULL,
  `role_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `mobile_number` (`mobile_number`),
  KEY `user_auth_user_branch_id_6560315a_fk_user_auth_branch_id` (`branch_id`),
  KEY `user_auth_user_role_id_92b4c322_fk_user_auth_userrole_id` (`role_id`),
  CONSTRAINT `user_auth_user_branch_id_6560315a_fk_user_auth_branch_id` FOREIGN KEY (`branch_id`) REFERENCES `user_auth_branch` (`id`),
  CONSTRAINT `user_auth_user_role_id_92b4c322_fk_user_auth_userrole_id` FOREIGN KEY (`role_id`) REFERENCES `user_auth_userrole` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth_user`
--

LOCK TABLES `user_auth_user` WRITE;
/*!40000 ALTER TABLE `user_auth_user` DISABLE KEYS */;
INSERT INTO `user_auth_user` VALUES (1,'pbkdf2_sha256$870000$N3pOm602YCHCoAYAWlNoad$2mtf46SiUI1RvNyERy3YLeLwQwgpFRng4aEAH6eJdnE=','2025-03-13 04:57:08.431593',1,'theju',1,'2025-03-13 04:56:58.016147',NULL,'thejas',NULL,'NM',NULL,NULL,NULL,'theju@gmail.com',NULL,NULL,'2025-03-13 04:56:58.848387','',1,NULL,1),(2,'pbkdf2_sha256$870000$BUhHDkHk7ZL4Dm93pO5BUo$ZALJpr6ybCtJEJnBkDRTKr1y8vV2wQTsCsXRMixhC/g=',NULL,0,'test1usetr',0,'2025-03-13 05:22:03.474379',NULL,'Test',NULL,'User',NULL,NULL,NULL,'test1user@example.com',NULL,'2025-03-13 05:39:00.215492','2025-03-13 05:22:04.411549','',0,2,2),(3,'pbkdf2_sha256$870000$mRs2EEMGWMZa9SwIpZKCMR$/bn80pnJLrZx77s5uNxwr6Tf5CMBGYD4L3O+RUka/D8=',NULL,0,'test1',0,'2025-03-13 05:24:23.000000',NULL,'Test',NULL,'User',NULL,NULL,NULL,'test1@example.com',NULL,NULL,'2025-03-13 05:24:24.636133','',1,1,2),(4,'pbkdf2_sha256$870000$7MSE0BgnL9so6kpc0lw2jQ$rJzJg/yk1cyGnIpCugrqom3YDh2F4duFp9oo6Nizqrg=',NULL,1,'snila',1,'2025-03-18 11:04:18.000379',NULL,'sani',NULL,'kh',NULL,NULL,NULL,'sanila@gmail.com',NULL,NULL,'2025-03-18 11:04:19.521161','',1,NULL,1),(5,'pbkdf2_sha256$870000$pfMaZwpRklvxHP0oMMtHls$B5aVcS0kK6/T0oqAQeNQgbI1X0Ok+Za9TYIwboQhMys=','2025-03-18 11:05:47.617119',1,'harishma',1,'2025-03-18 11:05:29.333278',NULL,'hari',NULL,'kh',NULL,NULL,NULL,'hari@gmail.com',NULL,NULL,'2025-03-18 11:05:30.091490','',1,NULL,1),(6,'',NULL,0,'kh',0,'2025-03-18 11:06:51.810804',NULL,'',NULL,'',NULL,NULL,NULL,'kh@example.com',NULL,NULL,'2025-03-18 11:06:51.811178','',1,NULL,2),(7,'pbkdf2_sha256$870000$4O8Ip65N5ZA1rsdOe1o0zS$HtOYK5BzYVcL4ljjlGoDTXQZoiahYrOqPexGjdUjkB8=',NULL,0,'kh1',0,'2025-03-18 11:08:47.470885',NULL,'',NULL,'',NULL,NULL,NULL,'kh1@example.com',NULL,NULL,'2025-03-18 11:08:47.471170','',1,NULL,2),(8,'pbkdf2_sha256$870000$8s6Iow3GzBuwKe4b395Ff4$aGYtZCOf4VjLmSyHjeTjeWGHwu+ZSuJhuq7mGcyOzMc=',NULL,0,'kh45451',0,'2025-03-21 10:49:56.786356',NULL,'',NULL,'',NULL,NULL,NULL,'kh5661@example.com',NULL,NULL,'2025-03-21 10:49:56.787093','',1,NULL,2),(9,'pbkdf2_sha256$870000$vZpdcn7tuv9leVFFuyzU0K$2Rl7J6BszkCVQr7SnJ4Cxi96ooOI9IYpZcPl3ZwikW4=',NULL,0,'kh4551',0,'2025-03-21 10:51:16.072354',NULL,'',NULL,'',NULL,NULL,NULL,'kh51@example.com',NULL,NULL,'2025-03-21 10:51:16.072635','',1,NULL,2),(10,'pbkdf2_sha256$870000$i2cdFB4ABRlRU0Nig1UNOz$QegKpwcOZUHFLt1z50X8rxKHU1Lp+vhqhJqj806GVDI=',NULL,0,'kh45751',0,'2025-03-21 10:54:31.406021',NULL,'',NULL,'',NULL,NULL,NULL,'kh517@example.com',NULL,NULL,'2025-03-21 10:54:31.406509','',1,NULL,2),(11,'pbkdf2_sha256$870000$efzLbEtzJknZ5uO0oi9AdF$EeiKMKPKaWyt5S4e6cN0wdcDz203e6rdkKGGmIRDozY=',NULL,0,'kh445751',0,'2025-03-21 10:55:52.000000',NULL,'KICKOFF2','TEST','STAFF',NULL,NULL,NULL,'kh5417@example.com',NULL,NULL,'2025-03-21 10:55:52.443184','',1,3,2),(12,'pbkdf2_sha256$870000$5IXlneLjNzH4vofwbLguhQ$l1qsXBsUDZQizH5NK7zG8QuckvB1OvJ++d5Oo4Ynuwc=',NULL,0,'kh44575901',0,'2025-03-22 06:00:05.416505',NULL,'Test',NULL,'User',NULL,NULL,NULL,'kh541907@example.com',NULL,NULL,'2025-03-22 06:00:05.417009','',1,3,2);
/*!40000 ALTER TABLE `user_auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth_user_groups`
--

DROP TABLE IF EXISTS `user_auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_auth_user_groups_user_id_group_id_6887c85a_uniq` (`user_id`,`group_id`),
  KEY `user_auth_user_groups_group_id_165f3b9d_fk_auth_group_id` (`group_id`),
  CONSTRAINT `user_auth_user_groups_group_id_165f3b9d_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_auth_user_groups_user_id_e339ec14_fk_user_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth_user_groups`
--

LOCK TABLES `user_auth_user_groups` WRITE;
/*!40000 ALTER TABLE `user_auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth_user_user_permissions`
--

DROP TABLE IF EXISTS `user_auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_auth_user_user_perm_user_id_permission_id_4df7833e_uniq` (`user_id`,`permission_id`),
  KEY `user_auth_user_user__permission_id_2c602bd2_fk_auth_perm` (`permission_id`),
  CONSTRAINT `user_auth_user_user__permission_id_2c602bd2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_auth_user_user__user_id_31fb400e_fk_user_auth` FOREIGN KEY (`user_id`) REFERENCES `user_auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth_user_user_permissions`
--

LOCK TABLES `user_auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `user_auth_user_user_permissions` DISABLE KEYS */;
INSERT INTO `user_auth_user_user_permissions` VALUES (1,3,34),(2,3,35),(3,3,36),(4,3,77);
/*!40000 ALTER TABLE `user_auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth_userrole`
--

DROP TABLE IF EXISTS `user_auth_userrole`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth_userrole` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth_userrole`
--

LOCK TABLES `user_auth_userrole` WRITE;
/*!40000 ALTER TABLE `user_auth_userrole` DISABLE KEYS */;
INSERT INTO `user_auth_userrole` VALUES (1,'Admin','2025-03-13 04:56:58.011228',NULL,1),(2,'User','2025-03-13 05:22:00.260100',NULL,1);
/*!40000 ALTER TABLE `user_auth_userrole` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth_userrole_permissions`
--

DROP TABLE IF EXISTS `user_auth_userrole_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth_userrole_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `userrole_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_auth_userrole_permi_userrole_id_permission_i_0f49121d_uniq` (`userrole_id`,`permission_id`),
  KEY `user_auth_userrole_p_permission_id_95c1f36a_fk_auth_perm` (`permission_id`),
  CONSTRAINT `user_auth_userrole_p_permission_id_95c1f36a_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_auth_userrole_p_userrole_id_221815a8_fk_user_auth` FOREIGN KEY (`userrole_id`) REFERENCES `user_auth_userrole` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth_userrole_permissions`
--

LOCK TABLES `user_auth_userrole_permissions` WRITE;
/*!40000 ALTER TABLE `user_auth_userrole_permissions` DISABLE KEYS */;
INSERT INTO `user_auth_userrole_permissions` VALUES (2,2,36);
/*!40000 ALTER TABLE `user_auth_userrole_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-24 13:37:30
