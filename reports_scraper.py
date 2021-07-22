from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
import time


def LogManualDownload():
    current_url = driver.current_url
    for_manual_download["Title"].append(link)
    for_manual_download["URL"].append(current_url)


start_pg = input("Enter the start page: ")
end_pg = input("Enter the end page: ")


driver = webdriver.Chrome(
    r".\chromedriver_win32\chromedriver.exe")


reports_manifest = {"Title": [], "Date": [],
                    "pdf_Name": [], "Description": [], "Related_Issues": []}

for_manual_download = {"Title": [], "URL": []}


for x in range(int(start_pg), int(end_pg)):
    url = f'https://www.aclu.org/search/a?page={str(x)}&f%5B0%5D=type%3Aasset&f%5B1%5D=field_asset_type%3Areport'
    driver.get(url)
    driver.maximize_window()
    time.sleep(2)

    titles = driver.find_elements_by_tag_name('h3.title')
    dates = driver.find_elements_by_tag_name('span.date')

    report_links = []

    for title in titles:
        report_links.append(title.text)
        reports_manifest["Title"].append(title.text)

    for date in dates:
        reports_manifest["Date"].append(date.text.title())

    for link in report_links:
        print(f"Page: {str(x)}")
        print(f"Now working on: {link}")
        time.sleep(2)

        driver.find_element_by_link_text(link).click()
        time.sleep(3)

        try:
            pdf_name = driver.find_element_by_class_name(
                'download-link').get_attribute('href')
            reports_manifest["pdf_Name"].append(pdf_name[56:])
        except NoSuchElementException:
            reports_manifest["pdf_Name"].append("NO PDF FOUND")

        try:
            description = driver.find_element_by_xpath(
                '/html/body/div[3]/div[2]/div/div[2]/div[2]/div/div/div[2]/p[1]')
            reports_manifest["Description"].append(description.text)
        except NoSuchElementException:
            reports_manifest["Description"].append(" ")

        try:
            related_issues = driver.find_element_by_class_name('item-list')
            reports_manifest["Related_Issues"].append(related_issues.text)
        except NoSuchElementException:
            reports_manifest["Related_Issues"].append(" ")

    # There is at least 1 without an iFrame. Throw up exception and place in PDF name "NO PDF FOUND"
        try:
            iframe = driver.find_element_by_xpath('//*[@id="iFrameResizer0"]')
            driver.switch_to.frame(iframe)
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="download"]').click()
        except NoSuchElementException:
            LogManualDownload()
        except ElementNotInteractableException:
            LogManualDownload()

        driver.switch_to.default_content()

        driver.back()

driver.quit()


# Print to CSV manifest and list of reports requiring manual download
output_folder = r"C:\Users\erics\Downloads"

df = pd.DataFrame.from_dict(reports_manifest)
csv_path = os.path.join(
    output_folder, f"reports_manifest_{start_pg}-{end_pg}.csv")
df.to_csv(csv_path, index=False, encoding='utf-8-sig')

df_for_manual_dl = pd.DataFrame.from_dict(for_manual_download)
csv_path_manual_dl = os.path.join(
    output_folder, f"for_manual_download_{start_pg}-{end_pg}.csv")
df_for_manual_dl.to_csv(csv_path_manual_dl, index=False, encoding='utf-8-sig')
