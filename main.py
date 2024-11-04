import streamlit as st

# Title for the app
st.title("Physio session summary")

# Upload the audio file
uploaded_file = st.file_uploader("Choose a file (MP3 or TXT)", type=["mp3", "txt"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Display the file name
    st.write("Uploaded file name:", uploaded_file.name)
else:
    st.write("Please upload an MP3 file to display its name.")