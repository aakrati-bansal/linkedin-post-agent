import os
import argparse
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client as NotionClient

# argparse — lets you pass extra options to your script from the terminal like --tool-note
# NotionClient — imports Client from notion but renames it to NotionClient so it's clearer what it does

from memory import get_past_topics, log_post
from agent import run_news_pipeline, run_concept_pipeline, run_tool_pipeline

# main.py starts
#     ↓
# reads memory from Sheet
#     ↓
# runs 3 pipelines (passing memory in)
#     ↓
# saves to Notion
#     ↓
# logs back to Sheet
#     ↓
# prints to terminal

load_dotenv()

notion = NotionClient(auth=os.getenv("NOTION_API_KEY"))
NOTION_DB_ID = os.getenv("NOTION_DATABASE_ID")


def save_to_notion(post_type: str, topic: str, post_text: str):
    now = datetime.now()
    title = f"[{post_type}] {topic} — Week of {now.strftime('%b %d, %Y')}"

    notion.pages.create(
        parent={"database_id": NOTION_DB_ID},
        properties={
            "Name": {
                "title": [{"text": {"content": title}}]
            },
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": post_text}}]
                }
            }
        ]
    )
    print(f"✅ Saved to Notion: {title}")

# Step 1 → Build title string with post type, topic and date
# Step 2 → Tell Notion which database to create the page in
# Step 3 → Set the page title using Notion's required format
# Step 4 → Add the post text as a paragraph inside the page
# Step 5 → Print confirmation to terminal

def main():
    parser = argparse.ArgumentParser(description="LinkedIn AI Post Generator")
    parser.add_argument(
        "--tool-note",
        type=str,
        default="",
        help="Optional note about something you built this week"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("🤖 LinkedIn AI Agent — Weekly Run")
    print(f"📅 {datetime.now().strftime('%A, %B %d, %Y')}")
    print("=" * 60)

    # Step 1 — Load memory
    print("\n📚 Reading past topics from Google Sheet...")
    past_topics = get_past_topics(limit=12)
    print(f"Found history:\n{past_topics}\n")

    results = []

    # Step 2 — Run all 3 pipelines
    print("\n" + "─" * 60)
    print("📰 PIPELINE 1: News + Take")
    print("─" * 60)
    news = run_news_pipeline(past_topics)
    results.append(news)

    print("\n" + "─" * 60)
    print("💡 PIPELINE 2: Concept Explainer")
    print("─" * 60)
    concept = run_concept_pipeline(past_topics)
    results.append(concept)

    print("\n" + "─" * 60)
    print("🔧 PIPELINE 3: Tool Spotlight")
    print("─" * 60)
    tool = run_tool_pipeline(past_topics, manual_note=args.tool_note)
    results.append(tool)

    # Step 3 — Save to Notion + log to Sheet
    print("\n" + "=" * 60)
    print("💾 Saving to Notion and logging to Google Sheet...")
    print("=" * 60)

    for result in results:
        save_to_notion(result["type"], result["topic"], result["post_text"])
        log_post(
            post_type=result["type"],
            topic=result["topic"],
            keywords=result["keywords"],
            status="Draft"
        )

    # Step 4 — Print all posts to terminal
    print("\n" + "=" * 60)
    print("✨ THIS WEEK'S POSTS — REVIEW BEFORE PUBLISHING")
    print("=" * 60)

    for result in results:
        print(f"\n{'─' * 40}")
        print(f"📌 {result['type'].upper()}: {result['topic']}")
        print(f"{'─' * 40}")
        print(result["post_text"])

    print("\n\n🎉 Done! Review the posts in Notion and publish when ready.")


if __name__ == "__main__":
    main()
    # if __name__ == "__main__" means "only run this code if I am the main file being executed, not if I'm being imported by someone else."
    

# Step 1 → Set up --tool-note argument
# Allows you to optionally pass a personal note from the terminal when running the script
# Step 2 → Print the header
# Shows the date and confirms the agent is running
# Step 3 → Read memory
# get_past_topics() fetches past topics from Google Sheet before anything else runs
# Step 4 → Run all 3 pipelines
# Calls run_news_pipeline, run_concept_pipeline, run_tool_pipeline — each gets past_topics so Ollama avoids repetition
# Step 5 → Collect results
# Each pipeline returns a dictionary — all 3 get appended to results list
# Step 6 → Save and log
# Loop through results — save each post to Notion and log each topic back to Google Sheet
# Step 7 → Print to terminal
# Loop through results again — print all 3 posts so you can review them immediately
# Step 8 → Safety guard
# if __name__ == "__main__" ensures main() only runs when you execute the file directly