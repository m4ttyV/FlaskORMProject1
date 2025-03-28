from flask import Blueprint, render_template
from structures.models import main_table, button1, button2, button3, button4, button5, button7, button6

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
    [buildings_head, buildings_body] = button1()
    html = render_template('table1.html',
        buildings_head=buildings_head,
        buildings_body=buildings_body
    )
    return html

@views.route("/query2")
def query2():
    [buildings_head, buildings_body] = button2()
    html = render_template(
        'table1.html',
        buildings_head=buildings_head,
        buildings_body=buildings_body
    )
    return html
@views.route("/query3")
def query3():
    [buildings_head, buildings_body] = button3()
    html = render_template(
        'table1.html',
        buildings_head=buildings_head,
        buildings_body=buildings_body
    )
    return html
@views.route("/query4")
def query4():
    [buildings_head, buildings_body] = button4()
    html = render_template(
        'table1.html',
        buildings_head=buildings_head,
        buildings_body=buildings_body
    )
    return html
@views.route("/query5")
def query5():
    [buildings_head, buildings_body] = button5()
    html = render_template(
        'table1.html',
        buildings_head=buildings_head,
        buildings_body=buildings_body
    )
    return html
@views.route("/query6")
def query6():
    [buildings_head, buildings_body] = button6()
    html = render_template(
        'table1.html',
        buildings_head=buildings_head,
        buildings_body=buildings_body
    )
    return html
@views.route("/query7")
def query7():
    [buildings_head, buildings_body] = button7()
    html = render_template(
        'table1.html',
        buildings_head=buildings_head,
        buildings_body=buildings_body
    )
    return html