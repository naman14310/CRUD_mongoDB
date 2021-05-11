from flask import Flask
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from passlib.hash import sha256_crypt

# COMMAND FOR GENERATING REQUIREMENTS.TXT ---->  pipreqs <Folder_path>

#-------------------------------------------------------------------------------------------------------------------------------#

app = Flask(__name__, template_folder='template')
cluster = MongoClient("mongodb+srv://<user>:<password>@cluster0.vawkj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# Replace <user> and <password> in above url
#-------------------------------------------------------------------------------------------------------------------------------#

db = cluster["demo_db"]
user = db['user']

#-------------------------------------------------------------------------------------------------------------------------------#

# FETCH DOCS COUNT
def get_doc_count(table):
    count = table.count_documents({})  #-----> will display all documents (rows)
    return count 

#-------------------------------------------------------------------------------------------------------------------------------#

# INSERT 
def insert(table, entry):
    table.insert_one(entry)
    # Use table.insert_many(entries)  ---> for multiple entries
    print("\nINSERT successfully!\n")

#-------------------------------------------------------------------------------------------------------------------------------#

# FIND OR READ OR SELECT
def find(table, filter):
    if filter == None:
        cursor = list(table.find())
        return cursor    
    else:
        cursor = list(table.find(filter))
        # Use table.find_one(filter) ---> for finding one only
        return cursor
#res = find(user, None)
#res2 = find(user, {'name' : 'naman'})

#-------------------------------------------------------------------------------------------------------------------------------#

# UPDATE
def update(table, filter, updation):
    table.update_one(filter, {'$set': updation})
#update(user, {'name' : 'naman'})

#-------------------------------------------------------------------------------------------------------------------------------#

# DELETE
def delete(table, filter):
    if filter == None:
        table.delete_many({})
    else:
        table.delete_one(filter)
#delete(user, None)

#-------------------------------------------------------------------------------------------------------------------------------#

@app.errorhandler(404)
def not_found():
    msg = {
        'status' : 404,
        'message' : 'Not Found' + request.url
    }

    resp = jsonify(msg)
    resp.status_code = 404
    return resp

#-------------------------------------------------------------------------------------------------------------------------------#

@app.route('/add', methods=['POST'])
def add_user():
    usr = request.json
    name = usr['name']
    pwd = usr['password']

    if name and pwd and request.method == 'POST':
        encrypted_password = sha256_crypt.hash(pwd)
        # print(sha256_crypt.verify("password", password)) for password verification
        insert(user, {'name' : name, 'password' : encrypted_password})
        resp = jsonify("User added successfully!")
        resp.status_code = 200
        return resp

    else:
        return not_found()

#-------------------------------------------------------------------------------------------------------------------------------#

@app.route('/users')
def users():
    users = find(user, None)
    resp = dumps(users)
    return resp

#-------------------------------------------------------------------------------------------------------------------------------#

# Here we are receiving name dynamically from url
@app.route('/user/<name>')
def get_user(name):
    usrs = find(user, {'name' : name})
    resp = dumps(usrs)
    return resp

#-------------------------------------------------------------------------------------------------------------------------------#

@app.route('/delete/<name>', methods = ['DELETE'])
def delete_user(name):
    delete(user, {"name" : name})
    resp = jsonify("User deleted successfully!")
    resp.status_code = 200
    return resp

#-------------------------------------------------------------------------------------------------------------------------------#

@app.route('/update/<name_from_url>', methods = ['PUT'])
def update_user(name_from_url):
    usr = request.json
    name = usr['name']
    pwd = usr['password']

    if name and pwd and request.method == 'PUT':
        new_password = sha256_crypt.hash(pwd)
        update(user, {"name" : name_from_url}, {"name" : name, "password" : new_password})
        resp = jsonify("User updated successfully!")
        resp.status_code = 200
        return resp
    else:
        return not_found()

#-------------------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":
    app.run(debug=True)
