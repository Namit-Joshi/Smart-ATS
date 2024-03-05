import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Pro Response
def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

# Taking the PDF and extracting the text from it
def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Hey Act Like a skilled or very experienced ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description(JD).
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on JD and the missing keywords with high accuracy

I want the response in JSON format in one single string having keys: "JD Match" whose value is a percentage,
"Missing Keywords" whose value is a list, "Profile Summary" and "Tips/Suggestions" which is a string
containing tips/suggestions to increase the JD match score by recommending changes to the resume. 
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume | Tech Jobs")
jd=st.text_area("Paste the Job Description", height = 350)
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please upload the resume in pdf format")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        input_prompt = input_prompt + "\n\nResume: " + text + "\n\nJD: " + jd
        print(input_prompt)
        response=get_gemini_repsonse(input_prompt)
        # st.subheader(response)
        print(response)
        response = response.replace('json','').replace('```','').replace('JSON','')
        # Parse the JSON response
        parsed_response = json.loads(response)

        # Display the parsed information
        st.write("**JD Match:**", parsed_response["JD Match"],"%")
        st.write("**Missing Keywords:**", ", ".join(parsed_response["Missing Keywords"]))
        st.write("**Profile Summary:**", parsed_response["Profile Summary"])
        st.write("**Tips/Suggestions:**", parsed_response["Tips/Suggestions"])
