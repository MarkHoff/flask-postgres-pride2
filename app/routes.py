from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ResetPasswordRequestForm, \
    ResetPasswordForm, ProjectForm, EditProjectForm, DbObjectForm, EditDbObjectForm, SearchForm
from app.email import send_password_reset_email
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Project, DbObject
from werkzeug.urls import url_parse
from datetime import datetime


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
        flash('Your project has been posted!')
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
    # all_proj = Project.query.all().outerjoin(DbObject, Project.pid == DbObject.project_id)
    all_proj = db.session.query(Project).outerjoin(DbObject, Project.pid == DbObject.project_id).all()
    return render_template('view_projects.html', title='View Projects', all_projects=all_proj)


@app.route('/project_detail/<id>')
def project_detail(id):
    # proj_detail = Project.query.filter_by(id=id).first_or_404()
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
        Project.notes
    ).first_or_404()
    obj_detail = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).filter(
        Project.id == id). \
        add_columns(
        DbObject.id,
        DbObject.db_object,
        DbObject.dm_seq
        # DbObject.data_type,
        # DbObject.schema,
        # DbObject.db_object,
        # DbObject.project_id,
        # DbObject.frequency,
        # DbObject.data_provider,
        # DbObject.providing_system,
        # DbObject.interface,
        # DbObject.topic,
        # DbObject.data_retention,
        # DbObject.latency,
        # DbObject.data_in_qa0,
        # DbObject.row_count_per_period,
        # DbObject.active_in_prod,
        # DbObject.order_by,
        # DbObject.segment_by,
        # DbObject.special_notes
    )
    return render_template('view_project_detail.html',
                           title='Project Detail',
                           project_detail=proj_detail, object_detail = obj_detail
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
    # obj_detail = db.session.query(DbObject).join(Project).filter(DbObject.id == id).first_or_404()
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
    # print(obj_detail.project_id)
    return render_template('view_object_detail.html',title='Object Detail', object_detail=obj_detail)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        proj_choice = request.form['proj_choices']
        print(proj_choice)
        obj_choice = request.form['obj_choices']
        print(obj_choice)
        # print(search_string)

        if proj_choice != '':
            search_string = request.form['proj_search']
            if proj_choice == 'PID':
                proj_list = Project.query.filter(Project.pid.like('%' + search_string + '%')).all()
            elif proj_choice == 'Dev Lead':
                proj_list = Project.query.filter(Project.dev_lead.like('%' + search_string + '%')).all()
            elif proj_choice == 'Developer':
                proj_list = Project.query.filter(Project.developers.like('%' + search_string + '%')).all()
            elif proj_choice == 'Release':
                proj_list = Project.query.filter(Project.release.like('%' + search_string + '%')).all()
            return render_template('view_projects.html', title='Search Results', all_projects=proj_list)
        elif obj_choice != '':
            search_string = request.form['obj_search']
            if obj_choice == 'Release':
                # obj_list = DbObject.query.filter(DbObject.release.like('%' + search_string + '%')).all()
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).filter(
                    Project.release.ilike ('%' + search_string + '%')).all()
            elif obj_choice == 'Schema':
                # obj_list = DbObject.query.filter(DbObject.schema.like('%' + search_string + '%')).all()
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).filter(
                    DbObject.schema.ilike ('%' + search_string + '%')).all()
            elif obj_choice == 'Object Name':
                # obj_list = DbObject.query.filter(DbObject.db_object.like('%' + search_string + '%')).all()
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).filter(
                    DbObject.db_object.ilike ('%' + search_string + '%')).all()
            elif obj_choice == 'Dev Lead':
                # obj_list = DbObject.query.join(Project).filter(Project.dev_lead.like('%' + search_string + '%')).all()
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).filter(
                    Project.dev_lead.ilike ('%' + search_string + '%')).all()
            elif obj_choice == 'Developer':
                # obj_list = DbObject.query.join(Project).filter(Project.developers.like('%' + search_string + '%')).all()
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).filter(
                    Project.developers.ilike ('%' + search_string + '%')).all()
            elif obj_choice == 'PID':
                # obj_list = DbObject.query.filter(DbObject.project_id.like('%' + search_string + '%')).all()
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).filter(
                    DbObject.project_id.ilike ('%' + search_string + '%')).all()
            elif obj_choice == 'DM Seq':
                # obj_list = DbObject.query.filter(DbObject.dm_seq.like('%' + search_string + '%')).all()
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).filter(
                    DbObject.dm_seq.ilike ('%' + search_string + '%')).all()
            elif obj_choice == 'Topic':
                # obj_list = DbObject.query.filter(DbObject.topic.like('%' + search_string + '%')).all()
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).filter(
                    DbObject.topic.ilike ('%' + search_string + '%')).all()
            elif obj_choice == 'Interface':
                # obj_list = DbObject.query.filter(DbObject.interface.like('%' + search_string + '%')).all()
                obj_list = db.session.query(DbObject).outerjoin(Project, Project.pid == DbObject.project_id).filter(
                    DbObject.interface.ilike ('%' + search_string + '%')).all()
            return render_template('view_objects.html', title='Search Results', all_objects=obj_list)

    else:
        return render_template('search_form.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))