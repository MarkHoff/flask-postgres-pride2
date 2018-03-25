from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')


class ProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[
        DataRequired(), Length(min=1, max=140)])
    pid = StringField('Project ID', validators=[
        DataRequired(), Length(min=1, max=140)])
    pmt = StringField('PMT', validators=[Length(min=1, max=140)])
    dev_lead = StringField('Dev Lead', validators=[Length(min=1, max=140)])
    developers = StringField('Developers', validators=[Length(min=1, max=140)])
    release = StringField('Release', validators=[Length(min=1, max=140)])
    sprint_schedule = StringField('Sprint Schedule', validators=[Length(min=1, max=140)])
    lpm = StringField('LPM', validators=[Length(min=1, max=140)])
    pm = StringField('PM', validators=[Length(min=1, max=140)])
    scrum_master = StringField('Scrum Master', validators=[Length(min=1, max=140)])
    se = StringField('SE', validators=[Length(min=1, max=140)])
    notes = TextAreaField('Notes', validators=[Length(min=1, max=1400)])
    submit = SubmitField('Submit')

class EditProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[
        DataRequired(), Length(min=1, max=140)])
    pid = StringField('Project ID', validators=[
        DataRequired(), Length(min=1, max=140)])
    pmt = StringField('PMT', validators=[Length(min=1, max=140)])
    dev_lead = StringField('Dev Lead', validators=[Length(min=1, max=140)])
    developers = StringField('Developers', validators=[Length(min=1, max=140)])
    release = StringField('Release', validators=[Length(min=1, max=140)])
    sprint_schedule = StringField('Sprint Schedule', validators=[Length(min=1, max=140)])
    lpm = StringField('LPM', validators=[Length(min=1, max=140)])
    pm = StringField('PM', validators=[Length(min=1, max=140)])
    scrum_master = StringField('Scrum Master', validators=[Length(min=1, max=140)])
    se = StringField('SE', validators=[Length(min=1, max=140)])
    notes = TextAreaField('Notes', validators=[Length(min=1, max=1400)])
    submit = SubmitField('Submit')


class DbObjectForm(FlaskForm):
    dm_seq = StringField('DM Sequence', validators=[Length(min=1, max=140)])
    data_type = StringField('Data Type', validators=[Length(min=1, max=140)])
    schema = StringField('Schema', validators=[Length(min=1, max=140)])
    db_object = StringField('DB Object', validators=[Length(min=1, max=140)])
    frequency = StringField('Frequency', validators=[Length(min=1, max=140)])
    data_provider = StringField('Data Provider', validators=[Length(min=1, max=140)])
    providing_system = StringField('Providing System', validators=[Length(min=1, max=140)])
    interface = StringField('Interface', validators=[Length(min=1, max=140)])
    topic = StringField('Topic', validators=[Length(min=1, max=140)])
    data_retention = StringField('Data Retention', validators=[Length(min=1, max=140)])
    latency = StringField('Latency', validators=[Length(min=1, max=140)])
    data_in_qa0 = StringField('Data In QA0', validators=[Length(min=1, max=140)])
    row_count_per_period = StringField('Row Count Per Period', validators=[Length(min=1, max=140)])
    active_in_prod = StringField('Active In Prod', validators=[Length(min=1, max=140)])
    order_by = StringField('Order By', validators=[Length(min=1, max=140)])
    segment_by = StringField('Segment By', validators=[Length(min=1, max=140)])
    special_notes = TextAreaField('Special Notes', validators=[Length(min=1, max=1400)])
    submit = SubmitField('Submit')


class EditDbObjectForm(FlaskForm):
    dm_seq = StringField('DM Sequence', validators=[Length(min=1, max=140)])
    data_type = StringField('Data Type', validators=[Length(min=1, max=140)])
    schema = StringField('Schema', validators=[Length(min=1, max=140)])
    db_object = StringField('DB Object', validators=[Length(min=1, max=140)])
    frequency = StringField('Frequency', validators=[Length(min=1, max=140)])
    data_provider = StringField('Data Provider', validators=[Length(min=1, max=140)])
    providing_system = StringField('Providing System', validators=[Length(min=1, max=140)])
    interface = StringField('Interface', validators=[Length(min=1, max=140)])
    topic = StringField('Topic', validators=[Length(min=1, max=140)])
    data_retention = StringField('Data Retention', validators=[Length(min=1, max=140)])
    latency = StringField('Latency', validators=[Length(min=1, max=140)])
    data_in_qa0 = StringField('Data In QA0', validators=[Length(min=1, max=140)])
    row_count_per_period = StringField('Row Count Per Period', validators=[Length(min=1, max=140)])
    active_in_prod = StringField('Active In Prod', validators=[Length(min=1, max=140)])
    order_by = StringField('Order By', validators=[Length(min=1, max=140)])
    segment_by = StringField('Segment By', validators=[Length(min=1, max=140)])
    special_notes = TextAreaField('Special Notes', validators=[Length(min=1, max=1400)])
    submit = SubmitField('Submit')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')