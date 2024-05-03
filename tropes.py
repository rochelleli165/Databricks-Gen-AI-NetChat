from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException

# BEFORE RUNNING:
# INSTALL CHROMEDRIVER FOR SELENIUM
# CHANGE chrom_driver_path to correct path

import csv
import string

chrome_driver_path = "../Downloads/mac/Google Chrome for Testing.app"
filename = 'tropes.csv'

types = []
titles = []
text = []

class ArticleException(Exception):
    pass

class InexactException(Exception):
    pass

with open('netflix_titles.csv', newline='') as csvfile:
    # Create a CSV reader object
    csv_reader = csv.reader(csvfile)
    # Skip the header row if it exists
    next(csv_reader, None)
    # Iterate over each row in the CSV
    for row in csv_reader:
        # Extract movieType and title from each row and append to respective arrays
        types.append(row[1])
        titles.append(row[2])


def remove_spaces_and_punctuation(input_string):
    # Capitalize
    input_string = input_string.title()
    # Remove spaces
    input_string = input_string.replace(" ", "")
    
    # Remove punctuation
    input_string = input_string.translate(str.maketrans('', '', string.punctuation))
    
    return input_string

def getText(title, type):

    service = Service(executable_path=chrome_driver_path)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome() 

    # Create a new instance of the Chrome driver

    url = "https://tvtropes.org/pmwiki/pmwiki.php/" + type + "/" + title
    # Open the URL in the browser
    driver.get(url)

    try:
        # See if article exists
        revealed_text = driver.find_element(By.ID, "main-article").text
        if ("Inexact title" in revealed_text):
            raise InexactException
        if ("We don't have an article" in revealed_text):
            raise ArticleException
        
        # See if folder exists
        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "folderlabel"))
        )
        # Click the button to reveal more text
        button.click()

        # Extract the text that was revealed
        revealed_text = driver.find_element(By.CLASS_NAME, "folder").text
        return revealed_text

    except TimeoutException:
        revealed_text = driver.find_element(By.ID, "main-article").text
        return revealed_text
    
    except ArticleException:
        return ''
    
    except InexactException:
        t = ''
        if (type == "Film"):
            t = getText(title, "Anime")
        elif (type == "Series"):
            t = getText(title, "Anime")
        
        elif (type == "Anime"):
            t = getText(title,"WesternAnimation")
        else:
            return t
        return t
    
    except Exception:
        return ''
    finally:
        # Close the browser window
        driver.quit()

#title = remove_spaces_and_punctuation("Naruto Shippuden: The Movie")
#print(getText(title, "Series"))
def formTable():
    for i in range(0, len(titles)):
        print(i)
        title = remove_spaces_and_punctuation(titles[i])
        type = ''
        if (types[i] == "Movie"):
            type = "Film"

        if (types[i] == "TV Show"):
            type = "Series"
        
        t = getText(title, type)
        if (t != ""):
            text.append("Title: " + titles[i] + t)
        
        if (i % 100 == 0):
            write()

def init(filename):
    with open(filename, mode='w', newline='') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Text"])
    
    print(f"CSV file '{filename}' created successfully.")

def write(): 
    # Open the CSV file in write mode
    with open(filename, mode='a', newline='') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)
        # Write the data to the CSV file
        for string in text:
            csv_writer.writerow([string])
        text.clear()

    print(f"CSV file '{filename}' created successfully.")

init(filename)
formTable()
