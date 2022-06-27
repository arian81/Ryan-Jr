from selenium import webdriver
from selenium.webdriver.common.by import *

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome("chromedriver", options=chrome_options)


def check_new_video():
    driver.get("https://www.youtube.com/channel/UC7gXXzu2D5rSu3NH4DJw9cw/videos")
    driver.implicitly_wait(3)

    videos = driver.find_elements(by=By.ID, value="video-title")
    for i in videos:
        if "1XC3" in i.text:
            latest_video = i.get_attribute("href")
            break

    with open("latest_video.txt", "r") as f:
        previous_video = f.read().strip("\n")
    with open("latest_video.txt", "w") as f:
        f.write(latest_video)

    return previous_video != latest_video
