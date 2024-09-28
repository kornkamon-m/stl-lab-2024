import streamlit as st
import google.generativeai as genai

st.title("😺 Cat Lover Chatbot")
st.subheader("Chat with your personalized cat care expert!")

# Capture Gemini API Key 
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password") 

# Define a persona to guide the AI's behavior as a cat lover
cat_lover_persona = """
You are a friendly, knowledgeable, and enthusiastic cat lover. 
Your goal is to help people take the best care of their cats, providing advice on grooming, feeding, health, and overall cat happiness. 
You love sharing tips about how to bond with cats, keep them entertained, and maintain their well-being.
"""

# Initialize session state for storing chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize the Gemini Model 
if gemini_api_key: 
    try: 
        # Configure Gemini with the provided API Key 
        genai.configure(api_key=gemini_api_key) 
        model = genai.GenerativeModel("gemini-pro") 
        st.success("Gemini API Key successfully configured.") 

    except Exception as e: 
        st.error(f"An error occurred while setting up the Gemini model: {e}") 

# Display previous chat history using st.chat_message (if available)
for role, message in st.session_state.chat_history:
    avatar = "🐈" if role == "assistant" else "🌝"  # Cat emoji for assistant, user emoji for user
    st.chat_message(role, avatar=avatar).markdown(message)

# Capture user input and generate bot response
if user_input := st.chat_input("Ask about cat care..."):
    # Store and display user message
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user", avatar="🌝").markdown(user_input)

    # Use Gemini AI to generate a bot response with a cat lover persona
    if model: 
        try: 
            # Send the persona and user input to the model
            response = model.generate_content(f"{cat_lover_persona}\nUser: {user_input}") 
            bot_response = response.text

            # Store and display the bot response
            st.session_state.chat_history.append(("assistant", bot_response)) 
            st.chat_message("assistant", avatar="🐈").markdown(bot_response) 
        except Exception as e: 
            st.error(f"An error occurred while generating the response: {e}")
