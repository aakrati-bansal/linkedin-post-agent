import os #os is a built-in Python toolkit that lets you interact with your operating system — we use it to read values from your .env file.
import gspread #gspread is the library we installed that talks to Google Sheets. Without this line, Python has no idea how to connect to Google.
from google.oauth2.service_account import Credentials #Credentials is what handles the authentication — it reads your service_account.json file and proves to Google that you're allowed in.
from datetime import datetime 
from dotenv import load_dotenv

load_dotenv()

SCOPES = [ #SCOPES is a list of permissions we're requesting from Google. Think of it like telling Google "I need permission to read/write Sheets AND Drive". Both are needed because gspread uses Drive to find the sheet by name.
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


def _get_sheet():
    creds = Credentials.from_service_account_file(
        os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"),
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1e33NUUbyxXVaVG5xqF-Q3smBFrYfUxOTdvXvsnv36YQ").sheet1
    return sheet

# Step 1 → Read the service account JSON file
#          (your keycard to get into Google)

# Step 2 → Define what you're allowed to do
#          (read? write? both? → that's SCOPES)

# Step 3 → Log into Google using that keycard
#          (gspread.authorize → you're now inside)

# Step 4 → Navigate to your specific spreadsheet
#          (open_by_key → like going to a specific room)

# Step 5 → Open the first tab of that spreadsheet
#          (.sheet1 → like opening the first page)

# Step 6 → Hand it back to whoever needs it
#          (return sheet)


def get_past_topics(limit: int = 12) -> str:
    sheet = _get_sheet()
    rows = sheet.get_all_records()
    #get_all_records() is a gspread built-in function that reads every row from your Google Sheet and converts it into a Python list of dictionaries.
    recent = rows[-limit:] if len(rows) > limit else rows

    if not recent:
        return "No past topics yet. This is the first run."

    lines = []
    for row in recent:
        lines.append(
            f"- [{row.get('Week', '?')}] {row.get('Post Type', '?')}: "
            f"{row.get('Topic', '?')} (keywords: {row.get('Keywords', '?')})"
        )
    return "\n".join(lines) #Why do we need to join? Because Claude expects plain text in the prompt — not a Python list. You can't paste a list into a prompt, but you can paste a string.

# Step 1 → Get the sheet
# sheet = _get_sheet() — call the function we already understand, get back the spreadsheet ready to read
# Step 2 → Fetch all rows
# sheet.get_all_records() — read every row from the sheet and convert it into a list of dictionaries, one dictionary per row
# Step 3 → Trim to recent rows only
# rows[-limit:] — if the sheet has more rows than the limit, take only the last 12. If less, use everything. We don't need Claude to remember 100 weeks of history
# Step 4 → Handle empty sheet
# if not recent — if the sheet is empty, return a default message instead of crashing. Safety net for the very first run
# Step 5 → Format each row into a readable line
# for row in recent: lines.append(...) — loop through each dictionary and convert it into a clean human readable string like - [Feb W1] Concept: Transformer basics
# Step 6 → Glue all lines into one string
# "\n".join(lines) — join the list into one single block of text because Claude reads strings, not Python lists
# Step 7 → Hand it back
# return "\n".join(lines) — send the final string back to main.py where it gets injected into Claude's prompt as memory

def log_post(post_type: str, topic: str, keywords: str, status: str = "Draft", notes: str = ""):
    sheet = _get_sheet()
    now = datetime.now()
    week_number = (now.day - 1) // 7 + 1
    week_label = f"{now.strftime('%b')} W{week_number} {now.year}"
    row = [week_label, post_type, topic, keywords, status, notes]
    sheet.append_row(row)
    print(f"✅ Logged to sheet: {post_type} — {topic}")