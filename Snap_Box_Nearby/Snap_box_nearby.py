import requests
import json
import numpy as np
import pandas as pd
import time
import datetime

def main(): 

    url = 'https://app.snapp-box.com/api/v1/customer/nearby_biker_locations'

    df = pd.read_excel("input_data.xlsx",sheet_name = "Sheet1")

    auth_token = 'eyJhbGciOiJIUzUxMiJ9.eyJjaWQiOjE5NzE3MzA3LCJjcmlkIjoiMzMzNjQ3MDAiLCJlIjoibXprbW56a21AeWFob28uY29tIiwid2UiOmZhbHNlLCJzdWIiOiIwOTExNDU5ODI4NCIsImF1dGgiOiJST0xFX0NVU1RPTUVSIiwidHlwZSI6ImN1c3RvbWVyIn0.JKdYVbt2npsgCl2wW6WiqWcHKFXRrgAAhY536M3ejpdFUqdZh_-pxlMEELu4Zj086B_EzJ20oMdavbZ6MeHXtg'

    client_type = 'jek-pwa'

    content_type = 'application/json'

    platform = 'web'

    data_list = []

    for i in range(0,len(df),1):
        
        request = {}
        request['longitude'] = df['Source_long'][i]
        request['latitude'] = df['Source_lat'][i]
        request['zoom'] = str(df['zoom'][i])

        headers = {'Content-Type': content_type, 'Clienttype': client_type, 'Authorization': auth_token, 'Platform': platform}
        
        # print(request)
        response = requests.post(url, json=request, headers=headers)
        data = response.json()
        # print(data)
        for item in data:
            dictionary = {}
            # print(item['apiValue'] )
            dictionary['type'] = item['apiValue'] 
            dictionary['count'] = item['count']
            dictionary['area'] = str(df['Area_name'][i])
            dictionary['date'] = str(datetime.date.today())
            dictionary['time'] = str(datetime.datetime.now().strftime("%X"))
            data_list.append(dictionary)

    with pd.ExcelWriter("Near_Bikes_{}.xlsx".format(datetime.datetime.now().strftime("%X").replace(":", "_" ))) as writer:
        
        df2 = pd.DataFrame(data_list)
        
        df2.to_excel(writer, sheet_name='Near_Bikes', index=False)



if __name__=="__main__":

    while(True):

        main()

        time.sleep(20*60)