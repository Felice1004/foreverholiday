import streamlit as st
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
# print (webdriver.__version__)
from bs4 import BeautifulSoup
from datetime import datetime
import datetime as dt

import time

st.title('Forever Holiday')
st.subheader('Extract worldwide holidays! (Notion Importable)')
st.caption('Supported Country:')
data = pd.read_csv('country.csv')
countries = data['country'].tolist()
text = ''
for c in countries:
    text += c + ', '
st.caption(text)

# # # # # # # # # # # # # #
st.divider()
# # # # # # # # # # # # # #

# YEAR INPUT
today = dt.date.today()
current_year = today.year
year = st.text_input('Year',value=current_year)

start = st.button("START")

if start:
    Country = [] ; Date = []; Name = []; Weekday = []; Type = []

    driver = webdriver.Chrome()
    for country in countries:
        print(country)
        driver.get(f"https://www.timeanddate.com/holidays/{str.lower(country)}/{year}") # 更改網址以前往不同網頁
        time.sleep(0.25)
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        holiday_selectors = soup.find_all('table',{"id": "holidays-table"})

        date_exist = False

        for holiday_selector in holiday_selectors:
            holiday_rows = holiday_selector.find_all('tr')
            for row in holiday_rows:
                dates = row.find_all('th')
                for date in dates:
                    if date.get_text() not in ['Date','Name','Type'] and len(date.get_text())>1:
                        date_str = date.get_text()
                        # print(date_str)

                        date_str = f"{date_str} {year}"
                        try:
                            print('wtf 0')
                            date_object = datetime.strptime(date_str, "%d %b %Y")
                            print('wtf 1')
                            formatted_date = date_object.strftime("%d/%m/%Y")
                            print('wtf 2')

                            Date.append(formatted_date)
                            print('wtf 3')
                            # print(country)
                            Country.append(country)
                            print('wtf 4')
                        except Exception as error:
                            print(error)
                            continue

                        holiday_other_infos = row.find_all('td');  
                        if len(holiday_other_infos) > 1:
                            
                            i = 0
                            for other_info in holiday_other_infos:
                                info = other_info.get_text()
                                if len(info) <= 0:
                                    info = "#ERROR"
                                match i:
                                    case 0:
                                        Weekday.append(info)
                                        pass
                                    case 1:
                                        Name.append(info)
                                        pass
                                    case 2: 
                                        Type.append(info)
                                        pass
                                i+=1
                        else:
                            Weekday.append('#ERROR')
                            Name.append('#ERROR')
                            Type.append('#ERROR')
        driver.quit()

                    
    data = {'Country':Country, 'Date':Date, 'Weekday':Weekday, 'Name':Name, 'Type':Type}
    print(data)
    holiday_list = pd.DataFrame(data)
    holiday_list['Type'] = holiday_list['Type'].astype(str)
    holiday_list = holiday_list[holiday_list['Type'].str.contains('holiday', case=False)]

    csv_file = holiday_list.to_csv(index=False).encode('utf-8')

    # holiday_list = holiday_list[holiday_list['Type'].str.contains('holiday', case=False)]
    # download = holiday_list.to_csv(f'output/holiday_{year}.csv', index=False)

    st.download_button(label="DOWNLOAD", data=csv_file, key='download_button', file_name=f'Holiday of {year}.csv')




