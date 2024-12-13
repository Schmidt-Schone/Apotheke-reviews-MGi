from bs4 import BeautifulSoup
import re
import json
import csv

def analyze_EPharma_Reviews(html_content, file_path):  
    try:  
        # Create soup object  
        soup = BeautifulSoup(html_content, 'html.parser')  
  
        # Initialize variables  
        identification_number = None  
        product_name = None  
        url = None  
        marketplace_id = 3  # Assign a unique ID for the new marketplace  
  
        # Extract identification_number and URL from the 'href' in the 'a' tag with class 'buttonLinks btnSpecial'  
        a_tag = soup.find('a', class_='buttonLinks btnSpecial')  
        if a_tag and a_tag.has_attr('href'):  
            href = a_tag['href']  
            url = href  
            match = re.search(r'prodId=(\d+)', href)  
            if match:  
                identification_number = match.group(1)  
  
        # Extract product name if available (adjust as needed)  
        # Assuming product name is in a <h1> tag or similar  
        product_name_tag = soup.find('h1', class_='product-name')  
        if product_name_tag:  
            product_name = product_name_tag.get_text(strip=True)  
  
        # Extract reviews  
        reviews = []  
        # Find all divs with class containing 'customerReviewsLine'  
        review_containers = soup.find_all('div', class_=lambda x: x and 'customerReviewsLine' in x)  
  
        for container in review_containers:  
            review = {}  
  
            # Extract review title  
            review_title_tag = container.find('span', class_='title', itemprop='name')  
            review['product_title'] = review_title_tag.get_text(strip=True) if review_title_tag else None  
  
            # Extract reviewer's name  
            name_tag = container.find('span', class_='name')  
            reviewer_name = None  
            if name_tag:  
                author_tag = name_tag.find('span', itemprop='author')  
                if author_tag:  
                    reviewer_name_tag = author_tag.find('span', itemprop='name')  
                    reviewer_name = reviewer_name_tag.get_text(strip=True) if reviewer_name_tag else None  
            review['name'] = reviewer_name  
  
            # Extract date  
            date_tag = container.find('span', class_='date', itemprop='datePublished')  
            review['date'] = date_tag.get_text(strip=True) if date_tag else None  
  
            # Extract star rating  
            # Try to get ratingValue  
            rating_tag = container.find('span', itemprop='ratingValue')  
            if rating_tag:  
                review_rating = rating_tag.get_text(strip=True)  
            else:  
                # Count the number of 'i' tags with class 'icon-star' in 'span class="rank image"'  
                rank_image_tag = container.find('span', class_='rank image')  
                if rank_image_tag:  
                    stars = rank_image_tag.find_all('i', class_='icon-star')  
                    review_rating = str(len(stars))  
                else:  
                    review_rating = None  
            review['review_rating'] = review_rating  
  
            # Extract review text  
            body_tag = container.find('p', class_='comment', itemprop='description')  
            review['review'] = body_tag.get_text(strip=True) if body_tag else None  
  
            # 'reviewer_age' is not present in the new HTML  
            review['reviewer_age'] = None  
  
            # Extract likes and dislikes  
            feedback_div = container.find('div', id=re.compile(r'feedback_\d+'))  
            review_liked = '0'  
            review_disliked = '0'  
            if feedback_div:  
                info_feedback = feedback_div.find('span', class_='info-feedback')  
                if info_feedback:  
                    feedback_text = info_feedback.get_text(strip=True)  
                    # Extract numbers from text like "4 von 5 Kunden fanden diese Bewertung hilfreich."  
                    match = re.search(r'(\d+)\s+von\s+(\d+)\s+Kunden', feedback_text)  
                    if match:  
                        likes = match.group(1)  
                        total = match.group(2)  
                        review_liked = likes  
                        review_disliked = str(int(total) - int(likes))  
            review['review_liked'] = review_liked  
            review['review_disliked'] = review_disliked  
  
            # 'comment' (secondary ratings) is not present in the new HTML  
            review['comment'] = None  
  
            # Static fields  
            review['url'] = url  
            review['marketplace_id'] = marketplace_id  
            
            #get filename of current html
            review['identification_number'] = re.search(r'Apotal_(\d+)\.html', file_path).group(1) if re.search(r'Apotal_(\d+)\.html', file_path) else identification_number      
  
            # Add the review to the list  
            reviews.append(review)  
  
        # Define the headers (column names)  
        headers = ['name', 'date', 'product_title', 'review_rating', 'review', 'reviewer_age',  
                   'review_liked', 'review_disliked', 'comment', 'url', 'marketplace_id',  
                   'identification_number', 'product_name']  
  
        # Write the reviews to a CSV file with headers  
        with open('reviews.csv', 'w', newline='', encoding='utf-8') as csvfile:  
            writer = csv.DictWriter(csvfile, fieldnames=headers)  
            writer.writeheader()  # Write the header row  
            for review in reviews:  
                writer.writerow(review)  
  
        # Return the reviews (optional)  
        return reviews  
  
    except Exception as e:  
        print(f"Error during execution: {e}")  
        return None  

    
if __name__ == "__main__":
    with open('./Reviews/Apotal_4115289.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    result = analyze_EPharma_Reviews(html_content, './Reviews/Apotal_4115289.html')
    
    # Print result to console
    print(json.dumps(result, indent=2))

    # Save result to a JSON file
    with open('./Reviews/DocMorris_reviews.json', 'w', encoding='utf-8') as output_file:
        json.dump(result, output_file, ensure_ascii=False, indent=2)