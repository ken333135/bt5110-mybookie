/*******************

  Create the schema

*******************/

CREATE TABLE IF NOT EXISTS holiday (
date DATE PRIMARY KEY,
holiday VARCHAR(32) NOT NULL
);


CREATE TABLE IF NOT EXISTS fee_schedule (
weekend VARCHAR(8) NOT NULL,
holiday VARCHAR(16) NOT NULL,
time_slot_Des VARCHAR(32) NOT NULL,
peak VARCHAR(8) NOT NULL,
PRIMARY KEY (weekend, holiday, time_slot_Des)
);


CREATE TABLE IF NOT EXISTS maintenance (
sports VARCHAR(16) PRIMARY KEY,
cleaning INT NOT NULL CHECK(cleaning >= 0),
electric_bill INT NOT NULL CHECK(electric_bill >= 0),
equipment INT NOT NULL CHECK(equipment >= 0)
);


CREATE TABLE IF NOT EXISTS booking_fee (
sports VARCHAR(16) PRIMARY KEY,
peak_fee INT NOT NULL CHECK(peak_fee >= 0),
non_peak_fee INT NOT NULL CHECK(non_peak_fee >= 0)
);


CREATE TABLE IF NOT EXISTS facility (
facility_id VARCHAR(16) PRIMARY KEY,
sports VARCHAR(16) NOT NULL,
operating_hours VARCHAR(16) NOT NULL,
aircon CHAR(1) NOT NULL,
indoor CHAR(1) NOT NULL,
court_size VARCHAR(16) NOT NULL,
FOREIGN KEY (sports) REFERENCES booking_fee(sports)
);


CREATE TABLE IF NOT EXISTS users (
user_id VARCHAR(16) UNIQUE NOT NULL,
first_name VARCHAR(64) NOT NULL,
last_name VARCHAR(64) NOT NULL,
email VARCHAR(64) PRIMARY KEY,
gender VARCHAR(64) NOT NULL,
job_title VARCHAR(64),
dob DATE NOT NULL CHECK (current_date > dob),
phone_number VARCHAR(16)
);


CREATE TABLE IF NOT EXISTS booking (
date DATE NOT NULL,
time_slot_Des VARCHAR(32) NOT NULL,
facility_id VARCHAR(16) NOT NULL,
user_id VARCHAR(16) NOT NULL,
weekend VARCHAR(8) NOT NULL,
CONSTRAINT fk1 FOREIGN KEY (facility_id) REFERENCES facility (facility_id),
CONSTRAINT fk2 FOREIGN KEY (user_id) REFERENCES users (user_id),
PRIMARY KEY (date, time_slot_Des, facility_id)
);





