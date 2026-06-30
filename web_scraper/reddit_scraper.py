from bs4 import BeautifulSoup
from pathlib import Path
import requests, json, time, csv

rows = []

SUBREDDIT_LIST_SIZE = 2
COMMENT_LIST_SIZE = 2
id_value = 1

main_dir = Path(__file__).resolve().parent

with open(main_dir / "games_list" / "reddit_urls.json", "r", encoding="utf-8") as f:
    game_urls = json.load(f)

headers = {'User-agent': 'RedditScraper/0.1'}

params = {
    "limit": SUBREDDIT_LIST_SIZE
}

for game, url in game_urls.items():

    print("Scrapping Text for game: " + game + "...")

    data = requests.get(url, headers=headers, params=params)

    # print(data.text)

    soup = BeautifulSoup(data.text, 'xml')

    items = soup.find_all('entry')

    # print(items)

    for item in items:
        item_url = item.find('link')['href'][:-1] + '.rss'
        print(item_url)
        time.sleep(60)
        item_data = requests.get(item_url, headers=headers)
        item_soup = BeautifulSoup(item_data.text, 'xml')
        
        comments = item_soup.find_all('entry')

        # print(item_soup.find_all('entry'))

        for comment in comments:
            # print(comment.find('content').string)
            html_elem = BeautifulSoup(comment.find('content').string.
                                      replace('<!-- SC_OFF -->', '').
                                      replace('<!-- SC_ON -->', ''), "lxml")
            
            text = html_elem.find('div', class_='md').get_text()

            # print(text)

            rows.append({
                        "id": id_value,
                        "game": game,
                        "text": text
                    })
            id_value = id_value + 1

    time.sleep(60)

print('Completed\n')

with open(main_dir / "text_data" / "reddit_text_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "game", "text"])
    writer.writeheader()
    writer.writerows(rows)
