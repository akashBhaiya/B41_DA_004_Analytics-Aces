# Indian EV Market Analysis (2001 - 2024)

Overview

This project provides an in-depth analysis of the Indian Electric Vehicle (EV) market from 2001 to 2024. It highlights sales trends, growth rates, major EV manufacturers, category-wise performance, and infrastructure development.
## Features
- Key Performance Indicators (KPIs): Displays important metrics like the number of companies, states, and total EV sales, which can be filtered by year and state.
- Trend Visualization: Visualizes EV sales by year, sales by category, and manufacturer growth over time.
- Interactive Filtering: Users can filter data by state, year, or specific EV maker to explore the sales history and distribution of manufacturers.
- Location Visualization: The app includes an interactive map that shows the locations of EV makers across India, providing insights into the geographic distribution of EV manufacturers.
## File Structure

- main.py: Main application file.

- requirements.txt: Python dependencies.

- style.css: Custom styling for the application.

- data/: Contains CSV files used for analysis.

- Animation - 1734640759652.json: Lottie animation for the "About Us" section.

- Analytics Aces.png: Logo for the application.
## Data Loading and Preprocessing:
   - Data is loaded from multiple CSV files, including EV sales data by maker and category, state-wise EV maker data, and vehicle class registrations.
   - The data is cleaned, and columns are formatted for analysis (e.g., date conversion for sales data).
   - Data aggregation and filtering are done based on user inputs (e.g., selected state or year).
## KPIs and Aggregations:
- Displays total EV companies, states, and sales, along with the top state by EV makers.
- Uses st.metric() to show important KPIs such as the total number of companies, states, and total sales in the selected filter range.
## Visualizations:

- Bar Charts: To show the trend of total EV sales by year and the number of EV companies in each state.
- Pie Charts: Display the distribution of companies across states.
- Top Manufacturers Growth: A bar chart for the top manufacturers based on their growth rate.
- EV Sales by Category: Bar chart for sales per vehicle category.
- Line Chart: Displays the sales history of a selected manufacturer
## Advanced Features:
- 3D Vehicle Data Heatmap: Allows users to select a date range and visualize a 3D surface plot for vehicle data over time.
- Map Visualization: Plots the locations of EV makers on an interactive map, with filters for specific makers and states. This map includes the use of GeoJSON for geographical boundaries, enhancing the visualization of state distributions.
## Additional Features:
- EV Maker Location: Displays EV maker locations on an interactive map using folium, with markers showing the maker's name, place, and state.
- State-wise PCS: Provides a bar chart showing the number of operational PCS in different states or a selected state.

