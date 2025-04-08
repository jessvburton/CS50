-- Keep a log of any SQL queries you execute as you solve the mystery.

-- view all tables
.tables

-- copied all info from .schema to a word document
.schema

-- the theft took place on July 28, 2021 and it took place on Humphrey Street
-- Select all to check date formatting
SELECT *
FROM crime_scene_reports

-- Same search but with date and street specifics
SELECT *
FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28 AND street LIKE "%Humphrey Street%";
-- ID: 295
-- Description: Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
-- Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery

-- Look at transcripts that mention 'bakery' on 2021-7-28
SELECT *
FROM interviews
WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE "%bakery%";
-- 3 results/witnesses
-- 161 Ruth - look at bakery security footage for car leaving parking lot
-- 161 Eugene - look at ATM transactions on Leggett Street for withdrawals
-- 163 Raymond - look at flights leaving fiftyville on 2021-7-29 / also look at phone calls on 2021-7-28, maybe ATM transactions

-- Bakery footage for cars leaving the parking lot
SELECT *
FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'exit' AND hour = 10;
-- 8 results of people leaving within 10 mins (10.15-10.25)

-- look at ATM transactions on Leggett Street for withdrawals
SELECT *
FROM atm_transactions
WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location LIKE "%Leggett Street%";
-- 8 withdrawals

-- look at flights leaving fiftyville on 2021-7-29
SELECT *
FROM flights
JOIN airports ON flights.origin_airport_id = airports.id
WHERE flights.year = 2021 AND flights.month = 7 AND flights.day = 29 AND airports.city = 'Fiftyville';
-- 5 flights leaving from Fiftyville

-- look at phone calls on 2021-7-28 lasting less than 60 seconds, around 10:15-10:25
SELECT *
FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

--Now got basic information, need to link it together.
-- Re-look at ATM transactions but join with other tables to get names and phone numbers to cross-check with previous info
SELECT *
FROM atm_transactions
JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number
JOIN people ON bank_accounts.person_ID = people.id
WHERE atm_transactions.year = 2021
    AND atm_transactions.month = 7
    AND atm_transactions.day = 28
    AND atm_transactions.atm_location LIKE "%Leggett Street%";
-- After comparing ATM transactions and phone calls, there are now only 4 suspects

-- Will now look at these 4 license plates against the ones leaving the bakery and link with people
-- 3 of those license plates match
-- Now need to check out of those 3, if they have a flight booked on 2021-7-29 by checking passports
SELECT *
FROM flights
JOIN airports ON flights.origin_airport_id = airports.id
JOIN passengers ON flights.id = passengers.flight_id
WHERE flights.year = 2021
    AND flights.month = 7
    AND flights.day = 29
    AND airports.city = 'Fiftyville'
    AND passengers.passport_number IN ('5773159633', '3592750733','1988161715');
-- All 3 flew so number of suspects not reduced...

-- Someone else booked the flight, lets see if a phone number dialed matches a transaction
SELECT *
FROM atm_transactions
JOIN phone_calls ON atm_transactions.id = phone_calls.id
JOIN people ON phone_calls.receiver = people.phone_number
WHERE atm_transactions.year = 2021
    AND atm_transactions.month = 7
    AND atm_transactions.transaction_type = 'deposit'
    AND phone_calls.duration < 60
    AND people.phone_number IN('(375) 555-8161','(725) 555-3243','(676) 555-6554');
-- not helpful

-- go back a step and re-look at phone calls but link in people table
SELECT *
FROM phone_calls
JOIN people ON phone_calls.receiver = people.phone_number
WHERE phone_calls.year = 2021
    AND phone_calls.month = 7
    AND phone_calls.day = 28
    AND phone_calls.duration < 60
    AND phone_calls.caller in ('(367) 555-5533','(770) 555-1861','(286) 555-6063');
-- 3 people who may have assisted

-- suspects: Dianne, Bruce, Taylor
-- accomplice: Robin, James, Philip

SELECT *
FROM bakery_security_logs
JOIN people ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.year = 2021
    AND bakery_security_logs.month = 7
    AND bakery_security_logs.day = 28
    AND bakery_security_logs.activity = 'exit'
    AND bakery_security_logs.hour = 10
    AND people.license_plate IN('94KL13X','322W7JE','1106N58');

-- suspects: Dianne, Bruce
-- accomplice: Robin, Philip

-- Re check flights, and look at which goes out first, this should be our suspect
SELECT *
FROM flights
JOIN airports ON flights.origin_airport_id = airports.id
JOIN passengers ON flights.id = passengers.flight_id
WHERE flights.year = 2021
    AND flights.month = 7
    AND flights.day = 29
    AND airports.city = 'Fiftyville'
    AND passengers.passport_number IN ('5773159633', '3592750733')
ORDER BY flights.hour;
-- Bruce is the thief, which means Robin was the accomplice
-- If I kept better lists at the beginning I wouldn't of had to re-run searches.

-- Need to find out what city Bruce went to

SELECT DISTINCT (city)
FROM flights
JOIN airports ON flights.destination_airport_id = airports.id
WHERE airports.id = 4;
-- escaped to New York City