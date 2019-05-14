import requests
import pygal

from operator import itemgetter

# Make an API call and store the response
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)

print("Status Code: " + str(r.status_code))

# Process informtion about each submission

submission_ids = r.json()
submission_dicts, titles = [], []
for submission in submission_ids[:30]:
    # Make a separate API call for each submission
    url = ('https://hacker-news.firebaseio.com/v0/item/' + 
        str(submission) +'.json')
    submission_r = requests.get(url)
    print(submission_r.status_code)
    response_dict = submission_r.json()
    
    submission_dict = {
    'title':response_dict['title'],
    'link':('htt://news.ycombinator.com/item?id-' + str(submission)),
    'value':response_dict.get('descendants', 0)
    }
    print(response_dict['descendants'])
    submission_dicts.append(submission_dict)
    titles.append(response_dict['title'])

submission_dicts = sorted(submission_dicts, key=itemgetter('value'),
    reverse=True)

for submission_dict in submission_dicts:
    print("\nTitle:", submission_dict['title'])
    print("Discussion link:", submission_dict['link'])
    print("Comments:", submission_dict['value'])
    
chart = pygal.Bar(x_label_rotation=90)
chart.add('Articles', submission_dicts)
chart.x_labels = titles


chart.render_to_file('hacker_news.svg')

