import json
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth


class Mode:
    '''
    Class wrapper for interacting with the mode API.
    
    '''
    def __init__(self, key_file):

        with open(key_file) as f:
            data = json.load(f)
            self.token = data.get('token')
            self.password = data.get('password')

        self.base_url = 'https://modeanalytics.com/api/beautiful'
    
    def get_report_data(self, page = 1):
        '''
        returns report data for a single page of data. 
        '''
        url = f'{self.base_url}/data_sources/dca975c09d87/reports?page={page}'
        r = requests.get(url, auth=HTTPBasicAuth(self.token, self.password))
        
        data = json.loads(r.content)
        
        return data.get('_embedded').get('reports')
    
    def get_query_data(self, report_token):
        '''
        returns query data for a single report. 
        '''
        url = f'{self.base_url}/reports/{report_token}/queries'
        r = requests.get(url, auth=HTTPBasicAuth(self.token, self.password))
        
        data = json.loads(r.content)
        
        return data.get('_embedded').get('queries')
    
    def collect_all_report_data(self):
        '''
        Saves all report data to a list
        '''
        page = 1
        page_data = self.get_report_data(page = page)
        data = []
        
        while page_data:
            data.extend(page_data)
            page += 1
            page_data = self.get_report_data(page = page)
        
        return data

    def collect_all_query_data(self):
        '''
        Saves all query level data to a pandas dataframe
        '''

        report_data = self.collect_all_report_data()
        unique_tokens = list(set([d['token'] for d in report_data]))

        query_data = []

        for report_token in unique_tokens:
            
            query_data.extend(
                self.get_query_data(report_token)
            )

        return query_data


        
    


query_data = Mode(key_file = 'creds.json').collect_all_query_data()
df = pd.DataFrame(query_data)
df.to_csv('output.csv')
pass
