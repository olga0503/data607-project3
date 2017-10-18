
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import nltk
import pandas as pd

def scrape_site():
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    locations = ["New+York,+NY"]
    index = 0
    for location in locations:
        #try:
        loc_d = {}
        url = 'https://www.indeed.com/jobs?as_and=data+science&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=100&l=' + location + '&fromage=any&limit=100&sort=&psf=advsrch'
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url,headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, 'html.parser')
        links = soup.find_all('a', attrs={'class': re.compile('.*turnstileLink')})
        for link in links[0:3]:
            entries_l = []
            try:
                #print(link['title'],link['href'])
                if link['href'].startswith('/pagead'):
                    #print('https://www.indeed.com' + link['href'])
                    sub_url = 'https://www.indeed.com' + link['href']
                    req = Request(sub_url,headers=hdr)
                    page = urlopen(req)
                    soup = BeautifulSoup(page, 'html.parser')
                    raw_entries = soup.find_all(['p','div','span','li'], text=True) 
                    for entry in raw_entries:
                        try:
                            #print(entry.get_text())
                            #print("______________")
                            entries_l.extend(tokenizer.tokenize(entry.get_text()))
                        except:
                            pass
                freqdist = [(k, v) for k, v in nltk.FreqDist(entries_l).items()]
                b_freqdist = [(k, v) for k, v in nltk.FreqDist(nltk.bigrams(entries_l)).items()]
                t_freqdist = [(k, v) for k, v in nltk.FreqDist(nltk.trigrams(entries_l)).items()]
                loc_d[index] = {"location":location, "title":link["title"], "ref":link["href"], "joblist":entries_l, "freqdist":freqdist, "b_freqdist":b_freqdist, "t_freqdist":t_freqdist}
                index += 1
            except:
                pass
        print(loc_d)
        links_df = pd.DataFrame.from_dict(loc_d, orient="index")
        links_df.to_csv("./links_data.csv", index = False)
        #except
            #pass
    return

if __name__ == "__main__":
    scrape_site()