from flask import Flask, render_template, request
from datetime import datetime
import pymongo
#dnspython is USUALLY IMPORTED ALONG WITH PYMONGO
from dotenv import load_dotenv #TAKES THE atlas-credentials.env FILE AND LOADS THE VARIABLES INTO THE CODE(CREDENTIALS)
import os

load_dotenv("atlas-credentials.env") # SYNTAX TO LOAD ENV FILE

env_Mongo_URI = os.getenv('MONGODB_URI') #COMES FROM atlas-credentials.emv

if not env_Mongo_URI:
    raise ValueError("MONGODB_URI was not loaded. Check your environment file.")

client = pymongo.MongoClient(
    env_Mongo_URI,
    serverSelectionTimeoutMS=5000
) #CREATED THE CLIENT

client.admin.command('ping')
print("MongoDB connected successfully!")

db = client.demo #DATABASE INSTANCE AND DEMO IS DB NAME

collection = db['flask-tutorial']

app = Flask(__name__)

@app.route('/')
def home():
    dow=datetime.today().strftime('%A')
    current_time=datetime.now().strftime('%H:%M:%S')
    return render_template('index.html', day=dow, t=current_time)

@app.route('/submit', methods=['POST'])
def submit():
    #CONVERTING THE INPUT DATA FROM THE FORM IN
    #"index.html" TO DICTIONARY, SO AS TO PRINT IT.
    form_data = dict(request.form)
    #COLLECTION NAMED 'flask-tutorial' IN DB NAME 'demo', insert_one() IS THE SIMPLEST WAY TO INSERT DATA
    #FORM DATA HAS TO BE A PYTHON DICTIONARY
    collection.insert_one(form_data)

    return 'Data Submitted Succsessfully!'

#AN ADMIN WANTS TO VIEW THE ENTERED DATA IN FLASK SERVER(TERMINAL)
@app.route('/view')
def view():
    #CREATE A LIST CONTAINING ALL DATA SENT TO DATABASE COLLECTION
    data = collection.find() #RETURNS A CURSOR
    data = list(data) # CONVERTS CURSOR TO LIST FOR ITERATING
    #COLLECTION IS A LIST OF DICTIONARIES AND HENCE CANNOT BE PRINTED
    #ITERATING IN THE LIST TO RETURN THE DATA
    for item in data:
        print(item)
        #_id IS A COLUMN THAT MONGODB USES AS UNIQUE ID FOR EACH DATA.
        #IT IS NOT REQUIRED FOR US. TO REMOVE UNWANTED DATA...
        del item['_id']
    #TAKE THE LIST data AND PUT IT AS A RETURNABLE DICTIONARY ON THE WEBSITE
    data = {
        'DATA' : data
    }
    return data

if __name__ == '__main__':
    app.run(debug=True)
