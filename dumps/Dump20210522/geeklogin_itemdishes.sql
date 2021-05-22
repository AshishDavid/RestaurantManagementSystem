-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: geeklogin
-- ------------------------------------------------------
-- Server version	8.0.24

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
-- Table structure for table `itemdishes`
--

DROP TABLE IF EXISTS `itemdishes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `itemdishes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `categoryId` int NOT NULL,
  `imagePath` varchar(450) NOT NULL,
  `enabled` tinyint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `CategoryId_idx` (`categoryId`),
  CONSTRAINT `CategoryId` FOREIGN KEY (`categoryId`) REFERENCES `categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itemdishes`
--

LOCK TABLES `itemdishes` WRITE;
/*!40000 ALTER TABLE `itemdishes` DISABLE KEYS */;
INSERT INTO `itemdishes` VALUES (1,'Samosa','Samosas are a typical pie from India but also from other nearby countries such as Pakistan or Tibet. It is a dish that is also common to find in Indian restaurants or kebabs in Europe',25,1,'static/images/samosa.jpg',1),(2,'Masala Dosa','The masala dosa is a kind of crêpe or galette rolled with potatoes, onion, curry, turmeric, coriander, rice and lentils. It is a forceful dish, since these and many more ingredients are hidden inside this crêpe accompanied by a coconut chutney',20,1,'static/images/masala-dosa.jpg',1),(3,'Chole Bhature','When you are in Delhi, the capital of India, you cannot miss the chole batura. It is a puffy fried bread that is eaten with chole, a spicy chickpea paste and spices.',15,1,'static/images/chole.jpg',1),(4,'Bhelpuri','This snack is made with a base of chickpea flour noodles, puffed rice, and tamarind sauce.',20,1,'static/images/bhelpuri.jpg',1),(5,'Kati roll','If you want to try an authentic kebab, you are sure to love the kati rolls: a rolled paratha bread dough with lamb and vegetables inside',19,1,'static/images/kathiRol.jpg',1),(6,'Daulat ki chaat','Daulat ki chaat is a kind of souffle - as the Indian food critic Pushpesh Pant calls it - made with milk, cream, sugar, pistachios and spices such as saffron.',20,1,'static/images/kichaat.jpg',1),(7,'Kashmiri Aloo Dum','Kashmiri Aloo Dum is a vegetarian potato-based dish. It is a recipe that is part of the traditional gastronomic culture of the Kashmir region, in the state of Jammu and Kashmir, in the north of the country.',25,2,'static/images/AlooDum.jpg',1),(8,'Pollo Tandoori','Tandoori chicken is a very popular dish in Southeast Asian cuisine. It consists of a chicken roasted in the oven with spices. In fact, tandoor means clay oven and it is cooked with firewood and charcoal',20,2,'static/images/tandori.jpg',1),(9,'Pollo Tikka Masala','Chicken marinated with baked yogurt and spices - and masala sauce. Masala literally means \"mixture of spices\", so the dish has a very aromatic flavor.',16,2,'static/images/pollotikamasala.jpg',1),(10,'Jalebi','These sweets are made from maida flour, sugar and oil and are bathed in a syrup with cardamom, saffron and lemon, which gives them a very characteristic flavor',4,3,'static/images/jalebi.jpg',1),(11,'Mithaa paan','The paan is made up of a rolled betel leaf that contains other ingredients, usually salty. In the case of mithaa paan, the taste is sweet (thanks to the sweetened fennel, cardamom or coconut, depending on the recipe) and therefore it is especially pleasant for both children and adults',3,3,'static/images/Mithaapaan.jpg',1),(12,' Falooda','And if what you are looking for is a refreshing drink, a perfect alternative is the falooda. This drink is made with milk, basil seeds, ice cream, vermicelli noodles, fruit, and ice cream',3,3,'static/images/Falooda.jpg',1),(13,'Masala chai','The masala chai is a tea that is boiled with water and milk. As is common in Indian sweet and savory dishes, this drink is also accompanied by various spices, such as cardamom, cloves or pepper.',2,3,'static/images/chai.jpg',1),(14,'Chaas','Chaas is a typical drink throughout the country. It is characterized by being a drink made from yogurt, which gives it a slightly creamy texture, very cold water, salt and spices such as cumin. The yogurt can be of the day or a yogurt that is already a little sour, which will give it a slightly stronger flavor',2,3,'static/images/Chaas.jpg',1);
/*!40000 ALTER TABLE `itemdishes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-22 17:09:26
