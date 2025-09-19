from bs4 import BeautifulSoup
import requests
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

practice_url= "https://appbrewery.github.io/instant_pot/"
live_url = "https://www.amazon.com.tr/Philips-HD9243-90-Airfryer-Kapasite/dp/B0CD2KVVRC/ref=sr_1_5?crid=UITOZGU6F854&dib=eyJ2IjoiMSJ9.hmWXxisfxSgLldAl8PZsWRGKlKvsPU7lqXDA80738vcXSJAcqFeXsMgr-__lGVmvSdQtmMdFL5bYNrojEw6UVHIyju-_6gDf5NfRihfgwM39JOH-cVfaRmv6yJ73UQCA0PSgCe93ZBHh4AxyU-WKiFCWRfRw_4ZpCq1je32SLoyDaHg3OiX4xw-02jKfXPjvzlb3oHFGZWo7Rs1HB-ejGNaWATXZcN46A1iJCeDkhOEmqGWHCiBDjcT1RvqfurQm6E7TzCoJtyTEdq8ONYVyEG9xKIRFIxPU_ex6JlBKblw.HDYnuWXqlpzq1ZZSt44cEENfjnqSvYdWOjUk9cmlZiM&dib_tag=se&keywords=airfryer&qid=1746347285&sprefix=airfr%2Caps%2C233&sr=8-5&th=1"
header = {"Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
          }

response = requests.get(live_url,headers=header)

soup = BeautifulSoup(response.content,"html.parser")

price = soup.find(class_="a-price-whole").getText().strip(",")
price_as_float = float(price)
print(price_as_float)

title = soup.find(id="productTitle").getText()
clean_title = " ".join(line.strip() for line in title.splitlines())


BUY_PRICE = 1500

if price_as_float < BUY_PRICE:

    message = f"{clean_title} is now below {BUY_PRICE}₺!"

    with smtplib.SMTP(host=os.getenv("SMTP_ADDRESS"),port=587) as connection:
        connection.starttls()
        connection.login(user=os.getenv("EMAIL_ADDRESS"), password=os.getenv("EMAIL_PASSWORD"))
        connection.sendmail(
            from_addr=os.getenv("EMAIL_ADDRESS"),
            to_addrs=os.getenv("EMAIL_ADDRESS"),
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{live_url}.".encode("utf-8")
        )

