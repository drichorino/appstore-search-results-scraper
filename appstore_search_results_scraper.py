import requests
from bs4 import BeautifulSoup

# Define headers to mimic a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fetch_apple_search_results(search_term, country="us"):
    """
    Scrapes Apple’s search results page for a given term and country.
    Ensures the results match what is displayed in the App Store.
    
    :param search_term: The search query
    :param country: Country code (e.g., 'us', 'gb')
    :return: List of search results
    """
    # Construct search URL
    search_url = f"https://www.apple.com/{country}/search/{search_term}?src=globalnav"
    
    # Send request
    response = requests.get(search_url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return []

    # Parse HTML response
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate the main search results container
    tab_container = soup.select_one(".rf-serp-search-tabcontainer")
    if not tab_container:
        print("No search results found.")
        return []

    # Extract search results
    search_results = []
    for item in tab_container.select(".rf-serp-curated-product"):
        try:
            title_element = item.select_one("h2.rf-serp-productname")
            title = title_element.text.strip() if title_element else "No title"
            
            description_element = item.select_one("p.rf-serp-productdescription")
            description = description_element.text.strip() if description_element else "No description"
            
            link_element = item.select_one("li.rf-serp-productoption-link a")
            link = link_element["href"] if link_element else "No link"
            
            search_results.append({
                "title": title,
                "description": description,
                "link": link
            })
        except AttributeError:
            continue  # Skip if missing data
    
    return search_results

if __name__ == "__main__":
    search_query = input("Enter search term: ")
    country_code = input("Enter country code (default: 'us'): ") or "us"

    results = fetch_apple_search_results(search_query, country_code)

    for index, result in enumerate(results, start=1):
        print(f"{index}. {result['title']}")
        print(f"   Description: {result['description']}")
        print(f"   Link: {result['link']}")
        print("-" * 50)