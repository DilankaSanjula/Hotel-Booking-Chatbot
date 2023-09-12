from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json

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

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        latest_message = tracker.latest_message.get("text")

        return []