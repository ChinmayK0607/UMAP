import os
import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from streamlit_plotly_events import plotly_events
import gdown

st.title("Math Questions Visualization")

# --- Download UMAP folder from Google Drive if not already present ---
umap_folder = "UMAP"
if not os.path.exists(umap_folder):
    st.info("Downloading UMAP folder from Google Drive...")
    # Folder URL from Google Drive
    folder_url = "https://drive.google.com/drive/folders/1mYhDf8NTKZhMd0KAQmH3h-941xueKrKF?usp=sharing"
    try:
        # Download the entire folder using gdown
        gdown.download_folder(url=folder_url, output=umap_folder, use_cookies=False)
        st.success("UMAP folder downloaded successfully.")
    except Exception as e:
        st.error(f"Error downloading folder: {e}")

# Update file paths
umap_model_path = os.path.join(umap_folder, "umap_model.pkl")
data_path = os.path.join(umap_folder, "embedded_data.csv")

# --- Load the UMAP reducer ---
try:
    umap_reducer = joblib.load(umap_model_path)
    st.success("Loaded UMAP model successfully.")
except Exception as e:
    st.error(f"Error loading UMAP model: {e}")

# --- Load the embedding data ---
try:
    df_embedded = pd.read_csv(data_path)
    st.success("Loaded embedded data successfully.")
except Exception as e:
    st.error(f"Error loading embedded data: {e}")

# --- Create a multicolored 3D scatter plot ---
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
