import requests
from bs4 import BeautifulSoup
import praw
import re
import pandas as pd
from tqdm import tqdm

nsubreddits = 250
subreddits_per_page = 125
blacklist = ["announcements", "wallstreetbets"]
subreddits = []

for n in range(1, (nsubreddits//subreddits_per_page)+1):
    r = requests.get(f"http://www.redditlist.com/?page={n}")
    soup = BeautifulSoup(r.text, "html.parser")
    subreddits.extend([x.text for x in soup.find(id="listing-parent").findAll(class_="span4 listing")[1].findAll("a", attrs={"class": "sfw"})])
    
subreddits = [x for x in subreddits if x not in blacklist]

df = pd.DataFrame(columns = ['Title', 'Subreddit'])

reddit = praw.Reddit(
    "user1",
    user_agent="android:com.example.myredditapp:v1.2.3",
)
    
assert reddit.read_only == True

for subreddit_name in tqdm(subreddits):
    # print("Scraping {}", subreddit_name)
    subreddit = reddit.subreddit(subreddit_name)

    for submission in subreddit.top(limit=1000):
        title = submission.title
        title = re.sub("\[.*?\]",'',title)
        title = '"'+title+'"'
        row = pd.DataFrame({'Title' : [title], 'Subreddit' : [subreddit_name]})
        df = pd.concat([df, row], axis=0, ignore_index=True)

df.to_csv('dataset.csv')
