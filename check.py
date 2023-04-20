import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_iframes_and_provider_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return set(), []

    soup = BeautifulSoup(response.text, "html.parser")
    iframes = {iframe["src"] for iframe in soup.find_all("iframe") if "src" in iframe.attrs}

    provided_by_texts = []
    for text in soup.stripped_strings:
        if text.startswith("Provided by "):
            provided_by_texts.append(text)

    return iframes, provided_by_texts

def main():
    with open("websites.txt", "r") as f:
        websites = [line.strip() for line in f.readlines()]

    with open("output.txt", "w") as f:
        for url in websites:
            print(f"Scraping website: {url}")
            iframes, provider_texts = get_iframes_and_provider_text(url)

            f.write(f"Website: {url}\n")

            if iframes:
                f.write("Found iframes:\n")
                for iframe_src in iframes:
                    f.write(f" - {iframe_src}\n")
            else:
                f.write("No iframes found.\n")

            if provider_texts:
                f.write("Found 'Provided by' texts:\n")
                for text in provider_texts:
                    f.write(f" - {text}\n")
            else:
                f.write("No 'Provided by' texts found.\n")

            f.write("\n")

if __name__ == "__main__":
    main()
