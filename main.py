from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser


def parse_item(html_page):
    results = []
    html = HTMLParser(html_page)
    data = html.css('tbody')
    for item in data:
        product = {
            "title": item.css_first("td.sorting_1").text(),
        }
        results.append(product)
    return results


def main():
    url = "https://data-sscasn.bkn.go.id/spf?jenisPengadaan=3&instansi=&tkPendidikan=40&tkPendidikan=&pendidikan=5100917"
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        next_page = page.locator(".page-link")
        while True:
            print(parse_item(page.content()))
            if next_page.is_disabled():
                break
            page.click("li.paginate_button page-item next")
            page.waitt_for_load_state("networkidle")


if __name__ == "__main__":
    main()
