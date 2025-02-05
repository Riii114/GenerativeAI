import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv() #Load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Gemini pro reference
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    # for page in reader(len(reader.pages)):
    #     page = reader.pages[page]
    for page_number in range(len(reader.pages)):
        page = reader.pages[page_number]
        text += str(page.extract_text())
    return text

#Prompt Template:
input_prompt = '''
Hey Act like a skilled or very experience ATS(Application Tracking System) witha a deep understanding of tech field,software
engineering,data science,data analyst and big data engineer.your task is to evaluate the resume based on the given job description 
you must consider the job market is very competitive and you should provide best assistance for improving the resumes.Assign the
percentage Matching based on Jd and the missing keyword with accuracy
resume:{text}
description:{jd}
I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":" "}}

''' 

#Streamlit app:
st.title("Personal ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste The Job Description")
uploaded_file = st.file_uploader("Upload Your Resume",type="pdf",help="Please Upload the PDF")
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response)

