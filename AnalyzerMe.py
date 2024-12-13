#from ShopApotheke.analyze_ShopApotheke_reviews import analyze_EPharma_Reviews
#from DocMorris.analyze_DocMorris_reviews import analyze_EPharma_Reviews
#from Apotal.analyze_Apotal_reviews import analyze_EPharma_Reviews
#from Medpex.analyze_Medpex_reviews import analyze_EPharma_Reviews
#from Mycare.analyze_Mycare_reviews import analyze_EPharma_Reviews  
from Volksversandapotheke.analyze_Volksversand_reviews import analyze_EPharma_Reviews

import csv
#loop through all html files in the Reviews folder
import os

if __name__ == "__main__":
    # Pfad zum Ordner mit den HTML-Dateien
    folder_path = './Reviews'

    # Liste aller Dateien im Ordner
    files = os.listdir(folder_path)

    # Durchlaufen aller Dateien
    for file_name in files:
        # Überprüfen, ob die Datei eine HTML-Datei ist
        if file_name.endswith('.html'):
            # Pfad zur HTML-Datei
            file_path = os.path.join(folder_path, file_name)

            # HTML-Datei öffnen und lesen
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Analyse durchführen
            result = analyze_EPharma_Reviews(html_content, file_path)

            # Create a list to store all reviews
            all_reviews = []
            all_reviews.extend(result)

            # Save all reviews to CSV at the end of processing
            csv_file_path = os.path.join(folder_path, "Volksversand_all_reviews.csv")
            # Open file in append mode if it exists, write mode if it doesn't
            mode = 'a' if os.path.exists(csv_file_path) else 'w'
            with open(csv_file_path, mode, encoding='utf-8', newline='') as csv_file:
                # Assuming result contains dictionaries, get headers from first review
                if all_reviews:
                    headers = all_reviews[0].keys()
                    writer = csv.DictWriter(csv_file, fieldnames=headers, delimiter=';')
                    # Only write header if creating new file or header empty
                    writer.writeheader()
                    # if mode == 'w':
                    #     writer.writeheader()
                    
                    writer.writerows(all_reviews)
            print(f"Analysis for {file_name} completed and added to {os.path.basename(csv_file_path)}")


