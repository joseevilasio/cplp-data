from selenium import webdriver  
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep

options = Options()
options.add_argument("window-size=400,800")


browser = webdriver.Firefox()

browser.get("https://diariodarepublica.pt/dr/home")

sleep(3)

input_place = browser.find_element(By.TAG_NAME, "input")
input_place.send_keys("Concede o estatuto de igualdade de direitos e deveres a vários cidadãos brasileiros")

buttom_search = browser.find_element(By.ID, "b2-b2-myButton2")
buttom_search.click()

sleep(1)


