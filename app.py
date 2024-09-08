from dotenv import load_dotenv

load_dotenv()

import streamlit as st 
import os 
import google.generativeai as genai 
import PyPDF2 as pdf


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Gemini-pro response 

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


import PyPDF2 as pdf  # Ensure you have the PyPDF2 library installed

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    
    # Iterate over all the pages in the PDF
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()  # Append the extracted text to the string
    
    return text



## Prompt Template 

input_prompt = '''
You are an expert ATS (Application Tracking system) with years of experience and deep understanding in the fields of software engineering,
data science, data analyst , big data engineer , AI/ML Engineer and many more tech jobs.Your task is to evaluate the resume based on the given 
job description. You have to consider that the job market is highly competitive and your role is to provide the best assistance in terms of 
improving the uploaded resumes.
Be consitent with your analysis.
Assign the percentage match based on JD and the missing words with high accuracy. Also provide some suggestions in improving the resume 
in order to match the Job descripton better.

 
description: the part from "\n ################ \n" to  the next "\n ################ \n"
resume: the part from "\n ################ \n" upto the end is the resume part 


Return the response in the form of 


Job Title:

JD match % : 

Missing Keywords: 

Advice to improve the resume: 


while providing the response , Provide one word job description in the summary for Job Title for example like Data Analyst
or Data scientist and many more.
and while rating the JD match '%' act like a experienced HR and critical provide the % matching 
Provide advice in a way an experienced person of that respective field would give. 
'''


## Streamlit app 

st.title('Gemini-Pro Assisted ATS')
st.text("Improve your resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume",type='pdf',help="Please upload the pdf file")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        
        text = input_pdf_text(uploaded_file)
        input = input_prompt + "\n ################ \n" + jd + "\n ################ \n" + text
        response = get_gemini_response(input)
        st.subheader("Summary for the Job Description:")
        st.text(response)
