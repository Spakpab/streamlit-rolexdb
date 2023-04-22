import pandas as pd
import plotly.express as px
import streamlit as st 

## Set page config ## 

st.set_page_config(
    page_title = "Rolex Index",
    page_icon  = ":bar_chart:"
)

## Get df fact ## 

#df_fact = pd.read_csv("Info_df.csv", index_col=False)

g_sheet_id = '1s-2ZVXJeMbyAT0SP7VIqlm5tODnD72zWQyS5oRE4Doo'
gsheet_url_fact = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet=Info_df".format(g_sheet_id)
df_fact  = pd.read_csv(gsheet_url_fact)

## Get df price ##

#df_price = pd.read_csv("Price_df.csv",index_col=False)

gsheet_url_price = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet=Price_df".format(g_sheet_id)
df_price  = pd.read_csv(gsheet_url_price)


## Create a Hot Model list ## 
gsheet_url_hotlist = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet=Retail_price".format(g_sheet_id)
df_hotlist  = pd.read_csv(gsheet_url_hotlist)
hotlist = df_hotlist[df_hotlist["Brand"] == "Rolex"]["Model"].unique()

## Create a chart from this model ## 

df_filtered = df_price[df_price["Model"].isin(hotlist)]
## Filter out old year ## (Get 2010 onward) ##
df_filtered = df_filtered[df_filtered["Year of production"] >= 2010]

df_avg_price = df_filtered.groupby(["Year of production"])["avg_price_USD"].mean().reset_index()


## Plot ## 

fig = px.line(df_avg_price, x="Year of production", y="avg_price_USD",title=f"Rolex Index",markers=True)

fig.update_layout(
yaxis_title = "USD",
legend=dict(traceorder='reversed')
)
fig = fig.update_layout(showlegend=True)
st.plotly_chart(fig)

## Create YoY comparison ## 
df_avg_price["YoY % Diff"] = df_avg_price["avg_price_USD"].pct_change(periods=1).mul(100).round(2)
st.table(df_avg_price)




