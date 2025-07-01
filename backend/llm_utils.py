import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_email(hr_name, hr_email, resume_text, jd_text, custom_prompt="") -> str:
    base_prompt = f"""
You are a helpful assistant that writes cold outreach emails for job applications.

Given the HR's name: {hr_name}, and their email: {hr_email},
and the following resume text and job description, 
I want you to be my cold-email generator to show my interest in the particular job role and company, generate the email by keeping all these conditions strictly in mind.

Conditions:
1. First Para: It should include who am i(just include my name, education and years of experience). and why am i reaching out to?(write something like i have applied for this position already, but just don't want to miss the exciting opportunity to increase my chances to show how my experiences align with the role and companies culture.)
2. Second Para: How my experience align with the job description.
3. Say that I am attaching the resume for your reference.
4. lastly, say that i would love to discuss how my experience align more with the job detailed and looking forward to have a call, and let me know what time works for you?
5. write the whole email in confident, professional and enthusiastic tone.
6. Make sure to keep the email under 250 words.


Resume:
{resume_text}

Job Description:
{jd_text}

{f"Additional Instructions: {custom_prompt}" if custom_prompt else ""}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You write friendly but professional emails for job applicants."},
            {"role": "user", "content": base_prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response['choices'][0]['message']['content'].strip()