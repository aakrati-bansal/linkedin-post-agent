import os
from groq import Groq
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"


def research_and_write(topic: str) -> str:
    result = tavily.search(topic,max_results = 5)
    l=[]
    for r in result.get("results",[]):
        l.append(f"{r.get('title','')}-{r.get('content','')}")
    search_result = "\n".join(l)
    
    response = groq_client.chat.completions.create(
        model = MODEL,
        messages = 
        [
            {
                "role":"system",
                "content":"""You are a LinkedIn content writer.
Write a short LinkedIn post — max 150 words.
No headers. No bullet points. No bold text.
First person. Conversational tone.
End with one question to invite comments.
Max 3 hashtags at the end."""
            },
            {
                "role":"user",
                "content":search_result
            }
        ],
        temperature = 0.9,
        max_tokens = 1024
    )
    
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    post = research_and_write("latest AI tools 2025")
    print(post)