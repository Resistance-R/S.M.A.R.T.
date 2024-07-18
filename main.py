import os
import time
import threading
import ollama
import pandas as pd
import chat
import search
import crawl

file_name = "./chat_history.csv"

def saving_conversation(Q, A):
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        history = pd.read_csv(file_name, delimiter="|")
    else:
        history = pd.DataFrame(columns=["User", "Assistant"])
    data = {
        'User' : [Q],
        'Assistant' : [A],
    }

    new_data_df = pd.DataFrame(data)
    updated_history = pd.concat([history, new_data_df], ignore_index=True)
    updated_history.to_csv(file_name, sep="|", index=False)

def analyze_command(command):
    response = ollama.chat(model='llama3:8b', messages=[
        {            
            'role' : 'system',
            'content' : f"""Classify the following command into one of the categories: 
                            'search', 'crawl', 'chat'.
                            \nJust enter A ONE WORD in above words.
                            \n\nCommand: {command}\nCategory:""",
        },
    ])

    category = response['message']['content'].strip().lower()
    return category

def execute_command(command):
    category = analyze_command(command)

    if category == 'search':
        user_ask = command
        search_word = search.Generate_search_query(user_ask)
        searching_google = search.Searching(search_word)
        summarized_result = search.Summarizing(user_ask, searching_google)
        return f"\n\nIt is the result what searched '{command}' in google.\n\nSearch Qurey: {search_word}\n\n{summarized_result}"

    elif category == 'crawl':
        user_ask = command
        query = crawl.Generate_search_query(user_ask)
        max_links_to_fetch = crawl.Generate_number(user_ask)
        image_urls = crawl.get_image_urls(query, max_links_to_fetch)
        folder_path = "./temp/"

        print(f"Found {len(image_urls)} image URLs:")
        for url in image_urls:
            print(url)

        crawl.save_images(query, image_urls, folder_path)

        return f"This is results that I crawled the things according to your command: {command}"

    else:
        prompt = command
        answer = chat.Chating(prompt)
        return f"\nAnswer of S.M.A.R.T.:\n{answer}"

def loading_animation():
    pers = ['-', '\\', '|',  '/']
    idx = 0
    while loading:
        print(f"\rGenerating Answers... {pers[idx % len(pers)]}", end='', flush=True)
        idx += 1
        time.sleep(0.1)

global loading

####################################
"""
MAIN
"""
####################################

while True:
    command = str(input("\nEnter Your Prompt: "))

    if command == "!exit":
        break

    loading = True
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()
    
    response = execute_command(command)

    saving_conversation(command, response)

    loading = False
    loading_thread.join()

    print("\r" + " " * 20, end='\r')

    print(response)