from bs4 import BeautifulSoup
import re
import json

def analyze_EPharma_Reviews(html_content):
    try:
        # Erstellen Sie ein BeautifulSoup-Objekt
        soup = BeautifulSoup(html_content, 'html.parser')

        # Suche nach dem <meta> Tag mit dem Attribut property="og:url"
        url = soup.find('meta', {'property': 'og:url'}).get('content')
        

        # Extrahiere den Teil der URL vor ".htm"
        match = re.search(r'/(\d+)/([a-zA-Z0-9\-]+)\.htm', url)

        if match:
            identification_number = match.group(1)  # Die PZN (Zahl)
            product_name = match.group(2)  # Der Name (letzter Teil vor ".htm")
        
        marketplace_id = 1 #Shop-Apotheke
        
        # Extrahieren der Reviews
        reviews = []
        review_containers = soup.find_all('li', class_='border-b border-b-dark-primary-min py-5')

        for container in review_containers:
            review = {}

            # Extrahieren des Namens des Rezensenten und des Datums
            # Extrahieren des Namens des Rezensenten und des Datums
            # Extrahieren des Namens des Rezensenten und des Datums
            name_date_tag = container.find('h4', class_='mb-2.5 text-xs font-medium')
            if name_date_tag:
                name_date_text = name_date_tag.get_text(strip=True)
                # Suche nach dem ersten Vorkommen einer Ziffer für das Datum
                date_match = re.search(r'\d', name_date_text)
                if date_match:
                    date_start = date_match.start()
                    review['name'] = name_date_text[:date_start].replace('von', '').replace(' am ', '').replace('am', '').strip()
                    review['date'] = name_date_text[date_start:].replace(' am ', '').replace(' ', '').strip()
                else:
                    review['name'] = name_date_text.replace('von', '').replace(' am ', '').strip()
                    review['date'] = None
            else:
                review['name'] = None
                review['date'] = None

            # Extrahieren des Produkttitels
            product_title_tag = container.find('span', class_='text-m font-medium tablet:ml-2.5')
            review['product_title'] = product_title_tag.get_text(strip=True) if product_title_tag else None

            # Extrahieren der Sternebewertung
            stars_tag = container.find('span', class_='rating')
            if stars_tag:
                filled_stars = len(stars_tag.find_all('svg', class_='rating__icon rating__icon_filled'))
                review['stars'] = f"{filled_stars} von 5 Sternen"
            else:
                review['stars'] = None

            # Extrahieren des Bewertungstexts
            body_tag = container.find('p', class_='text-s')
            review['body'] = body_tag.get_text(strip=True) if body_tag else None

            review['url'] = url

            review['marketplace_id'] = marketplace_id

            review['identification_number'] = identification_number

            review['product_name'] = product_name

            # Hinzufügen der Rezension zur Liste
            reviews.append(review)

            

        
        return reviews

    except Exception as e:
        print(f"Error during execution: {e}")
        return None
    
if __name__ == "__main__":
    with open('./Reviews/ShopApoReview.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    result = analyze_EPharma_Reviews(html_content)
    print(json.dumps(result, indent=2))