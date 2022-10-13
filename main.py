from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Player import Player
import credentials as creds
import time
import csv


FUT_WEBAPP = 'https://www.ea.com/fifa/ultimate-team/web-app/'
DRIVER_PATH = "/Users/manuelrodriguezurda/Documents/Projects/Fut-webscraper/chromedriver"

def set_options(options):
  options.add_argument('--start-maximized')
  options.add_argument('--disable-extensions')
  options.add_argument('--user-data-dir=/Users/manuelrodriguezurda/Library/Application Support/Google/Chrome/Default')
  return options

def login(driver:webdriver):
  WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-standard.call-to-action")))\
      .click()
  try:
    WebDriverWait(driver, 10)\
      .until(EC.element_to_be_clickable((By.ID, "email")))\
        .send_keys(creds.EMAIL)
    WebDriverWait(driver, 3)\
      .until(EC.element_to_be_clickable((By.ID, "password")))\
        .send_keys(creds.PASSWORD)

    WebDriverWait(driver, 3)\
      .until(EC.element_to_be_clickable((By.CLASS_NAME, "otkbtn.otkbtn-primary")))\
        .click()
  except:
    # will run if the app logs in without asking for credentials
    pass

def goto_players(driver:webdriver):
  WebDriverWait(driver, 30)\
    .until(EC.element_to_be_clickable((By.CLASS_NAME, "ut-tab-bar-item.icon-club")))\
      .click()

  WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CLASS_NAME, "tile.col-2-3-md.players-tile")))\
      .click()

def get_players_info(driver:webdriver, writer):
  html_players = driver.find_elements(By.CLASS_NAME, "listFUTItem")
  
  for player in html_players:
      
    player.click()

    time.sleep(0.1)
    # Get player info
    WebDriverWait(driver, 10)\
      .until(EC.element_to_be_clickable((By.CLASS_NAME, "more"))).click()
    
    WebDriverWait(driver, 10)\
      .until(EC.element_to_be_clickable((By.CLASS_NAME, "pseudo-table")))

    player_row = [None for x in Player.HEADERS]

    html_player_table = driver.find_element(By.CLASS_NAME, "pseudo-table")
    html_player_info = html_player_table.find_elements(By.TAG_NAME, "li")
    for item in html_player_info:
      column_arr = item.text.split('\n')
      if column_arr[0] in Player.HEADERS:
        player_row[Player.HEADERS[column_arr[0]]] = column_arr[1]
    
    #Get player rating
    WebDriverWait(driver, 5)\
      .until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Attributes']"))).click()

    WebDriverWait(driver, 5)\
      .until(EC.element_to_be_clickable((By.CLASS_NAME, "pseudo-table")))

    html_rating_table = driver.find_element(By.CLASS_NAME, "pseudo-table")
    html_rating_info = html_rating_table.find_elements(By.TAG_NAME, "li")
    rating = html_rating_info[0].find_element(By.CLASS_NAME, "value")
    player_row[0] = rating.text

    writer.writerow(player_row)
    print(player_row)
    time.sleep(0.1)

def update_players_db(driver:webdriver, writer):
  
  last_page = False
  counter = 0 # counter implemented bc of wierd behaviour if click too many times on players bio 
  while(last_page == False):
    try:
      WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.CLASS_NAME, "listFUTItem")))

      get_players_info(driver, writer)

      WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.CLASS_NAME, "flat.pagination.next")))\
          .click()

      # add random behaviour 
      if counter == 1:
        WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.CLASS_NAME, "flat.pagination.prev")))\
          .click()

        WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.CLASS_NAME, "flat.pagination.next")))\
          .click()

        counter = 0 
        
      counter = counter + 1
    except Exception as e:
      print(e)
      last_page = True
      print("Exception or last page")

def main():

  options = webdriver.ChromeOptions()
  set_options(options)

  driver = webdriver.Chrome(DRIVER_PATH, options=options)
  driver.set_window_position(2000, 0)
  driver.maximize_window()
  driver.get(FUT_WEBAPP)

  #initialize csv
  player_db = open('playerDB.csv', 'w')
  writer = csv.writer(player_db)
  writer.writerow(Player.HEADERS.keys())
        #player_db.close()

  try:
    
    driver.get(FUT_WEBAPP)
    try:
      login(driver)
    except:
      pass

    goto_players(driver)
    update_players_db(driver, writer)

  except Exception as e:
    print(e)
    # driver.quit()
    pass

  finally:
    player_db.close()

if __name__ == "__main__":
  main()
  time.sleep(100)