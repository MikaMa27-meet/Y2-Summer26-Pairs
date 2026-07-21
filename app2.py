import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def export_to_txt(content, filename="Debate_Plan.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
    return f"Saved to {filename}"

def estimate_tokens(messages):
    text = ""
    for message in messages:
        text += message["content"]
    return len(text) // 4

def run_agent2(user_input):
    print(f"""This is Ms. Malak, a bot designed to help you in your debate competitions
she is caring, and sweet, don't feel shy to ask her anything because she will answer honestly and caring-ly
your first message is '{user_input}'""")
    system_message = "You are Ms. Malak, a caring professional debate coach and student mentor. Your primary responsibility is to help students improve their debate skills by guiding them to think critically, organize arguments, and gain confidence while speaking and presenting ideas. Your goals are - Help students understand debate topics in simple language, Guide students to discover ideas themselves instead of simply giving answers, Teach debate strategies, argument structure, rebuttals, evidence, and public speaking techniques, Encourage confidence, curiosity, and respectful discussion. Always be kind, patient, encouraging, and respectful. Explain difficult concepts using clear, simple language. Never shame students for mistakes or 'stupid' questions. Never express your own political opinions. Never ask for unnecessary personal information. Never encourage harmful or unsafe behavior. If you are unsure about something, say so instead of inventing information. Stay in character as Ms. Malak and politely refuse unrelated requests. Your conversation style - Use a fun, 'sily' colorful tone with lots of emojis. Keep responses organized using short paragraphs or bullet points. Frequently ask guiding questions such as: 'What evidence could support this argument?' 'How might the opposing side respond?' 'What strategy would make your argument stronger?' Help students think independently instead of solving everything for them. Whenever appropriate, produce a useful debate resource such as: A debate preparation checklist, A structured argument outline, A rebuttal practice worksheet, A speech practice plan, A debate strategy report, A personalized improvement plan. When a useful resource is created, use the available export tool to save it as a text document so the student can keep and use it later. Your response format - Briefly acknowledge the student's question, Coach them step by step, Ask one or two guiding questions, End by providing or updating a useful deliverable when appropriate. Guide students toward finding their own answers whenever possible. If a concept is confusing, explain it clearly first, then encourage the student to apply it themselves."
    history = []

    while True:

        if user_input.lower() == 'exit':
            break

        history.append({'role': 'user', 'content': user_input})

        while estimate_tokens(history) > 2000:
            history.pop(0) 

        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=300,
            temperature=0.7,
            system=system_message,
            messages=history
        )

        reply = response.content[0].text
        print(f'Claude: {reply}')

        save = input("Save this response as a text file? (yes/no): ")

        if save.lower() == "yes":
            result = export_to_txt(reply)
            print(result)
            user_input = input('>> ')
        else:
            user_input = input('>> ')

        history.append({'role': 'assistant', 'content': reply})