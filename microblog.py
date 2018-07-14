from app import app, db
from app.models import User, Project, DbObject, UserStory, Task


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Project': Project, 'DbObject': DbObject, 'UserStory': UserStory, 'Task': Task}