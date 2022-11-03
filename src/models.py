from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os

class Models:
    def __init__(self):
        self.engine = create_engine(os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/bt5110'))

    def executeRawSql(self, statement, params={}):
        out = None
        with self.engine.connect() as con:
            out = con.execute(text(statement), params)
        return out

    """ NEW """

    """ MEMBER """
    def addMember(self, value):
        return self.executeRawSql("""INSERT INTO member (email, password) VALUES(:email, :password);""", value)

    def updateMember(self, value): 
        return self.executeRawSql("""UPDATE member SET first_name=:first_name, last_name=:last_name, gender=:gender, job_title=:job_title, dob=:dob, phone_number=:phone_number, password=:password WHERE email=:email""", value)

    def getMemberByEmail(self, email):
        values = self.executeRawSql("""SELECT * FROM member WHERE email=:email;""", {"email": email}).mappings().all()
        if len(values) == 0:
            raise Exception("Member {} does not exist".format(email))
        return values[0]

    def getAllMembers(self):
        return self.executeRawSql("""SELECT * FROM member;""").mappings().all()

    def getMemberCount(self):
        count = self.executeRawSql("""SELECT COUNT(*) FROM member;""").mappings().all()
        return count[0].count

    """ ADMIN """
    def addAdmin(self, value):
        return self.executeRawSql("""INSERT INTO admin (email, password) VALUES(:email, :password);""", value)

    def getAdminByEmail(self, email):
        values = self.executeRawSql("""SELECT * FROM admin WHERE email=:email;""", {"email": email}).mappings().all()
        if len(values) == 0:
            raise Exception("admin {} does not exist".format(email))
        return values[0]

    """ HOLIDAY """
    def addHoliday(self, value):
        return self.executeRawSql("""INSERT INTO holiday (holiday_date, holiday_des) VALUES(:holiday_date, :holiday_des);""", value)

    def checkIfDateIsHoliday(self, date):
        count = self.executeRawSql("""SELECT COUNT(*) FROM holiday WHERE holiday_date=:date;""", {"date": date}).mappings().all()
        return False if count[0].count == 0 else True

    def getAllHolidays(self):
        return self.executeRawSql("""SELECT * FROM holiday;""").mappings().all()

    """ BOOKING_FEE """
    def getAllBookingFee(self):
        return self.executeRawSql("""SELECT * FROM booking_fee;""").mappings().all()

    """ FACILITY """
    def getAllFacility(self):
        return self.executeRawSql("""SELECT * FROM facility;""").mappings().all()

    def getAllFacilityId(self):
        return self.executeRawSql("""SELECT facility_id FROM facility;""").mappings().all()

    """ FEE_SCHEDULE """
    def getAllFeeSchedule(self):
        return self.executeRawSql("""SELECT * FROM fee_schedule;""").mappings().all()

    def getTimeSlotDes(self):
        return self.executeRawSql("""SELECT DISTINCT(time_slot_des) FROM fee_schedule ORDER BY time_slot_des ASC""").mappings().all()

    """ MAINTENANCE """
    def getAllMaintenance(self):
        return self.executeRawSql("""SELECT * FROM maintenance;""").mappings().all()


    """ BOOKING """
    def getAllBookings(self):
        return self.executeRawSql("""SELECT * FROM booking;""").mappings().all()

    def getAllBookingByUser(self, email):
        values = self.executeRawSql("""SELECT * FROM booking WHERE email=:email ORDER BY date DESC, time_slot_des DESC;""", {"email": email}).mappings().all()
        if len(values) == 0:
            raise Exception("Bookings {} does not exist".format(email))
        return values

    def getAllBookingsInNextTwoWeeks(self):
        values = self.executeRawSql("""SELECT * FROM booking where date>=NOW() AND date <= NOW() + interval '14 days';""").mappings().all()
        return values

    def addBooking(self, value):
        return self.executeRawSql("""INSERT INTO booking (date, time_slot_des, facility_id, email, weekend, holiday) VALUES(:date, :time_slot_des, :facility_id, :email, :weekend, :holiday);""", value)

    def deleteBooking(self, value):
        return self.executeRawSql("DELETE FROM booking where date=:date and time_slot_des=:time_slot_des and facility_id=:facility_id;", value)

    """ ANALYTICS """
    def getAnalytics1(self, startDate, endDate):
        return self.executeRawSql("""SELECT f.sports,  ROUND(COUNT(*) / (COUNT(DISTINCT b.date) * 15.0 * COUNT(DISTINCT b.facility_id)), 3) booking_rate
            FROM booking b, fee_schedule fs, facility f
            WHERE b.weekend = fs.weekend
            AND b.holiday = fs.holiday
            AND b.time_slot_des = fs.time_slot_des
            AND b.facility_id = f.facility_id
            AND b.weekend = 'Weekend'
            AND b.date BETWEEN :startDate and :endDate
            GROUP BY f.sports 
            ORDER BY f.sports;
        """,{"startDate":startDate, "endDate":endDate}).mappings().all()

    def getAnalytics2(self, startDate, endDate):
        return self.executeRawSql("""SELECT f.sports,  ROUND(COUNT(*) / (COUNT(DISTINCT b.date) * 15.0 * COUNT(DISTINCT b.facility_id)), 3) booking_rate
            FROM booking b, fee_schedule fs, facility f
            WHERE b.weekend = fs.weekend
            AND b.holiday = fs.holiday
            AND b.time_slot_des = fs.time_slot_des
            AND b.facility_id = f.facility_id
            AND b.holiday = 'Holiday'
            AND b.date BETWEEN :startDate and :endDate
            GROUP BY f.sports 
            ORDER BY f.sports
        """,{"startDate":startDate, "endDate":endDate}).mappings().all()

    def getAnalytics3(self, startDate, endDate):
        return self.executeRawSql("""SELECT f.sports,  
                ROUND(SUM(CASE WHEN fs.peak = 'Non-Peak' THEN 1 ELSE 0 END) / (COUNT(DISTINCT b.date) * 11.0 * COUNT(DISTINCT b.facility_id)), 3) non_peak_booking_rate,
                ROUND(SUM(CASE WHEN fs.peak = 'Peak' THEN 1 ELSE 0 END) / (COUNT(DISTINCT b.date) * 4.0 * COUNT(DISTINCT b.facility_id)), 3) peak_booking_rate
            FROM booking b, fee_schedule fs, facility f
            WHERE b.weekend = fs.weekend
            AND b.holiday = fs.holiday
            AND b.time_slot_des = fs.time_slot_des
            AND b.facility_id = f.facility_id
            AND b.holiday = 'Non-Holiday'
            AND b.weekend = 'Weekday'
            AND b.date BETWEEN :startDate and :endDate
            GROUP BY f.sports 
            ORDER BY f.sports
        """,{"startDate":startDate, "endDate":endDate}).mappings().all()

    def getAnalytics4(self, startDate, endDate):
        return self.executeRawSql("""SELECT TO_CHAR(b.date,'MM - MON') month_, f.sports, m.cleaning + m.electric_bill + m.equipment main_fee,
            SUM(CASE WHEN fs.peak = 'Peak' THEN fee.peak_fee ELSE fee.non_peak_fee END) total_fee,
            SUM(CASE WHEN fs.peak = 'Peak' THEN fee.peak_fee ELSE fee.non_peak_fee END) -
            (m.cleaning + m.electric_bill + m.equipment) profit
        FROM booking b, fee_schedule fs, facility f, booking_fee fee, maintenance m
        WHERE b.weekend = fs.weekend
        AND b.holiday = fs.holiday
        AND b.time_slot_des = fs.time_slot_des
        AND b.facility_id = f.facility_id
        AND f.sports = fee.sports
        AND m.sports = f.sports
        AND b.date BETWEEN :startDate and :endDate
        AND b.date BETWEEN fee.valid_from AND fee.valid_till
        GROUP BY TO_CHAR(b.date,'MM - MON'), f.sports, cleaning+electric_bill+equipment
        ORDER BY f.sports, TO_CHAR(b.date,'MM - MON')
        """,{"startDate":startDate, "endDate":endDate}).mappings().all()

    def getAnalytics5(self, startDate, endDate):
        return self.executeRawSql("""SELECT TO_CHAR(b.date,'MM - MON') month_, f.sports, m.cleaning + m.electric_bill + m.equipment main_fee,
            SUM(CASE WHEN fs.peak = 'Peak' THEN fee.peak_fee ELSE fee.non_peak_fee END) total_fee,
            SUM(CASE WHEN fs.peak = 'Peak' THEN fee.peak_fee ELSE fee.non_peak_fee END) -
            (m.cleaning + m.electric_bill + m.equipment) profit
        FROM booking b, fee_schedule fs, facility f, booking_fee fee, maintenance m
        WHERE b.weekend = fs.weekend
        AND b.holiday = fs.holiday
        AND b.time_slot_des = fs.time_slot_des
        AND b.facility_id = f.facility_id
        AND f.sports = fee.sports
        AND m.sports = f.sports
        AND b.date BETWEEN :startDate and :endDate
        AND b.date BETWEEN fee.valid_from AND fee.valid_till
        GROUP BY TO_CHAR(b.date,'MM - MON'), f.sports, cleaning+electric_bill+equipment
        ORDER BY f.sports, TO_CHAR(b.date,'MM - MON')
        """,{"startDate":startDate, "endDate":endDate}).mappings().all()

    def getAnalytics6(self, sport, days):
        return self.executeRawSql("""SELECT f.sports, b.email, Current_Date - MAX(date) days_without_booking
            FROM booking b, facility f
            WHERE b.facility_id = f.facility_id
            AND f.sports =:sport
            GROUP BY f.sports, b.email
            HAVING Current_Date - MAX(date) > :days
            ORDER BY f.sports, Current_Date - MAX(date) ASC
        """,{"days": days, "sport": sport}).mappings().all()

    """ ENDNEW """

    def createModels(self):
        self.executeRawSql(
            """CREATE TABLE IF NOT EXISTS member (
                first_name VARCHAR(64) NOT NULL,
                last_name VARCHAR(64) NOT NULL,
                email VARCHAR(64) PRIMARY KEY,
                gender VARCHAR(64) NOT NULL,
                job_title VARCHAR(64),
                dob DATE NOT NULL CHECK (current_date > dob),
                phone_number VARCHAR(16),
                password TEXT NOT NULL
            );
            """)

        self.executeRawSql(
            """CREATE TABLE IF NOT EXISTS admin (
                email TEXT PRIMARY KEY,
                password TEXT NOT NULL
            );
            """)

        self.executeRawSql(
            """CREATE TABLE IF NOT EXISTS holiday (
                holiday_date DATE PRIMARY KEY,
                holiday_des VARCHAR(32) NOT NULL
            );
            """)
        
        self.executeRawSql(
            """CREATE TABLE IF NOT EXISTS maintenance (
                sports VARCHAR(16) PRIMARY KEY,
                cleaning INT NOT NULL CHECK(cleaning >= 0),
                electric_bill INT NOT NULL CHECK(electric_bill >= 0),
                equipment INT NOT NULL CHECK(equipment >= 0)
                );
            """)

        self.executeRawSql(
            """CREATE TABLE IF NOT EXISTS booking_fee (
                sports VARCHAR(16) NOT NULL,
                valid_till DATE NOT NULL,
                valid_from DATE NOT NULL,
                peak_fee INT NOT NULL CHECK(peak_fee >= 0),
                non_peak_fee INT NOT NULL CHECK(non_peak_fee >= 0)
                CHECK (valid_from < valid_till),
                PRIMARY KEY (sports, valid_till)
            );
            """)

        self.executeRawSql(
            """CREATE TABLE IF NOT EXISTS fee_schedule (
                weekend VARCHAR(8) NOT NULL,
                holiday VARCHAR(16) NOT NULL,
                time_slot_des VARCHAR(32) NOT NULL,
                peak VARCHAR(8) NOT NULL,
                PRIMARY KEY (weekend, holiday, time_slot_des)
            );
            """)
        
        self.executeRawSql(
            """CREATE TABLE IF NOT EXISTS facility (
                facility_id VARCHAR(16) PRIMARY KEY,
                sports VARCHAR(16) NOT NULL,
                operating_hours VARCHAR(16) NOT NULL,
                aircon CHAR(1) NOT NULL,
                indoor CHAR(1) NOT NULL,
                court_size VARCHAR(16) NOT NULL
                );
            """)

        self.executeRawSql(
            """CREATE TABLE IF NOT EXISTS booking (
                date DATE NOT NULL,
                time_slot_des VARCHAR(32) NOT NULL,
                facility_id VARCHAR(16) NOT NULL,
                email TEXT NOT NULL,
                weekend VARCHAR(8) NOT NULL,
                holiday VARCHAR(32) NOT NULL,
                CONSTRAINT fk1 FOREIGN KEY (facility_id) REFERENCES facility (facility_id),
                CONSTRAINT fk2 FOREIGN KEY (email) REFERENCES member (email),
                PRIMARY KEY (date, time_slot_Des, facility_id)
            );
            """)