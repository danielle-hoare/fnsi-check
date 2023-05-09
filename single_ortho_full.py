#This code checks all the plots for a single ortho,

import requests
import pandas as pd

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
ortho_name='6g2z4q_DroneDeploy_202211161621.tif'



pma_url = "https://plot-metadata-api.location360.ag"

token = get_new_token()



#should figure out some pagination logic for a working version
params = {
    "offset": 0,
    "limit": 100,
}


target_seed_count=[]
plot_id=[]
planting_session_id=[]

while True:
    print(params['offset'])
    r = requests.get(f"{pma_url}/ortho/{ortho_name}", params=params, headers={"Authorization": f"Bearer {token}"})
    
    
    jsondata=r.json()
        
    total_plots=jsondata['total'] #total # of plots, luckily this comes from the initial request :) 
    
    items=jsondata['items']
    
    items_df=pd.DataFrame.from_dict(items)
    
    properties=items_df['properties']
    
    
    
    #Parse through all elements of the properties series to grab all the target_seed_counts
    
    for i in range(0,len(properties)):
        target_seed_count.append(properties[i]['target_seed_count']) #list of FNSI from ortho
        plot_id.append(properties[i]['plot_id'])
        planting_session_id.append(properties[i]['planting_session_name'])
        
       
    
    
    response_list=list(zip(plot_id,target_seed_count,planting_session_id))
    response_df=pd.DataFrame(response_list,columns=['plot_id','target_seed_count','planting_session_id'])
    
    missing_df=response_df[response_df.isnull().any(axis=1)] #finds any empty FNSI values and adds them to it's own list
    
    
    if missing_df.empty==True:
        print('This ortho has FNSI populated for all plots so far...')
    else:
        print('This mission has some missing target seed count data, exiting...')
        break #you can remove break if you'd like to still run through all the plots, even if they are missing. 
        
    params['offset']+=100 #go to next 100 elements 
    
    if params['offset'] >= total_plots:
        print('All plots have FNSI.') 
        break
