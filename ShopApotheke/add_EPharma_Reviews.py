import psycopg2
import datetime
from ShopApotheke.analyze_ShopApotheke_reviews import analyze_EPharma_Reviews

#results_EPharma_Reviews = [{'name': 'Claudia L.', 'date': '01.05.2024', 'product_title': 'Gut', 'stars': '4 von 5 Sternen', 'body': 'Hilft gegen innere Unruhe. Habe aber was anderes für mich gefunden was ein wenig besser ist.', 'url': 'https://www.shop-apotheke.com/homoeopathie/4143009/neurexan-tabletten.htm', 'marketplace_id': 1, 'identification_number': '4143009', 'product_name': 'neurexan-tabletten'}]
#reviewer_name,rating,review_title,review,review_date,id,identification_number,product_name,asin,url,marketplace_id

with open('./Reviews/ShopApoReview.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

reviews = analyze_EPharma_Reviews(html_content=html_content)

def getCursor():
    
    connection = psycopg2.connect(  
            host="10.0.0.2",  
            database="buybox_crawler",  
            user="crawler",  
            password="eaZjfsltrxmJ7tN9Ljw2X73U9HvFtyam",  
            port="5432",  
            connect_timeout=3000  
    )  
    
    cursor = connection.cursor() 

    return cursor



def add_EPharma_Reviews(reviews):
    cursor = getCursor()
    data = []
    

    for item in reviews:
            
            try:
                reviewer_name = item.get('name', '')
                rating = item.get('stars', '')
                review_title = item.get('title', '')
                review = item.get('body', '')
                review_date = item.get('date', '')
                marketplace_id = item.get('marketplace_id', '')
                identification_number = item.get('identification_number', '')
                product_name = item.get('product_name', '')
                url = item.get('url', '')
                asin = ""

                record = (reviewer_name, rating, review_title, review, review_date, identification_number, product_name, url, marketplace_id, asin)

                data.append(record) 
            except:
                continue

    try:
        cursor.execute("BEGIN;")
        insert_query ="""
        INSERT INTO review_table (
            reviewer_name, rating, review_title, review, review_date, identification_number, product_name, url, marketplace_id, asin
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        cursor.executemany(insert_query, data)
        cursor.execute("COMMIT;")

        print(f"{len(data)} Datensätze erfolgreich in die Datenbank eingefügt.")

    except (Exception, psycopg2.Error) as error:
        cursor.execute("ROLLBACK;")
        print("Fehler beim Einfügen in die Datenbank:", error)

if __name__ == "__main__":
    add_EPharma_Reviews(reviews)