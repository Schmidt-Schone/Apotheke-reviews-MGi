from ShopApotheke.scrape_ShopApotheke_reviews import scrape_ShopApotheke


def main():
    with open('base_Url_list.csv', 'r') as f:
        #loop through each line in the file and start from second line
        for line in f:
            
            #ShopApotheke
            if line.split(',')[2] == '1\n':
                PZN = line.split(',')[0]
                base_url = line.split(',')[1]
                scrape_ShopApotheke(base_url, PZN)
                

        
if __name__ == "__main__":
    main()