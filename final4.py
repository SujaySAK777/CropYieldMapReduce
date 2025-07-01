import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_excel("updated_map_reduce_output.xlsx")

df = load_data()

# Sidebar for crop selection
st.sidebar.title("Crop Selection")
selected_crop = st.sidebar.selectbox("Select a crop:", df['Crop'].unique())

# Filter data based on selected crop
filtered_df = df[df['Crop'] == selected_crop].copy()

# Calculate additional metrics row-wise
filtered_df['Land Utilization Efficiency'] = filtered_df['Total Area'] / filtered_df['Total Agri Land']
filtered_df['Barren Land Percentage'] = (filtered_df['Total Barren Land'] / filtered_df['Total Agri Land']) * 100
filtered_df['Barren to Total Land Ratio'] = filtered_df['Total Barren Land'] / filtered_df['Total Area']

# Function to create bar charts
def create_bar_chart(data, x_col, y_col, title):
    fig = px.bar(data, x=x_col, y=y_col, title=title, labels={x_col: "State", y_col: title})
    fig.update_layout(xaxis_tickangle=-45)
    return fig

# Existing bar charts
st.subheader(f"Top 5 States by Average Yield for {selected_crop}")
top_yield = filtered_df.sort_values(by='Avg Yield', ascending=False).head(5)
st.plotly_chart(create_bar_chart(top_yield, 'State', 'Avg Yield', 'Average Yield'))

st.subheader(f"Top 5 States by Land Utilization Efficiency for {selected_crop}")
top_utilization = filtered_df.sort_values(by='Land Utilization Efficiency', ascending=False).head(5)
st.plotly_chart(create_bar_chart(top_utilization, 'State', 'Land Utilization Efficiency', 'Land Utilization Efficiency'))

st.subheader(f"Top 5 States with Lowest Barren Land Percentage for {selected_crop}")
lowest_barren = filtered_df.sort_values(by='Barren Land Percentage').head(5)
st.plotly_chart(create_bar_chart(lowest_barren, 'State', 'Barren Land Percentage', 'Barren Land Percentage'))

st.subheader(f"Top 5 States with Highest Barren Land Percentage for {selected_crop}")
highest_barren = filtered_df.sort_values(by='Barren Land Percentage', ascending=False).head(5)
st.plotly_chart(create_bar_chart(highest_barren, 'State', 'Barren Land Percentage', 'Barren Land Percentage'))


# -------- Additional Insights --------

# 1. Scatter plot: Avg Yield vs Land Utilization Efficiency
st.subheader(f"Avg Yield vs Land Utilization Efficiency for {selected_crop}")
fig_scatter = px.scatter(
    filtered_df,
    x='Land Utilization Efficiency',
    y='Avg Yield',
    color='State',
    size='Total Area',
    hover_name='State',
    title='Yield vs Land Utilization Efficiency (Size ~ Total Area)'
)
st.plotly_chart(fig_scatter)

# 2. Pie chart: Crop Area Distribution across States
st.subheader(f"Crop Area Distribution across States for {selected_crop}")
fig_pie = px.pie(
    filtered_df,
    values='Total Area',
    names='State',
    title='Crop Area Distribution by State',
    hole=0.4
)
st.plotly_chart(fig_pie)

# 3. Line chart: Normalized Avg Yield, Land Utilization, Barren Land %
scaler = MinMaxScaler()
norm_df = filtered_df.copy()
norm_df[['Avg Yield', 'Land Utilization Efficiency', 'Barren Land Percentage']] = scaler.fit_transform(
    norm_df[['Avg Yield', 'Land Utilization Efficiency', 'Barren Land Percentage']]
)

st.subheader(f"Normalized Trends of Yield, Land Utilization & Barren Land for {selected_crop}")
fig_line = px.line(
    norm_df.sort_values('State'),
    x='State',
    y=['Avg Yield', 'Land Utilization Efficiency', 'Barren Land Percentage'],
    title='Normalized Yield, Land Utilization & Barren Land Percentage by State',
    labels={'value': 'Normalized Value', 'variable': 'Metric'}
)
fig_line.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_line)

# 4. Heatmap: States vs Metrics
st.subheader(f"Heatmap of Yield, Land Utilization & Barren Land for {selected_crop}")
heatmap_data = filtered_df[['State', 'Avg Yield', 'Land Utilization Efficiency', 'Barren Land Percentage']]
heatmap_data = heatmap_data.set_index('State')

fig_heatmap = px.imshow(
    heatmap_data.T,
    labels=dict(x="State", y="Metric", color="Value"),
    x=heatmap_data.index,
    y=heatmap_data.columns,
    color_continuous_scale='Viridis',
    aspect="auto"
)
st.plotly_chart(fig_heatmap)

# 5. Box plot: Yield Distribution by State
st.subheader(f"Yield Distribution by State for {selected_crop}")
fig_box = px.box(
    filtered_df,
    x='State',
    y='Avg Yield',
    title='Yield Distribution across States',
    points='all'
)
fig_box.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_box)
