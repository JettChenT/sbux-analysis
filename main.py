#%%
import requests
import pandas as pd
import requests
import streamlit as st
import pydeck as pdk
import h3
#%%
st.title("Starbucks!")
st.write("## The financial report (data was gathered from [FAPI](https://site.financialmodelingprep.com/financial-statements/SBUX))")
data = pd.read_csv("./sbux.csv")
data.drop(columns=data.columns[0], axis=1, inplace=True)
st.write(data)

#%%
st.write("## A map of all Starbucks stores (data from [Kaggle](https://www.kaggle.com/starbucks/store-locations/version/1))")
df = pd.read_csv('./directory.csv')
locations = df[['Latitude', 'Longitude']]
locations.rename({'Latitude':'lat', 'Longitude':'lon'}, axis='columns', inplace=True)
locations.dropna(inplace=True)

st.write("### Simple map")
st.map(locations)

#%% Convert to H3 geohash
def to_hex(drow):
    return h3.geo_to_h3(drow['lat'], drow['lon'], 2)

locations['h3_hash'] = locations.apply(to_hex, axis=1)
hex_loc = locations.groupby('h3_hash').size().reset_index(name='count')
# hex_loc

#%%
st.write("### Hexagonal map")
hex_layer = pdk.Layer(
    "H3HexagonLayer",
    hex_loc,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    get_hexagon="h3_hash",
    get_fill_color="[count, 100, 255-count]",
)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v10',
    initial_view_state=pdk.ViewState(
        latitude=0.0,
        longitude=0.0,
        zoom=0,
    ),
    layers=[
        hex_layer
    ],
    tooltip={"text": "Count: {count}"}
))
