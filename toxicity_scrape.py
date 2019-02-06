import requests
from bs4 import BeautifulSoup
import pandas as pd

'''
https://en.wikipedia.org/wiki/List_of_poisonous_fungus_species

>>Edible category pages:
https://en.wikipedia.org/wiki/Category:Edible_fungi
https://en.wikipedia.org/w/index.php?title=Category:Edible_fungi&pagefrom=Lactarius+glyciosmus%0ALactarius+glyciosmus#mw-pages
https://en.wikipedia.org/w/index.php?title=Category:Edible_fungi&pagefrom=Suillus+Pungens%0ASuillus+pungens#mw-pages

>>Poisonous category pages:
https://en.wikipedia.org/wiki/Category:Poisonous_fungi
'''




def names_from_wiki_category_url(url: str):
    edible1_url = requests.get(url).text
    soup = BeautifulSoup(edible1_url,'lxml')

    # 1 find all groups
    categories = soup.find_all('div',{'class':'mw-category-group'})

    # 2 find all mushroom groups
    mushroom_categories = []
    for elem in categories:
         res = elem.find("h3")
         if res is None: continue
         restext = res.text
         if len(restext)==1 and str(restext).isalpha():
             mushroom_categories.append(elem)

    # 3 extract relevant blocks
    blocks = []
    for elem in mushroom_categories:
        blocks+= elem.find_all("a")

    # 4 extract names from blocks
    names = []
    for block in blocks:
        names.append(block.text)
    return names


def get_wiki_category_names():
    edible_urls = [
    "https://en.wikipedia.org/wiki/Category:Edible_fungi",
    "https://en.wikipedia.org/w/index.php?title=Category:Edible_fungi&pagefrom=Lactarius+glyciosmus%0ALactarius+glyciosmus#mw-pages",
    "https://en.wikipedia.org/w/index.php?title=Category:Edible_fungi&pagefrom=Suillus+Pungens%0ASuillus+pungens#mw-pages"
    ]

    edible_names = []
    for i,url in enumerate(edible_urls):
        names = names_from_wiki_category_url(url)
        print(i,len(names))
        edible_names += names

    poisonous_urls = ["https://en.wikipedia.org/wiki/Category:Poisonous_fungi"]

    poisonous_names = []
    for i,url in enumerate(poisonous_urls):
        names = names_from_wiki_category_url(url)
        print(i,len(names))
        poisonous_names += names

    edible_column = "wiki_category_edible"
    edible_df = pd.DataFrame(edible_names, columns=["name"])
    edible_df[edible_column]=True
    poisonous_df = pd.DataFrame(poisonous_names, columns=["name"])
    poisonous_df[edible_column]=False
    return edible_df.append(poisonous_df).reset_index(drop=True)

if __name__ == "__main__":
    df = get_wiki_category_names()
    df.to_csv("edible.csv")
