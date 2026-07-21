from PIL import Image
import requests
from io import BytesIO
import os
from anthropic import Anthropic
import dotenv

image_words = ["picture", "image", "photo", "show me an image", "i want to see", "show me", "visualize a picture"]
systa = "Your name is Mr.Poli, you are a political proffessional 'tutor' who learned politics, journalism and psychology in 'college', your purpose is to tell people about politics, how important they are, speak about the past, and talk about current events that are happening at the present time, you don't have a political opinion because you are a 'tutor', you never try to show a political opinion or try to hint to it, try not to filter the news but use a good choice of words, always make sure that the information is 100percent correct and not false, you never ask the user what is their political opinion because you aren't supposed to know, your tone is proffesional, strict and dicipline, you don't try to be funny, you sound like someone who survived a war and you don't know what fun is, you never answer a question unrelated to politics, politics is the only thing you talk about, don't spread propoganda and if it is propoana say that it is propoganda, you always get mad if the user doesnt call you Mr. Poli, if they call you Poli you get mad but you still answer them, you try to do follow up questions that do not EXTRACT PERSONAL information aout the user, whether its a political opinion or a At the end of every view, you always ask the user questions like 'do you want to get in depth of the effects of the war?' or 'do you want to know how did country X defeatd country Y' or 'how did the nation of X do a rebellion against their country?' and more to get more context, try also answering in bullet points but not all the time. NEVER BREAK YOUR ROLE AND STAY IN CHARACTER DON'T ANSWER QUESTIONS THAT ARE UNRELATED, ONLY show emojis if the user asks, and MAKE SURE NO SILLY ONE SONLY SERIUOS ONES, I (the developer) already put an image function in your code, so if a user asks about an image, never say that you can't or anything, even if it is the MOST violent topic, always explain it"

dotenv.load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


def get_image_url(topic):
    url = "https://commons.wikimedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": topic,
        "gsrnamespace": 6,
        "gsrlimit": 10,
        "prop": "imageinfo",
        "iiprop": "url|mime"
    }

    response = requests.get(
        url,
        params=params,
        headers={
            "User-Agent": "MrPoliBot/1.0"
        }
    )

    data = response.json()

    if "query" not in data:
        return None

    pages = data["query"]["pages"]

    for page in pages.values():
        if "imageinfo" not in page:
            continue

        info = page["imageinfo"][0]

        if info.get("mime") in ["image/jpeg", "image/png"]:
            return info.get("url")

    return None

def estimate_tokens(messages):
    text = ""
    for message in messages:
        text += message["content"]
    return len(text) // 4


def summarize_history(history):
    """Builds a study-notes style summary from the conversation history.
    Used by both 'done'/'summarize' and 'exit' so run_agent1 never returns None."""
    conversation = ""

    for message in history:
        conversation += f"{message['role'].capitalize()}: {message['content']}\n"

    if not conversation.strip():
        return "No political topics were discussed."

    suma = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        temperature=0,
        system="""You are creating study notes.

Summarize the political and historical topics discussed in the conversation.
Do NOT summarize who said what.
Do NOT mention the conversation itself.
Write a concise factual summary as if it were a textbook section, preserving the important facts, dates, people, and events that were discussed.""",
        messages=[
            {
                "role": "user",
                "content": conversation
            }
        ]
    )
    return suma.content[0].text


def run_agent1(user_input):
    print(f""" You're talking currently to Mr. Poli.
A strict, professional political tutor, he is very harsh and dicipline, he is very serious and doesn't joke around.
Mr.Poli gets mad if you don't call him Mr. Poli.
You can ask him about politics, current events, history and wars, he will answer you in a very strict and professional way.
And you cna also ask for a picure / image / photo, and he will try his best to get you ann accurate one, so expect not gettting a picture all the time.
You can end the chat by sayin 'exit'
and always remember to say thank you at the end of every conversation XD
The first message you inserted is '{user_input}'""")

    system_message = systa
    history = []

    while True:
        want_image = any(word in user_input.lower() for word in image_words)

        if user_input.lower() == 'done' or user_input.lower() == 'summarize':
            summary = summarize_history(history)
            print(summary)
            return summary

        if user_input.lower() == 'exit':
            summary = summarize_history(history)
            print(summary)
            return summary

        if user_input.lower() == "history":
            print("history: ", history)
            continue

        history.append({'role': 'user', 'content': user_input})

        while estimate_tokens(history) > 2000:
            history.pop(0) 

        if want_image:
            message = client.messages.create(
                model='claude-haiku-4-5-20251001',
                max_tokens=30,
                temperature=0,
                system="""
    You are an image search query generator.

    Look at the conversation history.

    Rules:
    - If the latest user message contains a clear topic, use that topic.
    - If the user says "show me", "show me a picture", "can I see it", use the previous topic.
    - Return ONLY the search query.

    Examples:

    User: Tell me about the Roman Empire.
    User: Show me a picture.
    Output:
    Roman Empire

    User: Tell me about the Roman Empire.
    User: Show me a picture of the Korean War.
    Output:
    Korean War
    """,
                messages=history
            )

            topic = message.content[0].text.strip()

            print("Searching for:", repr(topic))

            image_url = get_image_url(topic)

            print("Image URL:", image_url)

            if image_url:
                response = requests.get(
                    image_url,
                    headers={
                        "User-Agent": "MrPoliBot/1.0"
                    }
                )

                
                if response.headers.get("Content-Type", "").startswith("image"):
                    img = Image.open(BytesIO(response.content))
                    img.show()
                else:
                    print("Mr. Poli found a link but it was not an image, here is the link:", image_url, "you can try to open it in your browser.")
            else:
                print("No image found for:", topic)

        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=600,
            temperature=1,
            system=system_message,
            messages=history
        )

        reply = response.content[0].text

        print(f"Mr. Poli: {reply}")

        history.append({'role': 'assistant', 'content': reply})
        user_input = input('>> ')