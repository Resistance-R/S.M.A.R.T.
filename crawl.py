import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from io import BytesIO
import requests
import time

import ollama

def Generate_search_query(command):
    response_of_query = ollama.chat(model='llama3:8b', messages=[
        {
            'role' : 'system',
            'content' : f"""You are an AI agent that generates search keywords
                            from user commands for crawling images.
                            Your task is to extract the most relevant and 
                            accurate search keyword(s) from the user's command.
                            Only provide the keyword(s) without any additional explanation or text.
                            For example, if the user command is 'I want to crawal the images of band Metallica', 
                            you should respond with 'band Metallica'."""
        },

        {            
            'role' : 'user',
            'content' : f'{command}',
        },
    ])    

    search_word = response_of_query['message']['content']

    return search_word

def Generate_number(command):
    generated_number = ollama.chat(model='llama3:8b', messages=[
        {
            'role' : 'system',
            'content' : f"""Your task is generating number from user's command.
                            The number you generate is the number of times you want to save the image.
                            Generate the number of pictures the user wants to store.
                            The generated number must be an integer.
                            If the command does not specify or is unclear
                            about the number of photos to be saved, answer '5'.
                            Only provide the number without any additional explanation or text.
                            For example, if the user command is 'I want to crawal the 10 images of band Metallica', 
                            you should respond with '10'."""
        },

        {            
            'role' : 'user',
            'content' : f'{command}',
        },
    ]) 

    img_num = generated_number['message']['content']

    return int(img_num)

####################################
"""
CRAWL IMGS
"""
####################################

def get_image_urls(query, max_links_to_fetch):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    search_url = f"https://www.google.com/search?tbm=isch&q={query}"
    driver.get(search_url)

    image_urls = set()
    thumbnail_results = driver.find_elements(By.CSS_SELECTOR, ".H8Rx8c img")

    for img in thumbnail_results[:max_links_to_fetch]:
        try:
            img.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error clicking image: {e}")
            continue
        
        images = driver.find_elements(By.CSS_SELECTOR, "img.sFlh5c")
        for image in images:
            if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                image_urls.add(image.get_attribute('src'))

        if len(image_urls) >= max_links_to_fetch:
            break

    driver.quit()
    return list(image_urls)

####################################
"""
SAVE IMGS
"""
####################################

def save_images(keyword, image_urls, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img_format = img.format.lower()
            img.save(os.path.join(folder_path, f"{keyword}_{i}.{img_format}"))
            print(f"Saved image, {keyword}_{i}.{img_format}")
        except Exception as e:
            print(f"Could not save image, {keyword}_{i}: {e}")