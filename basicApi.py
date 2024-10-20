import os
import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


# initialize
PYPPETEER_CHROMIUM_REVISION = '1263111'

os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

url = "https://api-inference.huggingface.co/models/dbmdz/bert-large-cased-finetuned-conll03-english"
headers = {"Authorization": "Bearer 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"}

# Function to scrape Brave Search results
def brave_search_scrape(query):
    # Format the search query for the URL
    url = f"https://search.brave.com/search?q={query}"

    # Send an HTTP request to Brave Search
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find search result links and titles
        search_results = []
        for result in soup.find_all('a', class_="h svelte-1i8038p l1"):  # Adjust class if necessary
            link = result.get('href')  # Get the link (href attribute)
            title = result.text  # Get the title (text inside the <a> tag)
            search_results.append({'title': title, 'link': link})  # Store in list

        # Return the list of search results
        return search_results
    else:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return []

# Example usage
query = "top electronics retailers in India"
results = brave_search_scrape(query)

# breaks it into chunks
def chunk_text(text, max_tokens=512):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        token_length = len(word.split())

        if current_length + token_length > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = token_length
        else:
            current_chunk.append(word)
            current_length += token_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def google_search(company):
    url = f"https://search.brave.com/search?q={company}"

    # Send an HTTP request to Brave Search
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'lxml')

        # Find search result links and titles
        search_results = []
        for result in soup.find_all('a', class_="h svelte-1i8038p l1"):  # Adjust class if necessary
            link = result.get('href')  # Get the link (href attribute)
            title = result.text  # Get the title (text inside the <a> tag)
            search_results.append({'title': title, 'link': link})  # Store in list

        # Return the list of search results
        return search_results
    else:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return []


# Function to visit a result and check for electronics retail information
def visit_result(url, company):
    page.goto(url)
    content1 = page.inner_text('body').lower()
    if ("electronic" in content1 or "appliance" in content1) and company.lower() in content1 and any([i in content1 for i in ["retail", "sale"]]):
        return True
    return False


# Main function to check if companies are electronics retailers
def check_companies():
    retailer_companies = []

    for company in unique_companies_list:
        print("trying:", company)
        search_html = google_search(company)
        i = 0
        if search_html:
            while True:
                try:
                    if 'wikipedia' not in search_html[i]['link']:
                        if visit_result(search_html[i]['link'], company):
                            retailer_companies.append(company)
                            print(f"{company} is an electronics retailer.")
                    break
                except Exception:
                    i += 1
                    continue
    return retailer_companies

total_retailers = []
p = sync_playwright().start()
browser = p.chromium.launch(headless=True)
page = browser.new_page()
for i in results:
    print(i['link'])
    page.goto(i['link'])
    content = page.inner_text('body')

    text = content
    companies = []
    chunks = chunk_text(text)
    for chunk in chunks:
        response = requests.post(url, headers=headers, json={"inputs": chunk})

        if response.status_code == 200:

            entities = response.json()
            for entity in entities:
                if entity['entity_group'] == 'LABEL_6' or entity['entity_group'] == 'ORG':
                    companies.append(entity['word'])
        else:
            print(f"Request failed with status code: {response.status_code}, {response.json()}")

    normalized_companies = [company.lower().strip() for company in companies]
    unique_companies = set(normalized_companies)
    unique_companies_list = sorted(unique_companies)
    unique_companies_list = [i for i in unique_companies_list if i[0].isalnum() and len(i) > 1 and "electronics" != i]
    for i in range(len(unique_companies_list)):
        for j in ["private", "limited", "pvt", "ltd", "solutions", "solns", "corporations"]:
            if j in unique_companies_list[i]:
                unique_companies_list[i] = unique_companies_list[i].split(j)[0].strip()
    unique_companies = set(unique_companies_list)
    unique_companies_list = sorted(unique_companies)
    print(len(unique_companies_list))

    # Run the scraper
    electronics_retailers = check_companies()
    print("Electronics Retailers in India:")
    total_retailers += electronics_retailers
    print(total_retailers)

browser.close()
