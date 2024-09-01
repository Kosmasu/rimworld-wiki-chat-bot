import streamlit as st

from scraper import scrape_wiki_page
from settings import MAIN_PAGE_URL

# TODO:
# - Recursively index the rimworld wiki, storing it into database
# - Create a way to scrape one page, and all pages from the database that has been indexed, from step 1

if __name__ == "__main__":
    st.title("Scraping Page")


    st.markdown(
        scrape_wiki_page(MAIN_PAGE_URL)
    )