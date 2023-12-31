import math

from flask import render_template, request, redirect, jsonify, session
import dao
import utils
from salesapp.app import app, login
from flask_login import login_user, logout_user


@app.route("/")
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get("page")
    return render_template("index.html", products=dao.get_products(kw, cate_id, page), pages=math.ceil(dao.count_products()/app.config["PAGE_SIZE"]))


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


@app.route("/login", methods=['get', 'post'])
def process_user_login():
    if request.method.__eq__("POST"):
        username = request.form.get("username")
        password = request.form.get("password")

        user = dao.auth_user(username, password)
        if user:
            login_user(user)
            next = request.args.get("next")
            return redirect("/" if next is None else next)
    return render_template("/login.html")


@app.route("/logout")
def process_logout_user():
    logout_user()
    return redirect("/login")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/api/cart", methods=['post'])
def put_in_cart():
    '''
    {
    }
    :return:
    '''
    data = request.json

    cart = session.get("cart")

    if cart is None:
        cart = {}

    id = str(data.get("id"))
    if id in cart: #Nếu sản phẩm có trong giỏ
        cart[id]["quantity"] += 1
    else: #Nếu sản phẩm không có trong giỏ
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route("/api/cart/<product_id>", methods=['put'])
def update_cart(product_id):
    cart = session.get("cart")
    if cart and product_id in cart:
        quantity = request.json.get("quantity")
        cart[product_id]["quantity"] = int(quantity)

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route("/api/cart/<product_id>", methods=['delete'])
def delete_cart(product_id):
    cart = session.get("cart")
    if cart and product_id in cart:
        del cart[product_id]

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route("/cart")
def cart():
    return render_template("cart.html")


@app.context_processor
def common_response():
    return {
        "categories": dao.get_categories(),
        "cart": utils.count_cart(session.get("cart"))
    }


if __name__ == '__main__':
    from salesapp.app import admin

    app.run(debug=True)
