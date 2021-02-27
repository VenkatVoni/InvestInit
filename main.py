from bs4 import BeautifulSoup as bs
from requests import get
import re
import pickle
from os import path
import datetime

base = "https://www.imdb.com"
my_url = 'https://www.imdb.com/feature/genre/?ref_=nv_ch_gr'
file_name = 'dat.pickle'
time_file_name = "date.pickle"


def make_soup(url):
    tex = get(url).text
    soup = bs(tex, features='html.parser')
    return soup


def find_div(soup):
    div_links = soup.find_all('div', attrs={'class': 'ab_links'})
    links = [topic.find_all('a') for topic in div_links][:4]
    type_names = [i.find('h3').text.strip(' ') for i in div_links][:4]
    return zip(type_names, links)


def get_link_dict(link_zip):
    true_links = dict()
    for urls in link_zip:
        link_lis = []
        for link_ in urls[1]:
            link_lis.append(''.join([base, link_['href']]))
        true_links[urls[0]] = link_lis
    return true_links


def make_fin_dict(link_dict):
    final_dict = {}
    for key in link_dict:
        each_dict = {}
        for link in link_dict[key]:
            sp = make_soup(link)
            name = re.search("genres=(.*?)&", link)
            if name:
                top_3 = [(header.find('a').text, base + header.find("a")["href"]) for header in sp.find_all('h3', {'class': 'lister-item-header'})[:3]]
                each_dict[name.group(1)] = top_3
        final_dict[key] = each_dict
    return final_dict


def choice(data):
    for count, type_media in enumerate(data, start=1):
        print(count, type_media.lstrip("Popularime ").rstrip(" by Genre"))
    type_asked = int(input("Enter the number for selection : "))
    for i, type_media in enumerate(data, start=1):
        if type_asked == i:
            for j, genre_media in enumerate(data[type_media], start=1):
                print(j, genre_media, end="\t")
                if j % 3 == 0:
                    print()
            genre_asked = int(input("Enter the genre you want :"))
            for j, genre_media in enumerate(data[type_media], start=1):
                if genre_asked == j:
                    enum_fin = enumerate(data[type_media][genre_media], start=1)
                    for k, name in enum_fin:
                        print(k, name[0], '\n', 'The link to the media :-', name[1])
                    return False
            else:
                print("Wrong choice , enter valid choice")
            break
    else:
        print("Wrong choice , enter valid choice")
    return True


def main(url):
    print("Initializing")
    print("Will take time if you are using the program after a long time\n\n\n")
    time_now = datetime.datetime.now()
    if not path.exists(time_file_name):
        with open(time_file_name, 'wb') as f:
            pickle.dump(time_now, f)
        fin_dict = make_fin_dict(get_link_dict(find_div(make_soup(url))))
        with open(file_name, 'wb') as f:
            pickle.dump(fin_dict, f)
    else:
        with open(time_file_name, 'rb') as f:
            time_then = pickle.load(f)
        if time_now - time_then > datetime.timedelta(days=7):
            fin_dict = make_fin_dict(get_link_dict(find_div(make_soup(url))))
            with open(file_name, 'wb') as f:
                pickle.dump(fin_dict, f)
        else:
            with open(file_name, 'rb') as f:
                fin_dict = pickle.load(f)
    print("Welcome to Best Recommendation Service !!")
    while True:
        print("1.Continue \n2.Exit")
        ch = int(input())
        if ch == 1:
            while choice(fin_dict):
                pass
        else:
            break
    print("Thanks for using the service")


if __name__ == '__main__':
    main(my_url)

