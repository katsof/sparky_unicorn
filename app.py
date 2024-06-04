from flask import Flask, render_template, request, jsonify, json
import requests
from datetime import datetime, timedelta
from collections import Counter

app = Flask(__name__)

# Environment variables should be used in production for keys
NEWSAPI_KEY = 'your_key'
NEWSAPI_ENDPOINT = 'https://newsapi.org/v2/top-headlines'


import os
from dotenv import load_dotenv
import openai

load_dotenv()  # Load environment variables from a .env file if present
openai.api_key = os.getenv('your_key')








from app import Article, Interaction, DebateMessage

# For checking articles
articles = Article.query.all()
print(articles)

# For checking interactions
interactions = Interaction.query.all()
print(interactions)

# For checking debate messages
debate_messages = DebateMessage.query.all()
print(debate_messages)



@app.route('/interact', methods=['POST'])

def record_interaction():
    topic_id = request.form.get('topic_id')
    interaction_type = request.form.get('interaction_type')  # 'agree' or 'disagree'
    user_id = request.form.get('user_id')  # This should come from session or login system

    # Here you would create a new Interaction object with the data
    new_interaction = Interaction(topic_id=topic_id, user_id=user_id, interaction_type=interaction_type)
    
  
    return jsonify(success=True)

import openai
################## OPENN AI SECTION ##############
def summarize_article(article_content):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Ensure you're using the correct and latest model version
        prompt=f"Summarize this news article: {article_content}",
        temperature=0.7,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    summary = response.choices[0].text.strip()
    return summary
def generate_debate_topic(summary):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Update to the latest model as needed
        prompt=f"Generate a debate topic based on this summary: {summary}",
        temperature=0.7,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    debate_topic = response.choices[0].text.strip()
    return debate_topic
@app.route('/generate_debate_topic')
def get_debate_topic():
    articles = fetch_news()  # Assuming this returns a list of articles
    if articles:
        first_article = articles[0]  # Let's take the first article for simplicity
        summary = summarize_article(f"{first_article['title']} {first_article['description']}")
        debate_topic = generate_debate_topic(summary)
        return jsonify(debate_topic=debate_topic, summary=summary)
    else:
        return jsonify(error="No articles available to summarize"), 404



# Global variables for caching and debate messages
cache = {
    'news': None,
    'expiry': datetime.utcnow()
}
debate_messages = []

def fetch_news():
    """Fetch news from the NewsAPI with caching."""
    if cache.get('news') and cache.get('expiry') > datetime.utcnow():
        return cache['news']

    params = {'country': 'us', 'apiKey': NEWSAPI_KEY}
    response = requests.get(NEWSAPI_ENDPOINT, params=params)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        # Filter out articles that have 'null' or missing content
        valid_articles = [article for article in articles if article.get('title') and article.get('description')]
        if not valid_articles:
            # If all articles are removed or invalid, provide a fallback
            valid_articles = [{'title': 'No current news available', 'description': 'Please check back later.'}]
        cache['news'] = valid_articles
        cache['expiry'] = datetime.utcnow() + timedelta(minutes=5)
    else:
        # Log the error and provide a user-friendly message
        print(f"Error fetching articles: {response.status_code}")
        valid_articles = [{'title': 'News fetch error', 'description': f'Unable to fetch news, please try again later. (Error {response.status_code})'}]
    
    return valid_articles

def fetch_news_with_summary():
    articles = fetch_news()  # Your existing function to get news
    if articles:
        # For demonstration, let's summarize and generate a debate topic for the first article
        first_article = articles[0]
        summary = summarize_article(f"{first_article['title']} {first_article['description']}")
        debate_topic = generate_debate_topic(summary)

        # You could add the summary and debate topic to the article dictionary
        first_article['summary'] = summary
        first_article['debate_topic'] = debate_topic

        # Replace the first article in the list with the enriched version
        articles[0] = first_article

    return articles


@app.route('/get_articles')
def get_articles():
    """Route to serve articles as JSON."""
    articles = fetch_news()
    return jsonify(articles=articles)

@app.route('/')
def home():
    """Home page route."""
    return render_template('index.html')

@app.route('/debate', methods=['GET', 'POST'])
def debate():
    """Debate page route."""
    if request.method == 'POST':
        message = request.form.get('message')
        if message:  # Check if the message is not empty
            debate_messages.append(message)
    return render_template('debate.html', messages=debate_messages)

@app.route('/trending')
def trending():
    """Trending topics route."""
    articles = fetch_news()
    headlines = [article['title'] for article in articles]
    trending_topics = Counter(headlines)
    return render_template('trending.html', trending_topics=trending_topics.most_common(10))

if __name__ == '__main__':
    #app.run(debug=True, port=5001)
    app.run(debug=True, port=5001, use_reloader=False)