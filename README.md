# ReportsScraper
Crawler that identifies and downloads publications from ACLU website.

ABOUT:

ReportsScraper crawls through the pages publications on the ACLU website to identify and download all reports. After completing the downloads, the script creates a manifest (CSV file) containing key metadata: 

<b>Title:</b> The title of the report.
<b>Date:</b> The date of publication.
<b>pdf_Name:</b> The file name of the pdf downloaded.
<b>Description:</b> The text accompanying the pdf on the webpage, if present.
<b>Related_Issues:</b> Topic links included at the bottom of the page that serve as subject headings.

----------------------------------------------------

DEPENDENCIES:

chromedriver_win32 and wkhtmltopdf must be in the same director as reports_scraper.py.

chromedriver_win32 documentation = https://chromedriver.chromium.org/home

----------------------------------------------------

USAGE NOTES:

On running, the script will prompt for start page and end page. Remember, if you select pages 1-21, the program will download all documents on page 20 and stop once it reaches page 21, thus nothing on page 21 will download.

----------------------------------------------------

ERROR LOG:

ReportsScraper looks for reports as pdfs within an iframe on the ACLU website. If an iframe is not present, or download is not possible, the title and URL of this report is added to an error log "for_manual_download.csv" that is printed at the end of running the scrip.
