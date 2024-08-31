import streamlit as st

from scraper import scrape_wiki_page
from settings import MAIN_PAGE_URL

if __name__ == "__main__":
    st.title("Page Scraping")

    st.markdown(
        scrape_wiki_page(MAIN_PAGE_URL)
    )