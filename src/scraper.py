from bs4 import BeautifulSoup, NavigableString, Tag
from markdownify import markdownify
import urllib.parse
from pydantic import BaseModel
import requests

from src.settings import MAIN_PAGE_URL


class SearchResult(BaseModel):
    title: str
    url: str
    content: str
    metadata: str


def fix_url(content: Tag) -> Tag:
    for tag in content.find_all(["a", "img"]):
        if not isinstance(tag, Tag):
            continue
        if (
            tag.name == "a"
            and "href" in tag.attrs
            and not str(tag["href"]).startswith("https://")
        ):
            tag["href"] = "https://rimworldwiki.com" + str(tag["href"])
        elif (
            tag.name == "img"
            and "src" in tag.attrs
            and not str(tag["src"]).startswith("https://")
        ):
            tag["src"] = "https://rimworldwiki.com" + str(tag["src"])
    return content


def scrape_search_page(query: str):
    params = {
        "search": query,
    }
    query_string = urllib.parse.urlencode(params)
    url = f"{MAIN_PAGE_URL}?{query_string}"

    try:
        response: requests.Response = requests.get(url)
        response.raise_for_status()  # Ensure we handle bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    content_soup: Tag | NavigableString | None = soup.find(class_="mw-search-results")

    if not isinstance(content_soup, Tag):
        raise Exception("No search results found!")

    lis: list[Tag] = content_soup.find_all("li", class_="mw-search-result")

    search_results: list[SearchResult] = []
    for li in lis:
        li = fix_url(li)
        
        # Check if title_element is of type Tag
        title_element: Tag | NavigableString | None = li.find("a")
        if not isinstance(title_element, Tag):
            continue

        # Check if content_element is of type Tag
        content_element: Tag | NavigableString | None = li.find(
            "div", class_="searchresult"
        )
        if not isinstance(content_element, Tag):
            continue

        # Check if metadata_element is of type Tag
        metadata_element: Tag | NavigableString | None = li.find(
            "div", class_="mw-search-result-data"
        )
        if not isinstance(metadata_element, Tag):
            continue

        # Append search result if all elements are valid
        search_results.append(
            SearchResult(
                title=title_element.get_text(strip=True),
                url=str(title_element["href"]),
                content=content_element.get_text(strip=True),
                metadata=metadata_element.get_text(strip=True),
            )
        )

    return search_results


def scrape_wiki_page(url: str):
    try:
        response: requests.Response = requests.get(url)
        response.raise_for_status()  # Ensure we handle bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    content_soup: Tag | NavigableString | None = soup.find(id="content")

    if not isinstance(content_soup, Tag):
        raise Exception("No content found!")

    content = fix_url(content_soup).prettify()
    content = str(markdownify(content))
    return content


if __name__ == "__main__":
    result = scrape_search_page("caravan movement speed")
    print(result)
