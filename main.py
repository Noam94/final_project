import streamlit as st
import openai
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from deepgram import DeepgramClient, PrerecordedOptions
from pydub import AudioSegment
from io import BytesIO

st.title("Physio session summary")

if 'OPEN_API_KEY' in st.secrets:
    st.success('Proceed to load your file')
    openai.api_key = st.secrets['OPEN_API_KEY']
else:
    openai.api_key = st.text_input('Enter OpenAI API key:', type='password')
    if not (openai.api_key.dtsrtswith('sk-') and len(openai.api_key)==51):
        st.warning('Please enter your credentials')
    else:
        st.success('Proceed to load your file')



uploaded_file = st.file_uploader("Choose a file (mp3 or TXT)", type=["mp3", "txt"])


DEEPGRAM_API_KEY = '91fbd5d2589108fad6177d84435fe94f5518af52'

class ConversationSummary(BaseModel):
    patient_report: str
    therapist_recommendations: str

def summarize_conversation(conversation: str) -> ConversationSummary:
    # Define the prompt
    prompt = (
        "You are a physiotherapist expert in analyzing patient-therapist conversations and creating reports to "
        "other professionals in the medical field. Your task is to provide a concise summary, up to 5 bullets each, of the patient's key "
        "medical complaints and the therapist's recommendations. Focus solely on physiotherapy-related information "
        "and avoid any general topics discussions."
        f"Conversation:\n{conversation}\n\n"
        "Summary:"
    )

    # Call the OpenAI API to generate a summary
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",#model="gpt-4",  # Specify the model you want to use
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Extract content from the response
    summary_text = response['choices'][0]['message']['content']#.strip()
    return summary_text

# Check if a file is uploaded
if uploaded_file is not None:
    # Display the file name
    if uploaded_file.name.endswith(".txt"):
        # Read and save the content of the text file
        text_content = uploaded_file.read().decode("utf-8")
        summary = summarize_conversation(text_content)
        st.header("Summery of the Physio-patient conversation:")
        st.write(summary)
    if uploaded_file.name.endswith(".mp3"):
        # play file
        st.audio(uploaded_file, format="audio/mp3")
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)
        file_data = uploaded_file.read()  # Read the entire file into bytes
        audio_stream = BytesIO(file_data)
        payload = {'buffer': audio_stream}

        options = PrerecordedOptions(
            smart_format=True, model="nova-2", language="en-US"
        )

        if st.button("Summarize conversation"):
            # Pass the file-like object directly
            response = deepgram.listen.prerecorded.v('1').transcribe_file(payload, options)
            try:
                transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
                summary = summarize_conversation(transcript)
                st.header("Summary:")
                st.write(summary)
                st.header("Transcript:")
                st.write(transcript)
            except KeyError:
                st.write("Transcription not found in response.")
    else:
        st.write("Please upload an MP3 file or a txt file to display the session summery")
# Check if a file is uploaded
if uploaded_file is not None:
    # Display the file name
    st.write("Uploaded file name:", uploaded_file.name)
else:
    st.write("Please upload an MP3 file to display its name.")