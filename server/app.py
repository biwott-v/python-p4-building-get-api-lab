from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Bakery, BakedGood

@app.route('/')
def home():
    return '<h1>Bakery API</h1>'

@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    bakeries_data = [bakery.to_dict(include_baked_goods=True) for bakery in bakeries]
    return jsonify(bakeries_data)

@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    return jsonify(bakery.to_dict(include_baked_goods=True))

@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()
    baked_goods_data = [bg.to_dict(include_bakery=True) for bg in baked_goods]
    return jsonify(baked_goods_data)

@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(desc(BakedGood.price)).first()
    if most_expensive:
        return jsonify(most_expensive.to_dict(include_bakery=True))
    return jsonify({"error": "No baked goods found"}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)