import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

# ------------------ Load Data -----------------------
@st.cache_data
def load_data():
    df = pd.read_csv("adjusted_land_utilization.csv")  # Make sure this matches your latest output file
    return df

df = load_data()

# ------------------ Sidebar -----------------------
st.sidebar.title("Crop Dashboard")
selected_crop = st.sidebar.selectbox("Select a Crop:", df['Crop'].unique())

# ------------------ Filter -----------------------
filtered_df = df[df['Crop'] == selected_crop].copy()

# ------------------ Add derived metrics -----------------------
filtered_df['Land Utilization Efficiency'] = filtered_df['Avg Area'] / filtered_df['Avg Agri Land']
filtered_df['Barren Land Percentage'] = (filtered_df['Avg Barren Land'] / filtered_df['Avg Agri Land']) * 100
filtered_df['Barren to Total Land Ratio'] = filtered_df['Avg Barren Land'] / filtered_df['Avg Area']

# ------------------ Helper: Bar Chart -----------------------
def create_bar_chart(data, x_col, y_col, title):
    fig = px.bar(data, x=x_col, y=y_col, title=title, labels={x_col: "State", y_col: title})
    fig.update_layout(xaxis_tickangle=-45)
    return fig

# ------------------ Section 1: Basic Top 5 -----------------------
st.header(f"Key Insights for {selected_crop}")

st.subheader("Top 5 States by Average Yield")
top_yield = filtered_df.sort_values(by='Avg Yield', ascending=False).head(5)
st.plotly_chart(create_bar_chart(top_yield, 'State', 'Avg Yield', 'Average Yield'))

st.subheader("Top 5 States with Highest Barren Land %")
highest_barren = filtered_df.sort_values(by='Barren Land Percentage', ascending=False).head(5)
st.plotly_chart(create_bar_chart(highest_barren, 'State', 'Barren Land Percentage', 'Barren Land Percentage'))

# ------------------ Section 2: Relationships -----------------------
st.subheader("Barren Land % vs Average Rainfall")
fig_barren_rainfall = px.scatter(
    filtered_df,
    x='Avg Rainfall',
    y='Barren Land Percentage',
    color='State',
    size='Avg Area',
    hover_name='State',
    trendline='ols',
    title='Barren % vs Avg Rainfall'
)
st.plotly_chart(fig_barren_rainfall)

st.subheader("Barren Land % vs Fertilizer per ha")
fig_barren_fert = px.scatter(
    filtered_df,
    x='Fertilizer per ha',
    y='Barren Land Percentage',
    color='State',
    size='Avg Area',
    hover_name='State',
    trendline='ols',
    title='Barren % vs Fertilizer per ha'
)
st.plotly_chart(fig_barren_fert)

st.subheader("Barren Land % vs Pesticide per ha")
fig_barren_pest = px.scatter(
    filtered_df,
    x='Pesticide per ha',
    y='Barren Land Percentage',
    color='State',
    size='Avg Area',
    hover_name='State',
    trendline='ols',
    title='Barren % vs Pesticide per ha'
)
st.plotly_chart(fig_barren_pest)

# ------------------ Section 3: Normalized Multi-trend -----------------------
scaler = MinMaxScaler()
norm_df = filtered_df.copy()
norm_df[['Avg Yield', 'Land Utilization Efficiency', 'Barren Land Percentage']] = scaler.fit_transform(
    norm_df[['Avg Yield', 'Land Utilization Efficiency', 'Barren Land Percentage']]
)

st.subheader("Normalized Trends by State")
fig_line = px.line(
    norm_df.sort_values('State'),
    x='State',
    y=['Avg Yield', 'Land Utilization Efficiency', 'Barren Land Percentage'],
    title='Normalized: Avg Yield, Efficiency, Barren %',
    labels={'value': 'Normalized Value', 'variable': 'Metric'}
)
fig_line.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_line)

# ------------------ Section 4: Heatmap -----------------------
st.subheader("Heatmap: Yield, Efficiency & Barren %")
heatmap_data = filtered_df[['State', 'Avg Yield', 'Land Utilization Efficiency', 'Barren Land Percentage']].set_index('State')

fig_heatmap = px.imshow(
    heatmap_data.T,
    labels=dict(x="State", y="Metric", color="Value"),
    x=heatmap_data.index,
    y=heatmap_data.columns,
    color_continuous_scale='Viridis',
    aspect="auto"
)
st.plotly_chart(fig_heatmap)

# ------------------ Section 5: Pie Chart -----------------------
st.subheader("Crop Area Distribution")
fig_pie = px.pie(
    filtered_df,
    values='Avg Area',
    names='State',
    title='Average Area Share by State',
    hole=0.4
)
st.plotly_chart(fig_pie)

# ------------------ Section 6: Box Plot -----------------------
st.subheader("Yield Distribution by State")
fig_box = px.box(
    filtered_df,
    x='State',
    y='Avg Yield',
    title='Avg Yield Distribution',
    points='all'
)
fig_box.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_box)
