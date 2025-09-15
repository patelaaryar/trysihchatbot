from fastapi import FastAPI, Form
from twilio.twiml.messaging_response import MessagingResponse

app = FastAPI()

# A simple, rule-based chatbot function
def get_chatbot_response(user_message: str):
    """
    This is where your chatbot's core logic will go.
    For this example, it's a simple, rule-based system.
    In a real application, you'd replace this with an LLM call.
    """
    user_message = user_message.lower().strip()
    
    if "hello" in user_message or "hi" in user_message:
        return "Hello! I am a healthcare information assistant. How can I help you today? Please note, I cannot provide medical advice."
    elif "symptoms" in user_message or "sick" in user_message:
        return "I can't diagnose you, but I can provide general information. Please describe your symptoms. For a diagnosis, you must consult a doctor."
    elif "appointment" in user_message:
        return "I can help you find a healthcare provider. What is your zip code?"
    else:
        return "I'm sorry, I don't understand. Could you please rephrase that? Remember, I am an informational chatbot and not a substitute for a medical professional."

@app.post("/sms")
async def handle_sms(From: str = Form(...), Body: str = Form(...)):
    """
    This endpoint receives incoming SMS messages from the Twilio webhook.
    """
    print(f"Received message from {From}: {Body}")
    
    # Get the chatbot's response
    bot_response_text = get_chatbot_response(Body)

    # Create a TwiML response to send back to the user
    resp = MessagingResponse()
    resp.message(bot_response_text)
    
    return str(resp)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)