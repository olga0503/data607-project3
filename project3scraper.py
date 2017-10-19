
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import nltk
import pandas as pd
import time

def scrape_site():
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    locations = [("New+York%2C+NY","NYC"), ("Los+Angeles%2C+CA","LAN"), ("San+Diego%2C+CA", "SAD"), ("Chicago%2C+IL","CHI"), ("Houston%2C+TX","HOU"), ("Phoenix%2C+AZ", "PHO"), ("Philadelphia%2C+PA", "PHI"), ("San+Antonio%2C+TX", "SAN"), ("Dallas%2C+TX", "DAL"), ("San+Jose%2C+CA", "SAJ")]
    #locations = [("New+York%2C+NY","NY")]
    index = 0
    drop_l = ["new","york", "ny", "nyc", "los", "angeles", "ca", "chicago", "il", "houston", "tx", "phoenix", "az", "philadelphia", "pa", "san", "antonio", "diego", "dallas", "jose", "desired","30","days","ago","upload", "your", "resume", "sexual", "gender", "identity", "orientation" ,"equal", "opportunity", "employer" , "minority", "jobs", "job" , "full", "time", "female", "disability", "affirmative", "action", "contact", "us", "race", "color", "e", "g", "emploment", "without", "regard", "veteran", "diversity", "applicants", "discrimination", "sex"]
    global_l = []
    global_summary_d = {}
    loc_summary_d = {}
    link_check = []
    for location in locations:
        loc = location[0]
        #print(loc)
        full_l = []
        #try:
        loc_d = {}
        url = 'https://www.indeed.com/jobs?as_and=data+science&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=100&l=' + loc + '&fromage=any&limit=100&sort=&psf=advsrch'
        #print(url)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url,headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, 'html.parser')
        links = soup.find_all('a', attrs={'class': re.compile('.*turnstileLink')})
        for link in links:
            if link['href'][0:100] not in link_check:
                link_check.append(link['href'][0:100])    
                #print(link['href'])
                #print(".......")
                #print(link_check)
                entries_l = []
                try:
                    if link['href'].startswith('/pagead'):
                        sub_url = 'https://www.indeed.com' + link['href']
                    elif link['href'].startswith('https'):
                        sub_url = link['href']
                    elif link['href'].startswith('/rc'):
                        sub_url = 'https://www.indeed.com' + link['href']
                    else:
                        sub_url = None
                    req = Request(sub_url,headers=hdr)
                    page = urlopen(req)
                    soup = BeautifulSoup(page, 'html.parser')
                    raw_entries = soup.find_all(['p','li'], text=True) 
                    #print(raw_entries)
                    #'div','span'
                    for entry in raw_entries:
                        try:
                            #print(entry.get_text())
                            #print("______________")
                            entries_l.extend(tokenizer.tokenize(entry.get_text()))
                            full_l.extend(tokenizer.tokenize(entry.get_text()))
                            global_l.extend(tokenizer.tokenize(entry.get_text()))
                        except:
                            pass
                    #print(entries_l)
                    entries_l = [entry.lower() for entry in entries_l if entry not in nltk.corpus.stopwords.words('english')]
                    entries_l = [entry.lower() for entry in entries_l if entry not in drop_l]
                    print(entries_l)
                    freqdist = [(k, v) for k, v in nltk.FreqDist(entries_l).items()]
                    b_freqdist = [(k, v) for k, v in nltk.FreqDist(nltk.bigrams(entries_l)).items()]
                    t_freqdist = [(k, v) for k, v in nltk.FreqDist(nltk.trigrams(entries_l)).items()]
                    loc_d[index] = {"location":location[0], "title":link["title"], "ref":link["href"], "joblist":entries_l, "freqdist":freqdist, "b_freqdist":b_freqdist, "t_freqdist":t_freqdist}
                    index += 1
                    time.sleep(1)
                except:
                    pass
        links_df = pd.DataFrame.from_dict(loc_d, orient="index")
        links_df.to_csv("./links_data_" + location[1] + ".csv", index = False)
        #except
            #pass
        print(location[1])
        full_l = [entry.lower() for entry in full_l if entry not in nltk.corpus.stopwords.words('english')]
        full_l = [entry.lower() for entry in full_l if entry not in drop_l]
        print(full_l)
        print(nltk.FreqDist(full_l).most_common(10))
        print(nltk.FreqDist(nltk.bigrams(full_l)).most_common(10))
        print(nltk.FreqDist(nltk.trigrams(full_l)).most_common(10))
        loc_summary_d[location[1]] = {"location":location[1],"most_common": nltk.FreqDist(full_l).most_common(50), "most_common_bigrams":nltk.FreqDist(nltk.bigrams(full_l)).most_common(50), "most_common_trigrams": nltk.FreqDist(nltk.trigrams(full_l)).most_common(50)}
        time.sleep(1)
    links_summary_df = pd.DataFrame.from_dict(loc_summary_d, orient="index")
    links_summary_df.to_csv("./links_summary_data.csv", index = False)
    global_l = [entry.lower() for entry in global_l if entry not in nltk.corpus.stopwords.words('english')]
    global_l = [entry.lower() for entry in global_l if entry not in drop_l]
    global_summary_d[0] = {"most_common": nltk.FreqDist(global_l).most_common(50), "most_common_bigrams":nltk.FreqDist(nltk.bigrams(global_l)).most_common(50), "most_common_trigrams": nltk.FreqDist(nltk.trigrams(global_l)).most_common(50)}
    global_summary_df = pd.DataFrame.from_dict(global_summary_d, orient="index")
    global_summary_df.to_csv("./links_global_summary_data.csv", index=False)
    return

if __name__ == "__main__":
    scrape_site()