import pandas as pd
import plotly.express as px
import streamlit as st 

## Set page config ## 

st.set_page_config(
    page_title = "Dashboard v1",
    page_icon  = ":bar_chart:",
    layout = "wide"
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

## Create side bar ## 

st.sidebar.header("Please Filter here:")

## Filter by brand ## 
brand_list = df_fact['Brand'].unique()
selected_brand = st.sidebar.selectbox("Select Brand", brand_list)

## Filter by model ## 
model_list = df_fact[df_fact['Brand'] == selected_brand]['Model'].unique()
if len(model_list) == 1:
    selected_model = model_list[0]
else:
    selected_model = st.sidebar.selectbox("Select Model", ["All"] + list(model_list))

## Filter by ref ## 
if selected_model == "All":
    ref_list = df_fact[df_fact['Brand'] == selected_brand]['Ref_no'].unique()
    if len(ref_list) == 1:
        selected_ref_no = ref_list[0]
    else:
        selected_ref_no = st.sidebar.selectbox("Select Reference Number", ["All"] + list(ref_list))
else:
    ref_list = df_fact[(df_fact['Brand'] == selected_brand) & (df_fact['Model'] == selected_model)]['Ref_no'].unique()
    if len(ref_list) == 1:
        selected_ref_no = ref_list[0]
    else:
        selected_ref_no = st.sidebar.selectbox("Select Reference Number", ["All"] + list(ref_list))

## Filter by Dial ## 
if selected_ref_no == "All":
    dial_list = df_fact[df_fact['Brand'] == selected_brand]['Dial'].unique()
    if len(dial_list) == 1:
        selected_dial = dial_list[0]
    else:
        selected_dial = st.sidebar.selectbox("Select Dial", ["All"] + list(dial_list))
else:
    dial_list = df_fact[(df_fact['Brand'] == selected_brand) & (df_fact['Model'] == selected_model) & (df_fact['Ref_no'] == selected_ref_no)]['Dial'].unique()
    if len(dial_list) == 1:
        selected_dial = dial_list[0]
    else:
        selected_dial = st.sidebar.selectbox("Select Dial", ["All"] + list(dial_list))


## If filter not selected show all value, if selected show only selected ## 

if selected_brand and selected_model and selected_ref_no and selected_dial:

    if selected_model == "All" and selected_ref_no == "All" and selected_dial == "All":

        df_filtered = df_fact[df_fact["Brand"] == selected_brand]

        # Plot line chart # 
        df_filtered_price_frsth = df_price[(df_price["Brand"] == selected_brand) & (df_price["Condition"] == "First Hand")]
        df_filtered_price_secth = df_price[(df_price["Brand"] == selected_brand) & (df_price["Condition"] == "Second Hand")]
        df_filtered_price = pd.concat([df_filtered_price_frsth, df_filtered_price_secth])
        df_avg_price = df_filtered_price.groupby(["Year of production", "Condition"])["avg_price_USD"].mean().reset_index()

        fig = px.line(df_avg_price, x="Year of production", y="avg_price_USD", color="Condition" ,title=f"Price trend for All {selected_brand}",markers=True)

        fig.update_layout(
        yaxis_title = "USD",
        legend=dict(traceorder='reversed')
        )
        fig = fig.update_layout(showlegend=True)
        st.plotly_chart(fig)

        # Plot table # 
        st.write(df_filtered)


    elif selected_ref_no == "All" and selected_dial == "All":
        df_filtered = df_fact[(df_fact["Brand"] == selected_brand) & (df_fact["Model"] == selected_model)]

        # Plot line chart # 
        df_filtered_price_frsth = df_price[(df_price["Brand"] == selected_brand) & (df_price["Model"] == selected_model) & (df_price["Condition"] == "First Hand")]
        df_filtered_price_secth = df_price[(df_price["Brand"] == selected_brand) & (df_price["Model"] == selected_model) & (df_price["Condition"] == "Second Hand")]
        
        df_filtered_price = pd.concat([df_filtered_price_frsth, df_filtered_price_secth])
        df_avg_price = df_filtered_price.groupby(["Year of production", "Condition"])["avg_price_USD"].mean().reset_index()

        fig = px.line(df_avg_price, x="Year of production", y="avg_price_USD",color = "Condition",title=f"Price trend for All {selected_brand} {selected_model}",markers=True)

        fig.update_layout(
        yaxis_title = "USD",
        legend=dict(traceorder='reversed')
        )
        fig = fig.update_layout(showlegend=True)
        st.plotly_chart(fig)

        # Plot table # 
        st.write(df_filtered)

    elif selected_model == "All" and selected_ref_no == "All":
        df_filtered = df_fact[(df_fact["Brand"] == selected_brand) & (df_fact["Dial"] == selected_dial)]

        # Plot line chart # 
        df_filtered_price_frsth = df_price[(df_price["Brand"] == selected_brand) & (df_price["Dial"] == selected_dial) & (df_price["Condition"] == "First Hand")]
        df_filtered_price_secth = df_price[(df_price["Brand"] == selected_brand) & (df_price["Dial"] == selected_dial) & (df_price["Condition"] == "Second Hand")]

        df_filtered_price = pd.concat([df_filtered_price_frsth, df_filtered_price_secth])
        df_avg_price = df_filtered_price.groupby(["Year of production", "Condition"])["avg_price_USD"].mean().reset_index()

        fig = px.line(df_avg_price, x="Year of production", y="avg_price_USD",color = "Condition",title=f"Price trend for All {selected_brand} {selected_model}",markers=True)

        fig.update_layout(
        yaxis_title = "USD",
        legend=dict(traceorder='reversed')
        )
        fig = fig.update_layout(showlegend=True)
        st.plotly_chart(fig)

        # Plot table # 
        st.write(df_filtered)


    elif selected_model == "All" and selected_dial == "All":
        df_filtered = df_fact[(df_fact["Brand"] == selected_brand) & (df_fact["Ref_no"] == selected_ref_no)]

        # Plot line chart # 
        df_filtered_price_frsth = df_price[(df_price["Brand"] == selected_brand) & (df_price["Reference number"] == selected_ref_no) & (df_price["Condition"] == "First Hand")]
        df_filtered_price_secth = df_price[(df_price["Brand"] == selected_brand) & (df_price["Reference number"] == selected_ref_no) & (df_price["Condition"] == "Second Hand")]

        df_filtered_price = pd.concat([df_filtered_price_frsth, df_filtered_price_secth])
        df_avg_price = df_filtered_price.groupby(["Year of production", "Condition"])["avg_price_USD"].mean().reset_index()

        fig = px.line(df_avg_price, x="Year of production", y="avg_price_USD",color = "Condition",title=f"Price trend for All {selected_brand} {selected_model}",markers=True)

        fig.update_layout(
        yaxis_title = "USD",
        legend=dict(traceorder='reversed')
        )
        fig = fig.update_layout(showlegend=True)
        st.plotly_chart(fig)

        # Plot table # 
        st.write(df_filtered)


    elif selected_model == "All":
        df_filtered = df_fact[(df_fact["Brand"] == selected_brand) & (df_fact["Ref_no"] == selected_ref_no) & (df_fact["Dial"] == selected_dial)]

        # Plot line chart # 
        df_filtered_price_frsth = df_price[(df_price["Brand"] == selected_brand) & (df_price["Reference number"] == selected_ref_no) & (df_price["Dial"] == selected_dial) & (df_price["Condition"] == "First Hand")]
        df_filtered_price_secth = df_price[(df_price["Brand"] == selected_brand) & (df_price["Reference number"] == selected_ref_no) & (df_price["Dial"] == selected_dial) & (df_price["Condition"] == "Second Hand")]
        
        df_filtered_price = pd.concat([df_filtered_price_frsth, df_filtered_price_secth])
        df_avg_price = df_filtered_price.groupby(["Year of production", "Condition"])["avg_price_USD"].mean().reset_index()

        fig = px.line(df_avg_price, x="Year of production", y="avg_price_USD",color = "Condition",title=f"Price trend for All {selected_brand} {selected_ref_no} {selected_dial}",markers=True)

        fig.update_layout(
        yaxis_title = "USD",
        legend=dict(traceorder='reversed')
        )
        fig = fig.update_layout(showlegend=True)
        st.plotly_chart(fig)

        # Plot table # 
        st.write(df_filtered)

        
    elif selected_ref_no == "All":
        df_filtered = df_fact[(df_fact["Brand"] == selected_brand) & (df_fact["Model"] == selected_model) & (df_fact["Dial"] == selected_dial)]

        # Plot line chart # 
        df_filtered_price_frsth = df_price[(df_price["Brand"] == selected_brand) & (df_price["Model"] == selected_model) & (df_price["Dial"] == selected_dial) & (df_price["Condition"] == "First Hand")]
        df_filtered_price_secth = df_price[(df_price["Brand"] == selected_brand) & (df_price["Model"] == selected_model) & (df_price["Dial"] == selected_dial) & (df_price["Condition"] == "Second Hand")]

        df_filtered_price = pd.concat([df_filtered_price_frsth, df_filtered_price_secth])
        df_avg_price = df_filtered_price.groupby(["Year of production", "Condition"])["avg_price_USD"].mean().reset_index()

        fig = px.line(df_avg_price, x="Year of production", y="avg_price_USD",color = "Condition" ,title=f"Price trend for All {selected_brand} {selected_model} {selected_dial}",markers=True)

        fig.update_layout(
        yaxis_title = "USD",
        legend=dict(traceorder='reversed')
        )
        fig = fig.update_layout(showlegend=True)
        st.plotly_chart(fig)

        # Plot table # 
        st.write(df_filtered)


    elif selected_dial == "All":
        df_filtered = df_fact[(df_fact["Brand"] == selected_brand) & (df_fact["Model"] == selected_model) & (df_fact["Ref_no"] == selected_ref_no)]

        # Plot line chart # 
        df_filtered_price_frsth = df_price[(df_price["Brand"] == selected_brand) & (df_price["Model"] == selected_model) & (df_price["Reference number"] == selected_ref_no) & (df_price["Condition"] == "First Hand")]
        df_filtered_price_secth = df_price[(df_price["Brand"] == selected_brand) & (df_price["Model"] == selected_model) & (df_price["Reference number"] == selected_ref_no) & (df_price["Condition"] == "Second Hand")]
        
        df_filtered_price = pd.concat([df_filtered_price_frsth, df_filtered_price_secth])
        df_avg_price = df_filtered_price.groupby(["Year of production", "Condition"])["avg_price_USD"].mean().reset_index()

        fig = px.line(df_avg_price, x="Year of production", y="avg_price_USD",color = "Condition",title=f"Price trend for All {selected_brand} {selected_model} {selected_ref_no}",markers=True)
        
        fig.update_layout(
        yaxis_title = "USD",
        legend=dict(traceorder='reversed')
        )
        fig = fig.update_layout(showlegend=True)
        st.plotly_chart(fig)

        # Plot table # 
        st.write(df_filtered)

    else:

        df_filtered = df_fact[(df_fact["Brand"] == selected_brand) & (df_fact["Model"] == selected_model) & (df_fact["Ref_no"] == selected_ref_no) & (df_fact["Dial"] == selected_dial) ]

        # Plot line chart # 
        df_filtered_price_frsth = df_price[(df_price["Brand"] == selected_brand) & (df_price["Model"] == selected_model) & (df_price["Reference number"] == selected_ref_no)& (df_price["Dial"] == selected_dial) & (df_price["Condition"] == "First Hand")]
        df_filtered_price_secth = df_price[(df_price["Brand"] == selected_brand) & (df_price["Model"] == selected_model) & (df_price["Reference number"] == selected_ref_no)& (df_price["Dial"] == selected_dial) & (df_price["Condition"] == "Second Hand")]
        
        df_filtered_price = pd.concat([df_filtered_price_frsth, df_filtered_price_secth])
        df_avg_price = df_filtered_price.groupby(["Year of production", "Condition"])["avg_price_USD"].mean().reset_index()

        fig = px.line(df_avg_price, x="Year of production", y="avg_price_USD", title=f"Price trend for All {selected_brand} {selected_model} {selected_ref_no} {selected_dial}",markers=True)

        fig.update_layout(
        yaxis_title = "USD",
        legend=dict(traceorder='reversed')
        )
        fig = fig.update_layout(showlegend=True)
        st.plotly_chart(fig)

        # Plot table # 
        st.write(df_filtered)

else:

    if selected_model == "All":
        st.write(df_fact[df_fact["Brand"] == selected_brand])

    elif selected_ref_no == "All":
        st.write(df_fact[(df_fact["Brand"] == selected_brand) & (df_fact["Model"] == selected_model)])

    else:
        st.write(df_fact[(df_fact["Brand"] == selected_brand) & (df_fact["Model"] == selected_model) & (df_fact["Ref_no"] == selected_ref_no)])



        




