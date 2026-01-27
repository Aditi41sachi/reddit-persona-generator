import os
import re

import google.generativeai as genai
import praw
from dotenv import load_dotenv

load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
GOOGLE_GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')

missing_vars = [
    var for var in [REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, GOOGLE_GEMINI_API_KEY]
    if not var
]
if missing_vars:
    raise EnvironmentError(f'Missing one or more required environment variables: {", ".join(missing_vars)}. Please check your .env file.')

genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

while True:
    user_url = input('Enter the Reddit user profile URL (e.g., https://www.reddit.com/user/username): ').strip()
    try:
        match = re.match(r"https?://(?:www\.)?reddit\.com/user/([A-Za-z0-9_\-]+)", user_url)
        if not match:
            raise ValueError('Invalid Reddit user profile URL format.')
        
        username = match.group(1) 
        break
    except Exception as e:
        print(f"Error: {e}. Please try again.")

try:
    redditor = reddit.redditor(username)
except Exception as e:
    print(f"Failed to initialize Redditor object for {username}: {e}")
    exit(1)

scraped_data = []
print(f"Scraping comments and posts for user: {username}...")

try:
    for comment in redditor.comments.new(limit=50):
        scraped_data.append({
            'type': 'comment',
            'content': comment.body,
            'url': f"https://www.reddit.com{comment.permalink}"
        })
    print(f"Scraped {len([d for d in scraped_data if d['type'] == 'comment'])} comments.")
except Exception as e:
    print(f"Error scraping comments: {e}")

try:
    for submission in redditor.submissions.new(limit=50):
        content = submission.selftext if submission.is_self else submission.url
        scraped_data.append({
            'type': 'post',
            'content': f"{submission.title}\n{content}", 
            'url': f"https://www.reddit.com{submission.permalink}"
        })
    print(f"Scraped {len([d for d in scraped_data if d['type'] == 'post'])} posts.")
except Exception as e:
    print(f"Error scraping posts: {e}")

print(f"Total items scraped: {len(scraped_data)}")

full_text_for_llm = ""
for item in scraped_data:
    full_text_for_llm += f"---NEW_ITEM---\nType: {item['type']}\nURL: {item['url']}\nContent: {item['content']}\n\n"

MAX_LLM_INPUT_LENGTH = 10000 
if len(full_text_for_llm) > MAX_LLM_INPUT_LENGTH:
    print(f"Warning: Scraped data exceeds {MAX_LLM_INPUT_LENGTH} characters. Truncating to prevent token limit issues.")
    full_text_for_llm = full_text_for_llm[:MAX_LLM_INPUT_LENGTH]

llm_prompt = f"""
You are an advanced AI assistant specializing in generating comprehensive user personas based on provided text data.
Your task is to analyze the "Reddit User Content" provided below and generate a detailed persona for the user.

*Persona Characteristics (For EACH characteristic, you MUST cite the EXACT comment/post content snippet and its corresponding URL. If a characteristic cannot be inferred, state "Not inferable from provided data."):*

1.  *Name:* (If inferable, otherwise "Not inferable from provided data.")
    * Citation: [Snippet] (URL)

2.  *Demographics (Age, Gender, Location):* (If inferable, otherwise "Not inferable from provided data.")
    * Age Citation: [Snippet] (URL)
    * Gender Citation: [Snippet] (URL)
    * Location Citation: [Snippet] (URL)

3.  *Interests/Hobbies:* (List specific interests/hobbies with citations.)
    * Citation: [Snippet] (URL)

4.  *Values/Personality Traits:* (Describe values or personality traits with citations.)
    * Citation: [Snippet] (URL)

5.  *Commonly Discussed Topics:* (List topics the user frequently discusses with citations.)
    * Citation: [Snippet] (URL)

6.  *Communication Style:* (Describe their writing style, tone, use of slang, etc., with citations.)
    * Citation: [Snippet] (URL)

---
*Reddit User Content:*

{full_text_for_llm}
"""


user_persona_output = "Persona generation failed."
if scraped_data: 
    try:
        print("Calling Google Gemini API to generate persona...")
        response = llm_model.generate_content(llm_prompt)
        user_persona_output = response.text
        print("Persona generated successfully.")
    except Exception as e:
        user_persona_output = f"Error calling Google Gemini API: {e}\n" \
                              "Possible reasons: Invalid API key, network issues, or content policy violation."
        print(user_persona_output)
else:
    user_persona_output = "No Reddit data scraped to generate a persona."
    print(user_persona_output)

output_filename = f"{username}_persona.txt"
try:
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"--- User Persona for {username} ---\n\n")
        f.write(user_persona_output)
        f.write(f"\n\n--- End of Persona for {username} ---")
    print(f"\nUser persona saved to {output_filename}")
except IOError as e:
    print(f"Error saving persona to file {output_filename}: {e}")
