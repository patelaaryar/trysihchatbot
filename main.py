import os
import google.generativeai as genai
from fastapi import FastAPI, Form
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# Load environment variables from .env file
# --> load_dotenv()

# Get the API key from environment variables
# --> api_key = os.getenv("GEMINI_API_KEY")

# Configure the Generative AI model
genai.configure(api_key="AIzaSyCOElTIwhk7OMamYV97FkGXr61FOEGCYGE")

# Initialize the Gemini Pro model
# Use a specific model version if desired, e.g., 'gemini-1.5-flash'
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="You are a friendly and helpful healthcare information assistant. Your purpose is to provide general health information, answer questions about common ailments, and recommend consulting a healthcare professional for diagnosis or treatment. DO NOT provide medical advice, diagnosis, or prescriptions. Always preface your answers with a strong recommendation to see a doctor for personal medical advice. Be concise and empathetic."
)

app = FastAPI()

async def get_chatbot_response_ai(user_message: str):
    """
    This function uses the Gemini API to get a response.
    """
    try:
        # Create a conversation with the model
        chat = model.start_chat(history=[])
        
        # Send the user's message to the model and get the response
        response = await chat.send_message_async(user_message)
        
        # Return the generated text
        return response.text
        
    except Exception as e:
        print(f"An error occurred with the AI model: {e}")
        return "I'm sorry, I'm having trouble with my connection right now. Please try again in a moment."

@app.post("/sms")
async def handle_sms(From: str = Form(...), Body: str = Form(...)):
    """
    This endpoint receives incoming SMS messages from the Twilio webhook.
    """
    print(f"Received message from {From}: {Body}")
    
    # Get the AI chatbot's response
    bot_response_text = await get_chatbot_response_ai(Body)

    # Create a TwiML response to send back to the user
    resp = MessagingResponse()
    resp.message(bot_response_text)
    
    # Debugging print to see the final TwiML string
    final_twiml = str(resp)
    print(f"Final TwiML to be returned: '{final_twiml}'")
    
    return final_twiml

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)