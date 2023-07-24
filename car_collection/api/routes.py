from flask import Blueprint, request, jsonify
from car_collection.helpers import token_required
from car_collection.models import db, Car, car_schema, cars_schema




api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
def getdata():
    return { 'some': 'value'}

#Create
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(our_user):

    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    description = request.json['description']
    price = request.json['price']
    miles_per_gallon = request.json['miles_per_gallon']
    max_speed = request.json['max_speed']
    seats = request.json['seats'] 
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    car = Car(make, model, year, color, description, price, miles_per_gallon, max_speed, seats, user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)


@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(our_user, id):
    if id:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'message': 'ID is missing'}), 401
    

@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(our_user):
    token=our_user.token
    cars = Car.query.filter_by(user_token = token).all()
    response = cars_schema.dump(cars)

    return jsonify(response)



@api.route('/cars/<id>', methods = ['PUT'])
@token_required
def update_car(our_user, id):
    car = Car.query.get(id)

    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.color = request.json['color']
    car.description = request.json['description']
    car.price = request.json['price']
    car.miles_per_gallon = request.json['miles_per_gallon']
    car.max_speed = request.json['max_speed']
    car.seats = request.json['seats'] 
    car.user_token = our_user.token

    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)


@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(our_user, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)

