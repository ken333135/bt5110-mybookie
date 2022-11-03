from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, EmailField, IntegerField, DateField,  SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo

def length_check(form,field):
    if len(field.data) == 0:
        raise ValidationError('Fields should not be null')
    

class AddReaderForm(Form):
    email = StringField('Email', validators=[ DataRequired()])
    isbn = StringField('ISBN', validators = [DataRequired()])

class SignUpForm(Form):
    password = PasswordField('Password',validators=[ DataRequired(), Length(min=6)])
    email = EmailField('Email', validators= [DataRequired(), Email()])
    submit = SubmitField('Sign Up')


class SignInForm(Form):
    email = EmailField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired(), Length(min=6, max=30)])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign In')

""" NEW """

class SignUpFormAdmin(Form):
    password = PasswordField('Password',validators=[ DataRequired(), Length(min=6)])
    email = EmailField('Email', validators= [DataRequired(), Email()])
    secret = StringField('Secret', validators= [DataRequired(), EqualTo("mysecret123")])
    submit = SubmitField('Sign Up')

class AddHolidayForm(Form):
    holiday_date = DateField('Date', validators= [DataRequired()])
    holiday_des = StringField('Description',validators=[ DataRequired()])
    submit = SubmitField('Add Holiday')

class AddBookingForm(Form):
    date = DateField('Date',validators=[ DataRequired()])
    time_slot_des = SelectField('Time Slot Des', coerce=str)
    facility_id = SelectField('Facility  Id', coerce=str)
    submit = SubmitField('Add Booking')

class UpdateMemberForm(Form):
    first_name = StringField('First Name',validators=[ DataRequired()])
    last_name = StringField('Last Name',validators=[ DataRequired()])
    gender = SelectField('Email', choices=[('Male','Male'), ('Female','Female')])
    job_title = StringField('Job Title',validators=[ DataRequired()])
    dob = DateField('Date of Birth',validators=[ DataRequired()])
    phone_number = StringField('Phone Number',validators=[ DataRequired()])
    email = StringField('Email',validators=[ DataRequired()])
    password = StringField('Password',validators=[ DataRequired()])

""" END NEW """