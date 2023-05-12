import re
from contextlib import closing
from mechanize import Request, urlopen

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

from lxml import html

from qt.core import QUrl

from calibre import browser, url_slash_cleaner
from calibre.gui2 import open_url
from calibre.gui2.store import StorePlugin
from calibre.gui2.store.basic_config import BasicStoreConfig
from calibre.gui2.store.search_result import SearchResult
from calibre.gui2.store.web_store_dialog import WebStoreDialog


CURRENT_ALIAS_DOMAINS = (
    "https://libgen.is/fiction",
    "https://libgen.rs/fiction",
    "https://libgen.st/fiction",
)


class LibGenFictionStorePlugin(BasicStoreConfig, StorePlugin):
    def get_download_url(self, url, timeout=60):
        br = browser()

        with closing(br.open(url, timeout=timeout)) as f:
            raw = f.read()
            doc = html.fromstring(raw)
            download_url = doc.xpath('//*[@id="download"]/h2/a')[0].get("href")

            return download_url

    def get_book_page_info(self, current_domain, url, timeout=60):
        br = browser()
        print("bookinfourl: "+ url)
        with closing(br.open(url, timeout=timeout)) as f:
            raw = f.read()
            doc = html.fromstring(raw)
            cover_url = doc.xpath("/html/body/table/tr[2]/td[1]/a/img")[0].get("src")
            cover_url = "%s/%s" % (current_domain, cover_url)

            return cover_url

    def get_current_domain(self):
        for domain in CURRENT_ALIAS_DOMAINS:
            req = Request(url=domain, method="GET")
            res = urlopen(req)
            if res.code == 200:
                return domain

        return None

    def open(self, parent=None, detail_item=None, external=False):
        if external or self.config.get("open_external", False):
            open_url(
                QUrl(
                    url_slash_cleaner(
                        detail_item["book_page_url"]
                        if detail_item
                        else self.get_current_domain()
                    )
                )
            )
        else:
            d = WebStoreDialog(
                self.gui,
                self.get_current_domain(),
                parent,
                detail_item["book_page_url"],
            )
            d.setWindowTitle(self.name)
            d.set_tags(self.config.get("tags", ""))
            d.exec()

    def search(self, query, max_results=10, timeout=60):
        current_domain = self.get_current_domain()
        if current_domain is None:
            return
        url = "%s/?q=%s" % (current_domain, quote_plus(query))

        br = browser()

        counter = max_results
        with closing(br.open(url, timeout=timeout)) as f:
            raw = f.read()
            doc = html.fromstring(raw)

            table = doc.xpath("/html/body/table")[0]

            # get body of table
            tbody = table.xpath("tbody")[0]

            for row in tbody:
                if counter <= 0:
                    break

                title = row.xpath("td[3]")[0].xpath("p/a")[0].text
                print(title)
                if not title:
                    continue
                author = row.xpath("td[1]")[0].xpath("ul/li/a")[0].text
                print(author)

                formatsize = row.xpath("td[5]")[0].text
                format = "%s" % (formatsize[0]) if formatsize is not None else ""
                size = "%s" % (formatsize[1]) if formatsize is not None else ""
                language = row.xpath("td[4]")[0].text
                print(language)
                language = "%s" % (language) if language is not None else ""
                price = "%s%s" % (
                    size,
                    language,
                )  # use price column to display more info

                download_page_url = row.xpath("td[6]")[0].xpath("ul/li/a")[0].get("href")
                print(download_page_url)
                download_url = self.get_download_url(download_page_url)
                book_page_url = row.xpath("td[3]/p/a")[0].get("href")
                print("book_page_url: " + book_page_url)
                detail_item = {
                    "current_domain": current_domain,
                    "book_page_url": "%s/%s" % (current_domain, book_page_url),
                }

                counter -= 1

                s = SearchResult()
                s.title = title
                s.author = author
                s.price = price
                s.detail_item = detail_item
                s.downloads = {str(format).upper(): download_url}
                s.drm = SearchResult.DRM_UNLOCKED
                s.format = format

                yield s

    def get_details(self, search_result, timeout=60):
        cover_url = self.get_book_page_info(
            search_result.detail_item["current_domain"],
            search_result.detail_item["book_page_url"],
        )

        if cover_url is None:
            return False

        search_result.cover_url = cover_url

        return True
