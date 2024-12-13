from bs4 import BeautifulSoup
import re
import json

def analyze_EPharma_Reviews(html_content, file_path):  
    try:  
        # Erstellen Sie ein BeautifulSoup-Objekt  
        soup = BeautifulSoup(html_content, 'html.parser')  
  
        # Suche nach dem <meta> Tag mit dem Attribut property="og:url"  
        url_tag = soup.find('meta', {'property': 'og:url'})  
        url = url_tag.get('content') if url_tag else None  
          
        identification_number = re.search(r'Volksversandapotheke_(\d+)\.html', file_path).group(1) if re.search(r'Volksversandapotheke_(\d+)\.html', file_path) else identification_number      
        product_name = None  
          
        marketplace_id = 17  # Volksversand-Apotheke  
          
        # Extrahieren der Reviews  
        reviews = []  
        review_containers = soup.find_all('div', class_='review--entry')  
          
        for container in review_containers:  
            review = {}  
              
            # Extrahieren des Namens des Rezensenten und des Datums  
            author_tag = container.find('span', class_='content--field')  
            review['name'] = author_tag.get_text(strip=True) if author_tag else None  
              
            date_tag = container.find_all('span', class_='content--field')  
            review['date'] = date_tag[1].get_text(strip=True) if len(date_tag) > 1 else None  
              
            # Extrahieren des Produkttitels  
            product_title_tag = container.find('h4', class_='content--title')  
            review['product_title'] = product_title_tag.get_text(strip=True) if product_title_tag else None  
              
            # Extrahieren der Sternebewertung  
            stars_tag = container.find('span', class_='product--rating')  
            if stars_tag:  
                filled_stars = len(stars_tag.find_all('i', class_='icon--star'))  
                review['stars'] = f"{filled_stars} von 5 Sternen"  
            else:  
                review['stars'] = None  
              
            # Extrahieren des Bewertungstexts  
            body_tag = container.find('p', class_='content--box review--content')  
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
    
