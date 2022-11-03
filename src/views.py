from flask import request, session, redirect, url_for, render_template, flash
from datetime import date
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go

from . models import Models
from . forms import AddReaderForm, SignUpForm, SignInForm, SignUpFormAdmin, AddHolidayForm, AddBookingForm, UpdateMemberForm

from src import app

models = Models()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    try:
        session.clear()
        session['user_available'] = False
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))



""" NEW """

""" SIGNIN / SIGNOUT """
@app.route('/admin/signup', methods=['GET', 'POST'])
def signupadmin():
    try:
        signupformadmin = SignUpFormAdmin(request.form)
        if request.method == 'POST':
            if signupformadmin.secret.data == 'mysecret':
                models.addAdmin({"email": signupformadmin.email.data, "password": signupformadmin.password.data, "secret": signupformadmin.secret.data})
                return redirect(url_for('admin/signin'))
            else:
                flash('Invalid Secret')
        return render_template('admin/signup.html', signupformadmin=signupformadmin)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))

@app.route('/admin/signin', methods=['GET', 'POST'])
def signinadmin():
    try:
        signinform = SignInForm(request.form)
        if request.method == 'POST':
            em = signinform.email.data
            log = models.getAdminByEmail(em)
            if log.password == signinform.password.data:
                session['current_user'] = em
                session['user_available'] = True
                return redirect(url_for('show_holiday'))
            else:
                flash('Cannot sign in')
        return render_template('admin/signin.html', signinform=signinform)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        signupform = SignUpForm(request.form)
        if request.method == 'POST':
            models.addMember({"email": signupform.email.data, "password": signupform.password.data})
            return redirect(url_for('signin'))
        return render_template('signup.html', signupform=signupform)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    try:
        signinform = SignInForm(request.form)
        if request.method == 'POST':
            em = signinform.email.data
            log = models.getMemberByEmail(em)
            if log.password == signinform.password.data:
                session['current_user'] = em
                session['user_available'] = True
                return redirect(url_for('show_booking'))
            else:
                flash('Cannot sign in')
        return render_template('signin.html', signinform=signinform)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))

""" HOLIDAY """
@app.route('/admin/holiday', methods=['GET'])
def show_holiday():
    try:
        if session['user_available']:
            holidays = models.getAllHolidays()
            return render_template('admin/holiday/index.html', holidays=holidays)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/admin/holiday/add', methods=['GET', 'POST'])
def add_holiday():
    try:
        if session['user_available']:
            holiday = AddHolidayForm(request.form)
            if request.method == 'POST':
                models.addHoliday({
                    "holiday_date": holiday.holiday_date.data,
                    "holiday_des": holiday.holiday_des.data
                })
                return redirect(url_for('show_holiday'))
            return render_template('admin/holiday/add.html', holiday=holiday)
    except Exception as e:
        flash(str(e))
    flash('User is not Authenticated')
    return redirect(url_for('index'))

""" FEE SCHEDULE """
@app.route('/admin/fee_schedule', methods=['GET'])
def show_fee_schedule():
    try:
        if session['user_available']:
            fee_schedules = models.getAllFeeSchedule()
            return render_template('admin/fee_schedule/index.html', fee_schedules=fee_schedules)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

""" MAINTENANCE """
@app.route('/admin/maintenance', methods=['GET'])
def show_maintenance():
    try:
        if session['user_available']:
            maintenances = models.getAllMaintenance()
            return render_template('admin/maintenance/index.html', maintenances=maintenances)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

""" FACILITY """
@app.route('/admin/facility', methods=['GET'])
def show_facility():
    try:
        if session['user_available']:
            facilities = models.getAllFacility()
            return render_template('admin/facility/index.html', facilities=facilities)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

""" BOOKING_FEE """
@app.route('/admin/booking_fee', methods=['GET'])
def show_booking_fee():
    try:
        if session['user_available']:
            booking_fees = models.getAllBookingFee()
            return render_template('admin/booking_fee/index.html', booking_fees=booking_fees)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

""" MEMBER """
@app.route('/admin/member', methods=['GET'])
def show_member():
    try:
        if session['user_available']:
            members = models.getAllMembers()
            return render_template('admin/member/index.html', members=members)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/about')
def about_member():
    try:
        if session['user_available']:
            member = models.getMemberByEmail(session['current_user'])
            return render_template('member/index.html', member=member)
        flash('You are not a Authenticated User')
        return redirect(url_for('about_member'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))

@app.route('/update', methods=['GET', 'POST'])
def update_member():
    try:
        data = models.getMemberByEmail(session['current_user'])
        member = UpdateMemberForm(request.form, obj=data)
        if request.method == 'POST':
            models.updateMember({
                "first_name": member.first_name.data, 
                "last_name": member.last_name.data, 
                "gender": member.gender.data, 
                "job_title": member.job_title.data, 
                "dob": member.dob.data, 
                "phone_number": member.phone_number.data, 
                "email": member.email.data, 
                "password": member.password.data, 
            })
            return redirect(url_for('about_member'))
        return render_template('member/update.html', member=member)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))
            
        
""" BOOKING """
@app.route('/booking', methods=['GET'])
def show_booking():
    try:
        if session['user_available']:
            user_email = session["current_user"]
            bookings = models.getAllBookingByUser(user_email)
            today = date.today()

            def test(value):
                app.logger.info("HELLO WORLD FKKKK {}".format(value))

            return render_template('booking/index.html', bookings=bookings, today=today, test=test)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/booking/add', methods=['GET','POST'])
def add_booking():
    try:
        if session['user_available']:
            booking = AddBookingForm(request.form)
            if request.method == 'POST':
                user_email = session["current_user"]
                date = booking.date.data
                weekend = 'Weekend' if date.weekday() < 5 else 'Weekday' 
                holiday = 'Holiday' if models.checkIfDateIsHoliday(date) else 'Non-Holiday'
                app.logger.info(holiday)

                models.addBooking({
                    "date": date.strftime('%Y-%m-%d'),
                    "time_slot_des": booking.time_slot_des.data,
                    "facility_id": booking.facility_id.data,
                    "email": user_email,
                    "weekend": weekend,
                    "holiday": holiday
                })
                return redirect(url_for('show_booking'))

            facilities = models.getAllFacilityId()
            facilities = [i["facility_id"] for i in facilities]
            facilities_groups_list = [(i,i) for i in facilities]
            booking.facility_id.choices = facilities_groups_list

            time_slot_des = models.getTimeSlotDes()
            time_slot_des = [i["time_slot_des"] for i in time_slot_des]
            time_slot_des_groups_list = [(i,i) for i in time_slot_des]
            booking.time_slot_des.choices = time_slot_des_groups_list

            bookings = models.getAllBookingsInNextTwoWeeks()

            return render_template('booking/add.html', booking=booking, bookings=bookings)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('add_booking'))
    flash('User is not Authenticated')
    return redirect(url_for('show_booking'))

@app.route('/delete/<date>/<time_slot_des>/<facility_id>', methods=('GET', 'POST'))
def delete_booking(date, time_slot_des, facility_id):
    try:
        models.deleteBooking({"date": date, "time_slot_des": time_slot_des, "facility_id": facility_id})
        flash("Delete Success")
        return redirect(url_for('show_booking'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))

""" ANALYTICS """
@app.route('/admin/analytics/1')
@app.route('/admin/analytics/1/<startDate>/<endDate>')
def analytics_1(startDate='2022-01-01', endDate='2022-11-06'):
    try:

        # data 1
        data = models.getAnalytics1(startDate, endDate)
        app.logger.info(data)
        df = pd.DataFrame(data)
        fig = px.bar(df, x='sports', y='booking_rate')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # data 2
        data2 = models.getAnalytics2(startDate, endDate)
        df2 = pd.DataFrame(data2)
        fig2 = px.bar(df2, x='sports', y='booking_rate')
        graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

        # data 2
        data3 = models.getAnalytics3(startDate, endDate)
        df3 = pd.DataFrame(data3)
        nonPeakDf = df3[['sports','non_peak_booking_rate']]
        nonPeakDf.rename(columns = { 'non_peak_booking_rate': 'rate' }, inplace=True)
        nonPeakDf['type'] = 'non_peak'

        peakDf = df3[['sports','peak_booking_rate']]
        peakDf.rename(columns = { 'peak_booking_rate': 'rate' }, inplace=True)
        peakDf['type'] = 'peak'

        df3 = pd.concat([nonPeakDf, peakDf])
        fig3 = px.bar(df3, x='sports', y='rate', facet_col='type')

        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('admin/analytics/1.html', graphJSON=graphJSON, graphJSON2=graphJSON2, graphJSON3=graphJSON3)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))

@app.route('/admin/analytics/2')
@app.route('/admin/analytics/2/<startDate>/<endDate>')
def analytics_2(startDate='2022-01-01', endDate='2022-11-06'):
    try:
        data = models.getAnalytics4(startDate, endDate)
        df = pd.DataFrame(data)
        fig = px.bar(df, x='month_', y='profit', color='sports', barmode='group')

        # fig.add_trace(
        # go.Scatter(
        #     x=df['month_'],
        #     y=df['main_fee'],
        #     color='sports'
        # ))

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('admin/analytics/2.html', graphJSON=graphJSON)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))

@app.route('/admin/analytics/3')
@app.route('/admin/analytics/3/<sport>/<days>')
def analytics_3(sport='Basketball', days=180):
    try:
        data = models.getAnalytics6(sport, days)
        return render_template('admin/analytics/3.html', data=data)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))

""" END NEW """

if __name__ == '__main__':
    app.run()
