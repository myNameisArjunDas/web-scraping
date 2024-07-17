from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize the WebDriver
s = Service("D:/web scraping/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=s)

# Data lists
R_NO = []
GSTIN_NO = []
PAN_NO = []
NAME = []
PERMANENT_ADDRESS = []

try:
    # Open the desired webpage
    driver.get('https://hprera.nic.in/PublicDashboard')
    time.sleep(5)

    for i in range(1, 7):
        try:
            # Wait for the project element and click
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f'//*[@id="reg-Projects"]/div/div/div[{i}]/div/div/a'))
            )
            element.click()

            # Wait for the details to load
            time.sleep(5)

            # Extract required details
            try:
                time.sleep(2)
                r_no = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="modal-data-display-tab_project_main-content"]/div/div[1]/div/span'))
                ).text
                R_NO.append(r_no.strip())
            except:
                R_NO.append(None)

            try:
                time.sleep(2)
                pan_id = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="project-menu-html"]/div[2]/div[1]/div/table/tbody/tr[7]/td[2]/span'))
                ).text
                PAN_NO.append(pan_id.strip())
            except:
                PAN_NO.append(None)

            try:
                time.sleep(2)
                name = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="project-menu-html"]/div[2]/div[1]/div/table/tbody/tr[1]/td[2]'))
                ).text
                NAME.append(name.strip())
            except:
                NAME.append(None)

            try:
                time.sleep(2)
                gstin_no = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="project-menu-html"]/div[2]/div[1]/div/table/tbody/tr[8]/td[2]/span'))
                ).text
                GSTIN_NO.append(gstin_no.strip())
            except:
                GSTIN_NO.append(None)

            try:
                time.sleep(2)
                per_add = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="project-menu-html"]/div[2]/div[1]/div/table/tbody/tr[14]/td[2]/span'))
                ).text
                PERMANENT_ADDRESS.append(per_add.strip())
            except:
                PERMANENT_ADDRESS.append(None)

            # Wait before closing the tab
            time.sleep(5)

        except Exception as detail_error:
            print(f"Error while extracting data for index {i}: {detail_error}")
            R_NO.append(None)
            PAN_NO.append(None)
            NAME.append(None)
            GSTIN_NO.append(None)
            PERMANENT_ADDRESS.append(None)

        finally:
            # Close the details tab
            close_tab = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="modal-data-display-tab_project_main"]/div/div/div[3]/button'))
            )
            close_tab.click()
            time.sleep(2)

except Exception as e:
    print(f"An error occurred: {e}")

# Print lengths of collected data
print(f"Length of R_NO: {len(R_NO)}")
print(f"Length of GSTIN_NO: {len(GSTIN_NO)}")
print(f"Length of PAN_NO: {len(PAN_NO)}")
print(f"Length of NAME: {len(NAME)}")
print(f"Length of PERMANENT_ADDRESS: {len(PERMANENT_ADDRESS)}")

# Create a DataFrame
df = pd.DataFrame({
    "R_NO": R_NO,
    "NAME": NAME,
    "GSTIN_NO": GSTIN_NO,
    "PAN_NO": PAN_NO,
    "PERMANENT_ADDRESS": PERMANENT_ADDRESS
})

print(df)
df.to_csv("HPRERA.csv", index=False)

input("Press Enter to close...")
driver.quit()
