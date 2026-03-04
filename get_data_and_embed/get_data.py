import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urljoin

LIST_PAGES=[
    # 此处输入需要爬取的网页
]
BASE_URL = "" # 输入根url
HEADERS = {
    "User-Agent": "Mozilla/5.0 (educational crawler)"
}

session = requests.Session()
session.headers.update(HEADERS)

def get_list_page(url):
    """
    此函数输入根url用来查找你需要的LIST_PAGE
    """
    resp = session.get(url, timeout=8)
    resp.encoding = "utf-8"
    list_page_html=resp.text
    soup = BeautifulSoup(list_page_html, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "info" not in href and href.endswith(".htm"):
            full_url = urljoin(BASE_URL, href)
            links.add(full_url)
    for link in links:
        print('"'+link+'",')

def get_html(url):
    resp = session.get(url, timeout=8)
    resp.encoding = "utf-8"
    return resp.text

def extract_article_links(list_page_html):
    soup = BeautifulSoup(list_page_html, "html.parser")
    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]

        # 只要正文页
        if "info" in href and href.endswith(".htm"):
            full_url = urljoin(BASE_URL, href)
            links.add(full_url)

    return list(links)
def extract_article_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    
    content_div = soup.find("div", class_="v_news_content")
    if not content_div:
        return None
    
    return {
        "url": url,
        "title": soup.title.get_text(strip=True),
        "content": content_div.get_text(separator="\n", strip=True)
    }
def main():
    article_links = set()

    # 只爬指定列表页
    for page in LIST_PAGES:
        print(f"解析列表页：{page}")
        html = get_html(page)
        links = extract_article_links(html)
        article_links.update(links)

    print(f"共发现正文页：{len(article_links)}")

    results = []
    for i, url in enumerate(article_links):
        print(f"[{i+1}/{len(article_links)}] 抓取正文：{url}")
        data = extract_article_content(url)
        if data:
            results.append(data)
        time.sleep(1)  # 更快也没问题

    with open("szu_admission_articles.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("爬取完成")

if __name__ == "__main__":
    main()