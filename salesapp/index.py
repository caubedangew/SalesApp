from flask import Flask, render_template, request
import dao

app = Flask(__name__)

@app.route("/")
def index():
    kw = request.args.get('kw')
    return render_template("index.html", categories=dao.get_categories(), products=dao.get_products(kw))

if __name__ == '__main__':
    app.run(debug=True)
