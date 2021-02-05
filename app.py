import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px







st.title("Motor Vehicle Collisions in New York city")
st.markdown("On average there were 316 deaths each year due to motor vehicle traffic-related injuries where role of injured person is unspecified, killing 1.6 of every 100,000 New Yorkers. The rates were highest for males and New Yorkers aged 20-24, followed by those 65 and older.This Streamlit Application monitors the traffic accidents in New York city.")
DATA_URL = (r'C:\Users\Dell\Desktop\current_project\Motor_Vehicle_Collisions_-_Crashes.csv')

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL,nrows=nrows, parse_dates=[['CRASH_DATE','CRASH_TIME']])
    data.dropna(subset=['LATITUDE','LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data

data = load_data(100000)

st.header("Where are most of the people are injured in NYC?")
injured_people = st.slider("Number of people injured", 0 , 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))

st.header("How many collisions occured during a given time of the day?")
hour = st.slider("Hour to look at ", 0, 23)
data = data[data['date/time'].dt.hour == hour]

st.markdown("Vehicle Collisions between %i:00 and %i:00" % (hour, (hour + 1) %24))
midpoint = (np.average(data['latitude']),np.average(data['longitude']))


st.write(pdk.Deck(
 map_style="mapbox://styles/mapbox/light-v9",
 initial_view_state={
 "latitude": midpoint[0],
 "longitude": midpoint[1],
 "zoom": 11,
 "pitch": 50,
 },
 layers=[ pdk.Layer(
 "HexagonLayer",
 data=data[['date/time', 'latitude', 'longitude']],
 get_position=['longitude', 'latitude'],
 radius=100,
 extruded=True,
 pickable=True,
 elevation_scale=4,
 elevation_range=[0,1000],
 ),
 ],
))


st.markdown("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) %24))
filtered=data[
(data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour+1))
]

histogram = np.histogram(filtered['date/time'].dt.minute, bins=60 , range=(0,60))[0]
chart_data = pd.DataFrame({'minute': range(60), 'crashes':histogram})
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute','crashes'], height=400)
st.write(fig)




if st.checkbox("Show RAW data", False):
    st.subheader('RAW DATA')
    st.write(data)
