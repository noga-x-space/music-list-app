from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

def get_db():
    # מחבר למונגו עם בסיס הנתונים admin
    mongo_uri = f"mongodb://{os.environ.get('MONGO_USERNAME')}:{os.environ.get('MONGO_PASSWORD')}@{os.environ.get('MONGO_HOST')}:{os.environ.get('MONGO_PORT', 27017)}/admin"
    client = MongoClient(mongo_uri)
    # לאחר ההתחברות, בוחר את בסיס הנתונים הספציפי
    return client.singers_db

@app.route('/')
def index():
    db = get_db()
    singers = list(db.singers.find())
    songs = list(db.songs.find())
    return render_template('index.html', singers=singers, songs=songs)

@app.route('/add_singer', methods=['POST'])
def add_singer():
    name = request.form.get('name')
    if name:
        db = get_db()
        db.singers.insert_one({'name': name})
    return redirect(url_for('index'))

@app.route('/remove_singer/<singer_id>')
def remove_singer(singer_id):
    db = get_db()
    db.singers.delete_one({'_id': ObjectId(singer_id)})
    db.songs.update_many(
        {'singer_ids': singer_id},
        {'$pull': {'singer_ids': singer_id}}
    )
    return redirect(url_for('index'))

@app.route('/add_song', methods=['POST'])
def add_song():
    title = request.form.get('title')
    singer_ids = request.form.getlist('singers')
    if title and singer_ids:
        db = get_db()
        db.songs.insert_one({
            'title': title,
            'singer_ids': singer_ids
        })
    return redirect(url_for('index'))

@app.route('/remove_song/<song_id>')
def remove_song(song_id):
    db = get_db()
    db.songs.delete_one({'_id': ObjectId(song_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)