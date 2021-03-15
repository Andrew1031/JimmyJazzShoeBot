from requests import Session
from bs4 import BeautifulSoup as bs
import pickle

#logs in and adds shoe to cart in the same session, so that cookies carry over from page to page
with Session() as s:
    #logs in using python requests
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/73.0.3683.86 Safari/537.36'}
    data2 = s.get("https://www.jimmyjazz.com/account/login", headers=headers)
    soup2 = bs(data2.content, 'html.parser')
    token1 = soup2.find("input", {"name":"form_type"})["value"] # scrape dynamic value
    token2 = soup2.find("input", {"name":"utf8"})["value"]  # scrape dynamic value
    email = input("Enter email: ")
    password = input("Enter password: ")
    login_data = {"customer[email]": email, "customer[password]": password, "form_type": token1, "utf8":token2}
    s.post("https://www.jimmyjazz.com/account/login", login_data)

    #adds desired shoe and size to cart
    shoe_link = input("Enter shoe id: ")
    shoe_size = input("Enter shoe size: ")
    shoe_data = {"Size": shoe_size, "id": shoe_link, "form_type": "product", "utf8": token2}
    s.post("https://www.jimmyjazz.com/cart/add.js",shoe_data)

    #collects the cookies from the cart page
    home_page = s.get("https://www.jimmyjazz.com/cart")
    session_cookies = home_page.cookies
    cookies_dictionary = session_cookies.get_dict()

    #writes the cookies into the google chrome Cookies file so the user can use the Session's cart to check out
    path = r'C:\Users\15102\AppData\Local\Google\Chrome\User Data\Profile 1\Cookies'
    with open(path, "wb") as f:
        pickle.dump(session_cookies, f)