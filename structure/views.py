from flask import Blueprint, render_template
from structure.models import main_table, button1
views = Blueprint('views', __name__)
query = Blueprint('query', __name__)

@views.route("/")
def index():
    [buildings_head, buildings_body] = main_table()
    html = render_template(
        'index.html',
        buildings_head=buildings_head,
        buildings_body=buildings_body
    )
    return html

def query1():
    [buildings_head, buildings_body] = button1()
    html = render_template(
        'index.html',
        buildings_head=buildings_head,
        buildings_body=buildings_body
    )
    return html