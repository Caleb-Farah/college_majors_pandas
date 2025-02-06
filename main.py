import pandas as pd
import random
import time
from bs4 import BeautifulSoup
import requests

# Global Variables
URL = "https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors"
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0"
]

main_table = None


# Function to fetch the webpage
def fetch_page(url, max_attempts=5):
    """Fetches the webpage with user-agent rotation and retries."""
    global main_table
    for attempt in range(max_attempts):
        headers = {"User-Agent": random.choice(user_agents)}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
            soup = BeautifulSoup(response.text, "html.parser")
            main_table = soup.find("table", class_="data-table")  # Store table globally

            if main_table:
                return True
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(5)
    return False


# Main Execution
if fetch_page(URL):
    pay_headings = [th.text.strip() for th in main_table.select("thead tr th span") if th.text.strip()]
    if pay_headings:
        # print("Extracted Headings:", pay_headings)
        pay_headings.insert(0, "Major")
        pay_headings.pop(3)
        majors_data = main_table.find_all(name="td", class_="csr-col--school-name")
        majors = [td.find("span", class_="data-table__value").text for td in majors_data if td.find("span", class_="data-table__value")]
        row_data = main_table.find_all(name="tr", class_="data-table__row")
        early_cp = []
        mid_cp = []
        # print(row_data)
        for tr in row_data:
            cp = tr.find_all("td", class_="csr-col--right")
            early_cp.append(cp[0].find("span", class_="data-table__value").text)
            mid_cp.append(cp[1].find("span", class_="data-table__value").text)
        # for item in range(0, len(majors)):
        #     pay_headings
        data = {
            "Major": [],
            "Early": [],
            "Mid": [],
        }
        for item in range(0, len(majors)):
            data["Major"].append(majors[item])
            data["Early"].append(early_cp[item])
            data["Mid"].append(mid_cp[item])
        df = pd.DataFrame(data, columns=pay_headings)
    else:
        print("Failed to extract table headings.")
else:
    print("Failed to fetch page after multiple attempts.")


print(df)
