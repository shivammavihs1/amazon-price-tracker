import requests  #for accessing the URL
from bs4 import BeautifulSoup
import smtplib
import time
import csv
import datetime
import os

url = "https://www.amazon.in/Redmi-Note-10S/dp/B08LRDM44F/ref=asc_df_B08LRDM44F/?tag=googleshopdes-21&linkCode=df0&hvadid=397083168716&hvpos=&hvnetw=g&hvrand=9004679662037441800&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9300940&hvtargid=pla-1360809751371&psc=1&ext_vrnc=hi"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"}

def check_phone_price():
    page = requests.get(url, headers=headers) #this will take actually all the data from outside

    bs = BeautifulSoup(page.content, "html.parser") #this will parse everything and pull out individual pieces of information

    #print(bs.prettify().encode("utf-8"))

    product_name = bs.find(id="productTitle").get_text()
    print(product_name.strip()) #I used here strip() function to remove the blank spaces between them
    price = bs.find(id="priceblock_dealprice").get_text()
    print(price.strip())
    price = price[1:7] #to get only the price value
    print(price)
    price_float = float(price.replace(",", "")) #to remove the ',' from the price value in float
    print(price_float)
    file_exists = True

    if not os.path.exists("./phones.csv"):  # for asking if there exists any phones.csv file or not
        file_exists = False


    with open("phones.csv", "a") as file:   # open a file phones.csv as append 
        writer = csv.writer(file, lineterminator="\n")  # write the details
        fields = ["Timestrap", "price(₹)"]
        if not file_exists:
            writer.writerow(fields)   

        timestamp = f"{datetime.datetime.date(datetime.datetime.now())}, {datetime.datetime.time(datetime.datetime.now())}" 
        writer.writerow([timestamp, price_float])
        print("wrote data to file") # after printing the details

    return price_float

def send_mail():   #for connecting our conncetion with gmail connection
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()  # 587 is the port number and it is the default port number for TLS and EHLO is the command send by an email server to identify itself when conncecting to another email server
    server.starttls() # start the encryption traffic connection
    server.ehlo() # again to check if the encryption is working, check connection b/w server and client

    server.login("amazonprice.noreply@gmail.com", "bxjshiyucnwcmawa") # sender email id and password(the app pasword)

    subject = "Hey, The Price fell down!!"
    body = "Check the amazon product link here -  https://www.amazon.in/Redmi-Note-10S/dp/B08LRDM44F/ref=asc_df_B08LRDM44F/?tag=googleshopdes-21&linkCode=df0&hvadid=397083168716&hvpos=&hvnetw=g&hvrand=9004679662037441800&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9300940&hvtargid=pla-1360809751371&psc=1&ext_vrnc=hi"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        "amazonprice.noreply@gmail.com",
        "amazonprice.noreply@gmail.com",
        msg
    )
    print("Email has been sent !")
    server.quit()

while True:
    price = check_phone_price()
    if(price < 16000):
        send_mail()
        break
    time.sleep(10)
