from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import json
from chatgpt.chatgpt import *
import random

class ActionCheckAvailability(Action):
    """
    Custom action for to check availability of rooms. To check the availability a 
    post request is made to the developed mock api.

    """
    def name(self) -> Text:
        return "action_check_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entities = tracker.latest_message.get("entities", [])
        
        hotel_endpoint = "http://35.168.216.250:7005/availability"

        if entities:
            if entities[0]['value'] == 'standard':
                try:
                    json_obj = {"room_type": "standard"}
                    standard_number = requests.post(hotel_endpoint, json = json_obj).json()
                    dispatcher.utter_message(text=f"We are pleased to say that {standard_number} standard rooms are available at the moment")
                except Exception as e:
                    return {'status': False, 'cause':e}

            if entities[0]['value'] == 'deluxe':
                try:
                    json_obj = {"room_type": "deluxe"}
                    deluxe_number = requests.post(hotel_endpoint, json = json_obj).json()
                    dispatcher.utter_message(text=f"We are pleased to say that {deluxe_number} deluxe rooms are available at the moment")

                except Exception as e:
                    return {'status': False, 'cause':e}

            if entities[0]['value'] == 'suite':
                try:
                    json_obj = {"room_type": "suite"}
                    suite_number = requests.post(hotel_endpoint, json = json_obj).json()
                    dispatcher.utter_message(text=f"We are pleased to say that {suite_number} suite rooms are available at the moment")

                except Exception as e:
                    return {'status': False, 'cause':e}
        else:
            try:
                json_obj = {"room_type": "standard"}
                standard_number = requests.post(hotel_endpoint, json = json_obj).json()
                json_obj = {"room_type": "deluxe"}
                deluxe_number = requests.post(hotel_endpoint, json = json_obj).json()
                json_obj = {"room_type": "suite"}
                suite_number = requests.post(hotel_endpoint, json = json_obj).json()

                dispatcher.utter_message(text=f"We are pleased to say that the following rooms are available for your stay\n Standard rooms:{standard_number}\n Deluxe rooms: {deluxe_number}\n Suite Rooms: {suite_number}")
            except Exception as e:
                return {'status': False, 'cause':e}
            
        return []


class ActionReservation(Action):
    """
    Custom action for reservations. RASA Slots are used to record entities such as phone, email,
    check_in date, room type. For human like responses chatgpt is integrated. For chat completion
    user and assistant messages are appends and recorded/ taken forward using rasa list type slot.

    """
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
                        Make it short and human like. For further details contact number is +94119123123. Dont ask for confirmation after\
                        all room, email,chec in date and phone are retrieved"
                }
                ]
            
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
           
            if not any(elem is None for elem in entities_list):

                hotel_endpoint = "http://35.168.216.250:7005/availability"
                json_obj = {"room_type": room}
                room_count = requests.post(hotel_endpoint, json = json_obj).json()
              
                if room_count==0:
                    dispatcher.utter_message("Sorry we are currently out of rooms\n\n")

                else:
                    ID = str(random.randint(1111,9999))
                    ID = f"#{ID}"
                    hotel_endpoint_reserve = "http://35.168.216.250:7005/reserve"
                    json_obj = {
                            "reservation_id": ID,
                            "user_email": email,
                            "user_phone": phone,
                            "room_type": room,
                            "check_in_date": check_in
                        }
                    try: 
                        response_reservation = requests.post(hotel_endpoint_reserve, json = json_obj).json()
                        print(response_reservation)
                        dispatcher.utter_message(f"The reservation is made successfully\n\n Reservation ID :{ID}\n Room: {room}\n Date: {check_in}\n Email: {email}\n Contant: {phone}")

                        return [SlotSet(slot, None) for slot in tracker.slots.keys()]
                    except:
                        dispatcher.utter_message("Reservations cannot be made due to technical issue, we will contant you soon")

     
            
            return [SlotSet("conversation",messages)]

       
class ActionCancellation(Action):

    """
    Custom action to handle cancelations. A to  post request to the mock API is made to record a cancellation
    """

    def name(self) -> Text:
        return "action_cancellation"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        reservation_id = tracker.get_slot("reservation_id")
        
        hotel_cancellation = "http://35.168.216.250:7005/cancel_reservation"

        reservation_id =  str(reservation_id)
        json_obj = {"reservation_id": reservation_id}

        try:
            response= requests.post(hotel_cancellation, json=json_obj).json()
            if response['status'] == 'Successful':
                dispatcher.utter_message(text=f"We have removed your reservation under {reservation_id}")
        except:
            print('False')
            dispatcher.utter_message(text=f"Please enter a valid reservation ID")
                
        return []
    

class ActionCHATGPTFAllbak(Action):

    """
    Custom action to handle cancelations. A to  post request to the mock API is made to record a cancellation
    """

    def name(self) -> Text:
        return "action_gpt_fallback"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
    
        
        try:
            last_user_message = tracker.latest_message.get("text")
            prompt = f"Answer this only if it is realted to hotels only:{last_user_message}"
            gpt_resp= ChatGPTFallback().api_call(prompt)
            dispatcher.utter_message(text=gpt_resp)
        except Exception as e:
            print(e)
            dispatcher.utter_message(text=f"We are unable to answer this question. Please contact us")
                
        return []
