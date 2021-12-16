# coding=utf-8
from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS
import json
import os

BODY = 'body'
app = Flask(__name__)
CORS(app)

#with open('data.json') as todos_file:
#    todos = json.load(todos_file)
todos = []

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)

@app.route('/')
def index():
    return u"ToDo API ready!!!"

@app.route('/api/todos/', methods=['GET'])
def list_todos():
    response = jsonify({'todos': todos})
    #response.headers.add("Access-Control-Allow-Origin", "*")
    return response 

@app.route('/api/todos/', methods=['POST'])
def create_todo():
    if not request.json or not BODY in request.json:
        abort(400)

    maxId = max([int(t['id']) for t in todos]) if len(todos) > 0 else 0
    todo = {
        'id': str(maxId + 1),
        BODY: request.json[BODY],
        'done': False
    }
    todos.append(todo)
    response = jsonify(todo)
    #response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 201



@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    print(id, todos)
    todo = [t for t in todos if t['id'] == str(id)]

    if len(todo) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if BODY in request.json and type(request.json[BODY]) != str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) != bool:
        abort(400)
    if '$index' in request.json:
        newIndex = request.json.get('$index')

        if not(isinstance(request.json['$index'], int)):
            abort(400)
        if newIndex < 0:
            abort(400)
        if newIndex >= len(todos):
            abort(400)

        oldIndex = todos.index(todo[0])
        todos.insert(newIndex, todos.pop(oldIndex))

    todo[0][BODY] = request.json.get(BODY, todo[0][BODY])
    todo[0]['done'] = request.json.get('done', todo[0]['done'])

    return jsonify(todo[0])



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)