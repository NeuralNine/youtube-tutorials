import os
import io
import json

import PyPDF2
import uvicorn

from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from auth0_server_python.auth_server import ServerClient

load_dotenv()


class MemoryStore:

    def __init__(self):
        self.s = {}

    async def set(self, k, v, options=None):
        self.s[k] = v

    async def get(self, k, options=None):
        return self.s.get(k)

    async def delete(self, k, options=None):
        self.s.pop(k, None)


auth0 = ServerClient(
    domain=os.getenv("AUTH0_DOMAIN") or "",
    client_id=os.getenv("AUTH0_CLIENT_ID") or "",
    client_secret=os.getenv("AUTH0_CLIENT_SECRET") or "",
    secret=os.getenv("AUTH0_SECRET") or "",
    redirect_uri=(os.getenv("APP_BASE_URL") or "") + "/auth/callback",
    transaction_store=MemoryStore(),
    state_store=MemoryStore(),
    authorization_params={"scope": "openid profile email offline_access"}
)


class Invoice(BaseModel):
    invoice_number: str = Field(...)
    date: str = Field(...)
    total: float = Field(...)
    recipient: str = Field(...)
    sender: str = Field(...)



openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()

user_settings = {}


def render_template(template_name: str, **kwargs) -> str:
    with open(f'templates/{template_name}', 'r') as f:
        content = f.read()

    for k, v in kwargs.items():
        content = content.replace(f'{{{{{k}}}}}', str(v))

    with open('templates/base.html', 'r') as f:
        base = f.read()

    return base.replace('{{content}}', content).replace('{{title}}', kwargs.get('title', 'PDF Invoice Processor'))


def extract_pdf_text(drive_service, file_id: str) -> str:
    request = drive_service.files().get_media(fileId=file_id)
    file_io = io.BytesIO()
    downloader = MediaIoBaseDownload(file_io, request)

    done = False
    while not done:
        _, done = downloader.next_chunk()

    file_io.seek(0)

    return '\n'.join(page.extract_text() for page in PyPDF2.PdfReader(file_io).pages)


def extract_invoice_data(text: str) -> dict:
    response = openai_client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert at extracting structured data from invoice PDFs. Extract the key invoice information from the provided text."},
            {"role": "user", "content": text}
        ],
        response_format=Invoice
    )
    
    parsed_data = response.choices[0].message.parsed
    if parsed_data:
        return parsed_data.model_dump()

    raise ValueError("No invoice data extracted")


@app.get("/", response_class=HTMLResponse)
async def home():
    user = await auth0.get_user()
    if not user:
        login_url = await auth0.start_interactive_login()
        return render_template("login.html", login_url=login_url)
    
    settings = user_settings.get(user.get('sub'), {})
    folder_id, sheet_id = settings.get('folder_id', ''), settings.get('sheet_id', '')
    is_configured = folder_id and sheet_id
    
    return render_template("home.html",
        user_name=user.get('name'),
        folder_id=folder_id,
        sheet_id=sheet_id,
        disabled="" if is_configured else "disabled",
        warning_message='<div class="alert-warning">Please configure your Google Drive and Sheets IDs above.</div>' if not is_configured else ""
    )

@app.post("/settings")
async def save_settings(folder_id: str = Form(...), sheet_id: str = Form(...)):
    user = await auth0.get_user()
    if not user: 
        return RedirectResponse(url="/", status_code=303)
    
    user_settings[user.get('sub')] = {
        'folder_id': folder_id.strip(), 
        'sheet_id': sheet_id.strip()
    }
    return RedirectResponse(url="/", status_code=303)


@app.get("/auth/callback", response_class=HTMLResponse)
async def callback(request: Request):
    result = await auth0.complete_interactive_login(str(request.url))
    if result.get("error"): 
        return render_template("result.html", status="Error", message=f"Authentication error: {result['error']}")
    return HTMLResponse("<script>window.location.href='/'</script>")


@app.post("/process", response_class=HTMLResponse)
async def process():
    user = await auth0.get_user()
    if not user: 
        return RedirectResponse(url="/")
    
    settings = user_settings.get(user.get('sub'), {})
    folder_id, sheet_id = settings.get('folder_id'), settings.get('sheet_id')
    
    if not folder_id or not sheet_id: 
        return RedirectResponse(url="/")
    
    try:
        try:
            token = await auth0.get_access_token_for_connection(options={
                "connection": "google-oauth2",
                "scope": "https://www.googleapis.com/auth/drive.readonly https://www.googleapis.com/auth/spreadsheets"
            })
        except:
            login_url = await auth0.start_interactive_login()
            return render_template("result.html", 
                status="Google Re-authentication Required", 
                message=f'Your Google connection has expired. <a href="{login_url}&connection=google-oauth2">Click here to reconnect Google</a>.')
        
        creds = Credentials(token)
        drive = build("drive", "v3", credentials=creds)
        sheets = build("sheets", "v4", credentials=creds).spreadsheets()
        
        files = drive.files().list(
            q=f"'{folder_id}' in parents and mimeType='application/pdf' and trashed=false",
            fields="files(id,name,modifiedTime)"
        ).execute()["files"]
        
        rows = []
        for file in files:
            text = extract_pdf_text(drive, file["id"])
            data = extract_invoice_data(text)
            rows.append([
                data["invoice_number"], data["date"], data["total"],
                data["sender"], data["recipient"], file["name"], file["modifiedTime"]
            ])
        
        if rows:
            sheets.values().append(
                spreadsheetId=sheet_id,
                range="Sheet1!A1",
                valueInputOption="RAW",
                body={"values": rows}
            ).execute()
        
        return render_template("result.html", 
            status="Processing Complete!", 
            message=f"Successfully processed {len(rows)} PDF files"
        )
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Processing error: {error_details}") 
        return render_template("result.html", 
            status="Error", 
            message=f"Failed to process PDFs: {str(e)}<br><br>Details: {error_details.replace(chr(10), '<br>')}"
        )

@app.get("/logout")
async def logout():
    await auth0.logout()
    return RedirectResponse(url="/")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
