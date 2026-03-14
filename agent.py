import os
from groq import Groq
import requests #lets Python talk to Ollama over the internet
from tavily import TavilyClient #lets Python search the web for fresh AI content
from dotenv import load_dotenv

load_dotenv()

VOICE_PROFILE = """
My LinkedIn voice:
- Direct and clear — no fluff or corporate speak
- Curious and thoughtful — I like to explore ideas, not just report them
- Slightly contrarian — I look for the angle others are missing
- Grounded — I back opinions with reasoning, not hype
- Conversational — I write like I talk, not like a press release
"""

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
# MODEL = "llama3.1:8b"
# OLLAMA_URL = "http://localhost:11434/api/generate"
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"

def _search(query: str, max_results: int = 5) -> str:
    try:
        result = tavily.search(query, max_results=max_results)
        l = []
        for r in result.get("results", []):
            l.append(f"{r.get('title', '')} - {r.get('content', '')}")
        return "\n".join(l)
    except Exception as e:
        print(f"Search error: {e}")
        return "Could not fetch search results. Please try again."

# Step 1 → Receive the search query and limit
# query is what to search for, max_results=5 is how many results to fetch. Default is 5 because we don't need millions of results — just enough for Claude to pick from.
# Step 2 → Search the web using Tavily
# tavily.search(query=query, max_results=max_results) sends the search query to Tavily which goes to the internet and comes back with the top 5 results as a dictionary.
# Step 3 → Create an empty list to store formatted results
# lines = [] — blank piece of paper, same as in memory.py. We'll fill it up in the loop.
# Step 4 → Loop through each search result safely
# for r in results.get("results", []) — go through each article one by one. The [] fallback means if Tavily returns nothing, don't crash — just loop 0 times.
# Step 5 → Format each result into one readable line
# r['title'] gets the headline. r['content'][:300] gets only the first 300 characters of the article — we trim it so the prompt doesn't get too long and expensive.
# Step 6 → Glue everything into one string
# "\n".join(lines) — same as memory.py. Claude needs a string not a list, so we join everything with a newline between each result.
# Step 7 → Hand it back
# return "\n".join(lines) — send the formatted search results back to whichever pipeline called this function.


def _ask_groq(prompt: str) -> str:
    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a LinkedIn content writer. Output only the post itself. No intro line like 'Here is the post'. Just the raw post text."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.9,
        max_tokens=1024
    )
    return response.choices[0].message.content.strip()


# def _ask_ollama(prompt: str) -> str:
#     response = requests.post(OLLAMA_URL, json={
#         "model": MODEL,
#         "prompt": prompt + "\n\nIMPORTANT: Output only the post itself. No intro line like 'Here is the post'. Just the raw post text.",
#         "stream": False,
#         "options": {
#             "temperature": 0.9  # ← add this line (default is 0.7)
#         }
#     })
#     return response.json()["response"].strip()


# Step 1 → Receive the prompt
# prompt: str — accepts whatever text is sent in — could be a "pick the best news story" prompt or a "write a LinkedIn post" prompt. This function doesn't care what the prompt is — it just delivers it.
# Step 2 → Send the prompt to Ollama
# requests.post(OLLAMA_URL, json={...}) — the postman knocks on Ollama's door at localhost:11434 and delivers a package containing everything Ollama needs to generate a response.
# Step 3 → Tell Ollama which model to use
# "model": MODEL — specifies llama3.1:8b. Like telling a company "I want to speak to this specific person" — there could be multiple models installed, this picks the right one.
# Step 4 → Send the prompt with instructions
# "prompt": prompt + "\n\nIMPORTANT: Output only the post..." — sends your actual prompt PLUS a strict instruction to not add any intro lines like "Here is the post". Keeps the output clean and ready to publish.
# Step 5 → Wait for the full response
# "stream": False — don't send word by word, wait until the entire response is ready then return it all at once.
# Step 6 → Control creativity
# "temperature": 0.9 — tell Ollama to be creative and varied, not safe and robotic. Important for LinkedIn posts that need to sound human and fresh every week.
# Step 7 → Extract and clean the response
# response.json()["response"].strip() — three things happening here:

# .json() → convert Ollama's raw response into a Python dictionary
# ["response"] → extract just the text from that dictionary
# .strip() → remove any extra spaces or blank lines at the start and end

# Step 8 → Hand it back
# return — send the clean post text back to whichever pipeline called this function — news, concept or tool spotlight.


def run_news_pipeline(past_topics: str, manual_note: str = "") -> dict:
    if manual_note:
        print(f"\n📝 Using your note: {manual_note}")

        # Skip web search — write directly about what user mentioned
        pick_response = f"""
TOPIC: {manual_note}
SUMMARY: The user has shared this news or development they came across this week. Write their personal take on it.
KEYWORDS: AI, news, trends
"""
    else:
        print("\n🔍 Searching for AI news...")
        search_results = _search("top AI news this week artificial intelligence")

        pick_prompt = f"""
Here are recent AI news headlines and summaries:
{search_results}

Here are topics I've already covered.
YOU MUST NOT pick any of these. If you do, you have failed your task:
{past_topics}

Double check your answer against this list before responding.

Pick the single most interesting story for a LinkedIn audience.
Respond in this exact format:
TOPIC: [one line title]
SUMMARY: [2-3 sentence summary]
KEYWORDS: [3-5 comma-separated keywords]
"""
        pick_response = _ask_groq(pick_prompt)
        print(f"📌 Picked story:\n{pick_response}\n")

    write_prompt = f"""
{VOICE_PROFILE}

Write a LinkedIn post about this AI news story:
{pick_response}

IMPORTANT: If the user shared this news themselves, write from THEIR perspective —
use "I came across", "I read about", "This caught my attention this week".
Make it feel like their genuine reaction, not a news report.

Structure:
- Hook: One surprising opening line
- What happened: 2-3 lines in plain English
- What most people are saying: 1-2 lines
- What I actually think: Your genuine take
- Closing question to invite comments

Constraints:
- Max 200 words. No emojis. Max 3 hashtags at the end. First person.
"""
    post_text = _ask_groq(write_prompt)
    return {
        "post_text": post_text,
        "topic": _extract_field(pick_response, "TOPIC"),
        "keywords": _extract_field(pick_response, "KEYWORDS"),
        "type": "News"
    }


# **Step 1 → Search the web**
# `_search("top AI news this week")` — fetch the top 5 AI news stories from the internet this week

# **Step 2 → Build the picker prompt**
# Combine `search_results` + `past_topics` into one prompt. Tell Ollama "here's what's happening this week, here's what we've already covered, pick the best story we haven't done yet"

# **Step 3 → First Ollama call — the Researcher**
# `_ask_ollama(pick_prompt)` — Ollama reads the news, checks past topics, picks the single best story and returns it in a structured format with TOPIC, SUMMARY and KEYWORDS

# **Step 4 → Build the writer prompt**
# Combine `VOICE_PROFILE` + `pick_response` into a second prompt. Tell Ollama "here's the story, here's my voice, write a LinkedIn post in this exact structure"

# **Step 5 → Second Ollama call — the Writer**
# `_ask_ollama(write_prompt)` — Ollama writes the full LinkedIn post following your voice profile and structure constraints

# **Step 6 → Return everything as a dictionary**
# Package up the post text, topic, keywords and type into a dictionary and hand it back to `main.py` which will save it to Notion and log it to Google Sheets



def run_concept_pipeline(past_topics: str, manual_note: str = "") -> dict:
    if manual_note:
        print(f"\n📝 Using your note: {manual_note}")

        # Skip the researcher step — write directly about what user mentioned
        pick_response = f"""
TOPIC: {manual_note}
SUMMARY: The user wants to explain this concept from their own learning experience this week.
KEYWORDS: AI, concepts, learning
"""
    else:
        print("\n🔍 Searching for AI concepts...")
        search_results = _search("AI concepts explained machine learning trends 2025")

        pick_prompt = f"""
Here are trending AI concepts:
{search_results}

Topics already covered (DO NOT repeat):
{past_topics}

Pick one concept that's useful, interesting, and not overexplained yet.
Respond in this exact format:
TOPIC: [concept name]
SUMMARY: [what it is in 2-3 sentences]
KEYWORDS: [3-5 comma-separated keywords]
"""
        pick_response = _ask_groq(pick_prompt)
        print(f"📌 Picked concept:\n{pick_response}\n")

    write_prompt = f"""
{VOICE_PROFILE}

Write a LinkedIn post explaining this AI concept:
{pick_response}

IMPORTANT: If this is something the user learned or explored personally this week,
write from THEIR perspective — use "I learned", "I explored", "I finally understood".
Make it feel like a personal insight, not a textbook explanation.

Structure:
- Hook: A relatable analogy or question
- The explanation: Simple, use an analogy
- Why it matters: One practical implication
- Key takeaway: One sentence they'll remember

Constraints:
- Max 220 words. No emojis. Max 3 hashtags at the end. First person.
"""
    post_text = _ask_groq(write_prompt)
    return {
        "post_text": post_text,
        "topic": _extract_field(pick_response, "TOPIC"),
        "keywords": _extract_field(pick_response, "KEYWORDS"),
        "type": "Concept"
    }


def run_tool_pipeline(past_topics: str, manual_note: str = "") -> dict:
    if manual_note:
        print(f"\n📝 Using your note: {manual_note}")

        # Skip the researcher step — user already told us what to write about
        pick_response = f"""
TOPIC: {manual_note}
SUMMARY: The user built or tried this themselves this week. Write the post from their personal experience.
KEYWORDS: AI, personal project, buildinpublic
"""
    else:
        print("\n🔍 Searching for AI tools...")
        search_context = _search("best new AI tools productivity 2025")

        pick_prompt = f"""
Context about AI tools:
{search_context}

Topics already covered (DO NOT repeat):
{past_topics}

Pick one genuinely useful AI tool to spotlight.
Respond in this exact format:
TOPIC: [tool name]
SUMMARY: [what it does and why it's interesting]
KEYWORDS: [3-5 comma-separated keywords]
"""
        pick_response = _ask_groq(pick_prompt)
        print(f"📌 Picked tool:\n{pick_response}\n")

    write_prompt = f"""
{VOICE_PROFILE}

Write a LinkedIn post about this:
{pick_response}

IMPORTANT: If this is something the user built or tried personally, 
write the post from THEIR experience — use "I built", "I tried", "I discovered".
Make it personal and specific, not generic.

Structure:
- Hook: A problem this solves or what made you try it
- What it is: 2-3 lines, plain English
- Your personal experience with it
- Who else should check it out

Constraints:
- Max 200 words. No emojis. Max 3 hashtags at the end. First person.
"""
    post_text = _ask_groq(write_prompt)
    return {
        "post_text": post_text,
        "topic": _extract_field(pick_response, "TOPIC"),
        "keywords": _extract_field(pick_response, "KEYWORDS"),
        "type": "Tool Spotlight"
    }


def _extract_field(text: str, field: str) -> str:
    for line in text.splitlines():
        if line.startswith(f"{field}:"):
            return line.replace(f"{field}:", "").strip()
    return "Unknown"


# Step 1 → Receive the full Ollama response and the field to find
# text = the full pick_response from Ollama containing TOPIC, SUMMARY and KEYWORDS. field = the specific thing we want to extract like "TOPIC" or "KEYWORDS"
# Step 2 → Split the response into individual lines
# text.splitlines() — breaks the full response into a list of separate lines:
# ["TOPIC: Google Uses AI to Predict Flash Floods",
#  "SUMMARY: Google is leveraging AI...",
#  "KEYWORDS: AI, flood prediction, Google"]
# Step 3 → Loop through each line one by one
# for line in text.splitlines() — go through each line looking for the one that starts with our field name
# Step 4 → Check if this is the line we want
# if line.startswith(f"{field}:") — if we're looking for "TOPIC" check if the line starts with "TOPIC:". If yes, this is our line.
# Step 5 → Remove the field label and clean up
# line.replace(f"{field}:", "") — strip out the "TOPIC:" part leaving just the value. Then .strip() removes any leftover spaces:
# "TOPIC: Google Uses AI..."  →  "Google Uses AI..."
# Step 6 → Return the extracted value
# return — hand back just the clean value to whoever called this function — in our case run_news_pipeline() which puts it in the dictionary
# Step 7 → Safety net if nothing found
# return "Unknown" — if the loop finishes without finding the field, return "Unknown" instead of crashing


def classify_note(note: str) -> str:
    if not note:
        return None

    prompt = f"""
You are a strict classifier for a LinkedIn AI post generator.

The user has provided this note: "{note}"

Your job is to classify it into ONE of these three categories — BUT ONLY if it is clearly about AI or technology:
- News → a recent AI/tech event, launch, announcement or development
- Concept → understanding or explaining an AI/tech concept or idea
- Tool Spotlight → an AI/tech tool, product or something they built

STRICT RULES:
- If the note has nothing to do with AI or technology → reply UNKNOWN
- If the note is vague, personal or unrelated to AI → reply UNKNOWN
- If you are not at least 80% confident → reply UNKNOWN
- Do NOT try to force a category if it doesn't fit

Reply with ONLY one of these four words: News, Concept, Tool Spotlight, UNKNOWN
No explanation. No punctuation. Just the word.
"""

    result = _ask_groq(prompt)
    
    # Clean up response in case LLM adds extra text
    result = result.strip()
    if "News" in result:
        return "News"
    elif "Concept" in result:
        return "Concept"
    elif "Tool Spotlight" in result:
        return "Tool Spotlight"
    else:
        return "UNKNOWN"