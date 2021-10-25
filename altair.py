#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import csv
import os
import datetime as dt
from datetime import datetime
import altair as alt


# In[2]:


def create_electricity_used_and_dates_list(directory_to_file):
    electricity_used = []
    dates_string = []
    power_per_day = []
    for filename in os.listdir(directory_to_file):
        power_per_day = []
        filename_each_day = os.path.join(directory_to_file, filename)
        with open (filename_each_day) as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                power_per_day.append(row[0]) # loop through each row and append every entry in first column to the list
        power_per_day = map(float, power_per_day) # convert from string to float
        sum_electricity_used_per_day = sum(power_per_day)/3600000 # compute sum of electricity used in kWh
        electricity_used.append(sum_electricity_used_per_day) # append to electricity_used_04
        dates_string.append(filename[:-4]) # append filename(excluding .csv suffix) to dates_04
    dates_datetime = [dt.datetime.strptime(date, '%Y-%m-%d').date() for date in dates_string] # convert from string to datetime object    
    return electricity_used, dates_datetime


# In[3]:


# for pc:
pc_04, pc_date_04 = create_electricity_used_and_dates_list('./data/04_plugs/04')
pc_05, pc_date_05 = create_electricity_used_and_dates_list('./data/05_plugs/07')
pc_06, pc_date_06 = create_electricity_used_and_dates_list('./data/06_plugs/02')


# In[4]:



# for entertainment:
entertainment_04, entertainment_date_04 = create_electricity_used_and_dates_list('./data/04_plugs/07')
entertainment_05, entertainment_date_05 = create_electricity_used_and_dates_list('./data/05_plugs/06')
entertainment_06, entertainment_date_06 = create_electricity_used_and_dates_list('./data/06_plugs/05')


# In[5]:


# for fridge:
fridge_04, fridge_date_04 = create_electricity_used_and_dates_list('./data/04_plugs/01')
fridge_05, fridge_date_05 = create_electricity_used_and_dates_list('./data/05_plugs/05')
fridge_06, fridge_date_06 = create_electricity_used_and_dates_list('./data/06_plugs/06')


# In[6]:


def create_df_from_lists(list_date, list_electricity):
    return pd.DataFrame(
                        {'Date': list_date,
                         'Electricity Used (kWh)': list_electricity
                        })


# In[7]:


df_pc_04 = create_df_from_lists(pc_date_04, pc_04)
df_pc_05 = create_df_from_lists(pc_date_05, pc_05)
df_pc_06 = create_df_from_lists(pc_date_06, pc_06)


df_entertainment_04 = create_df_from_lists(entertainment_date_04, entertainment_04)
df_entertainment_05 = create_df_from_lists(entertainment_date_05, entertainment_05)
df_entertainment_06 = create_df_from_lists(entertainment_date_06, entertainment_06)


df_fridge_04 = create_df_from_lists(fridge_date_04, fridge_04)
df_fridge_05 = create_df_from_lists(fridge_date_05, fridge_05)
df_fridge_06 = create_df_from_lists(fridge_date_06, fridge_06)


# In[8]:


def add_app_name_and_sort_df(df,app_name):
    df['appliances'] = app_name
    df = df.sort_values(by="Date")
    return df


# In[9]:


df_pc_04 = add_app_name_and_sort_df(df_pc_04, 'PC')
df_pc_05 = add_app_name_and_sort_df(df_pc_05, 'PC')
df_pc_06 = add_app_name_and_sort_df(df_pc_06, 'PC')

df_entertainment_04 = add_app_name_and_sort_df(df_entertainment_04, 'Entertainment')
df_entertainment_05 = add_app_name_and_sort_df(df_entertainment_05, 'Entertainment')
df_entertainment_06 = add_app_name_and_sort_df(df_entertainment_06, 'Entertainment')

df_fridge_04 = add_app_name_and_sort_df(df_fridge_04, 'Fridge')
df_fridge_05 = add_app_name_and_sort_df(df_fridge_05, 'Fridge')
df_fridge_06 = add_app_name_and_sort_df(df_fridge_06, 'Fridge')


# In[10]:



df_plug_04 = df_pc_04.merge(df_entertainment_04,how='left', left_on=['Date','Electricity Used (kWh)', 'appliances'], right_on = ['Date','Electricity Used (kWh)', 'appliances']).merge(df_fridge_04,how='left', left_on=['Date','Electricity Used (kWh)', 'appliances'], right_on = ['Date','Electricity Used (kWh)', 'appliances'])


# In[11]:


df_plug_04 = pd.concat([df_pc_04,df_entertainment_04,df_fridge_04], axis=0)


# In[20]:


df_plug_05 = pd.concat([df_pc_05,df_entertainment_05,df_fridge_05], axis=0)
df_plug_06 = pd.concat([df_pc_06,df_entertainment_06,df_fridge_06], axis=0)


# In[23]:


df_plug_04["Date"] = pd.to_datetime(df_plug_04["Date"])
df_plug_05["Date"] = pd.to_datetime(df_plug_05["Date"])
df_plug_06["Date"] = pd.to_datetime(df_plug_06["Date"])


# In[24]:


df_plug_04['Household'] = 'Household_04'
df_plug_05['Household'] = 'Household_05'
df_plug_06['Household'] = 'Household_06'
df = pd.concat([df_plug_04,df_plug_05,df_plug_06], axis=0)


# In[33]:


brush = alt.selection_interval()


# In[34]:


alt.renderers.enable('html')


# In[37]:


chart1 = alt.Chart(df).mark_circle().encode(x="Date", y="Electricity Used (kWh)", column="appliances", color=alt.condition(brush, 'Household', alt.value('lightgray')),     tooltip = [alt.Tooltip('Date'),
               alt.Tooltip('Household'),
               alt.Tooltip('Electricity Used (kWh)')
              ]).add_selection(
    brush
)

chart2 = alt.Chart(df).mark_bar().encode(
  alt.X('Electricity Used (kWh):Q', bin=True), alt.Y('count()')
).transform_filter(
 brush
)

chart_final = chart1 | chart2


# In[38]:


chart_final.save('1altair.html')


# In[40]:


# print(chart_final)


# In[39]:


# chart1 = alt.Chart(df_plug_04).mark_line().encode(x="Date", y="Electricity Used (kWh)", column="appliances", color=alt.condition(brush, 'Electricity Used (kWh):N', alt.value('lightgray'))).add_selection(
#     brush
# )

# chart2 = alt.Chart(df_plug_05).mark_line().encode(x="Date", y="Electricity Used (kWh)", column="appliances", color=alt.condition(brush, 'Electricity Used (kWh):N', alt.value('lightgray'))).add_selection(
#     brush
# )

# chart3 = alt.Chart(df_plug_06).mark_line().encode(x="Date", y="Electricity Used (kWh)", column="appliances", color=alt.condition(brush, 'Electricity Used (kWh):N', alt.value('lightgray'))).add_selection(
#     brush
# )

# chart1+chart2+chart3

