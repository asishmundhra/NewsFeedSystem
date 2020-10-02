# News Feed Management System
The objective is to design and develop small working prototype of centralized newsfeed system.
## Description
A simple newsfeed management system that takes a text file containing the URL of news sites . 
Further it reads & extracts security code of individual news from the symbols.pickle file & stores these feeds as JSON files by date.
- Loop through symbols.pickle file & create a link by extracting security code from each row .
- Extracts article link from that URL
- Parses these links through Newspaper3k API
- Selects required fields
- The JSON file contain fields such as author, text, current_date, story_date, story_time, source etc..
- The fields are described here:
  - author - article author
  - text - article text 
  - summary - article summary 
  - title - story title 
  - keywords - article keywords 
  - company_code - security code extracted from symbols.pickle file    
  - company_name - comapany full name          
  - source - newspaper (give abbreviations to newspaper)  
  - story_date - extract story date from article  
  - story_time - extract story time from article  
  - current_date - current date
  - timestamp - current datetime object 
  - storytimestamp - story datetime object

- Stores every article object in MongoDB

## Features
1. No duplicity of feed by combination of (title, story_date, …).
2. Newsfeed document is stored in MongoDB database.
3. Storing the Newsfeed in JSON file.
4. Storing the source of the article.
5. Articles captured on a specific date can be retrieved.

## Contents
- `scraper.py` - to scrape the details from a given list of articles or news-websites
- `article.json` - gives all the scraped details in .json format
- `server/requirement.txt` - contains all the packages required to be installled, to run the program.
- `server/db.py` - connects the API to MongoDB cluster
- `server/main.py` - Initiates a local host development server(Here: http://127.0.0.1:8080/)

## Running locally
- Fork and clone the repo .
- `cd` to the API directory eg. cd server .
- Create an environment:
   - For macOS or Linux: `pip install virtualenv`
      - This line will create a virtualenv : `virtualenv virtualenv_name`
   - For windows:  `pip install virtualenv`
      - This line will create a virtualenv : `virtualenv myenv`
- Activate the Flask-python environment by:
   - For macOS or Linux: `source virtualenv_name/bin/activate`
   - For windows: `myenv\Scripts\activate`
- In the same environment, install all the packages specified in the requirement.txt file.
- Run `python main.py` to start the server .
- Open the browser and go to `http://localhost:8080/?date=MM/DD/YY` .
   Eg: `http://localhost:8080/?date=09/14/20` outputs all the articles published on 09/14/20 .
- Give the date as an input given in the specified format(MM/DD/YY), to retrieve all the news stories published on the same day in JSON format .
- Deactivate the environment after the process by typing `deactivate` in command prompt .

