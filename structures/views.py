from flask import Blueprint, render_template
from structures.models import main_table, minCountries, maxCountries, avgCountries

views = Blueprint('views', __name__)

@views.route("/")
@views.route("/index")
def index():
    [buildings_head, buildings_body] = main_table()
    html = render_template(
        'index.html',
        buildings_head=buildings_head,
        buildings_body=buildings_body
    )
    return html

@views.route("/query1")
def query1():
    [buildings_head, buildings_body] = maxCountries()
    html = render_template('table1.html',
        buildings_head=buildings_head,
        buildings_body=buildings_body
    )
    return html

@views.route("/query2")
def query2():
    [buildings_head, buildings_body] = minCountries()
    html = render_template(
        'table1.html',
        buildings_head=buildings_head,
        buildings_body=buildings_body
    )
    return html

@views.route("/query3")
def query3():
    [buildings_head, buildings_body] = avgCountries()
    html = render_template(
        'table1.html',
        buildings_head=buildings_head,
        buildings_body=buildings_body
    )
    return html
