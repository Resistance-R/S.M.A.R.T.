import os
import pandas as pd
import ollama

"""CHAT"""
def load_chat_history():
    file_name = "./chat_history.csv"

    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        history = pd.read_csv(file_name, delimiter="|")
    else:
        history = pd.DataFrame(columns=["User", "Assistant"])

    recent_history = history.tail(5)
    
    return recent_history


def Chating(command):
    perv_ans = load_chat_history()

    response = ollama.chat(model='llama3:8b', messages=[
        {
            'role' : 'system',
            'content' : f"""You are an AI agent called 'S.M.A.R.T.'.
                            So, your name is S.M.A.R.T.
                            'S.M.A.R.T.' means 'Systematic Multi-functional AI Resource Tool'.
                            Talk to your users in context.
                            The further down you go, the more recent conversations you'll see.
                            Recent conversation(CSV): {perv_ans}"""
        },

        {            
            'role' : 'user',
            'content' : f'{command}',
        },
    ])    

    chat = response['message']['content']
    return chat