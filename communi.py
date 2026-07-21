from app1 import run_agent1
from app2 import run_agent2

def communi(topic):
    ttopic = "Hey Mr. Poli, I am preparing a topic and I want to understand it truely, the topic is :" + topic
    print("You will soon start talking to the Mr. Poli, once you're done type done!")
    summary = run_agent1(ttopic)

    if not summary:
        summary = "No summary was generated."

    print("Summary now is being transported to Ms. Malak, you will make your debate plan with her!")
    tttopic = "I have a debate / MUN simulation, this is the summary of the topic :" + summary + " help me make a plan!"
    run_agent2(tttopic)

communi("roman empire")