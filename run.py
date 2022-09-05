# here we define the application instance
from app import create_app, db
from app.models import User, Role, Permission
from flask_migrate import Migrate


app = create_app('default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission)

