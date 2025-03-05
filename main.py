import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from streamlit_plotly_events import plotly_events

st.title("Math Questions Visualization")

# Load the UMAP reducer if needed (e.g., for transforming new data)
umap_model_path = "umap_model.pkl"
try:
    umap_reducer = joblib.load(umap_model_path)
    st.success("Loaded UMAP model successfully.")
except Exception as e:
    st.error(f"Error loading UMAP model: {e}")

# Load the embedding data with chapters, topics, and questions
data_path = "embedded_data.csv"
try:
    df_embedded = pd.read_csv(data_path)
    st.success("Loaded embedded data successfully.")
except Exception as e:
    st.error(f"Error loading embedded data: {e}")

# Create a 3D scatter plot using Plotly Express
fig = px.scatter_3d(
    df_embedded,
    x="x",
    y="y",
    z="z",
    color="chapter",      # multicolor based on chapter
    symbol="topic",       # different symbols based on topic
    hover_data=["question"],  # show the full question on hover
    title="3D Visualization of Math Questions by Chapter and Topic"
)

# Display the plot and capture click events using streamlit-plotly-events
selected_points = plotly_events(fig, click_event=True)

st.plotly_chart(fig, use_container_width=True)

# If a point is clicked, show its corresponding question text
if selected_points:
    # streamlit-plotly-events returns a list of dicts; get the first point clicked.
    point = selected_points[0]
    # 'pointIndex' gives the index of the point in the DataFrame
    idx = point.get("pointIndex")
    if idx is not None and idx < len(df_embedded):
        question = df_embedded.loc[idx, "question"]
        st.write("### Clicked Question")
        st.write(question)
    else:
        st.write("No valid point selected.")
