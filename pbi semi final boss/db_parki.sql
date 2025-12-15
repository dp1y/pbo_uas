/*
SQLyog Community v13.1.9 (64 bit)
MySQL - 8.0.30 : Database - parkiran
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`parkiran` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `parkiran`;

/*Table structure for table `bus` */

DROP TABLE IF EXISTS `bus`;

CREATE TABLE `bus` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nopol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `kategori` varchar(10) DEFAULT NULL,
  `kapasitas` int DEFAULT NULL,
  `tarif` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `bus` */

/*Table structure for table `kendaraan` */

DROP TABLE IF EXISTS `kendaraan`;

CREATE TABLE `kendaraan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nopol` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `waktu_masuk` datetime DEFAULT NULL,
  `petugas_masuk` varchar(20) DEFAULT NULL,
  `waktu_keluar` datetime DEFAULT NULL,
  `petugas_keluar` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `kendaraan` */

insert  into `kendaraan`(`id`,`nopol`,`waktu_masuk`,`petugas_masuk`,`waktu_keluar`,`petugas_keluar`,`status`) values 
(2,'AG 1 N','2025-12-02 09:05:10','Jung',NULL,NULL,'parkir'),
(3,'AG 2 N','2025-12-02 09:05:45','Frans','2025-12-02 09:06:04','Dapy','keluar'),
(4,'AG 3 N','2025-12-02 09:06:16','Dapy','2025-12-02 09:07:43','Jung','keluar'),
(5,'AG 4 N','2025-12-02 09:08:04','Dapy','2025-12-02 09:08:57','Jung','keluar'),
(6,'AG 5 N','2025-12-02 09:08:41','Dapy','2025-12-02 09:09:03','Jung','keluar');

/*Table structure for table `kendaraan_pribadi` */

DROP TABLE IF EXISTS `kendaraan_pribadi`;

CREATE TABLE `kendaraan_pribadi` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nopol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `tipe` varchar(10) DEFAULT NULL,
  `tarif` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `kendaraan_pribadi` */

insert  into `kendaraan_pribadi`(`id`,`nopol`,`tipe`,`tarif`) values 
(1,'AG 1 N','Motor',2500),
(2,'AG 1 N','Motor',2500);

/*Table structure for table `level` */

DROP TABLE IF EXISTS `level`;

CREATE TABLE `level` (
  `id` int NOT NULL,
  `level` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `level` */

insert  into `level`(`id`,`level`) values 
(1,'admin'),
(2,'kasir');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `username` varchar(55) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `nama` varchar(55) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `password` varchar(55) DEFAULT NULL,
  `level` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `user` */

insert  into `user`(`username`,`nama`,`password`,`level`) values 
('Admin','Admin','123','Admin'),
('Dapy','Dapy','123','Kasir'),
('Frans','Frans','123','Kasir'),
('Jung','Jung','123','Kasir');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
