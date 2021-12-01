import json
import urllib.request

from flask import Flask, request, jsonify, Response

app = Flask(__name__)
url = "https://www.10bis.co.il/NextApi/GetRestaurantMenu?culture=en&uiCulture=en&restaurantId=19156&deliveryMethod=pickup"



def extract_json():
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode())
    return data


def extract_dishes(dish_type):
    categories = json_data['Data']['categoriesList']
    dishes = {}
    dish_data = {}
    for category in categories:
        if category['categoryName'] == dish_type:
            dish_data = category['dishList']
    for dish in dish_data:
        dishes[dish['dishId']] = {key: value for key, value in dish.items() if
                                        key == 'dishId' or key == 'dishName' or key == 'dishDescription' or key == 'dishPrice'}
    return dishes


json_data = extract_json()


@app.route('/')
def welcome():
    return 'Welcome!'


@app.route('/drinks')
def get_drinks():
    return jsonify(extract_dishes('Drinks'))


@app.route('/drink/<id>')
def get_drink_by_id(dish_id):
    drinks = extract_dishes('Drinks')
    return jsonify(drinks[int(dish_id)])


@app.route('/pizzas')
def get_pizzas():
    return jsonify(extract_dishes('Pizzas'))


@app.route('/pizza/<id>')
def get_pizza_by_id(dish_id):
    pizzas = extract_dishes('Pizzas')
    return jsonify(pizzas[int(dish_id)])


@app.route('/desserts')
def get_desserts():
    return jsonify(extract_dishes('Desserts'))


@app.route('/dessert/<id>')
def get_desserts_by_id(dish_id):
    desserts = extract_dishes('Desserts')
    return jsonify(desserts[int(dish_id)])


@app.route('/order')
def total_sum_of_order():
    total = 0
    if request.method == 'POST':
        user_order = request.get_json(force=True)
        for category in user_order:
            dishes = extract_dishes(category.key())
            for dish_id in category:
                total += dishes[int(dish_id)]['dishPrice']
        return Response({"price": total})
    if request.method == 'GET':
        return "Unauthorized access!"


if __name__ == '__main__':
    app.run()
