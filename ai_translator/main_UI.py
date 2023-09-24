import sys
import os
import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator

def main():
    # Title
    st.title("PDF Translation App")

    # 1. Drop down list to allow user to select model
    models = ["gpt-3.5-turbo", "Model 2", "Model 3"]
    selected_model = st.selectbox("Select a model", models)

    # 2. File upload from local
    uploaded_file = st.file_uploader("Upload a file", type=["pdf"])

    # 3. Text field for API Key
    api_key = st.text_input("Enter API Key")

    # 4. Drop down list to allow user to select output file type
    output_formats = ["Markdown", "PDF"]
    selected_format = st.selectbox("Select output file format", output_formats)

    # 5. Button to trigger translation
    if st.button("Translate"):
        # load model
        model = OpenAIModel(model=selected_model, api_key=api_key)
        translator = PDFTranslator(model)

        currentDIR = os.path.dirname(os.path.abspath(__file__))
        # create temp folder if not exist
        if not os.path.exists(currentDIR + "/temp"):
            os.makedirs(currentDIR + "/temp")
        tempFile = currentDIR + "/temp/" + uploaded_file.name
        # save file to temp folder
        with open(tempFile, "wb") as f:
            f.write(uploaded_file.getbuffer())

        #LOG.debug("File Name: {}".format())
        translator.translate_pdf(tempFile, selected_format)

if __name__ == "__main__":
    main()
