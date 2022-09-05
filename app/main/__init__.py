from flask import Blueprint
from app.models import Permission

main = Blueprint('main', __name__)

from . import views, errors


# a context processor is used to make variables available to all templates during rendering instead
# of having to add a template argument to every render_template() call
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
