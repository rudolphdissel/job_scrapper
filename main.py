from requests import get
from bs4 import BeautifulSoup
from extractor.wwr import extract_wwr_jobs
from selenium import webdriver

def extract_indeed_jobs(keyword):
    browser = webdriver.Chrome()
    browser.get(f"https://kr.indeed.com/jobs?q={keyword}&l=&from=searchOnHP&vjk=89395b6ac5014113")

    results = []
    soup = BeautifulSoup(browser.page_source, "html.parser")
    job_list = soup.find("ul", class_="css-zu9cdh eu4oa1w0")
    jobs = job_list.find_all('li', recursive=False) 
    #이렇게 recursive=False처리를 해주면 바로 아래에 해당하는 애들만 찾아준다.
    for job in jobs:
        zone = job.find("div", class_="mosaic-zone")
        if zone ==None:
            anchor = job.select_one("h2 a") # 어쩌피 a가 한개라서 one을 쓰면 list로 안 받을 수 있다.
            title = anchor['aria-label']
            link = anchor['href']
            company = job.find("span", attrs={"data-testid": "company-name"})
            location = job.find("div", attrs={"data-testid": "text-location"})
            job_data = {
                'link':f"http://kr.indeed.com{link}",
                'company':company.string,
                'location':location.string,
                'position':title
            }
            results.append(job_data)
    for result in results:
        print(result)
        print("/////////////////\n///////////////")
extract_indeed_jobs("java")
