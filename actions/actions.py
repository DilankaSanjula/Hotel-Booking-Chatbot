from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import json
from chatgpt.chatgpt import *
import random

class ActionCheckAvailability(Action):

    def name(self) -> Text:
        return "action_check_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entities = tracker.latest_message.get("entities", [])
        print(entities)
        hotel_endpoint = "http://35.168.216.250:7005/availability"

        if entities:
            if entities[0]['value'] == 'standard':
                json_obj = {"room_type": "standard"}
                standard_number = requests.post(hotel_endpoint, json = json_obj).json()

                dispatcher.utter_message(text=f"We are pleased to say that {standard_number} standard rooms are available at the moment")

            if entities[0]['value'] == 'deluxe':
                json_obj = {"room_type": "deluxe"}
                deluxe_number = requests.post(hotel_endpoint, json = json_obj).json()
                dispatcher.utter_message(text=f"We are pleased to say that {deluxe_number} deluxe rooms are available at the moment")

            if entities[0]['value'] == 'suite':
                json_obj = {"room_type": "suite"}
                suite_number = requests.post(hotel_endpoint, json = json_obj).json()
                dispatcher.utter_message(text=f"We are pleased to say that {suite_number} suite rooms are available at the moment")
        else:
            
            json_obj = {"room_type": "standard"}
            standard_number = requests.post(hotel_endpoint, json = json_obj).json()
            json_obj = {"room_type": "deluxe"}
            deluxe_number = requests.post(hotel_endpoint, json = json_obj).json()
            json_obj = {"room_type": "suite"}
            suite_number = requests.post(hotel_endpoint, json = json_obj).json()

            dispatcher.utter_message(text=f"We are pleased to say that the following rooms are available for your stay\n Standard rooms:{standard_number}\n Deluxe rooms: {deluxe_number}\n Suite Rooms: {suite_number}")

            
        return []


class ActionReservation(Action):

    def name(self) -> Text:
        return "action_reservation"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message.get("entities", [])

        room = tracker.get_slot("room")
        phone = tracker.get_slot("phone")
        email = tracker.get_slot("email")
        check_in = tracker.get_slot("check_in")

        last_user_message = tracker.latest_message.get("text")
    
        if not tracker.get_slot("conversation"):
            messages=[
                {
                    "role": "system",
                    "content": "you are a helpful assistant of a Hotel. Need to ask the user about phone,\
                        email,check in date and room type for reservations. The available room types are standard, deluxe and suite. \
                        Make it short and human like. For further details contact number is +94119123123"
                }
                ]
            
            message = {
                    "role":"user",
                    "content": str(last_user_message)
                }
        

            messages.append(message)
            print(messages)
            response = ChatCompletion().chat_completion(messages)
            bot_response = response['choices'][0]['message']['content']
            dispatcher.utter_message(bot_response)
            
            message_bot = {
                    "role":"assistant",
                    "content": str(bot_response)
                }
            messages.append(message_bot)
            print(messages)
            return [SlotSet("conversation",messages)]

        else:
            messages = tracker.get_slot("conversation")
            last_user_message = tracker.latest_message.get("text")
            message = {
                "role":"user",
                "content": str(last_user_message)
            }
            messages.append(message)

            response = ChatCompletion().chat_completion(messages)
            bot_response = response['choices'][0]['message']['content']
            dispatcher.utter_message(bot_response)
            
            message_bot = {
                    "role":"assistant",
                    "content": str(bot_response)
                }

            messages.append(message_bot)
            entities_list = [room,phone,email,check_in]
            print(entities_list)
            if not any(elem is None for elem in entities_list):

                hotel_endpoint = "http://35.168.216.250:7005/availability"
                json_obj = {"room_type": room}
                room_count = requests.post(hotel_endpoint, json = json_obj).json()
                print(room_count)
                if room_count==0:
                    dispatcher.utter_message("Sorry we are currently out of rooms\n\n")

                else:
                    ID = random.randint(1111,9999)
                    hotel_endpoint_reserve = "http://35.168.216.250:7005/reserve"
                    json_obj = {"room_type": "standard"}
                    response_reservation = requests.post(hotel_endpoint_reserve, json = json_obj).json()
                    dispatcher.utter_message(f"The reservation is made successfully\n\n Reservation ID :{ID}\n Room: {room}\n Date: {check_in}\n Email: {email}\n Contant: {phone}")
     
            
            return [SlotSet("conversation",messages)]

       
       