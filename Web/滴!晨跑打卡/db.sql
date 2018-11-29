create database cgctf default character set utf8 collate utf8_general_ci;

use cgctf;


CREATE TABLE IF NOT EXISTS `pcnumber` (
  `id` int(100) NOT NULL,
  `bigtime` varchar(255) NOT NULL,
  `smalltime` varchar(255) NOT NULL,
  `flag` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `pcnumber`
--

INSERT INTO `pcnumber` (`id`, `bigtime`, `smalltime`) VALUES
(8, '2018.09.13', '07:02'),
(7, '2018.09.13', '06:55'),
(6, '2018.09.12', '06:53'),
(5, '2018.09.12', '06:49'),
(4, '2018.09.11', '06:59'),
(3, '2018.09.11', '06:52'),
(2, '2018.09.10', '06:56'),
(1, '2018.09.10', '06:50'),
(9, '2018.09.19', '06:57'),
(10, '2018.09.21', '07:01'),
(11, '2018.09.20', '06:52'),
(12, '2018.09.20', '06:59'),
(13, '2018.09.21', '06:53'),
(14, '2018.09.21', '06:59'),
(15, '2018.09.22', '06:55'),
(16, '2018.09.22', '07:02');
INSERT INTO `pcnumber` (`id`, `bigtime`, `smalltime`,`flag`) VALUES
(17, '2018.09.13', '07:02','flag{sqllllllllllllllllllllllllll}');
