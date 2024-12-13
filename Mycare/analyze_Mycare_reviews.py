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
        
        identification_number = re.search(r'Mycare_(\d+)\.html', file_path).group(1) if re.search(r'Mycare_(\d+)\.html', file_path) else identification_number      
        product_name = None
          
        marketplace_id = 16  # Mycare
          
        # Extrahieren der Reviews  
        reviews = []  
        review_containers = soup.find_all('div', class_='reviewDetail row')  
          
        for container in review_containers:  
            review = {}  
              
            # Extrahieren des Namens des Rezensenten und des Datums  
            author_tag = container.find('div', class_='autor')  
            if author_tag:  
                author_text = author_tag.get_text(strip=True)  
                review['name'] = author_text.replace(' aus ', ', ').strip()  
            else:  
                review['name'] = None  
  
            date_tag = container.find('span', class_='date')  
            review['date'] = date_tag.get_text(strip=True) if date_tag else None  
              
            # Extrahieren des Produkttitels (nicht vorhanden in diesem Container)  
            review['product_title'] = None  
              
            # Extrahieren der Sternebewertung  
            stars_tag = container.find('span', class_='stars')  
            if stars_tag:  
                stars_text = stars_tag.get_text(strip=True)  
                stars_match = re.search(r'(\d+(\.\d+)?)', stars_text)  
                if stars_match:  
                    review['stars'] = f"{stars_match.group(1)} von 5 Sternen"  
                else:  
                    review['stars'] = None  
            else:  
                review['stars'] = None  
              
            # Extrahieren des Bewertungstexts  
            body_tag = container.find('div', class_='body')  
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
    
