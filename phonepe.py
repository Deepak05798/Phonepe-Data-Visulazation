import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image
import urllib
import requests

# Setting up page configuration
icon = Image.open("C:/Users/deepa/OneDrive/Desktop/download.jpeg")
st.set_page_config(
    page_title="Phonepe Pulse Data Visualization | By Deepak Harikrishnan",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': """# This dashboard app is created by Deepak Harikrishnan
                            Data has been cloned from Phonepe Pulse Github Repo"""})

st.sidebar.header(":violet[**Hi! Welcome to the dashboard phonepe pulse**]")

# Creating connection with MySQL workbench
mydb = sql.connect(host="127.0.0.1",
                   user="root",
                   password="12345",
                   database="phonepe")
mycursor = mydb.cursor(buffered=True)

# Creating option menu in the sidebar
with st.sidebar:
    selected = option_menu("Menu", ["Home", "Top Charts", "Explore Data","About"],
                           icons=["house", "graph-up-arrow", "bar-chart-line","exclamation-circle"],
                           menu_icon="menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                                   "nav-link-selected": {"background-color": "#6F36AD"}})

# MENU 1 - HOME
if selected == "Home":
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app, you can visualize the phonepe pulse data and gain lots of insights on transactions, the number of users, top 10 state, district, pincode, and which brand has the most number of users, and so on. Bar charts, Pie charts, and Geo map visualizations are used to get some insights.")

# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1, col2 = st.columns([1, 1.5], gap="large")
    with col1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)

    with col2:
        st.info(
            """
            #### From this menu we can get insights like :
            - Overall ranking on a particular Year and Quarter.
            - Top 10 State, District, Pincode based on Total number of transactions and Total amount spent on phonepe.
            - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
            - Top 10 mobile brands and its percentage based on how many people use phonepe.
            """, icon="🔍"
        )

    # Top Charts - TRANSACTIONS
    if Type == "Transactions":
        col1, col2, col3 = st.columns([1, 1, 1], gap="small")

        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from aggregated_transaction where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                         names='State',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_transaction where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                         names='District',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_transaction where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    # Top Charts - USERS
    if Type == "Users":
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2], gap="small")

        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2, 3, 4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                mycursor.execute(
                    f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from aggregated_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users', 'Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(
                f"select district, sum(RegisteredUser) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users', 'Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(
                f"select Pincode, sum(RegisterdUser) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col4:
            st.markdown("### :violet[State]")
            mycursor.execute(
                f"select state, sum(RegisteredUser) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                         names='State',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Appopens'],
                         labels={'Total_Appopens': 'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

# MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1, col2 = st.columns(2)
    
# EXPLORE DATA - TRANSACTIONS

    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select state, sum(count) as Total_Transaction, sum(amount) as Total_amount from map_transaction where year = {Year} and quarter = {Quarter} group by state order by state")

# Fetch all rows from the query result
            result = mycursor.fetchall()

# Create DataFrame from the result
            df1 = pd.DataFrame(result, columns=['State', 'Total_Transaction', 'Total_amount'])

# Your static data for df2
            df2 = pd.DataFrame({
                 'State': ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Jammu & Kashmir', 'Ladakh', 'Andaman & Nicobar Islands'],
                  })

# Merge df1 and df2 on the 'State' column
            df1['State'] = df1['State'].str.replace('-', ' ').str.title()

# Merge df1 and df2 on the standardized 'State' column
            merged_df = pd.merge(df2, df1, on='State', how='left')

# Convert data types if needed
            merged_df['Total_amount'] = merged_df['Total_amount'].astype(float)
            with urllib.request.urlopen("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson") as response:
             geojson_data = json.load(response)
             first_feature_properties = geojson_data['features'][0]['properties']
# Create choropleth map
             fig = px.choropleth_mapbox(
                 merged_df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey="properties.ST_NM",  
                locations="State",
                color="Total_amount",
                hover_name="State",
                color_continuous_scale="sunset",
                mapbox_style="carto-positron",
                center={"lat": 20.5937, "lon": 78.9629},
                zoom=4
            )
# Adjust the height and width of the map
            fig.update_layout(
            mapbox=dict(center={"lat": 19.5937, "lon": 80.9629}, zoom=2.5),
            height=500,  # Adjust the height as needed
            width=800    # Adjust the width as needed
        )

# Display the map using Streamlit
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(margin={"r":30,"t":20,"l":50,"b":100})
            st.plotly_chart(fig,use_container_width=True)



# Overall State Data - TRANSACTIONS COUNT - INDIA MAP 
        with col2:         
           st.markdown("## :violet[Overall State Data - Transactions Count]")
           mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_transaction where year = {Year} and quarter = {Quarter} group by state order by state")
           # Fetch all rows from the query result
           result = mycursor.fetchall()

# Create DataFrame from the result
           df1 = pd.DataFrame(result, columns=['State', 'Total_Transaction', 'Total_amount'])

# Your static data for df2
           df2 = pd.DataFrame({
          'State': ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Jammu & Kashmir', 'Ladakh', 'Andaman & Nicobar Islands'],
        })

# Merge df1 and df2 on the 'State' column
           df1['State'] = df1['State'].str.replace('-', ' ').str.title()

# Merge df1 and df2 on the standardized 'State' column
           merged_df = pd.merge(df2, df1, on='State', how='left')
# Convert data types if needed
           merged_df['Total_Transaction'] = merged_df['Total_Transaction'].astype(float)
           with urllib.request.urlopen("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson") as response:
            geojson_data = json.load(response)
            first_feature_properties = geojson_data['features'][0]['properties']
# Create choropleth map
            fig = px.choropleth_mapbox(
               merged_df,
               geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
               featureidkey="properties.ST_NM",  
               locations="State",
               color="Total_Transaction",
               hover_name="State",
               color_continuous_scale="sunset",
               mapbox_style="carto-positron",
               center={"lat": 20.5937, "lon": 78.9629},
               zoom=4
            )
# Adjust the height and width of the map
            fig.update_layout(
            mapbox=dict(center={"lat": 19.5937, "lon": 80.9629}, zoom=2.5),
            height=500,  # Adjust the height as needed
            width=800    # Adjust the width as needed
        )

# Display the map using Streamlit
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(margin={"r":30,"t":20,"l":50,"b":100})
            st.plotly_chart(fig,use_container_width=True)



# BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from aggregated_transaction where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)
        
# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        mycursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_transaction where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)



    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        mycursor.execute(f"select state, sum(RegisteredUser) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
        result = mycursor.fetchall()

# Create DataFrame from the result
        df1 = pd.DataFrame(result, columns=['State', 'Total_Users', 'Total_Appopens'])

# Your static data for df2
        df2 = pd.DataFrame({
           'State': ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Jammu & Kashmir', 'Ladakh', 'Andaman & Nicobar Islands'],
          })

# Merge df1 and df2 on the 'State' column
        df1['State'] = df1['State'].str.replace('-', ' ').str.title()

# Merge df1 and df2 on the standardized 'State' column
        merged_df = pd.merge(df2, df1, on='State', how='left')
# Convert data types if needed
        merged_df['Total_Appopens'] = merged_df['Total_Appopens'].astype(float)
        with urllib.request.urlopen("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson") as response:
         geojson_data = json.load(response)
         first_feature_properties = geojson_data['features'][0]['properties']
# Create choropleth map
         fig = px.choropleth_mapbox(
            merged_df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey="properties.ST_NM",  
            locations="State",
            color="Total_Appopens",
            hover_name="State",
            title="India Map - Appoppens Frequency",
            color_continuous_scale="sunset",
            mapbox_style="carto-positron",
            center={"lat": 20.5937, "lon": 78.9629},
            zoom=4
        )
# Adjust the height and width of the map
         fig.update_layout(
         mapbox=dict(center={"lat": 20.5937, "lon": 78.9629}, zoom=3),
         height=500,  # Adjust the height as needed
         width=800    # Adjust the width as needed
    )

         fig.update_geos(fitbounds="locations", visible=False)
         fig.update_layout(margin={"r":50,"t":20,"l":50,"b":20})
         st.plotly_chart(fig,use_container_width=True)

 # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
         st.markdown("## :violet[Select any State to explore more]")
         selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        mycursor.execute(f"select State,year,quarter,District,sum(RegisteredUser) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)       


# MENU 4 - ABOUT
if selected == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        