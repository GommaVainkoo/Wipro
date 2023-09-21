import asyncio
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import sqlite3
from selenium.webdriver.common.by import By


def create_table(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            version TEXT,
            release_date TEXT,
            end_of_life_date TEXT,
            latest TEXT
        )
    """)
    conn.commit()


def scrape_and_store_data(url, database_name, table_name):
    chrome_driver_path = "C:\\Program Files\\Google\\Chromechromedriver.exe"  # Replace with the actual path
    service = Service(chrome_driver_path)

    driver = webdriver.Chrome(service=service)
    driver.get(url)

    table = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[3]/table/tbody')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    conn = sqlite3.connect(database_name)
    create_table(conn, table_name)
    cursor = conn.cursor()

    for row in rows:
        columns = row.find_elements(By.TAG_NAME, 'td')
        if len(columns) >= 4:
            version = columns[0].text.strip()
            release_date = columns[1].text.strip()
            end_of_life_date = columns[2].text.strip()
            latest = columns[3].text.strip()

            cursor.execute(f"""
                INSERT INTO {table_name} (version, release_date, end_of_life_date, latest)
                VALUES (?, ?, ?, ?)
            """, (version, release_date, end_of_life_date, latest))

    conn.commit()
    conn.close()

    driver.quit()


async def main():
    urls = [
        ("https://endoflife.date/ruby", "ruby_versions"),
        ("https://endoflife.date/python", "python_versions"),
        ("https://endoflife.date/alpine", "alpine_versions"),
        ("https://endoflife.date/postgresql", "postgresql_versions"),
        ("https://endoflife.date/kindle", "kindle_versions"),
        ("https://endoflife.date/android", "android_versions")

    ]

    database_name = "Check.db"

    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(executor, scrape_and_store_data, url, database_name, table_name) for
                 url, table_name in urls]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())