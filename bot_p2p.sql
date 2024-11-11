-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Май 20 2024 г., 22:40
-- Версия сервера: 8.0.30
-- Версия PHP: 7.3.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `bot_p2p`
--

-- --------------------------------------------------------

--
-- Структура таблицы `active_transactions`
--

CREATE TABLE `active_transactions` (
  `number` int NOT NULL,
  `sum` varchar(64) NOT NULL,
  `type_fiat` int NOT NULL,
  `type_crypt` int NOT NULL,
  `count` varchar(64) NOT NULL,
  `bank` varchar(64) NOT NULL,
  `login_customer` varchar(64) NOT NULL,
  `login_vendor` varchar(64) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `type` int NOT NULL DEFAULT '1',
  `delete_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `exchange_logs`
--

CREATE TABLE `exchange_logs` (
  `id` int NOT NULL,
  `login` varchar(64) NOT NULL,
  `type` varchar(64) NOT NULL,
  `currency_1` varchar(64) NOT NULL,
  `currency_2` varchar(64) NOT NULL,
  `count` double NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `number` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `exchange_rates`
--

CREATE TABLE `exchange_rates` (
  `id` int NOT NULL,
  `currency_1` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `currency_2` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `rate` varchar(64) NOT NULL DEFAULT '0',
  `minimum_exchange_amount` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `exchange_rates`
--

INSERT INTO `exchange_rates` (`id`, `currency_1`, `currency_2`, `rate`, `minimum_exchange_amount`) VALUES
(1, 'USDT', 'BTC', '0.000016', 0.00025),
(3, 'BTC', 'USDT', '60814.95', 0.0002),
(5, 'LTC', 'USDT', '81.34', 1),
(6, 'BTC', 'LTC', '749.65', 0),
(9, 'LTC', 'BTC', '0.001334', 0),
(10, 'BTC', 'RUB', '5646953', 0),
(13, 'USDT', 'RUB', '91.03', 0);

-- --------------------------------------------------------

--
-- Структура таблицы `freezing_of_funds`
--

CREATE TABLE `freezing_of_funds` (
  `number` int NOT NULL,
  `number_adv` int NOT NULL,
  `login` varchar(64) DEFAULT NULL,
  `login_vendor` varchar(64) NOT NULL,
  `USDT` varchar(64) DEFAULT NULL,
  `TON` varchar(64) DEFAULT NULL,
  `GRAM` varchar(64) DEFAULT NULL,
  `BTC` varchar(64) DEFAULT NULL,
  `LTC` varchar(64) DEFAULT NULL,
  `ETH` varchar(64) DEFAULT NULL,
  `BNB` varchar(64) DEFAULT NULL,
  `TRX` varchar(64) DEFAULT NULL,
  `USDC` varchar(64) DEFAULT NULL,
  `NOT_C` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `data` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `time` int NOT NULL,
  `delete_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `p2p_advertisements`
--

CREATE TABLE `p2p_advertisements` (
  `id` bigint DEFAULT NULL,
  `number` int NOT NULL,
  `login` varchar(64) NOT NULL,
  `currency` int NOT NULL,
  `currency_count` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `banks` varchar(64) NOT NULL,
  `crypt` int NOT NULL,
  `crypt_count` varchar(64) NOT NULL,
  `min` varchar(64) NOT NULL,
  `max` varchar(64) NOT NULL,
  `time` int NOT NULL,
  `conditions` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Не указаны.',
  `percentage` varchar(64) DEFAULT NULL,
  `fix_count_sell` varchar(64) DEFAULT NULL,
  `sum` varchar(64) NOT NULL,
  `type` int NOT NULL DEFAULT '1',
  `data` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` int NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `support_tickets`
--

CREATE TABLE `support_tickets` (
  `number_freezing` int NOT NULL,
  `number_adv` int NOT NULL,
  `id` bigint NOT NULL,
  `id_vendor` bigint NOT NULL,
  `message` varchar(64) NOT NULL,
  `data` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `number_tik` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` bigint NOT NULL,
  `login` varchar(64) NOT NULL,
  `currency` int NOT NULL DEFAULT '0',
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '0',
  `lang` varchar(64) NOT NULL DEFAULT 'lang_ru',
  `access` int NOT NULL DEFAULT '4',
  `active_user` int NOT NULL DEFAULT '1',
  `adm_pass` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `users_purses`
--

CREATE TABLE `users_purses` (
  `id` bigint NOT NULL,
  `login` varchar(64) NOT NULL,
  `USDT` varchar(64) NOT NULL DEFAULT '0',
  `TON` varchar(64) NOT NULL DEFAULT '0',
  `GRAM` varchar(64) NOT NULL DEFAULT '0',
  `BTC` varchar(64) NOT NULL DEFAULT '0',
  `LTC` varchar(64) NOT NULL DEFAULT '0',
  `ETH` varchar(64) NOT NULL DEFAULT '0',
  `BNB` varchar(64) NOT NULL DEFAULT '0',
  `TRX` varchar(64) NOT NULL DEFAULT '0',
  `USDC` varchar(64) NOT NULL DEFAULT '0',
  `NOT_C` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `saved_wallets_1` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `saved_wallets_2` varchar(64) DEFAULT NULL,
  `saved_wallets_3` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `users_vendor`
--

CREATE TABLE `users_vendor` (
  `id` bigint NOT NULL,
  `login` varchar(64) NOT NULL,
  `count` int NOT NULL DEFAULT '0',
  `sum` varchar(64) NOT NULL DEFAULT '0',
  `rep_plus` int NOT NULL DEFAULT '0',
  `rep_minus` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `active_transactions`
--
ALTER TABLE `active_transactions`
  ADD PRIMARY KEY (`number`);

--
-- Индексы таблицы `exchange_logs`
--
ALTER TABLE `exchange_logs`
  ADD PRIMARY KEY (`id`,`login`);

--
-- Индексы таблицы `exchange_rates`
--
ALTER TABLE `exchange_rates`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Индексы таблицы `p2p_advertisements`
--
ALTER TABLE `p2p_advertisements`
  ADD PRIMARY KEY (`number`);

--
-- Индексы таблицы `support_tickets`
--
ALTER TABLE `support_tickets`
  ADD PRIMARY KEY (`number_freezing`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`,`login`),
  ADD UNIQUE KEY `id_2` (`id`,`login`);

--
-- Индексы таблицы `users_purses`
--
ALTER TABLE `users_purses`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users_vendor`
--
ALTER TABLE `users_vendor`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `exchange_logs`
--
ALTER TABLE `exchange_logs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=66;

--
-- AUTO_INCREMENT для таблицы `exchange_rates`
--
ALTER TABLE `exchange_rates`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

DELIMITER $$
--
-- События
--
CREATE DEFINER=`root`@`%` EVENT `delete_specific` ON SCHEDULE EVERY 5 MINUTE STARTS '2024-05-20 22:18:06' ON COMPLETION NOT PRESERVE ENABLE DO DELETE FROM active_transactions WHERE delete_at <= NOW()$$

CREATE DEFINER=`root`@`%` EVENT `delete_specific_row` ON SCHEDULE EVERY 5 MINUTE STARTS '2024-05-20 22:11:51' ON COMPLETION NOT PRESERVE ENABLE DO DELETE FROM freezing_of_funds WHERE delete_at <= NOW()$$

DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
