-- phpMyAdmin SQL Dump
-- version 4.7.1
-- https://www.phpmyadmin.net/
--
-- Host: sql11.freemysqlhosting.net
-- Czas generowania: 14 Cze 2021, 11:21
-- Wersja serwera: 5.5.62-0ubuntu0.14.04.1
-- Wersja PHP: 7.0.33-0ubuntu0.16.04.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `sql11417642`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `accounts`
--

CREATE TABLE `accounts` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Zrzut danych tabeli `accounts`
--

INSERT INTO `accounts` (`id`, `username`, `password`, `email`) VALUES
(1, 'test', '$5$rounds=535000$qnjMmQlCcv/lqOWk$dFwPG8gpwRddNQmZjbk53AsaKJ1uWMVldZpfVBH9MlB', 'test@test.pl');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `app_groups`
--

CREATE TABLE `app_groups` (
  `Group_ID` int(11) NOT NULL,
  `Group_name` varchar(50) NOT NULL,
  `Liczba_uczestnikow` int(2) NOT NULL,
  `Admin_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Zrzut danych tabeli `app_groups`
--

INSERT INTO `app_groups` (`Group_ID`, `Group_name`, `Liczba_uczestnikow`, `Admin_ID`) VALUES
(1, 'test', 1, 1),
(2, 'test2', 0, 1);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `memberships`
--

CREATE TABLE `memberships` (
  `Membership_ID` int(11) NOT NULL,
  `Member_ID` int(11) NOT NULL,
  `Group_ID` int(11) NOT NULL,
  `Member_type` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indeksy dla zrzutów tabel
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app_groups`
--
ALTER TABLE `app_groups`
  ADD PRIMARY KEY (`Group_ID`),
  ADD KEY `Admin_ID` (`Admin_ID`);

--
-- Indexes for table `memberships`
--
ALTER TABLE `memberships`
  ADD PRIMARY KEY (`Membership_ID`),
  ADD KEY `Member_ID` (`Member_ID`),
  ADD KEY `Group_ID` (`Group_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT dla tabeli `accounts`
--
ALTER TABLE `accounts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT dla tabeli `app_groups`
--
ALTER TABLE `app_groups`
  MODIFY `Group_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT dla tabeli `memberships`
--
ALTER TABLE `memberships`
  MODIFY `Membership_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `app_groups`
--
ALTER TABLE `app_groups`
  ADD CONSTRAINT `app_groups_ibfk_1` FOREIGN KEY (`Admin_ID`) REFERENCES `accounts` (`id`);

--
-- Ograniczenia dla tabeli `memberships`
--
ALTER TABLE `memberships`
  ADD CONSTRAINT `memberships_ibfk_1` FOREIGN KEY (`Member_ID`) REFERENCES `accounts` (`id`),
  ADD CONSTRAINT `memberships_ibfk_2` FOREIGN KEY (`Group_ID`) REFERENCES `app_groups` (`Group_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
