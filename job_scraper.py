from requests import get
from bs4 import BeautifulSoup

base_url ="https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term="
search_term = "next"

response = get(f"{base_url}{search_term}")
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
    for result in results:
        print(result)
        print("/////////")
            #여기서 class가 keyword argument다. 근데 _를 쓴이유는 파이썬에서 class라는 단어가 이미 사용중이기
            #때문이다. 마치 if와 else처럼 말이다. else=0이라고 하면 말이 안되는것 처럼.


#1 keyword Arguments
# def say_hello(name,age):
#     print(f"Hello {name} you are {age} years old")

# say_hello("nico",12)
# say_hello(age=12, name="nico")


#2 파이썬에서 여러개의 변수에 함번에 저장하는 법
# list_of_numbers= [1,2,3]
# first,second,third = list_of_numbers
# print(first,second,third)
#3 String
#이걸 쓰면 HTML태그가 없어져 버린다.dddd