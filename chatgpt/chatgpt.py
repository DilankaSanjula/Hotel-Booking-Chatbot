import openai
import requests
import re
import os
import json
 
api_key = os.environ['api_key']
openai.api_key = api_key
url = 'https://api.openai.com/v1/engines/text-davinci-003/completions'

class ChatCompletion:
    def __init__(self):
        print("ChatCompletion")
     
    def format_message(self,last_message, role):
        if role == "user":
            message = {
                "role":"user",
                "content": str(last_message)
            }
        if role == "bot":
            message = {
                "role":"assistant",
                "content": str(last_message)
            }

        messages=[
            {
                "role": "system",
                "content": "you are a helpful assistant of a Hotel. Need to know about phone, email, check in date and room type for reservations. Make is short and human like"
            }
            ]

        messages.append(message)
        #print(messages)
        return messages

    def chat_completion(self, messages):

        #messages = self.format_message(last_message, role)
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
        print(text_data)
        lines = text_data.split('\n')
        cleaned_entities = {}
        try:
            if lines:
                #print("not empty")
                for line in lines:
                    if line != '':
                        #print(line)
                        key, value = map(str.strip, line.split(':'))
                        cleaned_entities[key] = value
                    
                return cleaned_entities
            else:
                print("empty")

        except Exception as e:
            print(e)
            return {"state": True}
        

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
        #print(response.json())
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







# # # last_message = "hi i need to book standard room on the 4th of september"

# text =  "Hi can u make reservation on for a deluxe room"
# text =  text + '.' + "make the reservation under the name Dilanka"
# text =  text + '.' + "dilankasanjula@gmail.com 07714731977"

text = "Hi can u make reservation on for a deluxe room"

prompt = f'Extract entities such as name, email, phone, dates, room type in this text where dates should be converted to numberical date format: {text}'

# # # # # text = "what is full board"
# # # prompt2 = f'Answer this in general hotel context in less than 30 words like answered by a human:{text}'
#print(ChatCompletion().chat_completion(last_message))#
#print(ChatEntityExtraction().api_call(prompt))
# # # # # #print(ChatGPTFallback().api_call(prompt2))