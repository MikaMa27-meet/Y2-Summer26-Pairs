from app1 import run_agent1
from app2 import run_agent2

while True:
    agent_choose = input("Which agent do you want to run?\nAgent1 is strict, dicipline and goes in depth of analayizing context.\nWhile agent2 is more fun and silly, very cutesty and is caring political support mentor.\nType '1' for agent1, type '2' for agent2 or 'exit' to exit : ")
    if agent_choose == '1':
        run_agent1()
        break

    elif agent_choose == '2':
        run_agent2()
        break

    elif agent_choose == 'exit':
        print("Exiting the program..")
        break

    else:
        print("Invalid input, please try again and insert a valid input..")
