from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import datetime
import requests
import calendar
import os

load_dotenv()
rapid_api_key = os.getenv("RAPID_API_KEY")

app = Flask(__name__)


def request_to_numbersAPI(day, month, year):
	date_url = f"https://numbersapi.p.rapidapi.com/{month}/{day}/date"
	year_url = f"https://numbersapi.p.rapidapi.com/{year}/year"
	querystring = {"fragment":"true", "json":"true"}
	headers = {
		"X-RapidAPI-Key": rapid_api_key,
		"X-RapidAPI-Host": "numbersapi.p.rapidapi.com"
	}
	response = {}
	response['response_date'] = requests.get(date_url, headers=headers, params=querystring).json()
	response['response_year'] = requests.get(year_url, headers=headers, params=querystring).json()
	return response	
    

@app.route('/', methods=['GET', 'POST'])
def home():
    todays_date = datetime.date.today()
    current_date = datetime.date.today()
    day, month, year = 0, 0, 0
    response = {}
    if request.method == 'POST':
        date = request.form['date']
        year, month, day = date.split('-')[0], date.split('-')[1], date.split('-')[-1]
        response = request_to_numbersAPI(day, month, year)
        current_date = date
    return render_template('home.html', 
                            todays_date=todays_date,
                           	current_date=current_date, 
                            response=response,
                            day=day, month=calendar.month_name[int(month)], year=year)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404