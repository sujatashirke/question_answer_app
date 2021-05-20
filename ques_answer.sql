-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 20, 2021 at 02:59 PM
-- Server version: 10.4.8-MariaDB
-- PHP Version: 7.1.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ques_answer`
--

-- --------------------------------------------------------

--
-- Table structure for table `ques_ans`
--

CREATE TABLE `ques_ans` (
  `q_id` int(11) NOT NULL,
  `question` varchar(500) NOT NULL,
  `answer` varchar(500) DEFAULT NULL,
  `asked_by` int(11) DEFAULT NULL,
  `answered_by` int(11) DEFAULT NULL,
  `qa_dttime` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `ques_ans`
--

INSERT INTO `ques_ans` (`q_id`, `question`, `answer`, `asked_by`, `answered_by`, `qa_dttime`) VALUES
(1, 'where do you live', 'I live in wadala', 3, 3, '2021-05-04 17:48:12'),
(3, 'what is your name', 'My name is sujata', 3, 4, '2021-05-04 18:23:42'),
(4, 'what is our county name', 'india', 1, 1, '2021-05-07 23:50:50'),
(5, 'what is our county name', 'america', 1, 1, '2021-05-07 23:51:46'),
(6, 'how are you', 'i am fine', 1, 1, '2021-05-11 17:16:59'),
(7, 'which fruit do you like', 'apple', 1, 19, '2021-05-12 17:45:05'),
(8, 'what is your son name', NULL, 1, 1, '2021-05-12 17:57:32'),
(9, 'which color do you like', 'pink', 1, 19, '2021-05-12 18:04:27');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(300) NOT NULL,
  `admin` tinyint(1) DEFAULT NULL,
  `dttime` datetime DEFAULT current_timestamp()
) ;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `admin`, `dttime`) VALUES
(1, 'sujata', 'sujata', 1, '2021-05-04 16:54:24'),
(2, 'expert', 'expert', 0, '2021-05-04 16:55:21'),
(3, 'sanvi', 'sanvi', 0, '2021-05-04 17:40:15'),
(4, 'expert2', 'expert2', 0, '2021-05-04 17:40:55'),
(19, 'vinod', 'pbkdf2:sha256:150000$4vBhF4ws$5bb06bc6c19d4cfd6469e7ab0b412c48b7f6b3122dcdc6b5947508f30ed4c195', 1, '2021-05-12 17:36:03'),
(20, 'sonal', 'pbkdf2:sha256:150000$G1q8QNsn$d0c0785b3d7ec7d5b2a753fe0ff2be71d9f2cb418069ffc893f42161f933f36c', 0, '2021-05-12 17:36:28'),
(27, 'vedu', 'pbkdf2:sha256:150000$VwcGsxYV$b15bb84ffab6e3c4fba35b151ec02e286459ba2d9d169abee65ac7954c4961b1', 0, '2021-05-12 17:57:04');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ques_ans`
--
ALTER TABLE `ques_ans`
  ADD PRIMARY KEY (`q_id`),
  ADD KEY `asked_by` (`asked_by`),
  ADD KEY `answered_by` (`answered_by`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ques_ans`
--
ALTER TABLE `ques_ans`
  MODIFY `q_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ques_ans`
--
ALTER TABLE `ques_ans`
  ADD CONSTRAINT `ques_ans_ibfk_1` FOREIGN KEY (`asked_by`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `ques_ans_ibfk_2` FOREIGN KEY (`answered_by`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
