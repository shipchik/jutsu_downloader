from bs4 import BeautifulSoup
import cloudscraper
import os
import shutil
import shutil
from tqdm.auto import tqdm


def download_videos(links, scraper, directory_name):
    print(f"всего {len(links)} серий")
    fr=int(input("from: "))
    to=input("to(skip if all):")
    if to=='':
        to=len(links)
    else:
        to=int(to)
    
    video_quantity = len(links)
    try:
        os.mkdir(f"./{directory_name}")
    except:
        shutil.rmtree(f"./{directory_name}")
        os.mkdir(f"./{directory_name}")
    finally:
        pass

    
    for i in range(fr-1,to-1,1):
        with scraper.get(links[i], stream=True) as r:
            total_length = int(r.headers.get("Content-Length"))
            with tqdm.wrapattr(r.raw, "read", total=total_length, desc="")as raw:
                with open(f'./{directory_name}/{i}.mp4', 'wb') as file:
                    shutil.copyfileobj(raw, file)
            print(f'{i+1}/{video_quantity} video downloaded')
        


def main():
    scraper = cloudscraper.create_scraper(delay=10, browser={'custom': 'ScraperBot/1.0', })
    link = input("Hello, please enter an anime link from jut.su(ex. https://jut.su/chainsaw-man/): \n")
    


    sub_list = ['https://jut.su/', 'jut.su/', '/']
    name = link
    for sub in sub_list:
        name = name.replace(sub, '')

    quality = input(" 1)1080p   2)720p    3)480p   4)360p\nEnter quality:")

    qual = {
        1: "1080",
        2: "720",
        3: "480",
        4: "360"
    }
    response = scraper.get(link)

    soup = BeautifulSoup(response.text, "html.parser")
    series = soup.find_all("a", class_=["short-btn black video the_hildi", "short-btn green video the_hildi"])
    links = []
    i=1
    for serie in series:
        
        response = scraper.get(f'https://jut.su{serie["href"]}')
        soup = BeautifulSoup(response.content, "html.parser")
        inf = soup.find_all('source', res=qual[int(quality)])
        links.append(inf[0]['src'])
        i+=1
    
    download_videos(links, scraper, directory_name=name)


if __name__ == '__main__':
    main()
