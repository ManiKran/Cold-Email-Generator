from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from llm_utils import generate_email
from extract_utils import extract_text
from email_utils import send_email_via_gmail
from auth_utils import get_authorization_url, exchange_code_for_token

app = FastAPI()

# CORS Middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary in-memory token store (use DB or session in production)
token_store = {}

@app.post("/generate-email/")
async def generate_email_endpoint(
    hr_name: str = Form(...),
    hr_email: str = Form(...),
    prompt: str = Form(""),
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...)
):
    resume_text = await extract_text(resume)
    jd_text = await extract_text(job_description)

    email_text = generate_email(hr_name, hr_email, resume_text, jd_text, prompt)
    return {"email": email_text}


@app.post("/send-email/")
async def send_email_endpoint(
    to_email: str = Form(...),
    subject: str = Form(...),
    body: str = Form(...)
):
    user_token = token_store.get("demo_user")
    if not user_token:
        return JSONResponse(status_code=401, content={"error": "User not authenticated"})

    status = send_email_via_gmail(to_email, subject, body, user_token)
    return JSONResponse(content={"status": status})


@app.get("/auth/login")
async def login():
    auth_url = get_authorization_url()
    return RedirectResponse(auth_url)


@app.get("/auth/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    token_data = exchange_code_for_token(code)

    # Save under demo_user key for now
    token_store["demo_user"] = token_data

    return JSONResponse({
        "message": "Login successful",
        "token": token_data
    })