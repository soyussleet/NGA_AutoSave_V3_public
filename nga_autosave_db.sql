-- MySQL dump 10.13  Distrib 5.7.26, for Win64 (x86_64)
--
-- Host: localhost    Database: nga_autosave
-- ------------------------------------------------------
-- Server version	5.7.26

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `monitoring_boards`
--

DROP TABLE IF EXISTS `monitoring_boards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `monitoring_boards` (
  `fidOrStid` varchar(50) NOT NULL COMMENT '版面id，以“fid=111”的形式',
  `fidTitle` varchar(255) DEFAULT NULL COMMENT '版面名称',
  PRIMARY KEY (`fidOrStid`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `monitoring_posts`
--

DROP TABLE IF EXISTS `monitoring_posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `monitoring_posts` (
  `tid` int(30) NOT NULL COMMENT '帖子id',
  `tidTitle` varchar(255) DEFAULT NULL COMMENT '帖子标题',
  `savedFilePath` varchar(255) DEFAULT NULL COMMENT '文件保存路径',
  `poster` varchar(255) DEFAULT NULL COMMENT '发帖人',
  `posterUrl` varchar(255) DEFAULT NULL COMMENT '发帖人url',
  `posterLocation` varchar(255) DEFAULT NULL COMMENT '发帖人ip属地',
  `validState` int(255) DEFAULT NULL COMMENT '帖子状态。1：正常；2：被锁；3：超时但仍暂存；4：超时删除前最后访问；5：确认超时',
  `lastPage` varchar(255) DEFAULT NULL COMMENT '末页页码',
  `repliesCnt` int(255) DEFAULT NULL COMMENT '回复数',
  `firstPostTime` datetime DEFAULT NULL COMMENT '发帖时间',
  `finalReplayTime` datetime DEFAULT NULL COMMENT '最终回帖时间',
  `fidOrStid` varchar(255) DEFAULT NULL COMMENT '版面id',
  `retryCnt` int(255) DEFAULT NULL COMMENT '帖子无法访问时的重试次数，默认超过10次重试都失败时设置帖子状态为被锁\r\n',
  `anonymousPoster` tinyint(255) DEFAULT NULL COMMENT '是否匿名',
  PRIMARY KEY (`tid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-04  1:33:09
