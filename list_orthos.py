#This code filters through a list of .csv provided ortho's and paginates
#through all elements of the API call to find where FNSI is missing. 
#THIS TAKES A LONG TIME TO RUN, if you have a small handful of missions, 
#the single ortho script maybe better.



import csv
import pandas as pd
import requests


def get_new_token():
    response = requests.post(
        f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "scope": f"{client_id}/.default",
        },
    )
    return response.json()["access_token"]

client_id =  ''
client_secret = ''
tenant =  ''
pma_url = "https://plot-metadata-api.location360.ag"


token = get_new_token()

params = {
    "offset": 0,
    "limit": 100,
}


#the csv must have no quotes in it to proceed 

with open('ortho_names.csv',newline='') as f:
    reader = csv.reader(f)
    ortho_names = list(reader)
    
df=pd.DataFrame(ortho_names,columns=['ortho_names'])



target_seed_count=[]
plot_id=[]
planting_session_id=[]
read_ortho_name=[]


while True:
    for i in range(0,len(df)):
        #print(params['offset'], df.loc[i]['ortho_names'])
        
      
        
        r = requests.get(f"{pma_url}/ortho/{df.loc[i]['ortho_names']}", params=params, headers={"Authorization": f"Bearer {token}"})
    
        jsondata=r.json()
        
    
        items=jsondata['items']
        
        total_plots=jsondata['total']
        
        items_df=pd.DataFrame.from_dict(items)
        
        properties=items_df['properties']
        
        
        # #Parse through all elements of the properties series to grab all the target_seed_counts
        
        for i in range(0,len(properties)):
            target_seed_count.append(properties[i]['target_seed_count']) #list of FNSI from ortho
            plot_id.append(properties[i]['plot_id'])
            planting_session_id.append(properties[i]['planting_session_name'])
            read_ortho_name.append(properties[i]['ortho_name'])
            
    
          
        response_list=list(zip(plot_id,target_seed_count,planting_session_id,read_ortho_name))
        response_df=pd.DataFrame(response_list,columns=['plot_id','target_seed_count','planting_session_id','read_ortho_name'])    
             
        
        #find elements of dataframe that are null or empty, these are the problem children
        missing_df=response_df[response_df.isnull().any(axis=1)]
        
            
        params['offset']+=100 #go to next 100 elements 
        
        if params['offset'] > total_plots:
            print('All plots checked...exiting')
            break
      
        
        #response_df.to_excel("output.xlsx")