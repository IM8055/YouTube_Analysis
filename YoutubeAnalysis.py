from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException


chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('start-maximized')
# chrome_options.add_argument('disable-infobars')
# chrome_options.add_argument("--disable-extensions")
# driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=chrome_options, executable_path=r'C:\Users\akkav\AppData\ChromeDriver\chromedriver.exe') #  , chrome_options=chrome_options)
# driver.get(r'https://www.youtube.com/results?search_query=machine+learning')
# driver.get('https://www.youtube.com/results?search_query=deep+learning')
# driver.get('https://www.youtube.com/results?search_query=convolutional+neural+network')
# driver.get('https://www.youtube.com/results?search_query=recurrent+neural+network')
driver.get('https://www.youtube.com/results?search_query=python+machine+learning')
driver.maximize_window()

SCROLL_PAUSE_TIME = 2
driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.find_element_by_tag_name('body').send_keys(Keys.END)
    # Scroll down to bottom
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
links = []
for i in user_data:
    links.append(i.get_attribute('href'))
print('Total Links is: ', len(links))
df = pd.DataFrame(columns=['link', 'id', 'title', 'description', 'category', 'count', 'date', 'likes', 'dislikes', 'duration', 'subscribers'])
wait = WebDriverWait(driver, 15)
v_category = "ML with Python"
xpathLIKES = r"/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]/a/yt-formatted-string"
xpathDISLIKES = r"/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[2]/a/yt-formatted-string"
xpathDURATION = r"/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[29]/div[2]/div[1]/div/span[3]"
# xpathCHANNEL = '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[8]/div[3]/ytd-video-secondary-info-renderer/div/div[2]/ytd-video-owner-renderer/div[1]/ytd-channel-name/div/div/yt-formatted-string/a'
xpathSUBSCRIBERS = r"/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[8]/div[3]/ytd-video-secondary-info-renderer/div/div[2]/ytd-video-owner-renderer/div[1]/yt-formatted-string"
for count, x in enumerate(links):
    if str(x) != 'None':
        try:
            driver.get(x)
            v_link = x
            v_id = x.strip('https://www.youtube.com//watch?v=')
            v_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.title yt-formatted-string"))).text
            v_description = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#description yt-formatted-string"))).text
            v_count = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#count > yt-view-count-renderer > span.view-count.style-scope.yt-view-count-renderer"))).text
            v_date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#date > yt-formatted-string"))).text
            v_likes = wait.until(EC.presence_of_element_located((By.XPATH, xpathLIKES))).text
            v_dislikes = wait.until(EC.presence_of_element_located((By.XPATH, xpathDISLIKES))).text
            v_duration = driver.find_elements_by_xpath("//span[@class='ytp-time-duration']")[0].text
            v_subscribers = 0
            # v_subscribers = wait.until(EC.presence_of_element_located((By.XPATH, xpathSUBSCRIBERS))).text
            # element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "comment-section-header-renderer")))
            # for comment_num in driver.find_elements_by_class_name("comment-section-header-renderer"):
            #     v_subscribers = comment_num.text.replace(u'COMMENTS • ', '')
            df.loc[len(df)] = [v_link, v_id, v_title, v_description, v_category, v_count, v_date, v_likes, v_dislikes, v_duration, v_subscribers]
        except NoSuchElementException:
            print("NoSuchElementException")
        except TimeoutException:
            print("TimeoutException")
        except Exception as e:
            print(e)
        finally:
            df.to_csv(r'C:\Users\akkav\Desktop\dfYoutube.csv')
            print('DF SAVED')
    if (count % 20) == 0:
        print(count)
        print('20 Links completed')
print('COMPLETED')
driver.quit()
