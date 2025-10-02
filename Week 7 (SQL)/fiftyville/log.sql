-- Keep a log of any SQL queries you execute as you solve the mystery.

-- check crime log
SELECT description FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street ='Humphrey Street';

-- check interview
SELECT transcript FROM interviews WHERE month = 7 AND day = 28 AND transcript LIKE "%bakery%";
-- Leggett Street withdraw $
-- Parking lot +- 10 min
-- 10:15 call helper for less than 1min, plane ticket

-- Check bakery security log
SELECT bakery_security_logs.activity,bakery_security_logs.license_plate,people.name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.year = 2024
AND bakery_security_logs.month = 7
AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute >= 15
AND bakery_security_logs.minute <= 25;

-- check bank transcation
SELECT people.name,atm_transactions.transaction_type FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON atm_transactions.account_number = atm_transactions.account_number
WHERE bakery_security_logs.year = 2024
WHERE atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_transactions.atm_location ='Leggett Street'
AND atm_transactions.transaction_type = "withdraw"
GROUP BY people.name;

-- Check Phone Record

-- Check parking lot(security log)

