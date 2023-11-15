import math

from flask import render_template, request, redirect
import dao
from salesapp.app import app, login
from flask_login import login_user


@app.route("/")
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get("page")
    return render_template("index.html", categories=dao.get_categories(),
                           products=dao.get_products(kw, cate_id, page), pages=math.ceil(dao.count_products()/app.config["PAGE_SIZE"]))


@app.route("/admin/login", methods=["post"])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect("/admin")


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_user_id(user_id)


if __name__ == '__main__':
    from salesapp.app import admin

    app.run(debug=True)
