import openai
import requests
import re
import os
 
api_key = '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'
openai.api_key = api_key
url = 'https://api.openai.com/v1/engines/text-davinci-003/completions'

class ChatCompletion:
    def __init__(self):
        print("ChatCompletion")
     
    def format_message(self,last_message):

        last_message = {
            "role":"user",
            "content": str(last_message)
        }

        messages=[
            {
                "role": "system",
                "content": "you are a helpful assistant"
            }
            ]

        messages.append(last_message)
        print(messages)
        return messages

    def chat_completion(self, last_message):

        messages = self.format_message(last_message)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response


class ChatEntityExtraction:
    def __init__(self):
        print("EntityExtraction")
     
    def extract_entities(self,response):

        response_data = response.json()
        text_data = response_data['choices'][0]['text']
        lines = text_data.split('\n')
        cleaned_entities = {}

        for line in lines:
            if line != '':
                key, value = map(str.strip, line.split(':'))
                cleaned_entities[key] = value
            
        return cleaned_entities

    def api_call(self, prompt):
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        data = {
            'prompt': prompt,
            'max_tokens': 50,  
            'temperature': 0.7,  
            'n': 1
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            entities_response = self.extract_entities(response)
            return entities_response


class ChatGPTFallback:
    def __init__(self):
        print("Fallback")
     

    def api_call(self, prompt):
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        data = {
            'prompt': prompt,
            'max_tokens': 50,  
            'temperature': 0.7,  
            'n': 1
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            text = response.json()['choices'][0]['text']
            cleaned_text = text.replace('\n', '')
            return cleaned_text







last_message = "hi i need to book standard room on the 4th of september"

text = "hi i need to book a standard room on the 8th of september, name is Dilanka Sanjula,0771473177, dilanka@gmail.com"
prompt = f'Extract entities such as name, email, phone, dates, room type in this text where dates should be converted to numberical date format: {text}'

text = "what is full board"
prompt2 = f'Answer this in general hotel context in less than 30 words like answered by a human:{text}'
#print(ChatCompletion().chat_completion(last_message))
#print(ChatEntityExtraction().api_call(prompt))
#print(ChatGPTFallback().api_call(prompt2))