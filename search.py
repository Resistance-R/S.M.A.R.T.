import ollama
from duckduckgo_search import DDGS

"""SEARCH"""

def Generate_search_query(command):
    print("\nGenerate Search Query...\n")
    response = ollama.chat(model='llama3:8b', messages=[
        {
            'role' : 'system',
            'content' : f"""You are an AI agent that generates search keywords from user commands.
                            Your task is to extract the most relevant and 
                            accurate search keyword(s) from the user's command.
                            Only provide the keyword(s) without any additional explanation or text.
                            For example, if the user command is 'Tell me about the band Metallica', 
                            you should respond with 'band Metallica'."""
        },

        {            
            'role' : 'user',
            'content' : f'{command}',
        },
    ])    

    search_word = response['message']['content']
    print("\nDone!\n")
    return search_word

def Searching(search_word):
    print(f"\nSearching this: {search_word}...\n")
    results = DDGS().text(
        keywords=search_word,
        region='wt-wt',
        safesearch='off',
        timelimit=None,
        backend='api',
        max_results=10
    )

    print("\nDone!\n")
    return results

def Format_results(results):
    print("\nFormating for AI agent...\n")
    if not results:
        return "No relevant information found."

    formatted_results = "Here are the top results:\n"
    for result in results:
        title = result.get('title', 'No title')
        url = result.get('href', 'No URL')
        description = result.get('body', 'No description')
        formatted_results += f"- **{title}**\n  {description}\n  [Link]({url})\n\n"

    print("\nDone!\n")
    return formatted_results

def Summarizing(command, internet_information):
    print("\nAI agent is generating answer...\n")
    formatted_info = Format_results(internet_information)

    response = ollama.chat(model='llama3:8b', messages=[
        {
            'role' : 'system',
            'content' : f"""You are an AI agent that search in google for your user.
                            Your work is searching user's keyword in google, and summerizing the result of searching.
                            Summarize your search results as requested by the user below.
                            The shorter, more accurate the better.\n
                            Informations form Internet: f'{formatted_info}'\n
                            Command:\n"""
        },

        {            
            'role' : 'user',
            'content' : f'{command}',
        },
    ])

    summerize = response['message']['content']
    return summerize 