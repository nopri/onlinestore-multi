-- MySQL dump 10.11
--
-- Host: localhost    Database: nopri_os1
-- ------------------------------------------------------
-- Server version	5.0.37

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
-- Table structure for table `ms_bank`
--

DROP TABLE IF EXISTS `ms_bank`;
CREATE TABLE `ms_bank` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(64) default NULL,
  `account` varchar(64) default NULL,
  `currency_id` int(11) default NULL,
  `holder` varchar(64) default NULL,
  `branch` varchar(64) default NULL,
  `address` varchar(255) default NULL,
  `country` varchar(64) default NULL,
  `swift` varchar(64) default NULL,
  `active` tinyint(1) default '1',
  `note` text,
  `log_id` int(11) default NULL,
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ms_bank`
--

LOCK TABLES `ms_bank` WRITE;
/*!40000 ALTER TABLE `ms_bank` DISABLE KEYS */;
/*!40000 ALTER TABLE `ms_bank` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ms_blog_category`
--

DROP TABLE IF EXISTS `ms_blog_category`;
CREATE TABLE `ms_blog_category` (
  `id` int(11) NOT NULL auto_increment,
  `log_id` int(11) default NULL,
  `category` mediumtext,
  `active` tinyint(1) default '1',
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ms_blog_category`
--

LOCK TABLES `ms_blog_category` WRITE;
/*!40000 ALTER TABLE `ms_blog_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `ms_blog_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ms_category`
--

DROP TABLE IF EXISTS `ms_category`;
CREATE TABLE `ms_category` (
  `id` int(11) NOT NULL auto_increment,
  `name` mediumtext,
  `priority` int(11) default NULL,
  `active` tinyint(1) default '1',
  `log_id` int(11) default NULL,
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ms_category`
--

LOCK TABLES `ms_category` WRITE;
/*!40000 ALTER TABLE `ms_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `ms_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ms_config`
--

DROP TABLE IF EXISTS `ms_config`;
CREATE TABLE `ms_config` (
  `param` varchar(64) NOT NULL default '',
  `value` text,
  `log_id` int(11) default NULL,
  PRIMARY KEY  (`param`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ms_config`
--

LOCK TABLES `ms_config` WRITE;
/*!40000 ALTER TABLE `ms_config` DISABLE KEYS */;
INSERT INTO `ms_config` VALUES ('allow_user','',NULL),('another_email','',NULL),('blog_show_style','date',NULL),('cart_check_stock','',NULL),('currency','',NULL),('expose_error','1',NULL),('extra_info','',NULL),('general_error_message','',NULL),('homepage','',NULL),('invoice_extra_info','',NULL),('invoice_show_bank','',NULL),('invoice_show_paypal','',NULL),('lang','',NULL),('logo_file','',NULL),('news_max','5',NULL),('offline','1',NULL),('payment_month','12',NULL),('promo_host','',NULL),('secure','',NULL),('site_description','',NULL),('site_keywords','',NULL),('sticky_info','',NULL),('template','default',NULL),('template_param','',NULL),('use_cart','',NULL);
/*!40000 ALTER TABLE `ms_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ms_currency`
--

DROP TABLE IF EXISTS `ms_currency`;
CREATE TABLE `ms_currency` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(8) default NULL,
  `csymbol` varchar(8) default NULL,
  `log_id` int(11) default NULL,
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ms_currency`
--

LOCK TABLES `ms_currency` WRITE;
/*!40000 ALTER TABLE `ms_currency` DISABLE KEYS */;
INSERT INTO `ms_currency` VALUES (1,'IDR','Rp',NULL,NULL),(2,'USD','$',NULL,NULL),(3,'SGD','$',NULL,NULL),(4,'MYR','RM',NULL,NULL),(5,'HKD','$',NULL,NULL),(6,'JPY','¥',NULL,NULL),(7,'CNY','¥',NULL,NULL),(8,'GBP','£',NULL,NULL),(9,'AUD','$',NULL,NULL),(10,'NZD','$',NULL,NULL);
/*!40000 ALTER TABLE `ms_currency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ms_file`
--

DROP TABLE IF EXISTS `ms_file`;
CREATE TABLE `ms_file` (
  `id` int(11) NOT NULL auto_increment,
  `log_id` int(11) default NULL,
  `name` varchar(255) default NULL,
  `name_add` varchar(8) default NULL,
  `size` bigint(20) default NULL,
  `description` varchar(255) default NULL,
  `type` varchar(255) default NULL,
  `type_options` text,
  `disposition` varchar(255) default NULL,
  `disposition_options` text,
  `content` mediumblob,
  `date_file` datetime default NULL,
  `headers` text,
  `purpose` varchar(64) default NULL,
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ms_file`
--

LOCK TABLES `ms_file` WRITE;
/*!40000 ALTER TABLE `ms_file` DISABLE KEYS */;
/*!40000 ALTER TABLE `ms_file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ms_group`
--

DROP TABLE IF EXISTS `ms_group`;
CREATE TABLE `ms_group` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(64) default NULL,
  `extra` text,
  `log_id` int(11) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ms_group`
--

LOCK TABLES `ms_group` WRITE;
/*!40000 ALTER TABLE `ms_group` DISABLE KEYS */;
INSERT INTO `ms_group` VALUES (1,'ADMIN',NULL,NULL),(2,'USER',NULL,NULL);
/*!40000 ALTER TABLE `ms_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ms_link`
--

DROP TABLE IF EXISTS `ms_link`;
CREATE TABLE `ms_link` (
  `id` int(11) NOT NULL auto_increment,
  `code` text,
  `purpose` varchar(64) default NULL,
  `log_id` int(11) default NULL,
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ms_link`
--

LOCK TABLES `ms_link` WRITE;
/*!40000 ALTER TABLE `ms_link` DISABLE KEYS */;
/*!40000 ALTER TABLE `ms_link` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ms_payment_type`
--

DROP TABLE IF EXISTS `ms_payment_type`;
CREATE TABLE `ms_payment_type` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(64) default NULL,
  `log_id` int(11) default NULL,
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ms_payment_type`
--

LOCK TABLES `ms_payment_type` WRITE;
/*!40000 ALTER TABLE `ms_payment_type` DISABLE KEYS */;
INSERT INTO `ms_payment_type` VALUES (1,'Cash',NULL,NULL),(2,'Cash On Delivery',NULL,NULL),(3,'Bank/Wire Transfer',NULL,NULL),(11,'Credit',NULL,NULL),(21,'Debit Card',NULL,NULL),(22,'Credit Card',NULL,NULL),(31,'PayPal',NULL,NULL),(32,'2CO',NULL,NULL),(33,'MoneyBookers',NULL,NULL),(51,'Voucher',NULL,NULL),(81,'Gift Card',NULL,NULL),(99,'Other',NULL,NULL);
/*!40000 ALTER TABLE `ms_payment_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ms_paypal`
--

DROP TABLE IF EXISTS `ms_paypal`;
CREATE TABLE `ms_paypal` (
  `id` int(11) NOT NULL auto_increment,
  `account` varchar(255) default NULL,
  `active` tinyint(1) default '1',
  `log_id` int(11) default NULL,
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ms_paypal`
--

LOCK TABLES `ms_paypal` WRITE;
/*!40000 ALTER TABLE `ms_paypal` DISABLE KEYS */;
/*!40000 ALTER TABLE `ms_paypal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ms_product`
--

DROP TABLE IF EXISTS `ms_product`;
CREATE TABLE `ms_product` (
  `id` int(11) NOT NULL auto_increment,
  `name` mediumtext,
  `category_id` int(11) default NULL,
  `description` mediumtext,
  `full_info` mediumtext,
  `file_id` int(11) default NULL,
  `related` text,
  `active` tinyint(1) default '1',
  `priority` int(11) default NULL,
  `allow_comment` tinyint(1) default '0',
  `log_id` int(11) default NULL,
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ms_product`
--

LOCK TABLES `ms_product` WRITE;
/*!40000 ALTER TABLE `ms_product` DISABLE KEYS */;
/*!40000 ALTER TABLE `ms_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ms_product_variant`
--

DROP TABLE IF EXISTS `ms_product_variant`;
CREATE TABLE `ms_product_variant` (
  `id` int(11) NOT NULL auto_increment,
  `product_id` int(11) default NULL,
  `name` mediumtext,
  `stock` int(11) default NULL,
  `price` decimal(24,8) default NULL,
  `currency_id` int(11) default NULL,
  `taxratio` decimal(24,8) default NULL,
  `variant_file_id` int(11) default NULL,
  `active` tinyint(1) default '1',
  `log_id` int(11) default NULL,
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ms_product_variant`
--

LOCK TABLES `ms_product_variant` WRITE;
/*!40000 ALTER TABLE `ms_product_variant` DISABLE KEYS */;
/*!40000 ALTER TABLE `ms_product_variant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ms_redirect`
--

DROP TABLE IF EXISTS `ms_redirect`;
CREATE TABLE `ms_redirect` (
  `id` int(11) NOT NULL auto_increment,
  `url` varchar(255) default NULL,
  `target` varchar(255) default NULL,
  `type` varchar(64) default NULL,
  `log_id` int(11) default NULL,
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ms_redirect`
--

LOCK TABLES `ms_redirect` WRITE;
/*!40000 ALTER TABLE `ms_redirect` DISABLE KEYS */;
/*!40000 ALTER TABLE `ms_redirect` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ms_user`
--

DROP TABLE IF EXISTS `ms_user`;
CREATE TABLE `ms_user` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(64) default NULL,
  `group_id` int(11) default NULL,
  `password` varchar(64) default NULL,
  `first_name` varchar(64) default NULL,
  `last_name` varchar(64) default NULL,
  `email` text,
  `phone` text,
  `fax` text,
  `web` text,
  `icontact` text,
  `acontact` text,
  `govid` text,
  `address` text,
  `active` tinyint(1) default '1',
  `payment` text,
  `photo` mediumblob,
  `log_id` int(11) default NULL,
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ms_user`
--

LOCK TABLES `ms_user` WRITE;
/*!40000 ALTER TABLE `ms_user` DISABLE KEYS */;
INSERT INTO `ms_user` VALUES (1,'admin',1,'21232f297a57a5a743894a0e4a801fc3',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `ms_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ms_user_content`
--

DROP TABLE IF EXISTS `ms_user_content`;
CREATE TABLE `ms_user_content` (
  `id` int(11) NOT NULL auto_increment,
  `page` mediumtext,
  `content` mediumtext,
  `active` tinyint(1) default '1',
  `show_in_menu` int(11) default NULL,
  `priority` int(11) default NULL,
  `log_id` int(11) default NULL,
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ms_user_content`
--

LOCK TABLES `ms_user_content` WRITE;
/*!40000 ALTER TABLE `ms_user_content` DISABLE KEYS */;
/*!40000 ALTER TABLE `ms_user_content` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ms_yahoo`
--

DROP TABLE IF EXISTS `ms_yahoo`;
CREATE TABLE `ms_yahoo` (
  `id` int(11) NOT NULL auto_increment,
  `account` varchar(255) default NULL,
  `type` varchar(8) default NULL,
  `log_id` int(11) default NULL,
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ms_yahoo`
--

LOCK TABLES `ms_yahoo` WRITE;
/*!40000 ALTER TABLE `ms_yahoo` DISABLE KEYS */;
/*!40000 ALTER TABLE `ms_yahoo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tr_blog`
--

DROP TABLE IF EXISTS `tr_blog`;
CREATE TABLE `tr_blog` (
  `id` int(11) NOT NULL auto_increment,
  `log_id` int(11) default NULL,
  `category_id` int(11) default NULL,
  `date_news` datetime default NULL,
  `title` mediumtext,
  `description` mediumtext,
  `blog` mediumtext,
  `allow_comment` tinyint(1) default '0',
  `active` tinyint(1) default '1',
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tr_blog`
--

LOCK TABLES `tr_blog` WRITE;
/*!40000 ALTER TABLE `tr_blog` DISABLE KEYS */;
/*!40000 ALTER TABLE `tr_blog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tr_comment`
--

DROP TABLE IF EXISTS `tr_comment`;
CREATE TABLE `tr_comment` (
  `id` int(11) NOT NULL auto_increment,
  `log_id` int(11) default NULL,
  `date_comment` datetime default NULL,
  `product_id` int(11) default NULL,
  `blog_id` int(11) default NULL,
  `nested_comment_id` int(11) default NULL,
  `url` varchar(255) default NULL,
  `author` varchar(64) default NULL,
  `email` varchar(255) default NULL,
  `web` varchar(255) default NULL,
  `comment` text,
  `published` tinyint(1) default NULL,
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tr_comment`
--

LOCK TABLES `tr_comment` WRITE;
/*!40000 ALTER TABLE `tr_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `tr_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tr_faq`
--

DROP TABLE IF EXISTS `tr_faq`;
CREATE TABLE `tr_faq` (
  `id` int(11) NOT NULL auto_increment,
  `log_id` int(11) default NULL,
  `category` mediumtext,
  `question` mediumtext,
  `answer` mediumtext,
  `file_id` int(11) default NULL,
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tr_faq`
--

LOCK TABLES `tr_faq` WRITE;
/*!40000 ALTER TABLE `tr_faq` DISABLE KEYS */;
/*!40000 ALTER TABLE `tr_faq` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tr_invoice_detail`
--

DROP TABLE IF EXISTS `tr_invoice_detail`;
CREATE TABLE `tr_invoice_detail` (
  `id` int(11) NOT NULL auto_increment,
  `header_id` int(11) default NULL,
  `product_variant` int(11) default NULL,
  `saved_price` decimal(24,8) default NULL,
  `saved_tax` decimal(24,8) default NULL,
  `amount` int(11) default NULL,
  `log_id` int(11) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tr_invoice_detail`
--

LOCK TABLES `tr_invoice_detail` WRITE;
/*!40000 ALTER TABLE `tr_invoice_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `tr_invoice_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tr_invoice_header`
--

DROP TABLE IF EXISTS `tr_invoice_header`;
CREATE TABLE `tr_invoice_header` (
  `id` int(11) NOT NULL auto_increment,
  `cart_id` varchar(64) default NULL,
  `log_id` int(11) default NULL,
  `total` decimal(24,8) default NULL,
  `date_purchase` datetime default NULL,
  `date_due` datetime default NULL,
  `date_paid` datetime default NULL,
  `payment_type` int(11) default NULL,
  `used_currency` int(11) default NULL,
  `cust_name` varchar(64) default NULL,
  `cust_email` varchar(255) default NULL,
  `ship_addr` text,
  `note` text,
  `payment_info` text,
  `confirm_info` text,
  `invoice_text` mediumtext,
  `invoice_lang` varchar(8) default NULL,
  `done` tinyint(1) default '0',
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tr_invoice_header`
--

LOCK TABLES `tr_invoice_header` WRITE;
/*!40000 ALTER TABLE `tr_invoice_header` DISABLE KEYS */;
/*!40000 ALTER TABLE `tr_invoice_header` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tr_log`
--

DROP TABLE IF EXISTS `tr_log`;
CREATE TABLE `tr_log` (
  `id` int(11) NOT NULL auto_increment,
  `date_log` datetime default NULL,
  `date_log_last` datetime default NULL,
  `activity` int(11) default NULL,
  `ip` varchar(64) default NULL,
  `country` varchar(64) default NULL,
  `referer` varchar(255) default NULL,
  `url` varchar(255) default NULL,
  `url_last` varchar(255) default NULL,
  `method` varchar(8) default NULL,
  `user_agent` varchar(255) default NULL,
  `user_id` int(11) default NULL,
  `user_id_last` int(11) default NULL,
  `login_activity` mediumtext,
  `audit` mediumtext,
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tr_log`
--

LOCK TABLES `tr_log` WRITE;
/*!40000 ALTER TABLE `tr_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `tr_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tr_news`
--

DROP TABLE IF EXISTS `tr_news`;
CREATE TABLE `tr_news` (
  `id` int(11) NOT NULL auto_increment,
  `log_id` int(11) default NULL,
  `date_news` datetime default NULL,
  `title` mediumtext,
  `description` mediumtext,
  `news` mediumtext,
  `file_id` int(11) default NULL,
  `extra` text,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tr_news`
--

LOCK TABLES `tr_news` WRITE;
/*!40000 ALTER TABLE `tr_news` DISABLE KEYS */;
/*!40000 ALTER TABLE `tr_news` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-06-08  6:25:04
