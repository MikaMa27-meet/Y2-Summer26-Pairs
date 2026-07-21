#its importand to download PIL / Pillow and requests in the terminal, do pip install pillow & pip install requests, or you can do python -m pip install pillow and python -m pip install requests, if it doesnt work fix it on ur own idc. :D



from app1 import run_agent1
from app2 import run_agent2
from communi import communi 

while True:
    agent_choose = input("Which agent do you want to run?\nAgent1 is strict, dicipline and goes in depth of analayizing context.\nWhile agent2 is more fun and silly, very cutesty and is caring political support mentor.\n Or you can access a special feature if you have an MUN confrence or a Debate competition, you give the bot your role and topic and it tunrs it into a plan with context and information you need to know, type 3 to use this feature.\nType '1' for agent1, type '2' for agent2, type '3' for the special featrure or 'exit' to exit : ")
    if agent_choose == '1':
        run_agent1()
        break

    elif agent_choose == '2':
        run_agent2()
        break

    elif agent_choose == '3':
        topic = input("What topic do you want to turn into a plan? ")
        communi(topic)
        break
        
    elif agent_choose == 'exit':
        print("Exiting the program..")
        break

    else:
        print("Invalid input, please try again and insert a valid input..")




#its importand to download PIL / Pillow and requests in the terminal, do pip install pillow & pip install requests, or you can do python -m pip install pillow and python -m pip install requests, if it doesnt work fix it on ur own idc. :D
