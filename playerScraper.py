from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# @param player First Name Last Name, ex: James Harden
# @return the new URL
def createURL(player):
    BASE_URL = "https://www.basketball-reference.com/players/"
    names = player.split(' ')
    firstName = names[0].lower()
    lastName = names[1].lower()
    BASE_URL += lastName[0] + "/" + lastName[:5] + firstName[:2] + "01.html"
    return BASE_URL

def openURL(url):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)
    df = pd.read_html(browser.page_source)[3]
    for i in range(df.shape[0], 1, -1):
        if not ("-" in str(df['Season'][i-1])):
            df.drop(i-1, inplace=True)
    print(df)
    return df