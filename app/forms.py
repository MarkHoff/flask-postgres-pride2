from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, HiddenField, IntegerField
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
    about_me = TextAreaField('About me', validators=[Length(min=0, max=100)])
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
        DataRequired(), Length(min=0, max=100)])
    submit = SubmitField('Submit')


class ProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[
        DataRequired(), Length(min=0, max=100)])
    pid = StringField('Project ID', validators=[
        DataRequired(), Length(min=1, max=100)])
    pmt = StringField('PMT', validators=[Length(min=0, max=100)])
    dev_lead = StringField('Dev Lead', validators=[Length(min=0, max=100)])
    developers = StringField('Developers', validators=[Length(min=0, max=100)])
    release = StringField('Release', validators=[Length(min=0, max=100)])
    sprint_schedule = StringField('Sprint Schedule', validators=[Length(min=0, max=100)])
    lpm = StringField('LPM', validators=[Length(min=0, max=100)])
    pm = StringField('PM', validators=[Length(min=0, max=100)])
    scrum_master = StringField('Scrum Master', validators=[Length(min=0, max=100)])
    se = StringField('SE', validators=[Length(min=0, max=100)])
    notes = TextAreaField('Notes', validators=[Length(min=0, max=1000)])
    submit = SubmitField('Submit')

class EditProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[
        DataRequired(), Length(min=0, max=100)])
    pid = StringField('Project ID', validators=[
        DataRequired(), Length(min=0, max=100)])
    pmt = StringField('PMT', validators=[Length(min=0, max=100)])
    dev_lead = StringField('Dev Lead', validators=[Length(min=0, max=100)])
    developers = StringField('Developers', validators=[Length(min=0, max=100)])
    release = StringField('Release', validators=[Length(min=0, max=100)])
    sprint_schedule = StringField('Sprint Schedule', validators=[Length(min=0, max=100)])
    lpm = StringField('LPM', validators=[Length(min=0, max=100)])
    pm = StringField('PM', validators=[Length(min=0, max=100)])
    scrum_master = StringField('Scrum Master', validators=[Length(min=0, max=100)])
    se = StringField('SE', validators=[Length(min=0, max=100)])
    notes = TextAreaField('Notes', validators=[Length(min=0, max=1000)])
    submit = SubmitField('Submit')


class DbObjectForm(FlaskForm):
    dm_seq = StringField('DM Sequence', validators=[Length(min=0, max=100)])
    data_type = StringField('Data Type', validators=[Length(min=0, max=100)])
    schema = StringField('Schema', validators=[Length(min=0, max=100)])
    db_object = StringField('DB Object', validators=[Length(min=0, max=100)])
    frequency = StringField('Frequency', validators=[Length(min=0, max=100)])
    data_provider = StringField('Data Provider', validators=[Length(min=0, max=100)])
    providing_system = StringField('Providing System', validators=[Length(min=0, max=100)])
    interface = StringField('Interface', validators=[Length(min=0, max=100)])
    topic = StringField('Topic', validators=[Length(min=0, max=100)])
    data_retention = StringField('Data Retention', validators=[Length(min=0, max=100)])
    latency = StringField('Latency', validators=[Length(min=0, max=100)])
    data_in_qa0 = StringField('Data In QA0', validators=[Length(min=0, max=100)])
    row_count_per_period = StringField('Row Count Per Period', validators=[Length(min=0, max=100)])
    active_in_prod = StringField('Active In Prod', validators=[Length(min=0, max=100)])
    order_by = StringField('Order By', validators=[Length(min=0, max=100)])
    segment_by = StringField('Segment By', validators=[Length(min=0, max=100)])
    project_id = StringField('Project ID', validators=[Length(min=0, max=100)])
    special_notes = TextAreaField('Special Notes', validators=[Length(min=0, max=1000)])
    submit = SubmitField('Submit')


class EditDbObjectForm(FlaskForm):
    dm_seq = StringField('DM Sequence', validators=[Length(min=0, max=100)])
    data_type = StringField('Data Type', validators=[Length(min=0, max=100)])
    schema = StringField('Schema', validators=[Length(min=0, max=100)])
    db_object = StringField('DB Object', validators=[Length(min=0, max=100)])
    frequency = StringField('Frequency', validators=[Length(min=0, max=100)])
    data_provider = StringField('Data Provider', validators=[Length(min=0, max=100)])
    providing_system = StringField('Providing System', validators=[Length(min=0, max=100)])
    interface = StringField('Interface', validators=[Length(min=0, max=100)])
    topic = StringField('Topic', validators=[Length(min=0, max=100)])
    data_retention = StringField('Data Retention', validators=[Length(min=0, max=100)])
    latency = StringField('Latency', validators=[Length(min=0, max=100)])
    data_in_qa0 = StringField('Data In QA0', validators=[Length(min=0, max=100)])
    row_count_per_period = StringField('Row Count Per Period', validators=[Length(min=0, max=100)])
    active_in_prod = StringField('Active In Prod', validators=[Length(min=0, max=100)])
    order_by = StringField('Order By', validators=[Length(min=0, max=100)])
    segment_by = StringField('Segment By', validators=[Length(min=0, max=100)])
    project_id = StringField('Project ID', validators=[Length(min=0, max=100)])
    special_notes = TextAreaField('Special Notes', validators=[Length(min=0, max=1000)])
    submit = SubmitField('Submit')


class StoryForm(FlaskForm):
    user_story_id = StringField('Story ID', validators=[Length(min=0, max=100)])
    dev_lead = StringField('Dev Lead', validators=[Length(min=0, max=100)])
    developers = StringField('Developers', validators=[Length(min=0, max=100)])
    sprint = StringField('Sprint', validators=[Length(min=0, max=300)])
    points = StringField('Points', validators=[Length(min=0, max=10)])
    size = StringField('Size', validators=[Length(min=0, max=10)])
    epic = StringField('Epic', validators=[Length(min=0, max=20)])
    story_notes = TextAreaField('Notes', validators=[Length(min=0, max=3000)])
    user_story_desc = TextAreaField('Description', validators=[Length(min=0, max=3000)])
    user_story_name = StringField('Story Name', validators=[Length(min=0, max=100)])
    project_id = StringField('Project ID', validators=[Length(min=0, max=100)])
    project_name = StringField('Project Name', validators=[Length(min=0, max=100)])
    submit = SubmitField('Submit')


class EditStoryForm(FlaskForm):
    user_story_id = StringField('Story ID', validators=[Length(min=0, max=100)])
    dev_lead = StringField('Dev Lead', validators=[Length(min=0, max=100)])
    developers = StringField('Developers', validators=[Length(min=0, max=100)])
    sprint = StringField('Sprint', validators=[Length(min=0, max=300)])
    points = StringField('Points', validators=[Length(min=0, max=10)])
    size = StringField('Size', validators=[Length(min=0, max=10)])
    epic = StringField('Epic', validators=[Length(min=0, max=20)])
    story_notes = TextAreaField('Notes', validators=[Length(min=0, max=3000)])
    user_story_desc = TextAreaField('Description', validators=[Length(min=0, max=3000)])
    user_story_name = StringField('Story Name', validators=[Length(min=0, max=100)])
    project_id = StringField('Project ID', validators=[Length(min=0, max=100)])
    project_name = StringField('Project Name', validators=[Length(min=0, max=100)])
    submit = SubmitField('Submit')


class TaskForm(FlaskForm):
    task_id = StringField('Task ID', validators=[Length(min=0, max=100)])
    dev_lead = StringField('Dev Lead', validators=[Length(min=0, max=100)])
    developers = StringField('Developers', validators=[Length(min=0, max=100)])
    sprint = StringField('Sprint', validators=[Length(min=0, max=300)])
    task_name = StringField('Task Name', validators=[Length(min=0, max=100)])
    task_desc = StringField('Task Desc', validators=[Length(min=0, max=1000)])
    task_hours = IntegerField('Task Hours')
    task_notes = TextAreaField('Notes', validators=[Length(min=0, max=2000)])
    user_story_id = StringField('Story ID', validators=[Length(min=0, max=100)])
    project_id = StringField('Project ID', validators=[Length(min=0, max=100)])
    submit = SubmitField('Submit')


class EditTaskForm(FlaskForm):
    task_id = StringField('Task ID', validators=[Length(min=0, max=100)])
    dev_lead = StringField('Dev Lead', validators=[Length(min=0, max=100)])
    developers = StringField('Developers', validators=[Length(min=0, max=100)])
    sprint = StringField('Sprint', validators=[Length(min=0, max=300)])
    task_name = StringField('Task Name', validators=[Length(min=0, max=100)])
    task_desc = StringField('Task Desc', validators=[Length(min=0, max=1000)])
    task_hours = IntegerField('Task Hours')
    task_notes = TextAreaField('Notes', validators=[Length(min=0, max=2000)])
    user_story_id = StringField('Story ID', validators=[Length(min=0, max=100)])
    project_id = StringField('Project ID', validators=[Length(min=0, max=100)])
    submit = SubmitField('Submit')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


# class SearchForm(FlaskForm):
#     choices = StringField('Search Field', validators=[Length(min=0, max=100)])
#     string_search = StringField('Search Criteria', validators=[Length(min=0, max=100)])
#     submit = SubmitField('Submit')


class DownloadDataForm(FlaskForm):
    proj_list = HiddenField()
    submit = SubmitField('Download')