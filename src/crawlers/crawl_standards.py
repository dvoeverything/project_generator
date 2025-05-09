from playwright.sync_api import sync_playwright
import pdfplumber, requests, hashlib, json, s3fs, datetime, os, io

BASE = "https://www.in.gov/doe/students/indiana-academic-standards/science-and-computer-science/"

def pdf_hash(blob): return hashlib.md5(blob).hexdigest()

def crawl():
    with sync_playwright() as p:
        page = p.firefox.launch(headless=True).new_page()
        page.goto(BASE, timeout=60000)
        pdfs = [a.get_attribute("href")
                for a in page.query_selector_all("a[href$='.pdf']")]

    for link in pdfs:
        blob = requests.get(link, timeout=30).content
        h = pdf_hash(blob)
        if h_already_seen(link, h):           
            continue

        with pdfplumber.open(io.BytesIO(blob)) as pdf:
            for page in pdf.pages:
                for bullet in page.extract_text().split("\n"):
                    if not bullet.strip(): continue
                    record = parse_standard(bullet)  
                    upsert_standard(record)          
        save_hash(link, h)
