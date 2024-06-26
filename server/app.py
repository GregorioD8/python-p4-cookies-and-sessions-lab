#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

# Define the route for listing all articles
@app.route('/articles')
def index_articles():
    # Query all articles and convert them to dictionaries

    articles = [article.to_dict() for article in Article.query.all()]
    #Return a JSON response with the list of articles
    return make_response(jsonify(articles), 200)

# Define teh route for showing a single article
@app.route('/articles/<int:id>', methods=['GET'])
def show_article(id):
    # Get 'page_views' from session, default to 0 if not set
    # Use a ternary-like operation to initialize 'page_views' in session if not already set
    session['page_views'] = session.get('page_views') or 0
    # Increment 'page_views' by 1
    session['page_views'] += 1

    # Check if the user has viewed 3 or fewer pages
    if session['page_views'] <= 3: 
        #Return the Article as a JSON
        return Article.query.filter(Article.id == id).first().to_dict(), 200
    #Return an error message if page view limit is exceeded
    return {'message': 'Maximum pageview limit reached'}, 401 


if __name__ == '__main__':
    app.run(port=5555)
