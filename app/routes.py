from flask import render_template, flash, redirect, url_for, request, send_file
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, \
    ResetPasswordForm, ProjectForm, EditProjectForm, DbObjectForm, EditDbObjectForm, StoryForm, \
    EditStoryForm, TaskForm, EditTaskForm
from app.email import send_password_reset_email
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Project, DbObject, Task, UserStory
from werkzeug.urls import url_parse
from datetime import datetime
import csv
import numpy as np
import pandas as pd


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(project_name=form.project_name.data,
                          pid = form.pid.data,
                          pmt = form.pmt.data,
                          dev_lead = form.dev_lead.data,
                          developers = form.developers.data,
                          release = form.release.data,
                          sprint_schedule = form.sprint_schedule.data,
                          lpm = form.lpm.data,
                          pm = form.pm.data,
                          scrum_master = form.scrum_master.data,
                          se = form.se.data,
                          notes = form.notes.data
                          )
        db.session.add(project)
        db.session.commit()
        flash('Your project has been saved')
        return redirect(url_for('view_projects'))
    all_proj = Project.query.all()
    # page = request.args.get('page', 1, type=int)
    # posts = current_user.followed_posts().paginate(
    #     page, app.config['POSTS_PER_PAGE'], False)
    # next_url = url_for('index', page=posts.next_num) \
    #     if posts.has_next else None
    # prev_url = url_for('index', page=posts.prev_num) \
    #     if posts.has_prev else None
    return render_template('project.html', title='Projects', form=form)


@app.route('/view_projects', methods=['GET'])
def view_projects():
    all_proj = db.session.query(Project).outerjoin(DbObject, Project.pid == DbObject.project_id).order_by(Project.pid).all()
    return render_template('view_projects.html', title='View Projects', all_projects=all_proj)


@app.route('/project_detail/<id>')
def project_detail(id):
    proj_detail = db.session.query(Project).outerjoin(DbObject, Project.pid == DbObject.project_id).filter(Project.id == id).\
        add_columns(
        Project.id,
        Project.pid,
        Project.project_name,
        Project.dev_lead,
        Project.developers,
        Project.release,
        Project.pmt,
        Project.sprint_schedule,
        Project.lpm,
        Project.pm,
        Project.scrum_master,
        Project.se,
        Project.impact,
        Project.readiness_status,
        Project.deployment_cr,
        Project.notes,
        # Project.user_story_id,
        # Project.user_story_desc,
        # Project.user_story_name,
        # Project.task_id,
        # Project.task_name,
        # Project.task_desc
    ).first_or_404()
    obj_detail = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).filter(
        Project.id == id). \
        add_columns(
        DbObject.id,
        DbObject.db_object,
        DbObject.dm_seq
    )
    us_detail = db.session.query(UserStory).outerjoin(Project, Project.pid == UserStory.project_id). \
        filter(Project.id == id). \
        add_columns(
        UserStory.id,
        UserStory.user_story_id,
        UserStory.user_story_name,
        UserStory.user_story_desc,
        UserStory.sprint,
        UserStory.points,
        UserStory.size,
        UserStory.epic,
        UserStory.story_notes

    )
    return render_template('view_project_detail.html',
                           title='Project Detail',
                           project_detail=proj_detail,
                           object_detail= obj_detail,
                           us_detail = us_detail
                           )


@app.route('/edit_project/<id>', methods=['GET', 'POST'])
def edit_project(id):
    proj_id = Project.query.get(id)
    form = EditProjectForm(formdata=request.form, obj=proj_id)
    if form.validate_on_submit():
        form.populate_obj(proj_id)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('view_projects'))
    elif request.method == 'GET':
            return render_template('edit_project_detail.html',
                            title='Edit Project',
                            form=form)


@app.route('/delete_project/<id>', methods=['GET', 'POST'])
def delete_project(id):
    proj_id = db.session.query(Project).filter(Project.id == id).first_or_404()
    db.session.delete(proj_id)
    db.session.commit()
    print("The object id is {} and the object name is {}".format(str(proj_id.id), str(proj_id.project_name)))
    flash('Project ID {}, {} has been deleted'.format(str(proj_id.pid), str(proj_id.project_name)))
    all_proj = Project.query.all()
    return render_template('view_projects.html', title='View Projects', all_projects=all_proj)


@app.route('/view_objects', methods=['GET'])
def view_objects():
    all_obj = DbObject.query.all()
    return render_template('view_objects.html', title='View Objects', all_objects=all_obj)


@app.route('/add_object', methods=['GET', 'POST'])
def add_object():
    form = DbObjectForm()
    if form.validate_on_submit():
        dbobject = DbObject(
          dm_seq=form.dm_seq.data,
          data_type = form.data_type.data,
          schema = form.schema.data,
          db_object = form.db_object.data,
          frequency = form.frequency.data,
          data_provider = form.data_provider.data,
          providing_system = form.providing_system.data,
          interface = form.interface.data,
          topic = form.topic.data,
          data_retention = form.data_retention.data,
          latency = form.latency.data,
          data_in_qa0 = form.data_in_qa0.data,
          row_count_per_period = form.row_count_per_period.data,
          active_in_prod = form.active_in_prod.data,
          order_by = form.order_by.data,
          segment_by = form.segment_by.data,
          project_id = form.project_id.data,
          special_notes = form.special_notes.data
                          )
        db.session.add(dbobject)
        db.session.commit()
        flash('Your object has been posted!')
        return redirect(url_for('view_objects'))
    return render_template('add_object.html', title='Add DB Objects', form=form)


@app.route('/edit_object/<id>', methods=['GET', 'POST'])
def edit_object(id):
    obj_id = DbObject.query.get(id)
    form = EditDbObjectForm(formdata=request.form, obj=obj_id)
    if form.validate_on_submit():
        form.populate_obj(obj_id)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('view_objects'))
    elif request.method == 'GET':
            return render_template('edit_object_detail.html',
                                    title='Edit Object',
                                    form=form)


@app.route('/delete_object/<id>', methods=['GET', 'POST'])
def delete_object(id):
    obj_id = db.session.query(DbObject).filter(DbObject.id == id).first_or_404()
    db.session.delete(obj_id)
    db.session.commit()
    print("The object id is {} and the object name is {}".format(str(obj_id.id), str(obj_id.db_object)))
    flash('Record no. {}, {} has been deleted'.format(str(obj_id.id), str(obj_id.db_object)))
    all_obj = DbObject.query.all()
    return render_template('view_objects.html', title='View Objects', all_objects=all_obj)


@app.route('/object_detail/<id>')
def object_detail(id):
    obj_detail = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).filter(DbObject.id == id).\
        add_columns(
        Project.pid,
        Project.project_name,
        Project.dev_lead,
        Project.developers,
        Project.release,
        DbObject.id,
        DbObject.dm_seq,
        DbObject.data_type,
        DbObject.schema,
        DbObject.db_object,
        DbObject.project_id,
        DbObject.frequency,
        DbObject.data_provider,
        DbObject.providing_system,
        DbObject.interface,
        DbObject.topic,
        DbObject.data_retention,
        DbObject.latency,
        DbObject.data_in_qa0,
        DbObject.row_count_per_period,
        DbObject.active_in_prod,
        DbObject.order_by,
        DbObject.segment_by,
        DbObject.special_notes
    ).first_or_404()
    return render_template('view_object_detail.html',title='Object Detail', object_detail=obj_detail)


@app.route('/view_stories', methods = ['GET'])
def view_stories():
    all_stories = db.session.query(UserStory).order_by(UserStory.user_story_id).all()
    return render_template('view_stories.html', title='View Stories', all_stories = all_stories)


@app.route('/add_story', methods=['GET', 'POST'])
def add_story():
    form = StoryForm()
    if form.validate_on_submit():
        story = UserStory(
            user_story_id = form.user_story_id.data,
            dev_lead = form.dev_lead.data,
            developers = form.developers.data,
            sprint = form.sprint.data,
            points = form.points.data,
            size = form.size.data,
            epic = form.epic.data,
            story_notes = form.story_notes.data,
            user_story_desc = form.user_story_desc.data,
            user_story_name = form.user_story_name.data,
            project_id = form.project_id.data,
            project_name = form.project_name.data
        )
        db.session.add(story)
        db.session.commit()
        flash('Your story has been saved')
        return redirect(url_for('view_projects'))
    return render_template('story.html', title='Add Story', form=form)


@app.route('/edit_story/<id>', methods=['GET', 'POST'])
def edit_story(id):
    story_id = UserStory.query.get(id)
    form = EditStoryForm(formdata=request.form, obj=story_id)
    if form.validate_on_submit():
        form.populate_obj(story_id)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('view_stories'))
    elif request.method == 'GET':
            return render_template('edit_story_detail.html',
                                    title='Edit Story',
                                    form=form)


@app.route('/delete_story/<id>', methods=['GET', 'POST'])
def delete_story(id):
    story_id = db.session.query(UserStory).filter(UserStory.id == id).first_or_404()
    db.session.delete(story_id)
    db.session.commit()
    print("The story id is {} and the story name is {}".format(str(story_id.id), str(story_id.user_story_name)))
    flash('User Story id no. {}, {} has been deleted'.format(str(story_id.id), str(story_id.user_story_name)))
    all_stories = UserStory.query.all()
    return render_template('view_stories.html', title='View Stories', all_stories=all_stories)


@app.route('/story_detail/<id>')
def story_detail(id):
    story_detail = db.session.query(UserStory).outerjoin(Project, Project.pid == UserStory.project_id).filter(UserStory.id == id).\
        add_columns(
        Project.pid,
        Project.project_name,
        Project.dev_lead,
        Project.developers,
        Project.release,
        UserStory.id,
        UserStory.project_id,
        UserStory.user_story_id,
        UserStory.user_story_name,
        UserStory.user_story_desc,
        UserStory.dev_lead,
        UserStory.developers,
        UserStory.sprint,
        UserStory.size,
        UserStory.points,
        UserStory.epic,
        UserStory.story_notes,
    ).first_or_404()
    task_detail = db.session.query(Task).outerjoin(UserStory, UserStory.user_story_id == Task.user_story_id).filter(
        UserStory.id == id). \
        add_columns(
        Task.id.label('t_id'),
        Task.task_id,
        Task.task_name
    )
    return render_template('view_story_detail.html',title='User Story Detail',
                           story_detail=story_detail,
                           task_detail=task_detail)


@app.route('/view_tasks', methods = ['GET'])
def view_tasks():
    all_tasks = db.session.query(Task).order_by(Task.task_id).all()
    return render_template('view_tasks.html', title='View Tasks', all_tasks = all_tasks)


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            task_id = form.user_story_id.data,
            dev_lead = form.dev_lead.data,
            developers = form.developers.data,
            sprint = form.sprint.data,
            task_name = form.task_name.data,
            task_desc = form.task_desc.data,
            task_hours = form.task_hours.data,
            task_notes = form.task_notes.data,
            user_story_id = form.user_story_id.data,
            project_id = form.project_id.data,
        )
        db.session.add(task)
        db.session.commit()
        flash('Your task has been saved')
        return redirect(url_for('view_tasks'))
    return render_template('task.html', title='Add Task', form=form)


@app.route('/edit_task/<id>', methods=['GET', 'POST'])
def edit_task(id):
    task_id = Task.query.get(id)
    form = EditTaskForm(formdata=request.form, obj=task_id)
    if form.validate_on_submit():
        form.populate_obj(task_id)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('view_tasks'))
    elif request.method == 'GET':
            return render_template('edit_task_detail.html',
                                    title='Edit Task',
                                    form=form)


@app.route('/delete_task/<id>', methods=['GET', 'POST'])
def delete_task(id):
    task_id = db.session.query(Task).filter(Task.id == id).first_or_404()
    db.session.delete(task_id)
    db.session.commit()
    print("The task id is {} and the task name is {}".format(str(task_id.id), str(task_id.task_name)))
    flash('Task id no. {}, {} has been deleted'.format(str(task_id.id), str(task_id.task_name)))
    all_tasks = Task.query.all()
    return render_template('view_tasks.html', title='View Tasks', all_tasks=all_tasks)


@app.route('/task_detail/<id>')
def task_detail(id):
    task_detail = db.session.query(Task).outerjoin(UserStory, UserStory.user_story_id == Task.user_story_id).\
        outerjoin(Project, Project.pid == UserStory.project_id).filter(Task.id == id).\
        add_columns(
        Project.pid,
        Project.project_name,
        UserStory.id.label("us_id"),
        UserStory.user_story_id,
        UserStory.user_story_name,
        Task.id,
        Task.task_id,
        Task.task_name,
        Task.dev_lead,
        Task.developers,
        Task.sprint,
        Task.task_desc,
        Task.task_hours,
        Task.task_notes
    ).first_or_404()
    return render_template('view_task_detail.html',title='Task Detail', task_detail=task_detail)


@app.route('/csv/', methods=['GET', 'POST'])
def download_csv(proj_list):
    filename = 'all_projects.csv'
    all_proj = proj_list
    csv_list = [['PID', 'PROJECT NAME', 'PMT', 'DEV LEAD', 'DEVELOPERS', 'RELEASE']]
    for row in all_proj:
        csv_list.append([row.pid, row.project_name, row.pmt, row.dev_lead, row.developers, row.release])
    csv_list = np.asarray(csv_list)

    csvList = pd.DataFrame(csv_list)
    print(str(csvList))
    csvList.to_csv(filename, header=False, sep='\t', index=False)
    send_file(filename, as_attachment=True, mimetype='text/csv')
    return filename


@app.route('/search', methods=['GET', 'POST'])
def search():

    if request.method == 'POST':
        proj_choice = request.form['proj_choices']
        obj_choice = request.form['obj_choices']
        if request.form['download']:
            download = request.form['download']
        else: download =''
        if proj_choice != '':
            search_string = request.form['proj_search']
            if proj_choice == 'PID':
                search_item = 'pid'
                proj_list = Project.query.order_by(Project.pid).filter(Project.pid.like('%' + search_string + '%')).all()
            elif proj_choice == 'Dev Lead':
                search_item = 'dev_lead'
                proj_list = Project.query.order_by(Project.pid).filter(Project.dev_lead.like('%' + search_string + '%')).all()
            elif proj_choice == 'Developer':
                search_item = 'developers'
                proj_list = Project.query.order_by(Project.pid).filter(Project.developers.like('%' + search_string + '%')).all()
            elif proj_choice == 'Release':
                search_item = 'release'
                proj_list = Project.query.order_by(Project.pid).filter(Project.release.like('%' + search_string + '%')).all()
            print(proj_list)
            if download == 'csv':
                csv_list = [['PID', 'PROJECT NAME', 'PMT', 'DEV LEAD', 'DEVELOPERS', 'RELEASE']]
                filename = 'all_projects.csv'
                for row in proj_list:
                    csv_list.append([row.pid, row.project_name, row.pmt, row.dev_lead, row.developers, row.release])
                csv_list = np.asarray(csv_list)
                csvList = pd.DataFrame(csv_list)
                csvList.to_csv(filename, header=False, sep='\t', index=False)
                return send_file(filename, as_attachment=True, mimetype='text/csv')
            else:
                return render_template('view_projects.html', title='Search Results', all_projects=proj_list)
        elif obj_choice != '':
            search_string = request.form['obj_search']
            if obj_choice == 'Release':
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).order_by(Project.pid).filter(
                    Project.release.ilike ('%' + search_string + '%')).\
                            add_columns(
                            Project.pid,
                            Project.project_name,
                            Project.dev_lead,
                            Project.pmt,
                            Project.developers,
                            Project.release,
                            DbObject.id,
                            DbObject.dm_seq,
                            DbObject.data_type,
                            DbObject.schema,
                            DbObject.db_object,
                            DbObject.project_id,
                            DbObject.frequency,
                            DbObject.data_provider,
                            DbObject.providing_system,
                            DbObject.interface,
                            DbObject.topic,
                            DbObject.data_retention,
                            DbObject.latency,
                            DbObject.data_in_qa0,
                            DbObject.row_count_per_period,
                            DbObject.active_in_prod,
                            DbObject.order_by,
                            DbObject.segment_by,
                            DbObject.special_notes
                        ).all()
            elif obj_choice == 'Schema':
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).order_by(Project.pid).filter(
                    DbObject.schema.ilike ('%' + search_string + '%')).\
                            add_columns(
                            Project.pid,
                            Project.project_name,
                            Project.dev_lead,
                            Project.pmt,
                            Project.developers,
                            Project.release,
                            DbObject.id,
                            DbObject.dm_seq,
                            DbObject.data_type,
                            DbObject.schema,
                            DbObject.db_object,
                            DbObject.project_id,
                            DbObject.frequency,
                            DbObject.data_provider,
                            DbObject.providing_system,
                            DbObject.interface,
                            DbObject.topic,
                            DbObject.data_retention,
                            DbObject.latency,
                            DbObject.data_in_qa0,
                            DbObject.row_count_per_period,
                            DbObject.active_in_prod,
                            DbObject.order_by,
                            DbObject.segment_by,
                            DbObject.special_notes
                        ).all()
            elif obj_choice == 'Object Name':
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).order_by(Project.pid).filter(
                    DbObject.db_object.ilike ('%' + search_string + '%')).\
                            add_columns(
                            Project.pid,
                            Project.project_name,
                            Project.dev_lead,
                            Project.pmt,
                            Project.developers,
                            Project.release,
                            DbObject.id,
                            DbObject.dm_seq,
                            DbObject.data_type,
                            DbObject.schema,
                            DbObject.db_object,
                            DbObject.project_id,
                            DbObject.frequency,
                            DbObject.data_provider,
                            DbObject.providing_system,
                            DbObject.interface,
                            DbObject.topic,
                            DbObject.data_retention,
                            DbObject.latency,
                            DbObject.data_in_qa0,
                            DbObject.row_count_per_period,
                            DbObject.active_in_prod,
                            DbObject.order_by,
                            DbObject.segment_by,
                            DbObject.special_notes
                        ).all()
            elif obj_choice == 'Dev Lead':
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).order_by(Project.pid).filter(
                    Project.dev_lead.ilike ('%' + search_string + '%')).\
                            add_columns(
                            Project.pid,
                            Project.project_name,
                            Project.dev_lead,
                            Project.pmt,
                            Project.developers,
                            Project.release,
                            DbObject.id,
                            DbObject.dm_seq,
                            DbObject.data_type,
                            DbObject.schema,
                            DbObject.db_object,
                            DbObject.project_id,
                            DbObject.frequency,
                            DbObject.data_provider,
                            DbObject.providing_system,
                            DbObject.interface,
                            DbObject.topic,
                            DbObject.data_retention,
                            DbObject.latency,
                            DbObject.data_in_qa0,
                            DbObject.row_count_per_period,
                            DbObject.active_in_prod,
                            DbObject.order_by,
                            DbObject.segment_by,
                            DbObject.special_notes
                        ).all()
            elif obj_choice == 'Developer':
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).order_by(Project.pid).filter(
                    Project.developers.ilike ('%' + search_string + '%')).\
                            add_columns(
                            Project.pid,
                            Project.project_name,
                            Project.dev_lead,
                            Project.pmt,
                            Project.developers,
                            Project.release,
                            DbObject.id,
                            DbObject.dm_seq,
                            DbObject.data_type,
                            DbObject.schema,
                            DbObject.db_object,
                            DbObject.project_id,
                            DbObject.frequency,
                            DbObject.data_provider,
                            DbObject.providing_system,
                            DbObject.interface,
                            DbObject.topic,
                            DbObject.data_retention,
                            DbObject.latency,
                            DbObject.data_in_qa0,
                            DbObject.row_count_per_period,
                            DbObject.active_in_prod,
                            DbObject.order_by,
                            DbObject.segment_by,
                            DbObject.special_notes
                        ).all()
            elif obj_choice == 'PID':
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).order_by(Project.pid).filter(
                    DbObject.project_id.ilike ('%' + search_string + '%')).\
                            add_columns(
                            Project.pid,
                            Project.project_name,
                            Project.dev_lead,
                            Project.pmt,
                            Project.developers,
                            Project.release,
                            DbObject.id,
                            DbObject.dm_seq,
                            DbObject.data_type,
                            DbObject.schema,
                            DbObject.db_object,
                            DbObject.project_id,
                            DbObject.frequency,
                            DbObject.data_provider,
                            DbObject.providing_system,
                            DbObject.interface,
                            DbObject.topic,
                            DbObject.data_retention,
                            DbObject.latency,
                            DbObject.data_in_qa0,
                            DbObject.row_count_per_period,
                            DbObject.active_in_prod,
                            DbObject.order_by,
                            DbObject.segment_by,
                            DbObject.special_notes
                        ).all()
            elif obj_choice == 'DM Seq':
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).order_by(Project.pid).filter(
                    DbObject.dm_seq.ilike ('%' + search_string + '%')).\
                            add_columns(
                            Project.pid,
                            Project.project_name,
                            Project.dev_lead,
                            Project.pmt,
                            Project.developers,
                            Project.release,
                            DbObject.id,
                            DbObject.dm_seq,
                            DbObject.data_type,
                            DbObject.schema,
                            DbObject.db_object,
                            DbObject.project_id,
                            DbObject.frequency,
                            DbObject.data_provider,
                            DbObject.providing_system,
                            DbObject.interface,
                            DbObject.topic,
                            DbObject.data_retention,
                            DbObject.latency,
                            DbObject.data_in_qa0,
                            DbObject.row_count_per_period,
                            DbObject.active_in_prod,
                            DbObject.order_by,
                            DbObject.segment_by,
                            DbObject.special_notes
                        ).all()
            elif obj_choice == 'Topic':
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).order_by(Project.pid).filter(
                    DbObject.topic.ilike ('%' + search_string + '%')).\
                            add_columns(
                            Project.pid,
                            Project.project_name,
                            Project.dev_lead,
                            Project.pmt,
                            Project.developers,
                            Project.release,
                            DbObject.id,
                            DbObject.dm_seq,
                            DbObject.data_type,
                            DbObject.schema,
                            DbObject.db_object,
                            DbObject.project_id,
                            DbObject.frequency,
                            DbObject.data_provider,
                            DbObject.providing_system,
                            DbObject.interface,
                            DbObject.topic,
                            DbObject.data_retention,
                            DbObject.latency,
                            DbObject.data_in_qa0,
                            DbObject.row_count_per_period,
                            DbObject.active_in_prod,
                            DbObject.order_by,
                            DbObject.segment_by,
                            DbObject.special_notes
                        ).all()
            elif obj_choice == 'Interface':
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).order_by(Project.pid).filter(
                    DbObject.interface.ilike ('%' + search_string + '%')).\
                            add_columns(
                            Project.pid,
                            Project.project_name,
                            Project.dev_lead,
                            Project.pmt,
                            Project.developers,
                            Project.release,
                            DbObject.id,
                            DbObject.dm_seq,
                            DbObject.data_type,
                            DbObject.schema,
                            DbObject.db_object,
                            DbObject.project_id,
                            DbObject.frequency,
                            DbObject.data_provider,
                            DbObject.providing_system,
                            DbObject.interface,
                            DbObject.topic,
                            DbObject.data_retention,
                            DbObject.latency,
                            DbObject.data_in_qa0,
                            DbObject.row_count_per_period,
                            DbObject.active_in_prod,
                            DbObject.order_by,
                            DbObject.segment_by,
                            DbObject.special_notes
                        ).all()
            if download == 'csv':
                csv_list = [['PID', 'PROJECT NAME', 'DEV LEAD', 'PMT', 'DEVELOPERS', 'RELEASE', 'DM SEQ',
                             'DATA TYPE', 'SCHEMA', 'FREQUENCY', 'DATA PROVIDER', 'PROVIDING SYSTEM',
                             'INTERFACE', 'TOPIC', 'DATA RETENTION', 'LATENCY', 'DATA IN QA0', 'ROW COUNT PER PERIOD',
                             'ACTIVE IN PROD', 'ORDER BY ', 'SEGMENT BY']]
                filename = 'all_objects.csv'
                # for row in obj_list:
                    # csv_list.append([row.db_object_project_name, row.db_object_dev_lead, row.db_object_pmt, row.db_object_developers,
                    #                  row.db_object_release,
                    #                  row.db_object_dm_seq, row.db_object_data_type, row.db_object_schema, row.db_object_frequency,
                    #                  row.db_object_data_provider,
                    #                  row.db_object_providing_system, row.db_object_interface, row.db_object_topic,
                    #                  row.db_object_data_retention, row.db_object_latency,
                    #                  row.db_object_data_in_qa0, row.db_object_row_count_per_period, row.db_object_active_in_prod,
                    #                  row.db_object_order_by, row.db_object_segment_by ])
                    # csv_list.append([row.pid, row.project_name, row.dev_lead, row.pmt, row.developers, row.release])
                csv_list = np.asarray(csv_list)
                csvList = pd.DataFrame(csv_list)
                csvList.to_csv(filename, header=False, sep='\t', index=False)
                return send_file(filename, as_attachment=True, mimetype='text/csv')
                    # print(row)
            else:
                return render_template('view_objects.html', title='Search Results', all_objects=obj_list)
    else:
        return render_template('search_form.html')


    return render_template('upload.html')


@app.route('/proj_uploader', methods=['GET', 'POST'])
def upload_projfile():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        with open(f.filename, 'r') as load_file:
            readfile = csv.reader(load_file, delimiter='\t')
            next(readfile) # headers
            for line in readfile:
                # print(line)
                project = Project(
                    project_name = line[0],
                    pid = line[1],
                    pmt = line[2],
                    dev_lead = line[3],
                    developers = line[4],
                    release = line[5],
                    sprint_schedule = line[6],
                    lpm = line[7],
                    pm = line[8],
                    scrum_master = line[9],
                    se = line[10],
                    notes = line[11],
                    impact = line[12],
                    readiness_status = line[13],
                    deployment_cr = line[14]
                )
                db.session.add(project)
            db.session.commit()
        flash('Your file has been uploaded successfully!')
        return redirect(url_for('view_projects'))
    else:
        return render_template('file_upload.html')


@app.route('/obj_uploader', methods=['GET', 'POST'])
def upload_objfile():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        with open(f.filename, 'r') as load_file:
            readfile = csv.reader(load_file, delimiter='\t')
            next(readfile) # headers
            for line in readfile:
                # print(line)
                object = DbObject(
                    project_id = line[0],
                    dm_seq = line[1],
                    data_type = line[2],
                    schema = line[3],
                    db_object = line[4],
                    frequency = line[5],
                    data_provider = line[6],
                    providing_system = line[7],
                    interface = line[8],
                    topic = line[9],
                    data_retention = line[10],
                    latency = line[11],
                    data_in_qa0 = line[12],
                    row_count_per_period = line[13],
                    active_in_prod = line[14],
                    order_by = line[15],
                    segment_by = line[16],
                    special_notes = line[17]
                )
                db.session.add(object)
            db.session.commit()
        flash('Your file has been uploaded successfully!')
        return redirect(url_for('view_objects'))
    else:
        return render_template('db_file_upload.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))