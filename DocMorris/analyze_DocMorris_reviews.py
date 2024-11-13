from bs4 import BeautifulSoup
import re
import json
import csv

def analyze_EPharma_Reviews(html_content):
    try:
        # Create a BeautifulSoup object
        soup = BeautifulSoup(html_content, 'html.parser')

        # Initialize identification_number and product_name to None
        identification_number = None
        product_name = None

       # Find the <meta> tag with the attribute property="og:url"
        url_tag = soup.find('meta', {'property': 'og:url'})
        if url_tag:
            url = url_tag.get('content')
        
            # Extract the part of the URL before ".htm"
            match = re.search(r'/(\d+)/([a-zA-Z0-9\-]+)\.htm', url)
            if match:
                identification_number = match.group(1)  # The PZN (number)
                product_name = match.group(2)  # The name (last part before ".htm")

        marketplace_id = 2  # DocMorris
        
        # Extract reviews
        reviews = []
        review_containers = soup.find_all('li', class_='bv-content-item bv-content-top-review bv-content-review')
        
        for container in review_containers:
            review = {}

            # Extract the reviewer's name and date
            name_tag = container.find('button', class_='bv-author bv-fullprofile-popup-target bv-focusable')
            date_tag = container.find('span', class_='bv-content-datetime-stamp')
            review['name'] = name_tag.h3.get_text(strip=True) if name_tag else None
            review['date'] = date_tag.get_text(strip=True) if date_tag else None
            
            # Extract product title
            product_title_tag = container.find('h3', class_='bv-content-title')
            review['product_title'] = product_title_tag.get_text(strip=True) if product_title_tag else None
            
            # Extract star rating
            stars_tag = container.find('span', class_='bv-off-screen')
            review['review_rating'] = stars_tag.get_text(strip=True) if stars_tag else None
            
            # Extract review text
            body_tag = container.find('div', class_='bv-content-summary-body-text')
            review['review'] = body_tag.p.get_text(strip=True) if body_tag else None
            
            # New fields
            # Reviewer age
            age_tag = container.find('span', class_='bv-author-userinfo-value')
            review['reviewer_age'] = age_tag.get_text(strip=True) if age_tag else None
            
            # Likes and dislikes
            review_liked_tag = container.find('button', class_='bv-content-btn-feedback-yes')
            review_disliked_tag = container.find('button', class_='bv-content-btn-feedback-no')
            review['review_liked'] = review_liked_tag.find('span', class_='bv-content-btn-count').get_text(strip=True) if review_liked_tag else '0'
            review['review_disliked'] = review_disliked_tag.find('span', class_='bv-content-btn-count').get_text(strip=True) if review_disliked_tag else '0'
            
            # Comment (secondary ratings)
            secondary_ratings = container.find_all('span', class_='bv-off-screen')
            review['comment'] = ', '.join([rating.get_text(strip=True) for rating in secondary_ratings])

            # Static fields
            review['url'] = url
            review['marketplace_id'] = marketplace_id
            review['identification_number'] = identification_number
            review['product_name'] = product_name

            # Add the review to the list
            reviews.append(review)

        return reviews

    except Exception as e:
        print(f"Error during execution: {e}")
        return None

    
if __name__ == "__main__":
    with open('./Reviews/DocMorris.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    result = analyze_EPharma_Reviews(html_content)
    
    # Print result to console
    print(json.dumps(result, indent=2))

    # Save result to a JSON file
    with open('./Reviews/DocMorris_reviews.json', 'w', encoding='utf-8') as output_file:
        json.dump(result, output_file, ensure_ascii=False, indent=2)