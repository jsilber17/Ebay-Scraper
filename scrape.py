import requests as r 
from bs4 import BeautifulSoup
import pandas as pd
import pickle as pkl 


class EbayComputerScraper(object): 

    def __init__(self): 
        self.page_num = 1
        self.end_page = 500
        self.url = url = 'https://www.ebay.com/sch/i.html?_nkw=computers&ssPageName=GSTL&_pgn={}'.format(self.page_num) 

    def check_for_200(self): 

        """ """ 
        page = r.get(url) 
        if page.status_code == 200: 
            pass 
        else: 
            pass # Add code that waits a few seconds and attempts request again 

    def soupify(self, url): 

        """ """ 
        page = r.get(url) 
        # insert check for 200 code here  

        soup = BeautifulSoup(page.text, 'html.parser') 

        return soup

    def turn_the_page(self): 

        """ """
        self.page_num += 1 
        print('Turning the page to page {}'.format(self.page_num)) 

    def scrape_ad(self, url): 

        soup = self.soupify(url)
        
        d_attr = {}

        for tag in soup.find_all(class_='it-ttl'):  
            d_attr['Title'] = tag.get_text().strip().replace('Details about', '') 

        for tag in soup.find_all(class_='it-sttl'): 
            d_attr['SubTitle'] = tag.get_text().strip()

        for tag in soup.find_all('span', {'style' : 'font-weight:bold;'}):  
            d_attr['Views Per Day'] = tag.get_text()

        for tag in soup.find_all(id='si-fb'):  
            d_attr['Seller Feedback Rate'] = tag.get_text()

        for tag in soup.find_all('div', {'itemprop' : 'itemCondition'}):  
            d_attr['Condition'] = tag.get_text()

        for tag in soup.find_all('span', {'itemprop' : 'price'}):  
            d_attr['Price'] = tag.get_text().replace(" ", "").replace("US", "").replace("$", "") 

        for tag in soup.find_all('td', {'class' : 'attrLabels'}):
            clean_tag = tag.get_text().strip().replace(':', '')

            if clean_tag == 'Model': 
                d_attr['Model'] = tag.findNext('td').get_text().strip() 
            elif clean_tag == 'Hard Drive Capacity': 
                d_attr['Hard Drive Capacity'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Operating System': 
                d_attr['Operating System'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'MPN': 
                d_attr['MPN'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Graphics Processing Type': 
                d_attr['Graphics Processing Type'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'GPU': 
                d_attr['GPU'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Item Heigh': 
                d_attr['Item Height'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Item Length': 
                d_attr['Item Length'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Item Width': 
                d_attr['Item Width'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Storage Type': 
                d_attr['Storage Type'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'RAM Size': 
                d_attr['RAM Size'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Connectivity': 
                d_attr['Connectivity'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Brand': 
                d_attr['Brand'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Series': 
                d_attr['Series'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Manufacturer Warranty': 
                d_attr['Manufacturer Warranty'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Type': 
                d_attr['Type'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Form Factor': 
                d_attr['Form Factor'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Processor Speed': 
                d_attr['Processor Speed'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Most Suitable for': 
                d_attr['Most Suitable For'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Maximum RAM Capacity': 
                d_attr['Maximum RAM Capacity'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Processor': 
                d_attr['Processor'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Features': 
                d_attr['Features'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Screen Size': 
                d_attr['Screen Size'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Color': 
                d_attr['Color'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'UPC': 
                d_attr['UPC'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'SSD Capacity': 
                d_attr['SSD Capacity'] = tag.findNext('td').get_text().strip() 
            elif clean_tag == 'Most Suitable For': 
                d_attr['Most Suitable For'] = tag.findNext('td').get_text().strip()
            elif clean_tag == 'Operating System Edition': 
                d_attr['Operating System Edition'] = tag.findNext('td').get_text().strip()
            else: 
                pass
           
        return d_attr 

    def scrape_results_page(self): 
        
        """ """
        if self.page_num == 1: 
            soup = self.soupify(self.url)
            self.turn_the_page()
        else: 
            self.turn_the_page() 
            soup = self.soupify(self.url) 
        
        self.result_links = []
        for a in soup.find_all('a', href=True): 
            if a.text:
                try: 
                    if a['href'].split('/')[3] == 'itm': 
                        self.result_links.append(a['href'])
                    else: 
                        continue 
                except IndexError: 
                    continue 
        
        return self.result_links

    def get_results(self): 

        attr_lst = [] 
        for _ in range(0, self.end_page): 
            ads = self.scrape_results_page()
            for idx, ad in enumerate(ads):
                d_result = self.scrape_ad(ad)
                if d_result in attr_lst: 
                    pass 
                else:
                    attr_lst.append(d_result)
        df = pd.DataFrame(attr_lst).drop_duplicates() 
        return df 
    

def main(): 
    
    x = EbayComputerScraper() 
    df = x.get_results()
    df.to_pickle('page_results_500.pkl')
    print("Dataframe magically turned into a pickle... I'm DataFrame pickle *burb*")  

if __name__ == '__main__': 
    main() 
