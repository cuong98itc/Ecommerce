import json
import requests
import mysql.connector
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import time
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="websitebangiay"
)
mycursor = mydb.cursor()
# mycursor.execute("CREATE TABLE IF NOT EXISTS store_productdev(ID id AUTO_INCREMENT PRIMARY KEY, name VARCHAR(200), price double, ratingstars double, priceminbeforediscount double, historicalsold double, cmtcount double, rawdiscount double, description longtext, digital longtext, description longtext)")


def mining(name, price, ratingstars, priceminbeforediscount, historicalsold, cmtcount, rawdiscount, description, digital, baner, likedcount, url, digitalCmt, digitalLike, digitalStart):
    sql = "insert ignore into store_productdev(id, name, price, ratingstars, priceminbeforediscount, historicalsold, cmtcount, rawdiscount, description, digital, baner, likedcount, url, digitalCmt, digitalLike, digitalStart) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = ('null', name, price, ratingstars, priceminbeforediscount, historicalsold, cmtcount, rawdiscount, description,digital, baner, likedcount, url, digitalCmt, digitalLike, digitalStart)
    mycursor.execute(sql, val)
    mydb.commit()
    print('=> Inserted scholarship with Title: ', name)
    print("___price: ", price)
    print("___ratingstars: ", ratingstars)
    print("___historicalsold: ", historicalsold)
    print("___url ", url)



def getdata(keyword):
    url = "https://shopee.vn/api/v4/search/search_items"
    querystring = {"by": "relevancy", "keyword": keyword, "limit": "50","newest": "0", "order": "desc", "page_type": "search", "version": "2"}
    response = requests.request("GET", url, params=querystring)
    source = json.loads(response.text)
    sourceshop = source['items']
    

    for item in sourceshop:
        linkshop = 'https://shopee.vn/api/v2/item/get?itemid='+str(item['itemid'])+'&shopid='+str(item['shopid'])
        
        def info(url):
            headers = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "vi,en;q=0.9",
                "referer": url,
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/94.0.202 Chrome/88.0.4324.202 Safari/537.36",
                "x-api-source": "pc",
                "x-requested-with": "XMLHttpRequest",
                "x-shopee-language": "vi"
            }
            response = requests.request("GET", url, headers=headers)
            data = json.loads(response.text)
            try:
                description = data['item']['description']
            except:
                description = ''
            return description

        try:
            name = item['item_basic']['name']
        except:
            name = ''
        try:
            price = int(str((item['item_basic']['price']))[:-5])
        except:
            price = 0
        try:
            ratingstars = round(item['item_basic']['item_rating']['rating_star'], 1)
        except:
            ratingstars = 0
        try:
            priceminbeforediscount = int(str((item['item_basic']['price_max_before_discount']))[:-5])
        except:
            priceminbeforediscount = 0
        try:
            historicalsold = (item['item_basic']['historical_sold'])
        except:
            historicalsold = 0
        try:
            cmtcount = item['item_basic']['cmt_count']
        except:
            cmtcount = 0
        try:
            rawdiscount = item['item_basic']['raw_discount']
        except:
            rawdiscount = 0
        try:
            baner ='https://cf.shopee.vn/file/'+item['item_basic']['image']
        except:
            baner = ''
        try:
            description = info(linkshop)
        except:
            description = ''
        try:
            likedcount = item['item_basic']['liked_count']
        except:
            likedcount = 0

        try:
            if historicalsold>1000:
                digital=0
            else:
                digital=1
        except:
            digital = 0

        try:
            if cmtcount>200:
                digitalCmt=0
            else:
                digitalCmt=1
        except:
            digitalCmt = 0

        try:
            if likedcount>1000:
                digitalLike=0
            else:
                digitalLike=1
        except:
            digitalLike = 0
        
        try:
            if ratingstars>=4.8:
                digitalStart=0
            else:
                digitalStart=1
        except:
            digitalStart = 0
        
        pro_descriptions = {
            'name': name,
            'price': price,
            'ratingstars': ratingstars,
            'priceminbeforediscount': priceminbeforediscount,
            'historicalsold': historicalsold,
            'cmtcount': cmtcount,
            'rawdiscount': rawdiscount,
            'description': description,
            'digital': digital,
            'baner': baner,
            'likedcount': likedcount,
            'url': 'https://shopee.vn/'+name+'-i.'+str(item['item_basic']['shopid'])+'.'+str(item['item_basic']['itemid']),
            'digitalCmt': digitalCmt,
            'digitalLike': digitalLike,
            'digitalStart': digitalStart,
        }
        mining(pro_descriptions['name'], pro_descriptions['price'], pro_descriptions['ratingstars'], pro_descriptions['priceminbeforediscount'], pro_descriptions['historicalsold'], pro_descriptions['cmtcount'], pro_descriptions['rawdiscount'], pro_descriptions['description'], pro_descriptions['digital'], pro_descriptions['baner'], pro_descriptions['likedcount'], pro_descriptions['url'],pro_descriptions['digitalCmt'],pro_descriptions['digitalLike'],pro_descriptions['digitalStart'])




        


getdata('giày nam')
