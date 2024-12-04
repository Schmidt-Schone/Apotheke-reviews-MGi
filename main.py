from ShopApotheke.scrape_ShopApotheke_reviews import scrape_ShopApotheke
from DocMorris.scrape_DocMorris_reviews import scrape_DocMorris
from ApoNeo.scrape_ApoNeo_reviews import scrape_ApoNeo
from Medpex.scrape_Medpex_reviews import scrape_Medpex
from Apotal.scrape_Apotal_reviews import scrape_Apotal
from Mycare.Scrape_Mycare_reviews import scrape_MyCare
from Volksversandapotheke.scrape_Volksversandapotheke_reviews import scrape_Volksversand
from Bodfeld.scrape_Bodfeld_reviews import scrape_Bodfeld
from Aliva.scrape_Aliva_reviews import scrape_Aliva

def main():
    with open('base_Url_list.csv', 'r') as f:
        #loop through each line in the file
        for line in f:
            
            #ShopApotheke // OK
            # if line.split(',')[2] == '1\n':
            #     PZN = line.split(',')[0]
            #     base_url = line.split(',')[1]
            #     scrape_ShopApotheke(base_url, PZN)

            #DocMorris // OK
            if line.split(',')[2] == '2\n':
                PZN = line.split(',')[0]
                base_url = line.split(',')[1]
                scrape_DocMorris(base_url, PZN)

            #Medpex // OK
            elif line.split(',')[2] == '7\n':
                PZN = line.split(',')[0]
                base_url = line.split(',')[1]
                scrape_Medpex(base_url, PZN)

            #Apotal // OK
            elif line.split(',')[2] == '14\n':
                PZN = line.split(',')[0]
                base_url = line.split(',')[1]
                scrape_Apotal(base_url, PZN)
            
            #MyCare // OK
            elif line.split(',')[2] == '16\n':
                PZN = line.split(',')[0]
                base_url = line.split(',')[1]
                scrape_MyCare(base_url, PZN)

            #Volksversand // OK
            elif line.split(',')[2] == '17\n':
                PZN = line.split(',')[0]
                base_url = line.split(',')[1]
                scrape_Volksversand(base_url, PZN)

            #ApoNeo // FEHLERHAFT //
            # elif line.split(',')[2] == '6\n':
            #     PZN = line.split(',')[0]
            #     base_url = line.split(',')[1]
            #     scrape_ApoNeo(base_url, PZN)
            
            #Bodfeld // Abbruchbedingung für Scrolling fehlt -> Endlosschleife
            # elif line.split(',')[2] == '19\n':
            #     PZN = line.split(',')[0]
            #     base_url = line.split(',')[1]
            #     scrape_Bodfeld(base_url, PZN)

            #Aliva // Abbruchbedingung für Scrolling fehlt -> Endlosschleife
            # elif line.split(',')[2] == '20\n':
            #     PZN = line.split(',')[0]
            #     base_url = line.split(',')[1]
            #     scrape_Aliva(base_url, PZN)

if __name__ == "__main__":
    main()