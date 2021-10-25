#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly
import plotly.graph_objs as go
import csv
import os
import datetime as dt
from datetime import datetime
import plotly.express as px


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


e_04,d_04 = create_electricity_used_and_dates_list('./data/04_sm/04/')


# In[4]:


e_05,d_05 = create_electricity_used_and_dates_list('./data/05_sm/')
e_06,d_06 = create_electricity_used_and_dates_list('./data/06_sm/')


# In[5]:


df_sm_04 = pd.DataFrame(
    {'Date': d_04,
     'Electricity Used (kWh)': e_04
    })


# In[6]:


df_sm_05 = pd.DataFrame(
    {'Date': d_05,
     'Electricity Used (kWh)': e_05
    })

df_sm_06 = pd.DataFrame(
    {'Date': d_06,
     'Electricity Used (kWh)': e_06
    })


# In[7]:


sm_04 = pd.DataFrame(
    {'Date': d_04,
     'Electricity Used (kWh)': e_04
    })


# In[8]:


df_sm_04 = df_sm_04.sort_values(by="Date")
df_sm_05 = df_sm_05.sort_values(by="Date")
df_sm_06 = df_sm_06.sort_values(by="Date")


# In[14]:


# dict for the dataframes and their names
dfs = {"Household_04" : df_sm_04, "Household_05": df_sm_05, "Household_06" : df_sm_06}

# plot the data

layout = go.Layout(title='Electricity Usage (kWh) Per Day from Three Example Households',
                   xaxis=dict(title='Date'),
                   yaxis=dict( title='Electricity Usage (kWh)'))

fig = go.Figure(layout=layout)
for i in dfs:
    fig = fig.add_trace(go.Line(x = dfs[i]["Date"],
                                   y = dfs[i]["Electricity Used (kWh)"], 
                                   name = i,
                                   hovertemplate='Date: %{x}'+'<br>Electricity Used (kWh): %{y}'))
fig.show()


# In[18]:


import plotly.io as pio
pio.write_html(fig, file='plotly.html', auto_open=False)
# plotly_html = pio.to_html(fig, full_html=True)

# with open("altair copy.html", "a") as out_file:
#     out_file.write(plotly_html)


# In[ ]:





# In[ ]:




