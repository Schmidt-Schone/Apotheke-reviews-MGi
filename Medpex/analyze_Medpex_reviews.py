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
          
        # Extrahiere den Teil der URL vor ".htm"  
        if url:  
            match = re.search(r'/(\d+)/([a-zA-Z0-9\-]+)\.htm', url)  
            if match:  
                identification_number = match.group(1)  # Die PZN (Zahl)  
                product_name = match.group(2)  # Der Name (letzter Teil vor ".htm")  
            else:  
                identification_number = None  
                product_name = None  
        else:  
            identification_number = None  
            product_name = None  
          
        marketplace_id =7  # Medpex
          
        # Extrahieren der Reviews  
        reviews = []  
        review_containers = soup.find_all('div', class_='review-list-entry')  
          
        for container in review_containers:  
            review = {}  
              
            # Extrahieren des Namens des Rezensenten und des Datums  
            name_date_tag = container.find('div', class_='name')  
            if name_date_tag:  
                name_date_text = name_date_tag.get_text(strip=True)  
                # Suche nach dem ersten Vorkommen einer Ziffer für das Datum  
                date_match = re.search(r'\d{2}\.\d{2}\.\d{4}', name_date_text)  
                if date_match:  
                    date_text = date_match.group(0)  
                    review['date'] = date_text.strip()  
                    review['name'] = name_date_text.replace(f'schreibt am {date_text}', '').strip()  
                else:  
                    review['name'] = name_date_text.strip()  
                    review['date'] = None  
            else:  
                review['name'] = None  
                review['date'] = None  
              
            # Extrahieren des Produkttitels  
            product_title_tag = container.find('h3')  
            review['product_title'] = product_title_tag.get_text(strip=True) if product_title_tag else None  
              
            # Extrahieren der Sternebewertung  
            stars_tag = container.find('div', class_='sp-star')  
            if stars_tag:  
                stars_class = stars_tag.get('class')  
                filled_stars = [cls for cls in stars_class if cls.startswith('sp-star-')]  
                if filled_stars:  
                    review['stars'] = f"{filled_stars[0].split('-')[-1]} von 5 Sternen"  
                else:  
                    review['stars'] = None  
            else:  
                review['stars'] = None  
              
            # Extrahieren des Bewertungstexts  
            body_tag = container.find('div', class_='text')  
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
    
