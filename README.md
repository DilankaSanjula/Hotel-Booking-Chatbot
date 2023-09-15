# Hotel-Booking-Chatbot

## Prerequisites

1. Python version :3.7-3.11
2. Setup aws account.
3. Configure aws using the AWS Access Key ID, AWS Secret Access Key, Region.
4. Postman

## Setting up locally

1. Clone the repository
2. Install all requirements using pip using the requirements.txt file. Command: "pip install -r requirements.txt"
3. ste openai api key as a environment vaiable using the command "set API_KEY='XXXXXXXXXXXXXXXXXXXXXXX'
4. Run command "rasa train" to train the model.
4. Run command "rasa run actions" to start the rasa actions server locally.
5. Run comman "rasa run --enable-api" to start the rasa server.

## Testing
1. Use postman to make a post request to 'http://localhost:5005/webhooks/rest/webhook' with a body containing a message, ex: {"message": "Hi"}