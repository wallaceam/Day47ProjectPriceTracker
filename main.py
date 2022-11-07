import requests
from bs4 import BeautifulSoup
from smtplib import SMTP

URL = "https://www.amazon.com/Instant-Pot-Plus-Programmable-Sterilizer/dp/B075CWJ3T8/ref=dp_prsubs_3?pd_rd_w=KrlLc" \
      "&content-id=amzn1.sym.ec3cee7c-6bd8-496a-8166-4fdb6d51cad1&pf_rd_p=ec3cee7c-6bd8-496a-8166-4fdb6d51cad1" \
      "&pf_rd_r=T306AR59H27SG9NX5HHN&pd_rd_wg=Jbdpl&pd_rd_r=63b14aa2-3d5e-4eaa-bcd0-5bfdee025e37&pd_rd_i=B075CWJ3T8" \
      "&th=1 "

EMAIL = "example@gmail.com"
PW = "password"

response = requests.get(URL, headers={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/107.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,sv;q=0.8"})
site_html = response.text

soup = BeautifulSoup(site_html, "html.parser")

raw_price = soup.find(name="span", class_="a-offscreen").getText()

price_float = float(raw_price.strip("$"))

product_name = soup.find(name="span", id="productTitle").getText()
tidy_product_name = (product_name.split(",")[0]).strip("        ")

if price_float <= 100:
    with SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(EMAIL, PW)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg=f"Subject: Low price alert!\n\nThe price of {tidy_product_name} is now ${price_float}.\n\nOrder it at: {URL} "
        )
