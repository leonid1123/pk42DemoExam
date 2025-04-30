-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Апр 30 2025 г., 12:48
-- Версия сервера: 10.4.28-MariaDB
-- Версия PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `partners`
--

-- --------------------------------------------------------

--
-- Структура таблицы `partners`
--

CREATE TABLE `partners` (
  `ID` int(11) NOT NULL,
  `Name` text NOT NULL,
  `Country` text NOT NULL,
  `type` text DEFAULT NULL,
  `Founded` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `partners`
--

INSERT INTO `partners` (`ID`, `Name`, `Country`, `type`, `Founded`) VALUES
(1, 'ООО Вася', 'Россия', NULL, 0),
(2, 'ООО Петя', 'Россия', NULL, 0),
(3, 'ООО Маша', 'Россия', NULL, 0),
(4, 'ООО Солнышко', 'Беллорусь', NULL, 0),
(5, 'ООО Мячик', 'Беллорусь', NULL, 0),
(6, 'ООО Галактика', 'Китай', NULL, 0),
(7, 'ООО Суслик', 'Сусликистан', NULL, 0),
(8, 'ООО Ежик', 'Россия', 'Норм', 0);

-- --------------------------------------------------------

--
-- Структура таблицы `sales`
--

CREATE TABLE `sales` (
  `id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `id_partner` int(11) NOT NULL,
  `id_goods` int(11) NOT NULL,
  `sale_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `sales`
--

INSERT INTO `sales` (`id`, `quantity`, `id_partner`, `id_goods`, `sale_date`) VALUES
(1, 200, 1, 1, '2025-10-10'),
(2, 700, 1, 1, '2025-11-10'),
(3, 600, 2, 1, '2025-10-12'),
(4, 500, 2, 1, '2025-10-18'),
(5, 300, 3, 1, '2025-09-10'),
(6, 1200, 4, 1, '2025-10-20');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `partners`
--
ALTER TABLE `partners`
  ADD PRIMARY KEY (`ID`);

--
-- Индексы таблицы `sales`
--
ALTER TABLE `sales`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_partner` (`id_partner`),
  ADD KEY `id_goods` (`id_goods`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `partners`
--
ALTER TABLE `partners`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `sales`
--
ALTER TABLE `sales`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
