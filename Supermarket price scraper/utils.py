# Libraries
import re
from bs4 import BeautifulSoup
import requests


# Function to access the html of the websites via BeautifulSoup
def get_soups(url):
    html_text = requests.get(url).content
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup


# Function to navigate the html's elements and build the urls with the catalog's sections
def get_dpts(soup):
    nav_sub_cont = soup.find_all("ul", {"id": "nav-submenu-container"})
    nav_submenu = nav_sub_cont[0]
    urls = []
    for item in nav_submenu:
        if item.name and "iconoCat" in item.contents[1].attrs['class']:
            href = item.find('a', href=True)
            urls.append(href.get('href'))
    return urls


# Function to build urls to access to each product
def get_products(dpt, root_url):
    products = []                                  # Array of arrays with price of description of each product
    show_dpto = root_url + dpto
    soup = get_soups(show_dpto)
    products.append(soup.h1.text)                  # First entry in array is the department's name

# Loop to get names of the elements of the pages of interest
    while soup is not None:
        forms = soup.find_all('form')
        for f in forms:
            if len(f.contents) == 15:
                name = f.attrs['data-productdescription']
                name = re.sub("\\n", "", name)     # Delete newline
                price = f.find('input', class_="price").attrs['value']
                products.append([name, price])
        nx = soup.find('a', rel="next")            # Find the "nextpage" button
        soup = None
        if nx is not None:                         # If it exists, go to the next page
            nx_url = nx.get("href")
            soup = get_soups(root_url + nx_url)

    return products
