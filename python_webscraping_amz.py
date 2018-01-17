import sqlite3
import urllib.error
import ssl
from urllib.parse import urljoin as ujoin
from urllib.parse import urlparse as upar
from urllib.request import urlopen as uopen
from bs4 import BeautifulSoup as soup

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# using Amazon with keyword of laptop
my_url = "https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=laptop"

try:
    #my_url = "https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=graphic+card&ignorear=0&N=-1&isNodeId=1"
# opening up connection
    uClient = uopen(my_url, context=ctx)
    page_html = uClient.read()
    if page_html.getcode() !=200:
        print("Error on page", page_html.getcode())
    uClient.close()
except:
    print("Unable to retrieve or parse page")
    #continue

#html parsing
page_soup = soup(page_html, "html.parser")

#graps each product: s-item-container is for Amazon,
# while for newegg, it will be item-container
#containers = page_soup.findAll("li",{"class":"s-result-item celwidget"})
containers = page_soup.findAll("div", {"class":"s-item-container"})
#containers = page_soup.findAll("div",{"class":"item-container"})

filename = "amazon_laptop.csv"
f = open(filename,"w")

header = "product_name, price\n"
f.write(header)

for container in containers:

    title_tag = container.find("h2", {"class":"a-size-base s-inline s-access-title a-text-normal"})
    product_name = title_tag.text
    try:
        price_tag = container.find("span",{"class":"a-offscreen"})
        if price_tag is None:
            continue #price_tag = container.find("span",{"class":"sx-price-whole"})
        #if price_tag is Non: continue
        price = price_tag.string
        price2 = price.split("$")[1]
    except:
        print("No price tag is found")

    #title_container = container.findAll("a",{"class":"item-title"})
    #product_name = title_container[0].text
    #shipping_container =container.findAll("li",{"class":"price-ship"})
    #shipping = shipping_container[0].text.strip()

    #print("brand" + brand)
    print("product_name " , product_name)
    print("price ", price)

    f.write( product_name.replace(","," ") + "," + price + "\n")

f.close()
