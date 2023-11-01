from flask import render_template, request
import dao
from app import app

@app.route("/")
def index():
    kw = request.args.get('kw')
    return render_template("index.html", categories=dao.get_categories(), products=dao.get_products(kw))

if __name__ == '__main__':
    app.run(debug=True)
