import requests
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET


class EuropePMCScraper:
    def __init__(self, query="chronic pancreatitis", days_back=30):
        self.query = query
        self.days_back = days_back
        self.base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

    def get_recent_articles(self, max_results=100):
        date_threshold = datetime.now() - timedelta(days=self.days_back)
        query = f"TITLE_ABS:\"{self.query}\" sort_date:y"

        params = {
            "query": query,
            "format": "json",
            "pageSize": max_results
        }

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()

        results = data.get("resultList", {}).get("result", [])
        recent_articles = []

        for article in results:
            pub_date_str = article.get("firstPublicationDate") or article.get("pubYear")
            if not pub_date_str:
                continue
            try:
                pub_date = datetime.strptime(pub_date_str, "%Y-%m-%d")
            except ValueError:
                try:
                    pub_date = datetime.strptime(pub_date_str, "%Y")
                except ValueError:
                    continue

            if pub_date >= date_threshold:
                full_text = self.get_full_text(article.get("pmcid")) if article.get("pmcid") else None
                recent_articles.append({
                    "title": article.get("title"),
                    "authors": article.get("authorString"),
                    "journal": article.get("journalTitle"),
                    "date": pub_date_str,
                    "link": f"https://doi.org/{article['doi']}" if article.get("doi") else f"https://europepmc.org/article/{article['source']}/{article['id']}",
                    "source": article.get("source"),
                    "text": full_text
                })

        return recent_articles

    def get_full_text(self, pmcid: str) -> str:
        url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
        try:
            response = requests.get(url)
            response.raise_for_status()
            root = ET.fromstring(response.content)

            text_parts = []

            for sec in root.findall(".//body//sec"):
                sec_title = sec.find("title")
                if sec_title is not None:
                    text_parts.append(sec_title.text.strip())
                for p in sec.findall("p"):
                    if p.text:
                        text_parts.append(p.text.strip())

            return "\n\n".join(text_parts)
        except Exception as e:
            print(f"Failed to fetch full text for PMCID {pmcid}: {e}")
            return ""
