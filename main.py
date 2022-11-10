from bs4 import BeautifulSoup
import cloudscraper
import os
import shutil


def download_videos(links, scraper, directory_name):
    video_quantity = len(links)
    try:
        os.mkdir(f"./{directory_name}")
    except:
        shutil.rmtree(f"./{directory_name}")
        os.mkdir(f"./{directory_name}")
    finally:
        pass

    i = 1
    for link in links:
        r = scraper.get(link, stream=True)
        with open(f'./{directory_name}/{i}.mp4', 'wb') as file:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)
            print(f'{i}/{video_quantity} video downloaded')
        i += 1


def main():
    scraper = cloudscraper.create_scraper(delay=10, browser={'custom': 'ScraperBot/1.0', })
    link = input("Hello, please enter an anime link from jut.su(ex. https://jut.su/chainsaw-man/): \n")
    count = input("Write a count of series. Skip if all:")


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
        if i==count and count!='':
            break
        response = scraper.get(f'https://jut.su{serie["href"]}')
        soup = BeautifulSoup(response.content, "html.parser")
        inf = soup.find_all('source', res=qual[int(quality)])
        links.append(inf[0]['src'])
        i+=1

    download_videos(links, scraper, directory_name=name)


if __name__ == '__main__':
    main()
