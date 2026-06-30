from bs4 import BeautifulSoup
from pathlib import Path
import requests, csv, json

rows = []

FORUM_LIST_PAGE_SIZE = 2
COMMENT_LIST_PAGE_SIZE = 2
id_value = 1

main_dir = Path(__file__).resolve().parent

with open(main_dir / "games_list" / "steam_urls.json", "r", encoding="utf-8") as f:
    game_urls = json.load(f)

for game, url in game_urls.items():

    print("Scrapping Text for game: " + game + "...")

    params = {
        "fp" : 1
    }

    for i in range(FORUM_LIST_PAGE_SIZE):

        params['fp'] = params['fp'] * (i + 1)

        data = requests.get(url, params=params)
        parent_html = data.text

        soup = BeautifulSoup(parent_html, 'lxml')

        forum_discussions = soup.find('div', class_='forum_area').find_all('a', class_='forum_topic_overlay')

        for discussion in forum_discussions:

            child_params = {
                "ctp" : 1
            }

            for j in range(COMMENT_LIST_PAGE_SIZE):
                child_params['ctp'] = child_params['ctp'] * (j + 1)

                new_data = requests.get(discussion['href'], params=child_params).text

                child_soup = BeautifulSoup(new_data, 'lxml')

                comments = child_soup.find_all('div', class_='commentthread_comment_text')

                for comment in comments:

                    for child in comment.find_all():
                        child.extract()

                    text = comment.get_text(strip=True)
                    # print(text)
                    rows.append({
                        "id": id_value,
                        "game": game,
                        "text": text
                    })
                    id_value = id_value + 1

    print('Completed\n')

with open(main_dir / "text_data" / "steam_text_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "game", "text"])
    writer.writeheader()
    writer.writerows(rows)
    
    
