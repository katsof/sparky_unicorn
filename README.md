# sparky_unicorn

Still under development
A Flask-based web application that fetches the latest news headlines and provides summaries of news articles using OpenAI's GPT-3.

### Features
Fetch Latest News: Retrieves top headlines from the NewsAPI.
Article Summarization: Uses OpenAI's GPT-3 to generate concise summaries of news articles.
Interactive Web Interface: Displays news headlines on the home page and allows users to submit articles for summarization.
### Setup and Installation
Prerequisites
Python 3.6 or higher
Flask
Requests
OpenAI
Dotenv
### Usage
Home Page: Displays the top headlines fetched from the NewsAPI.
Summarization: Users can input the content of a news article to get a summarized version generated by GPT-3.
### Code Overview
app.py: Main application file containing the Flask app and route definitions.
templates/index.html: HTML template for displaying the news headlines.
fetch_news(): Function to fetch the latest news articles from the NewsAPI.
summarize_article(article_content): Function to summarize a given article using GPT-3.
Environment Variables: Used for storing API keys securely.
