import os
import pickle
import requests
import arxiv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from selenium.webdriver import ChromeOptions
from helium import start_chrome, go_to

# Setup persistent token storage
TOKEN_PATH = os.path.expanduser("~/.skyscope/token.pickle")
CREDS_PATH = os.path.expanduser("~/.skyscope/credentials.json")

# --- Google OAuth2 flow for Drive or Gmail ---
def google_oauth(scopes):
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, scopes=scopes)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    return creds

# --- Arxiv Paper Search ---
def arxiv_search(query, max_results=10):
    search = arxiv.Search(query=query, max_results=max_results)
    results = []
    for result in search.results():
        results.append({
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "summary": result.summary,
            "published": result.published.strftime("%Y-%m-%d"),
            "pdf_url": result.pdf_url
        })
    return results

# --- Google Drive Access ---
def list_drive_files():
    scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly']
    creds = google_oauth(scopes)
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(pageSize=20, fields='files(id, name)').execute()
    return results.get('files', [])

# --- Gmail Access ---
def list_gmail_threads():
    scopes = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = google_oauth(scopes)
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().threads().list(userId='me', maxResults=10).execute()
    return results.get('threads', [])

# --- GitHub OAuth helper (placeholder for real OAuth flow) ---
def github_auth():
    # Implementation context-aware (e.g., local browser popup)
    pass
