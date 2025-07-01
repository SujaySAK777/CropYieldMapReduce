import streamlit as st
import os
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
import subprocess

# ------------------ HOME -----------------------
st.title("Crop Yield & Resource Analysis")

page = st.sidebar.radio(
    "Go to:",
    ("Spark MLlib Prediction", "Visualization Dashboard", "Hadoop Resource Monitoring")
)

# ------------------ SPARK PREDICTION -----------------------
if page == "Spark MLlib Prediction":
    st.header("Crop Yield Prediction")

    st.info("Enter values to predict average crop yield:")

    # ✅ Load unique States & Crops dynamically
    @st.cache_data
    def load_states_crops():
        df = pd.read_csv("adjusted_land_utilization.csv")
        states = sorted(df['State'].dropna().unique().tolist())
        crops = sorted(df['Crop'].dropna().unique().tolist())
        return states, crops

    states_list, crops_list = load_states_crops()

    state = st.selectbox("State", states_list)
    crop = st.selectbox("Crop", crops_list)

    avg_area = st.number_input("Average Area (hectare)", min_value=0.0, value=500000.0)
    avg_agri_land = st.number_input("Average Agri Land (hectare)", min_value=0.0, value=550000.0)
    avg_barren_land = st.number_input("Average Barren Land (hectare)", min_value=0.0, value=50000.0)
    avg_rainfall = st.number_input("Average Rainfall (mm)", min_value=0.0, value=900.0)
    fertilizer_per_ha = st.number_input("Fertilizer per hectare (kg)", min_value=0.0, value=200.0)
    pesticide_per_ha = st.number_input("Pesticide per hectare (litre)", min_value=0.0, value=0.5)

    if st.button("Predict"):
        with st.spinner("Running Spark job..."):
            spark_submit = r"C:\Users\Dell\pyspark\spark-3.5.5\spark-3.5.5-bin-hadoop3\bin\spark-submit.cmd"
            script = os.path.join(os.getcwd(), "spark_easy_web.py")

            cmd = [
                spark_submit,
                script,
                state,
                crop,
                str(avg_area),
                str(avg_agri_land),
                str(avg_barren_land),
                str(avg_rainfall),
                str(fertilizer_per_ha),
                str(pesticide_per_ha)
            ]

            st.write("Running command:", " ".join(cmd))  # Debug tip

            subprocess.run(cmd, check=True)

            # ✅ Read prediction output saved by spark_easy_web.py
            result = pd.read_csv("prediction_result.csv")
            st.success("Prediction done!")
            st.write(result)


# ------------------ VISUALIZATION -----------------------
elif page == "Visualization Dashboard":
    st.header("Crop Data Visualization")

    @st.cache_data
    def load_data():
        return pd.read_csv("adjusted_land_utilization.csv")

    df = load_data()
    st.sidebar.title("Crop Dashboard")
    selected_crop = st.sidebar.selectbox("Select a Crop:", df['Crop'].unique())

    filtered_df = df[df['Crop'] == selected_crop].copy()
    filtered_df['Land Utilization Efficiency'] = filtered_df['Avg Area'] / filtered_df['Avg Agri Land']
    filtered_df['Barren Land Percentage'] = (filtered_df['Avg Barren Land'] / filtered_df['Avg Agri Land']) * 100
    filtered_df['Barren to Total Land Ratio'] = filtered_df['Avg Barren Land'] / filtered_df['Avg Area']

    def create_bar_chart(data, x_col, y_col, title):
        fig = px.bar(data, x=x_col, y=y_col, title=title, labels={x_col: "State", y_col: title})
        fig.update_layout(xaxis_tickangle=-45)
        return fig

    st.header(f"Key Insights for {selected_crop}")

    st.subheader("Top 5 States by Average Yield")
    top_yield = filtered_df.sort_values(by='Avg Yield', ascending=False).head(5)
    st.plotly_chart(create_bar_chart(top_yield, 'State', 'Avg Yield', 'Average Yield'))

    st.subheader("Top 5 States with Highest Barren Land %")
    highest_barren = filtered_df.sort_values(by='Barren Land Percentage', ascending=False).head(5)
    st.plotly_chart(create_bar_chart(highest_barren, 'State', 'Barren Land Percentage', 'Barren Land Percentage'))

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

    st.subheader("Crop Area Distribution")
    fig_pie = px.pie(
        filtered_df,
        values='Avg Area',
        names='State',
        title='Average Area Share by State',
        hole=0.4
    )
    st.plotly_chart(fig_pie)

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

# ------------------ HADOOP MONITOR -----------------------
elif page == "Hadoop Resource Monitoring":
    st.header("Hadoop MapReduce Resource & Heat Monitoring")

    if st.button("Run MapReduce & Monitor"):
        st.info("Running Hadoop Streaming job with Heat & Resource Monitoring...")
        subprocess.run(["python", "monitor_hadoop_heat.py"], check=True)

        st.success("✅ Job done! Showing CPU, Memory, Disk & Temperature usage:")

        df_log = pd.read_csv("real_system_usage.csv")

        st.subheader("Raw System Usage Data")
        st.dataframe(df_log)

        st.subheader("CPU Usage (%)")
        st.line_chart(df_log.set_index("time_sec")["cpu_percent"])

        st.subheader("Memory Usage (%)")
        st.line_chart(df_log.set_index("time_sec")["mem_percent"])

        st.subheader("Disk Usage (%)")
        st.line_chart(df_log.set_index("time_sec")["disk_percent"])

        if "cpu_temp_C" in df_log.columns:
            st.subheader("CPU Temperature (°C)")
            st.line_chart(df_log.set_index("time_sec")["cpu_temp_C"])
        else:
            st.warning("⚠️ CPU temperature column not found. Please check your OpenHardwareMonitor or WMI output.")


