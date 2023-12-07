from requests import get
from bs4 import BeautifulSoup
def extract_wwr_jobs(keyword):
    base_url ="https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term="
    response = get(f"{base_url}{keyword}")
    if response.status_code != 200:
        print("Can't request website")
    else:
        results = []
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all('section', class_='jobs')
        for job_section in jobs:
            job_posts = job_section.find_all('li')
            job_posts.pop(-1)
            for post in job_posts:
                anchors = post.find_all('a')
                anchor = anchors[1]
                link = anchor['href']
                #bs4가 dict 처럼 사용할 수 있게 해준다.
                company, kind, region = anchor.find_all('span', class_="company")
                title = anchor.find('span', class_='title')
                #find all은 list로 가져오고, find는 result로 가져온다.
                job_data = {
                    'link' :f"https://weworkremotely.com{link}",
                    'company' : company.string,
                    'region' : region.string,
                    'position' : title.string
                }
                results.append(job_data)
        return results



