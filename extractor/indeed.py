from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
def get_page_count(keyword):
    browser = webdriver.Chrome()
    browser.get(f"https://kr.indeed.com/jobs?q={keyword}&l=&from=searchOnHP&vjk=89395b6ac5014113")
    soup = BeautifulSoup(browser.page_source,"html.parser")
    pagination = soup.find("nav", attrs={"aria-label": "pagination"})
    if pagination == None:
        return 1
    pages = pagination.find_all("li")
    count = len(pages)
    if count >=5:
        return 5
    else:
        return count
def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    results = []
    for page in range(pages):
        browser = webdriver.Chrome()
        final_url=f"https://kr.indeed.com/jobs?q={keyword}&start={page*10}"
        print("Requesting", final_url)
        browser.get(final_url)
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
                    'company':company.string.replace(","," "),
                    'location':location.string.replace(","," "),
                    'position':title.replace(","," ")
                }
                results.append(job_data)
    return results