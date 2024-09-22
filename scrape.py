import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service 
import time
from bs4 import BeautifulSoup

def scrape_website(website):
    print("Launching chrome browser....")
    
    chrome_driver_path = "./chromedriver"
    options = webdriver.ChromeOptions()
    
    chrome_service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=chrome_service, options=options)
    
    try:
        driver.get(website)
        print("Page loaded...")
        html = driver.page_source
        time.sleep(3)
        
        return html
    finally:
        driver.quit()

# There is a problem of captcha's as the sites are now able to detect bots.

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content,"html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    
    for script_or_style in soup (["script", "style"]):     # here we are removing excess body content like style and script
        script_or_style.extract()                           # that are not needed by us  
    cleaned_content= soup.get_text(separator="\n")
    cleaned_content= "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )            
    #this is going to effectively remove any \n that are uneccessary 
    # to remove 'empty text string' if the \n is not seperating anything , if there is no text between it and the next thing we are going to remove it
    # using stripping will remove that ||""" line.strip() for line in cleaned_content.splitlines() if line.strip()"""
    return cleaned_content

# token limit of LLM's are usually about 8000 so:-
def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range (0 , len(dom_content), max_length)
    ]
