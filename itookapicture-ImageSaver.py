import praw
import urllib
import json
import MySQLdb
from time import sleep
from urlparse import urlparse

from pprint import pprint

# Get settings
with open('config.json') as json_data_file:
  settings = json.load(json_data_file)
# print(settings['reddit']['username']);

# Connect to db
db = MySQLdb.connect("localhost", settings['db_info']['user'], settings['db_info']['pass'], settings['db_info']['db']);
cursor = db.cursor();

def get_submissions():
  r = praw.Reddit(user_agent='linux:itookapicture-ImageSaver:1.0 - Looking at pictures of ITAP');
  submissions = r.get_subreddit('itookapicture').get_top();
  return submissions

def save_image(imageURL):
  URL = urlparse(imageURL);
  if URL.netloc == 'i.imgur.com':
    urllib.urlretrieve(imageURL, settings['save_path'] + URL.path);

def db_insert_rid(rid):
  with db:
    cursor.execute("INSERT INTO pictures(rid) VALUES (%s)", rid);

def db_check_existing_rid(rid):
  with db:
    cursor.execute("SELECT * FROM pictures WHERE rid = %s", rid);
    result = cursor.fetchone();
    if result is None:
      return False;
    return True;


while True:
  submissions = get_submissions();
  for submission in submissions:
    if not db_check_existing_rid(submission.id):
      db_insert_rid(submission.id);
      save_image(submission.url);
  sleep(1800);
