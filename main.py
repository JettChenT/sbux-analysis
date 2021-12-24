#%%
import requests
import pandas as pd
import requests
import streamlit as st
import pydeck as pdk
import h3
import plotly.express as px
import plotly.graph_objects as go
#%%
st.title("Starbucks!")
st.write("## The financial report (data was gathered from [FAPI](https://site.financialmodelingprep.com/financial-statements/SBUX))")
data = pd.read_csv('./finance_data.csv')
data.set_index('calendarYear')
data = data.iloc[::-1]

st.write(data)
def bplot(col, desc=''):
    return px.bar(data, x='calendarYear', y=col, color=col, color_continuous_scale=px.colors.sequential.Blugrn, title=desc if desc else col)

for col,dsc in zip(['revenue', 'netIncome', 'grossProfit'], ['Starbucks Revenue By Year','Net Income By Year', 'Gross Profit By Year']):
    st.plotly_chart(bplot(col, dsc))

# year = st.selectbox('Year number: ', [2021])
year = 2021

rr = 'relative'
tt = 'total'

# st.write(year)

fig = go.Figure(
    go.Waterfall(
        name = '20' , orientation='v',
        measure = [rr,rr,rr,tt,rr,rr,tt,rr,tt],
        y=[18.32*1e9, 5.05*1e9, 5.69*1e9,None, data['interestIncome'][0], -data['costAndExpenses'][0], None, -data['incomeTaxExpense'][0], None],
        # y=[10,-2,8],
        x=['Beverage revenues', 'Food revenues', 'Other revenues', 'Gross revenue', 'Interest income', 'Costs & Expenses', 'Income before tax', 'tax', 'net income']
    )
)


fig.update_layout(
    title = f"Starbucks financial statement waterfall chart: year {year}",
    showlegend = True
)
st.write(fig)

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
