import pandas as pd
import plotly.express as px
import streamlit as st

## Set page config ## 

st.set_page_config(initial_sidebar_state="collapsed", page_title="Rolex Index", page_icon=":smiley:")

st.write("Rolex Index")

## Get df fact ## 

g_sheet_id = '1s-2ZVXJeMbyAT0SP7VIqlm5tODnD72zWQyS5oRE4Doo'
gsheet_url_fact = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet=Info_df".format(g_sheet_id)
df_fact = pd.read_csv(gsheet_url_fact)

## Get df price ##

gsheet_url_price = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet=Price_df".format(g_sheet_id)
df_price = pd.read_csv(gsheet_url_price)


## Create a Hot Model list ## 
gsheet_url_hotlist = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet=Retail_price".format(g_sheet_id)
df_hotlist = pd.read_csv(gsheet_url_hotlist)
hotlist = df_hotlist[df_hotlist["Brand"] == "Rolex"]["Model"].unique()

## Create a chart from this model ## 

df_filtered = df_price[df_price["Model"].isin(hotlist)]
## Filter out old year ## (Get 2010 onward) ##
df_filtered = df_filtered[df_filtered["Year of production"] >= 2010]

df_avg_price = df_filtered.groupby(["Year of production"])["avg_price_USD"].mean().reset_index()

## Plot ## 

fig = px.line(df_avg_price, x="Year of production", y="avg_price_USD",markers=True)

fig.update_layout(
    yaxis_title="USD",
    legend=dict(traceorder='reversed')
)
fig.update_traces(line_color='orange')
fig = fig.update_layout(showlegend=True)

## Plot chart ##
st.plotly_chart(fig, use_container_width=True)

## Create YoY comparison ## 
df_avg_price["YoY % Diff"] = df_avg_price["avg_price_USD"].pct_change(periods=1).mul(100).round(2)

## Rename columns ## 
df_avg_price = df_avg_price.rename(columns={"Year of production": "Year", "avg_price_USD": "Index Price", "YoY % Diff": "YoY %"})

# Convert 'YoY' column to numeric
df_avg_price['YoY %'] = pd.to_numeric(df_avg_price['YoY %'], errors='coerce')

## Pivot the table so that the first row becomes column names and the next row becomes the values
df_avg_price = df_avg_price.set_index('Year').transpose()

## Add year to top left of dataframe
df_avg_price.index.name = 'Year'
df_avg_price.reset_index(inplace=True)
df_avg_price.set_index('Year', inplace=True)

# Style the 'YoY %' column based on its values
def color_negative_red(val):
    color = 'red' if val < 0 else 'green'
    return 'color: %s' % color

# Apply color function #
df_avg_price_styled = df_avg_price.style.apply(lambda col: [color_negative_red(val) if col.name == 'YoY %' and val != '' else '' for val in col], axis=1)

## Plot dataframe ##
st.dataframe(df_avg_price_styled.set_properties(**{'font-weight': 'bold'}))
