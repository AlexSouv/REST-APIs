# Name: Alex Souv
# Date: 10/14/2022
# Assignment: HW3
# File: server.py
# Description: Simple Python Flask Web Server to build a REST API.

from flask import Flask, request, jsonify

app = Flask(__name__)

PORT = 8080
HOST = "127.0.0.1"

user_data = [
{"id": 1, "name": "Alex", "type": "chef"},
{"id": 2, "name": "Daniel", "type": "chef"},
{"id": 3, "name": "John", "type": "chef"},
{"id": 4, "name": "Eric", "type": "chef"}
]

recipe_data = [
    {"id": 1, "user_id": 1, "steps": "don't eat dough"},
    {"id": 2, "user_id": 1, "steps": "mix batter"},
    {"id": 3, "user_id": 1, "steps": "bake cookies"},
    {"id": 4, "user_id": 2, "steps": "chop lettuce"},
    {"id": 5, "user_id": 3, "steps": "bake potato"},
    {"id": 6, "user_id": 4, "steps": "cut onions"}
    ]


def find_next_id(data_list: list):
    return max(data["id"] for data in data_list) + 1

#CRUD for user_data
#GET all users

@app.get("/api/v1/users")
def get_all_user_data():
    return jsonify(user_data)

#GET one user
@app.get("/api/v1/users/<int:user_id>")
def get_one_user_data(user_id: int):
    data = [data for data in user_data if data['id'] == user_id]
    if len(data) == 0:
        return {"error": f"No data found for ID {user_id}"}, 404
    return jsonify(data), 200 #instead of 0 find a way to get all info on user_id

#POST/add a user
@app.post("/api/v1/users")
def add_user_data():
    if request.is_json:
        response = request.get_json()
        if "name" not in response or "type" not in response:
            return {"error": f"Missing fields"}, 400
        #TODO: Add a error handling for here
        if response["name"] == "" or response["type"] == "":
            return {"error": f"Missing fields"}, 400
        response["id"] = find_next_id(user_data)
        user_data.append(response)
        return response, 201
    return {"error": "Request must be JSON"}, 415

#PUT edit an existing user
@app.put("/api/v1/users/<int:user_id>")
def edit_user_data(user_id: int):
    if request.is_json:
        data = [data for data in user_data if data['id'] == user_id]
        if len(data) == 0:
            return {"error": f"No data found for ID {user_id}"}, 404
        if 'name' in request.json:
            data[0]['name'] = request.json.get('name') or data[0]['name']
            return jsonify(data[0]), 200
        else:
            return {"error": "Malformed request. Missing required user fields"}, 400
    return {"error": "Request must be JSON"}, 415

#DELETE existing user
@app.delete("/api/v1/users/<int:user_id>")
def delete_user_data(user_id: int):
    datalist = [data for data in user_data if data['id'] == user_id]
    if len(datalist) == 0:
        return {"error": f"No data found for ID {user_id} cannot delete"}, 404
    user_data.remove(datalist[0])
    recipe_num = [data for data in recipe_data if data['user_id'] == user_id]
    for x in recipe_num:
        y = x['id']
        delete_recipe_data(user_id, y)
    return {"sucess": f"Deleted user {user_id}"}, 204

#start of the CRUD for recipe

#GET all user's recipes
@app.get("/api/v1/users/<int:user_id>/recipes")
def get_all_user_recipes(user_id: int):
    datalist = [data for data in recipe_data if data['id'] == user_id]
    if len(datalist) == 0:
        return {"error": f"No recipes found for ID {user_id}"}, 404
    return jsonify(datalist), 200

#GET all recipes for that user
@app.get("/api/v1/users/<int:user_id>/recipes/<int:recipe_id>")
def get_user_recipes(user_id: int, recipe_id: int):
    datalist = [data for data in recipe_data if data['user_id'] == user_id and data['id'] == recipe_id]
    if len(datalist) == 0:
        return {"error": f"No recipes found for ID {user_id} under recipe {recipe_id}"}, 404
    return jsonify(datalist), 200

#POST a new recipe for a user
@app.post("/api/v1/users/<int:user_id>/recipes")
def add_recipe(user_id: int):
    if request.is_json:
        response = request.get_json()
        if "steps" not in response:
            return {"error": f"Missing fields"}, 400
        found_users = [user for user in user_data if user['id'] == user_id]
        if len(found_users) == 0:
            return {"error": f"No data found for ID {user_id}"}, 404
        response["id"] = find_next_id(recipe_data)
        recipe_data.append(response)
        return jsonify(response), 200
    return {"error": "Request must be JSON"}, 415

#PUT or edit a existing recipe
@app.put("/api/v1/users/<int:user_id>/recipes/<int:recipe_id>")
def edit_recipe_data(user_id: int, recipe_id: int):
    if request.is_json:
        datalist = [data for data in recipe_data if data['user_id'] == user_id and data['id'] == recipe_id]
        if len(datalist) == 0:
            return {"error": f"No data found for ID {recipe_id}"}, 404
        if 'steps' in request.json:
            datalist[0]['steps'] = request.json.get('steps') or datalist[0]['steps']
            return jsonify(datalist[0]), 200
        else:
            return {"error": "Malformed request. Missing required user fields"}, 400
    return {"error": "Request must be JSON"}, 415

#DELETE an existing user's recipe
@app.delete("/api/v1/users/<int:user_id>/recipes/<int:recipe_id>")
def delete_recipe_data(user_id: int, recipe_id: int):
    datalist = [data for data in recipe_data if data['user_id'] == user_id and data['id'] == recipe_id]
    if len(datalist) == 0:
        return {"error": f"No data found for ID {recipe_id} cannot delete"}, 404
    recipe_data.remove(datalist[0])
    return {"sucess": f"Deleted recipe"}, 204


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)