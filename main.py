# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from streamlit_lottie import st_lottie
import altair as alt
import geopandas as gpd
from PIL import Image
import base64
from random import randrange
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly import offline
from streamlit.components.v1 import html


# Page configuration
st.set_page_config(
    page_title="Indian EV Market Analysis",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded")

# Setting Title
# st.title('🚔 India EV Market Analysis(2001 - 2024) 🚖')
st.markdown(
    "<h1 style='color:#FFA500; text-align:center; text-decoration:underline;'>🚔 India EV Market Analysis (2001 - 2024) 🚖</h1>",
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style='font-size:15px; text-align:justify;'>
         This Analysis and Visualization is the detailed overview of the electric vehicle (EV) market in India from 2001 to 2024. It includes monthly sales data, sales data categorized by manufacturer, and vehicle class-wise sales data for different manufacturers. This rich dataset is ideal for market analysis, trend forecasting, and research on the adoption and growth of electric vehicles in India.
    </div>
    """,
    unsafe_allow_html=True
)

#st.subheader("Key Performance Indicator (KPI)")
# Subheader with Color
st.write('----')
st.markdown(
    "<h3 style='color:#FF6347;text-align:left; text-decoration:underline;'>Key Performance Indicator (KPI)</h3>",
    unsafe_allow_html=True
)


# Reading DataSet
df= pd.read_csv('ev_sales_by_makers_and_cat_15-24.csv')
df1=pd.read_csv('ev_cat_01-24.csv')
df3= pd.read_csv('OperationalPC.csv')
df4=pd.read_csv('EV Maker by Place.csv')
df5=pd.read_csv('Vehicle Class - All.csv')
df6=pd.read_csv('EV_Maker_with_Location.csv')

df3['State'] = df3['State'].replace("Odisha", "Orissa")
# Creating minidf
yearly_sales = df.iloc[:, 5:-1].sum()
year_df = pd.DataFrame(yearly_sales).reset_index()
year_df.columns = ['Year', 'Total Sales']

### Converting columns type 
df1['Date'] = df1['Date'].astype(str)
#df1['Date'] = df1['Date'].replace('0', pd.NaT)
df1['Date'] = np.where(df1['Date'] == '0', pd.NaT, df1['Date'])
df1['Date'] = pd.to_datetime(df1['Date'], format='%m/%d/%y', errors='coerce')

# Setting Page Logo
st.sidebar.image("Analytics Aces.png")

#Creating Side Bar
st.sidebar.header("Choose the given Option : ")





# Sidebar Filters
State = st.sidebar.multiselect("Pick the State", df4["State"].unique())
if not State:
    df4_copy = df4.copy()
else:
    df4_copy = df4[df4['State'].isin(State)]

Year = st.sidebar.multiselect("Pick the Year", year_df["Year"].unique())
if not Year:
    year_df1 = year_df.copy()
else:
    year_df1 = year_df[year_df['Year'].isin(Year)]

# Filtered Data
if not State:
    filter_data = df4
else:
    filter_data = df4[df4['State'].isin(State)]

if not Year:
    filter_Year = year_df
else:
    filter_Year = year_df[year_df['Year'].isin(Year)]

# Aggregation for KPIs
total_companies = len(filter_data['EV Maker'].unique())
total_states = len(filter_data['State'].unique())
total_sales = filter_Year['Total Sales'].sum()


top_state = filter_data['State'].value_counts().idxmax()
top_state_count = filter_data['State'].value_counts().max()

fd1 = filter_data['State'].value_counts().reset_index()
fd1.columns = ['State', 'Number of Company']

# KPI Display
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)


with kpi_col1:
    st.metric("Total EV Companies", total_companies)

with kpi_col2:
    st.metric("Total States Represented", total_states)

with kpi_col3:
    st.metric("Total EV Sales", total_sales)

kpi_col4, kpi_col5 = st.columns(2)

with kpi_col4:
    st.metric("Top State", top_state)

with kpi_col5:
    st.metric("Companies in Top State", top_state_count)

st.write('----')

# Visualizations
col1, col2 = st.columns((2))
st.write('----')
with col1:
    st.markdown(
    "<h3 style='color:#FF7F50; text-align:center; text-decoration:underline;'>Total EV Sales By Year</h3>",
    unsafe_allow_html=True
)

    fig = px.bar(filter_Year, x='Year', y='Total Sales', template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200, width=50)
    st.markdown(
    """
    <div style='font-size:15px;'>
        Summary:
         This chart shows the trend of total EV sales over the years, helping to understand if EV sales are increasing or decreasing over time.
    </div>
    """,
    unsafe_allow_html=True
)

with col2:
    st.markdown(
    "<h3 style='color:#FF7F50; text-align:center; text-decoration:underline;'>EV Company State Wise</h3>",
    unsafe_allow_html=True
)

    fig = px.pie(fd1, values="Number of Company", names="State", hole=0.5)
    fig.update_traces(text=fd1["State"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
    """
    <div style='font-size:15px;'>
        Summary:
         The pie chart displays the number of EV companies in different states, highlighting which states have the highest concentration of EV companies.
    </div>
    """,
    unsafe_allow_html=True
)

# Add line breaks
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)





# Clean column names by stripping any leading or trailing spaces
df.columns = df.columns.str.strip()

# Calculate the growth
df['Growth'] = ((df['2024'] - df['2015']) / df['2015']).replace([float('inf'), -float('inf')], 0) * 100

# Sorting top manufacturers by growth
top_manufacturers_growth = df[['Maker', 'Growth']].sort_values(by='Growth', ascending=False).head(10)

# Aggregating sales by category
category_sales = df.groupby('Cat').sum().loc[:, '2015':'2024']

# Reshaping the category sales for plotting
category_sales_long = category_sales.reset_index().melt(id_vars='Cat', var_name='Year', value_name='Total Sales')

# Summing total sales per category
cat = category_sales_long.groupby('Cat')['Total Sales'].sum().reset_index()
cat.columns = ['Car Category', 'Total Sales']

# Using Streamlit columns for the layout
chart1, chart2 = st.columns(2)

with chart1:
    st.markdown(
    "<h3 style='color:#6495ED; text-align:center; text-decoration:underline;'>Top 10 EV Manufacturers by Growth</h3>",
    unsafe_allow_html=True
)

    fig = px.bar(top_manufacturers_growth, x = 'Growth', y = 'Maker', 
                 color_discrete_sequence=['#4bf465'])
    fig.update_yaxes(autorange='reversed')
    st.plotly_chart(fig,use_container_width=True, height = 200)
    st.markdown(
    """
    <div style='font-size:15px;'>
        Summary:
         Top 5 EV Manufacturers by Growth: Shows the fastest-growing EV manufacturers based on recent sales growth.
    </div>
    """,
    unsafe_allow_html=True
)

with chart2:
    st.markdown(
    "<h3 style='color:#6495ED; text-align:center; text-decoration:underline;'>Category-wise Sales</h3>",
    unsafe_allow_html=True
)

    fig = px.bar(cat, 
                 x='Total Sales', 
                 y='Car Category', 
                 orientation='h',  # Horizontal orientation
                 color_discrete_sequence=['#4bf465'])  # Keep the color consistent
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
    """
    <div style='font-size:15px;'>
        Summary:
         Category-wise Sales: Displays the distribution of EV sales across different car categories, highlighting which types of EVs are most popular.
    </div>
    """,
    unsafe_allow_html=True
)
st.write('----')







# Filtering recent sales data and calculating total sales
recent_sales = df[['Maker', '2021', '2022', '2023', '2024']]
recent_sales['Total Recent Sales'] = recent_sales[['2021', '2022', '2023', '2024']].sum(axis=1)
emerging_companies_sorted = recent_sales[['Maker', 'Total Recent Sales']].sort_values(by='Total Recent Sales', ascending=False).head(10)

# Streamlit UI
st.markdown("<br>", unsafe_allow_html=True)

coll1, coll2 = st.columns((2))
# User Input to Select a Maker

with coll1:
    st.markdown(
    "<h3 style='color:#FF7F50; text-align:center; text-decoration:underline;'>Top 10 EV Manufacturers by Sales</h3>",
    unsafe_allow_html=True
)


with coll2:
    selected_maker = st.selectbox("Select a Maker to View Sales History", emerging_companies_sorted['Maker'])



# Filter Data for the Selected Maker
maker_history = df[df['Maker'] == selected_maker]
maker_history.drop(columns=['Cat', 'Growth'], inplace=True)
maker_history_sum = maker_history.iloc[:, 1:-1].sum()
year_df_maker = pd.DataFrame(maker_history_sum).reset_index()
year_df_maker.columns = ['Years', 'Total Sales']



cl5, cl6 = st.columns((2))
# with cl5:
# # Bar Chart
#     fig_bar = px.bar(emerging_companies_sorted, x='Total Recent Sales', y='Maker',
#                  color_continuous_scale='dense', labels={'Maker': 'Company', 'Total Recent Sales': 'Sales'})
#     fig_bar.update_yaxes(autorange='reversed')
#     st.plotly_chart(fig_bar, use_container_width=True)
with cl5:
    fig_bar = px.bar(
        emerging_companies_sorted, 
        x='Total Recent Sales', 
        y='Maker', 
        color='Total Recent Sales',  # Add color based on Total Recent Sales
        color_continuous_scale='rainbow',  # Vibrant color palette
        labels={'Maker': 'Company', 'Total Recent Sales': 'Sales'}
    )
    fig_bar.update_yaxes(autorange='reversed')  # Reverse y-axis for better visibility
    fig_bar.update_layout(
    title="Top 10 EV Manufacturers by Sales",  # Underlines the title
    xaxis_title="Total Recent Sales",
    yaxis_title="Company",
    coloraxis_colorbar=dict(
        title="Sales",  # Label for the color bar
        tickformat=".0f",  # Format ticks as integers
    )
)
    
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown(
    """
    <div style='font-size:15px;'>
        Summary:
         This chart identifies the top emerging EV companies by their recent sales performance, highlighting the most successful new players in the market.
    </div>
    """,
    unsafe_allow_html=True
)

with cl6:
# Line Chart for the Selected Maker
    st.markdown(
    f"<h3 style='color:#FF7F50; text-align:center; text-decoration:underline;'>{selected_maker}'s Sales History</h3>",
    unsafe_allow_html=True
)

    fig_line = px.line(year_df_maker, x='Years', y='Total Sales')
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown(
    """
    <div style='font-size:15px;'>
        Summary:
         CThe line chart visualizes the sales history of the selected maker over the years, showing Years on the x-axis and Total Sales on the y-axis. It highlights trends in sales performance, such as growth, decline, or consistency, and provides an interactive experience for detailed insights.
    </div>
    """,
    unsafe_allow_html=True
)

st.write('----')
       


# Preprocess the data
df5['Total Registration'] = df5['Total Registration'].str.replace(',', '').astype(int)
vehicle_summary = df5[['Vehicle Class', 'Total Registration']].copy().sort_values(by='Total Registration')
vehicle_summary.columns = ['Vehicle Class', 'Total Registration']
#vehicle_summary.sort_values(by='Total Registration',ascending=False)

st.markdown("<br>", unsafe_allow_html=True)  # Adds a line break
st.markdown("<br>", unsafe_allow_html=True)  # Adds a line break

#cl7, cl8 = st.columns((2))
# with cl7:
#     # Generate the bar chart for the top 10 vehicle classes
#     top_5_classes = vehicle_summary.sort_values(by='Total Sales', ascending=False).head(5)
#     fig_top_5 = px.bar(top_5_classes, x='Total Sales', y='Vehicle Class', orientation='h',
#                     color_discrete_sequence=['#f4a24b'], title="Top 5 Vehicle Classes by Total Sales")
#     st.plotly_chart(fig_top_5,use_container_width=True, height = 250)

#with cl8:
    # Generate the bar chart for all vehicle classes
st.markdown(
    "<h3 style='color:#FF7F50; text-align:center; text-decoration:underline;'>Vehicle Class Registration Summary</h3>",
    unsafe_allow_html=True
)

fig_bar = px.bar(vehicle_summary, x='Total Registration', y='Vehicle Class', orientation='h',
                    color_discrete_sequence=['#ec4f37'], title="Vehicle Class Registration Summary")
fig_bar.update_layout(yaxis=dict(autorange="reversed"))
st.plotly_chart(fig_bar,use_container_width=True, height = 250)
st.markdown(
    """
    <div style='font-size:15px;'>
        Summary:
         the bar chart provides a clear, comparative view of how vehicle registrations are distributed across various classes, assisting stakeholders in making data-driven decisions.
    </div>
    """,
    unsafe_allow_html=True
)

st.write('----')



    

# Vehicle Data Heatmap

st.markdown("<br>", unsafe_allow_html=True)  # Adds a line break

st.markdown(
    "<h3 style='color:#FF7F50; text-align:center; text-decoration:underline;'>Vehicle Data Heatmap</h3>",
    unsafe_allow_html=True
)

coll1, coll2 = st.columns((2))
# Getting the min and max date 
startDate = pd.to_datetime(df1["Date"]).min()
#startDate = max(pd.to_datetime("2020-01-01"), df1["Date"].min())
endDate = pd.to_datetime(df1["Date"]).max()

# Making StartDate and end date columns
with coll1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with coll2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df1= df1[(df1['Date'] >= date1) & (df1['Date'] <= date2)].copy()      

# Melt the dataframe (already done)
df_melted = df1.melt(id_vars=["Date"], var_name="Vehicle Type", value_name="Count")

# Pivot the dataframe to make it suitable for 3D plotting
df_pivoted = df1.set_index("Date").T

# Create the 3D plot
fig = go.Figure(data=[go.Surface(
    z=df_pivoted.values,  # Values for the 3D surface
    x=df_pivoted.columns,  # Date values (X-axis)
    y=df_pivoted.index,  # Vehicle types (Y-axis)
    colorbar=dict(title="Count"),  # Color scale
    colorscale="Turbo"  # Color scale
)])

# Updating layout for 3D plot
fig.update_layout(
    title="Vehicle Data 3D Surface Plot",
    template="plotly_dark",
    scene=dict(
        xaxis_title="Date",
        yaxis_title="Vehicle Type",
        zaxis_title="Count",
        xaxis=dict(titlefont=dict(size=12)),  # Font size for x-axis
        yaxis=dict(titlefont=dict(size=12)),  # Font size for y-axis
        zaxis=dict(titlefont=dict(size=12)),  # Font size for z-axis
    ),
    height=700,  # Adjust the height of the graph
    width=1500,  # Adjust the width of the graph
    margin=dict(l=50, r=50, t=100, b=50)  # Adjust margins for better label spacing
)

# Show the plot using Streamlit
st.plotly_chart(fig)
st.markdown(
    """
    <div style='font-size:15px;'>
        Summary:
         This  allows users to select a date range using an interactive interface, dynamically filters the vehicle data based on the selected range, and prepares it for visualization in a heatmap to analyze time-based trends or patterns.
    </div>
    """,
    unsafe_allow_html=True
)
st.write('----')



# # Vehicle Data Heatmap
# st.markdown("<br>", unsafe_allow_html=True)  # Adds a line break
# st.markdown("<br>", unsafe_allow_html=True)  # Adds a line break

# st.markdown("<h3 style='text-align: center;'>Vehicle Data 3D Heatmap</h3>", unsafe_allow_html=True)
# st.markdown("<br>", unsafe_allow_html=True)  # Adds a line break

# coll1, coll2 = st.columns((2))
# # Getting the min and max date 
# startDate = max(pd.to_datetime("2020-01-01"), df1["Date"].min())
# endDate = pd.to_datetime(df1["Date"].max())

# # Making StartDate and end date columns
# with coll1:
#     date1 = pd.to_datetime(st.date_input("Start Date", startDate))

# with coll2:
#     date2 = pd.to_datetime(st.date_input("End Date", endDate))

# df1 = df1[(df1['Date'] >= date1) & (df1['Date'] <= date2)].copy()      

# # Preparing data for 3D Heatmap
# df_melted = df1.melt(id_vars=["Date"], var_name="Vehicle Type", value_name="Count")

# fig = go.Figure()

# # Adding traces for 3D representation
# for vehicle in df_melted["Vehicle Type"].unique():
#     vehicle_data = df_melted[df_melted["Vehicle Type"] == vehicle]
#     fig.add_trace(go.Surface(
#         z=[vehicle_data["Count"].values],
#         x=[vehicle_data["Date"].astype(str).values],
#         y=[vehicle],
#         colorscale='Viridis',  # Updated colorscale for better contrast
#         showscale=True
#     ))

# # Enhancing interactivity and layout
# fig.update_layout(
#     title="3D Heatmap of Vehicle Data",
#     scene=dict(
#         xaxis=dict(title="Date", backgroundcolor="rgb(200, 200, 230)", gridcolor="white", showbackground=True),
#         yaxis=dict(title="Vehicle Type", backgroundcolor="rgb(230, 200, 230)", gridcolor="white", showbackground=True),
#         zaxis=dict(title="Count", backgroundcolor="rgb(230, 230, 200)", gridcolor="white", showbackground=True),
#     ),
#     template="plotly_dark",
#     margin=dict(l=20, r=20, b=20, t=100),
#     width=1200,  # Set graph width
#     height=800   # Set graph height
# )

# st.plotly_chart(fig)





# Filter by state
states = df3['State'].unique()
selected_state = st.selectbox("Select a state to know the No. of PCS", ['All'] + list(states))

if selected_state != 'All':
    filtered_df = df3[df3['State'] == selected_state]
    title = f"Histogram of PCS in {selected_state}"
else:
    filtered_df = df3
    title = "Histogram of PCS by State"



# get some geojson for India.  Reduce somplexity of geomtry to make it more efficient
url = "https://raw.githubusercontent.com/Subhash9325/GeoJson-Data-of-Indian-States/master/Indian_States"
gdf = gpd.read_file(url)
gdf["geometry"] = gdf.to_crs(gdf.estimate_utm_crs()).simplify(1000).to_crs(gdf.crs)
india_states = gdf.rename(columns={"NAME_1": "ST_NM"}).__geo_interface__




# Plot the 3D bar graph
fig = px.bar(
    filtered_df,
    x='State',
    y='No. of Operational PCS',
    title=title,
    labels={'State': 'State', 'No. of Operational PCS': 'No. of Operational PCS'},
    color='State',
    template="seaborn"
)
fig.update_traces(marker=dict(line=dict(width=0.5)))
fig.update_layout(
    scene=dict(
        xaxis_title="State",
        yaxis_title="No. of Operational PCS",
        zaxis_title="Values"
    ),
    margin=dict(l=0, r=0, b=0, t=50),
)

st.plotly_chart(fig, use_container_width=True)
st.markdown(
    """
    <div style='font-size:15px;'>
        Summary:
         This visualization provides a clear understanding of the state-wise distribution of operational PCS, making it easy to identify gaps and opportunities for infrastructure development.
         By selecting a specific state or viewing the overall data, users can compare the density of PCS across different regions.
    </div>
    """,
    unsafe_allow_html=True
)
st.write('----')






cl9, cl10 = st.columns((2))

# ev_makers
# Load Data from CSV
@st.cache_data
def load_data():
    try:
        data =pd.read_csv('EV_Maker_with_Location.csv')
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return pd.DataFrame()  # Returning empty DataFrame if error occurs
    
    # Necessary columns
    required_columns = ['EV Maker', 'Place', 'State', 'Latitude', 'Longitude']
    if not all(col in data.columns for col in required_columns):
        st.error("CSV file must contain columns: EV Maker, Place, State, Latitude, Longitude")
        return pd.DataFrame()  # Returning empty DataFrame if columns are missing
    
    # Converting Latitude and Longitude to numeric
    data['Latitude'] = pd.to_numeric(data['Latitude'], errors='coerce')
    data['Longitude'] = pd.to_numeric(data['Longitude'], errors='coerce')

    # Dropping rows with missing values in Latitude or Longitude
    data = data.dropna(subset=['Latitude', 'Longitude'])
    
    return data

# Main Streamlit App
def main():
    st.markdown("<br>", unsafe_allow_html=True)  # Adds a line break
    st.markdown("<br>", unsafe_allow_html=True)  # Adds a line break
    st.markdown("<h3 style='text-align: center;'>Explore the Electric Vehicle Makers Location in India</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)  # Adds a line break

    data = load_data()
    if data.empty:
        return  # Exit if data is not valid

    # Filter valid latitude and longitude ranges
    data = data[(data['Latitude'].between(-90, 90)) & (data['Longitude'].between(-180, 180))]

    # columns for filter options and map
    col1, col2 = st.columns([1, 2])  # Adjustment of proportions as needed

    with col1:
        # horizontal layout for the logo and header
        st.markdown("<h4 style='margin: 0;'>Filter Options</h4>", unsafe_allow_html=True)
        selected_maker = st.multiselect("Select EV Maker", options=data['EV Maker'].unique())
        #selected_place = st.multiselect("Select Place", options=data['Place'].unique())
        #selected_state = st.multiselect("Select State", options=data['State'].unique())

    # Filter data based on selections
    if selected_maker:
        data = data[data['EV Maker'].isin(selected_maker)]
    # if selected_place:
    #     data = data[data['Place'].isin(selected_place)]
    # if selected_state:
    #     data = data[data['State'].isin(selected_state)]

    # Create a Folium map centered around India
    india_map = folium.Map(location=[23.0, 82.0], zoom_start=4, tiles="CartoDB Positron")

    # Optional: Add custom boundaries (GeoJSON overlay)
    geojson_file = 'india_with_disputed_boundaries.geojson.geojson'  # Replace with the correct file path
    try:
        folium.GeoJson(
            geojson_file,
            name="Disputed Boundaries",
            style_function=lambda x: {
                'fillColor': 'transparent',
                'color': 'red',
                'weight': 2
            }
        ).add_to(india_map)
    except FileNotFoundError:
        st.warning("GeoJSON file for India's boundaries not found. Proceeding without it.")

    # Add data points to the map
    marker_cluster = MarkerCluster().add_to(india_map)

    for _, row in data.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['EV Maker']} at {row['Place']} ({row['State']})",
            tooltip=f"{row['EV Maker']} at {row['Place']}",
            icon=folium.Icon(color='blue')
        ).add_to(marker_cluster)

    # Render the map in the second column
    with col2:
        st_folium(india_map, width=700, height=500)

if __name__ == "__main__":
    main()








st.markdown("<br>", unsafe_allow_html=True)  # Adds a line break
st.markdown("<br>", unsafe_allow_html=True)  # Adds a line break
# feedback form 
st.header(":mailbox: Get In Touch With EV News!")
contact_form = """

<form action="https://formsubmit.co/sstl16102001@gmail.com" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit">Send</button>
</form>
"""
st.markdown(contact_form, unsafe_allow_html=True)

# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("./style.css")
# About us section

c22, c23 = st.columns((2))
with c22:
    st.markdown("""# :male-student: What We Performed - 
This study examines the growth trends, policies, infrastructure, major players, sales data, and consumer preferences of the Indian EV industry from 2001 to 2024. It offers a succinct overview of India's EV development and offers insights into market drivers, obstacles, and opportunities.

**Done By**
\n:one: Akash Vishwakarma 
\n:two: Aditya 
\n:three: Siva Maruthi
\n Thanks :heartpulse:
""")
    
with c23:
    with open("Animation - 1734640759652.json", "r") as f:
        lottie_animation = json.load(f)

    st_lottie(lottie_animation)

# End 