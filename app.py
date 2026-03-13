import streamlit as st
import streamlit.components.v1 as components
from agent import run_news_pipeline, run_concept_pipeline, run_tool_pipeline

st.set_page_config(
    page_title="LinkedIn AI Post Generator",
    page_icon="🤖",
    layout="centered"
)

# ── Hero Section ──────────────────────────────────────────
st.title("🤖 LinkedIn AI Post Generator")
st.markdown("""
Built by **Aakrati Bansal** — a personal AI agent that generates
3 ready-to-publish LinkedIn posts every week about AI.

This is not ChatGPT. Here is what makes it different:
""")

# ── 3 Differentiator Cards ────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **🔍 Searches the web**

    Finds real AI news
    from this week —
    not old training data
    """)

with col2:
    st.info("""
    **🧠 Has memory**

    Tracks past topics
    so it never repeats
    the same content
    """)

with col3:
    st.info("""
    **✍️ Knows your voice**

    Every post sounds
    like you — not like
    a generic AI
    """)

st.divider()

# ── How It Works Expander ─────────────────────────────────
with st.expander("⚙️ How does this work?", expanded=False):
    st.markdown("""
    Every week this agent does 5 things automatically:

    1. **Reads memory** — checks Google Sheet for topics already covered
    2. **Searches the web** — uses Tavily to find fresh AI news and tools
    3. **Picks the best angle** — AI researcher picks what's worth writing about
    4. **Writes the post** — AI writer crafts it in your personal voice
    5. **Saves everything** — drafts go to Notion, topics logged to Google Sheet

    **Tech used:** Python · Ollama (llama3.1) · Tavily Search · Notion API · Google Sheets API

    **This is a demo version** — in the full version posts are saved to Notion
    and topics are tracked in Google Sheets so the agent never repeats itself.
    """)

    st.markdown("### Agent Architecture")

    diagram = """
    <svg width="100%" viewBox="0 0 680 820" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M2 1L8 5L2 9" fill="none" stroke="#666" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </marker>
    </defs>

    <!-- TRIGGER -->
    <rect x="240" y="20" width="200" height="44" rx="8" fill="#f1efea" stroke="#888" stroke-width="0.5"/>
    <text x="340" y="42" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#2c2c2a">python main.py</text>
    <line x1="340" y1="64" x2="340" y2="100" stroke="#888" stroke-width="1.5" marker-end="url(#arrow)"/>

    <!-- MEMORY READ -->
    <rect x="190" y="100" width="300" height="56" rx="8" fill="#e1f5ee" stroke="#0f6e56" stroke-width="0.5"/>
    <text x="340" y="120" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#085041">memory.py</text>
    <text x="340" y="140" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#0f6e56">reads past topics from Google Sheet</text>
    <line x1="340" y1="156" x2="340" y2="196" stroke="#888" stroke-width="1.5" marker-end="url(#arrow)"/>

    <!-- PIPELINE CONTAINER -->
    <rect x="30" y="196" width="620" height="280" rx="12" fill="none" stroke="#ccc" stroke-width="1" stroke-dasharray="6 4"/>
    <text x="50" y="216" font-family="sans-serif" font-size="12" fill="#888">agent.py — 3 pipelines running in sequence</text>

    <!-- Pipeline 1 -->
    <rect x="50" y="224" width="170" height="56" rx="8" fill="#eeedfe" stroke="#534ab7" stroke-width="0.5"/>
    <text x="135" y="244" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#3c3489">News + Take</text>
    <text x="135" y="262" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#534ab7">top AI news this week</text>

    <!-- Pipeline 2 -->
    <rect x="255" y="224" width="170" height="56" rx="8" fill="#eeedfe" stroke="#534ab7" stroke-width="0.5"/>
    <text x="340" y="244" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#3c3489">Concept explainer</text>
    <text x="340" y="262" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#534ab7">trending AI concepts</text>

    <!-- Pipeline 3 -->
    <rect x="460" y="224" width="170" height="56" rx="8" fill="#eeedfe" stroke="#534ab7" stroke-width="0.5"/>
    <text x="545" y="244" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#3c3489">Tool spotlight</text>
    <text x="545" y="262" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#534ab7">best new AI tools</text>

    <!-- Arrows to web search -->
    <line x1="135" y1="280" x2="135" y2="320" stroke="#888" stroke-width="1.5" marker-end="url(#arrow)"/>
    <line x1="340" y1="280" x2="340" y2="320" stroke="#888" stroke-width="1.5" marker-end="url(#arrow)"/>
    <line x1="545" y1="280" x2="545" y2="320" stroke="#888" stroke-width="1.5" marker-end="url(#arrow)"/>

    <!-- Web search row -->
    <rect x="50" y="320" width="170" height="44" rx="8" fill="#faeeda" stroke="#ba7517" stroke-width="0.5"/>
    <text x="135" y="342" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#633806">Tavily web search</text>

    <rect x="255" y="320" width="170" height="44" rx="8" fill="#faeeda" stroke="#ba7517" stroke-width="0.5"/>
    <text x="340" y="342" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#633806">Tavily web search</text>

    <rect x="460" y="320" width="170" height="44" rx="8" fill="#faeeda" stroke="#ba7517" stroke-width="0.5"/>
    <text x="545" y="342" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#633806">Tavily web search</text>

    <!-- Arrows to ollama -->
    <line x1="135" y1="364" x2="135" y2="404" stroke="#888" stroke-width="1.5" marker-end="url(#arrow)"/>
    <line x1="340" y1="364" x2="340" y2="404" stroke="#888" stroke-width="1.5" marker-end="url(#arrow)"/>
    <line x1="545" y1="364" x2="545" y2="404" stroke="#888" stroke-width="1.5" marker-end="url(#arrow)"/>

    <!-- Ollama row -->
    <rect x="50" y="404" width="170" height="56" rx="8" fill="#faece7" stroke="#993c1d" stroke-width="0.5"/>
    <text x="135" y="424" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#4a1b0c">Ollama (llama3.1)</text>
    <text x="135" y="442" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#993c1d">pick + write post</text>

    <rect x="255" y="404" width="170" height="56" rx="8" fill="#faece7" stroke="#993c1d" stroke-width="0.5"/>
    <text x="340" y="424" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#4a1b0c">Ollama (llama3.1)</text>
    <text x="340" y="442" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#993c1d">pick + write post</text>

    <rect x="460" y="404" width="170" height="56" rx="8" fill="#faece7" stroke="#993c1d" stroke-width="0.5"/>
    <text x="545" y="424" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#4a1b0c">Ollama (llama3.1)</text>
    <text x="545" y="442" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#993c1d">pick + write post</text>

    <!-- Merge arrows -->
    <line x1="135" y1="460" x2="240" y2="530" stroke="#888" stroke-width="1.5" marker-end="url(#arrow)"/>
    <line x1="340" y1="460" x2="340" y2="530" stroke="#888" stroke-width="1.5" marker-end="url(#arrow)"/>
    <line x1="545" y1="460" x2="440" y2="530" stroke="#888" stroke-width="1.5" marker-end="url(#arrow)"/>

    <!-- Output layer -->
    <rect x="190" y="530" width="300" height="56" rx="8" fill="#e1f5ee" stroke="#0f6e56" stroke-width="0.5"/>
    <text x="340" y="550" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#085041">main.py — output layer</text>
    <text x="340" y="568" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#0f6e56">saves all 3 posts</text>

    <!-- Two output arrows -->
    <line x1="280" y1="586" x2="190" y2="650" stroke="#888" stroke-width="1.5" marker-end="url(#arrow)"/>
    <line x1="400" y1="586" x2="490" y2="650" stroke="#888" stroke-width="1.5" marker-end="url(#arrow)"/>

    <!-- Notion -->
    <rect x="60" y="650" width="240" height="56" rx="8" fill="#e6f1fb" stroke="#185fa5" stroke-width="0.5"/>
    <text x="180" y="670" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#042c53">Notion</text>
    <text x="180" y="688" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#185fa5">3 draft posts to review</text>

    <!-- Google Sheet -->
    <rect x="380" y="650" width="240" height="56" rx="8" fill="#eaf3de" stroke="#3b6d11" stroke-width="0.5"/>
    <text x="500" y="670" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#173404">Google Sheet</text>
    <text x="500" y="688" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#3b6d11">logs topics to memory</text>

    <!-- Memory feedback arrow -->
    <path d="M500 706 Q500 760 340 770 Q180 780 180 760 Q180 740 190 720" fill="none" stroke="#aaa" stroke-width="1" stroke-dasharray="5 4" marker-end="url(#arrow)"/>
    <text x="340" y="785" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#888">feeds back into memory next week</text>
    </svg>
    """

    components.html(diagram, height=840, scrolling=False)

st.divider()

# ── The 3 Post Types ──────────────────────────────────────
st.subheader("📬 3 Posts Generated Every Week")
st.markdown("""
| Post | What it does | Why it works on LinkedIn |
|---|---|---|
| 📰 News + Take | Top AI news + your opinion | Shows you're up to date |
| 💡 Concept Explainer | Explains an AI concept simply | Builds your credibility |
| 🔧 Tool Spotlight | Interesting AI tool to know | Gives practical value |
""")

st.divider()

# ── Generator ─────────────────────────────────────────────
st.subheader("🚀 Try It Now")

tool_note = st.text_input(
    "Built or tried something this week? (optional)",
    placeholder="e.g. I tried Cursor AI, it helped me write code 2x faster"
)

if st.button("✨ Generate This Week's Posts", use_container_width=True, type="primary"):

    past_topics = "No past topics. This is a demo — pick any fresh interesting topic."
    results = []

    progress = st.progress(0, text="Starting up...")

    with st.spinner("📰 Searching AI news and writing post 1 of 3..."):
        news = run_news_pipeline(past_topics)
        results.append(news)
        progress.progress(33, text="Post 1 done...")

    with st.spinner("💡 Finding AI concept and writing post 2 of 3..."):
        concept = run_concept_pipeline(past_topics)
        results.append(concept)
        progress.progress(66, text="Post 2 done...")

    with st.spinner("🔧 Spotlighting AI tool and writing post 3 of 3..."):
        tool = run_tool_pipeline(past_topics, manual_note=tool_note)
        results.append(tool)
        progress.progress(100, text="All 3 posts ready!")

    st.divider()
    st.subheader("✨ Your Posts Are Ready")

    icons = {"News": "📰", "Concept": "💡", "Tool Spotlight": "🔧"}
    descriptions = {
        "News": "Current AI news + your personal take",
        "Concept": "An AI concept explained simply",
        "Tool Spotlight": "An AI tool worth knowing about"
    }

    for result in results:
        icon = icons.get(result["type"], "📝")
        desc = descriptions.get(result["type"], "")

        with st.expander(
            f"{icon} {result['type']} — {result['topic']}",
            expanded=True
        ):
            st.caption(desc)
            st.text_area(
                label="Edit before copying to LinkedIn:",
                value=result["post_text"],
                height=220,
                key=result["type"]
            )
            st.caption(f"🔑 Keywords: {result['keywords']}")

    st.divider()
    st.success("🎉 Done! Edit the posts above and copy them directly to LinkedIn.")

    st.info("""
    **Want the full version?**

    The full agent saves drafts to Notion, tracks history in Google Sheets
    and can be scheduled to run every Monday automatically.

    Built with Python · Ollama · Tavily · Notion API · Google Sheets API
    """)

# ── Page Footer ───────────────────────────────────────────
st.divider()
st.caption("Built by Aakrati Bansal · Powered by Ollama + Tavily · Not just ChatGPT 🤖")