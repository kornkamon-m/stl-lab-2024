import streamlit as st
import google.generativeai as genai

st.title("☕ Coffee Connoisseur Chatbot")
st.subheader("Chat with your personalized coffee expert!")

# Capture Gemini API Key 
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password") 

# Define a persona and instructions to guide the AI's behavior as a coffee expert
coffee_expert_persona = """
You are a kind, friendly, and knowledgeable coffee expert. Your goal is to help people explore the world of coffee.
You provide advice on brewing methods, coffee beans, and coffee drink recipes. 
If a user asks about the coffee process, give a detailed solution and recommend suitable products.
If a user seeks a cafe in Thailand, ask for their location and recommend the nearest cafe.
If a user inquires about a coffee recipe, explain the ingredients and the preparation method.
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
        
        # Greet the user only once after successful API key input
        if "greeting_displayed" not in st.session_state or not st.session_state.greeting_displayed:
            greeting_message = """
            Welcome to the Coffee Connoisseur Chatbot! ☕ I'm here to help you discover amazing coffee experiences.
            Whether you're curious about coffee beans, brewing techniques, or finding the best cafes in Thailand, just ask!
            How can I assist you in your coffee journey today?
            """
        
            # Append the greeting only once
            st.session_state.chat_history.append(("assistant", greeting_message))
            st.chat_message("assistant", avatar="☕").markdown(greeting_message)

            # Set the flag to prevent showing the greeting again
            st.session_state.greeting_displayed = True

    except Exception as e: 
        st.error(f"An error occurred while setting up the Gemini model: {e}") 

# Display previous chat history using st.chat_message (if available)
for role, message in st.session_state.chat_history:
    avatar = "☕" if role == "assistant" else "👤"  # Coffee cup emoji for assistant, person emoji for user
    st.chat_message(role, avatar=avatar).markdown(message)

# Capture user input and generate bot response
if user_input := st.chat_input("Ask me anything about coffee..."):
    # Store and display user message
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user", avatar="👤").markdown(user_input)

    # Use Gemini AI to generate a bot response with a coffee expert persona
    if model: 
        try: 
            # Send the persona and user input to the model
            response = model.generate_content(f"{coffee_expert_persona}\nUser: {user_input}") 
            bot_response = response.text

            # Store and display the bot response
            st.session_state.chat_history.append(("assistant", bot_response)) 
            st.chat_message("assistant", avatar="☕").markdown(bot_response) 
        except Exception as e: 
            st.error(f"An error occurred while generating the response: {e}")
