import streamlit as st
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import json
import os

# Placeholder for subscription management (Replace with actual implementation)
subscriptions = {}

def check_subscription(user_id):
    if user_id in subscriptions:
        expiry_date = subscriptions[user_id]
        if expiry_date > datetime.now():
            return True, expiry_date
        else:
            return False, expiry_date
    return False, None

def extend_subscription(user_id, days=30):
    if user_id in subscriptions:
        subscriptions[user_id] += timedelta(days=days)
    else:
        subscriptions[user_id] = datetime.now() + timedelta(days=days)

def main():
    st.set_page_config(page_title="E-Copyright", page_icon="🤖")

    # Inject CSS with st.markdown
    st.markdown("""
        <style>
            body {
                background-image: url('https://www.vecteezy.com/vector-art/21835780-artificial-intelligence-chatbot-assistance-background');
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                font-family: sans-serif;
            }
            .title {{
                text-align: center;
                font-size: 2.5em;
                color: #4D869C;
                margin-top: 20px;
            }}
            .input-area {{
                display: flex;
                justify-content: center;
                align-items: center;
                margin-top: 20px;
            }}
            .input-text {{
                padding: 10px;
                border: 1px solid #CCC;
                border-radius: 5px;
                margin-right: 10px;
                width: 70%;
            }}
            .submit-button {{
                padding: 10px 20px;
                background-color: #4D869C;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.2s ease-in-out;
            }}
            .submit-button:hover {{
                background-color: #9FB3C4;
            }}
            .response {{
                background-color: #F2F7FF;
                padding: 10px;
                border-radius: 5px;
                margin-top: 10px;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
                color: #333;
                width: 70%;
                margin: 10px auto;
            }}
            .back-button {{
                display: inline-block;
                text-align: center;
                padding: 5px 10px;
                background-color: #4D869C;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.2s ease-in-out;
                margin-top: 20px;
            }}
            .back-button:hover {{
                background-color: #9FB3C4;
            }}
            .payment-section {{
                text-align: center;
                margin-top: 30px;
            }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title">E-Copyright</div>', unsafe_allow_html=True)

    # Initialize the chatbot
    try:
        with open('config.json') as config_file:
            config = json.load(config_file)
            api_key = config.get('openai_api_key', None)

        if api_key is None:
            st.error("API key is missing or incorrect. Please provide a valid API key in the config.json file.")
            return

        # Initialize chatbot model
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=api_key)

        # Initialize conversation chain with memory
        buffer_memory = ConversationBufferWindowMemory(k=5, return_messages=True)
        system_msg_template = SystemMessagePromptTemplate.from_template(
            template="""Answer the question as truthfully as possible using the provided context, 
            and if the answer is not contained within the text below, say 'I don't know'"""
        )
        human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")
        prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])
        conversation = ConversationChain(memory=buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

        # Initialize session state
        if "history" not in st.session_state:
            st.session_state.history = []

        # Main page content
        menu = ["Chatbot", "About Us", "Login", "Subscription"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Chatbot":
            chatbot_page(conversation)
        elif choice == "About Us":
            about_us_page()
        elif choice == "Login":
            login_page()
        elif choice == "Subscription":
            subscription_page()

    except Exception as e:
        st.error(f"An error occurred during initialization: {e}")

def login_page():
    st.subheader("Login")
    user_id = st.text_input("Enter your user ID", key="login_user_id")
    login_button = st.button("Login")

    if login_button and user_id:
        # Placeholder for actual login/authentication
        st.success(f"Logged in as {user_id}")

def subscription_page():
    st.subheader("Subscription")
    user_id = st.text_input("Enter your user ID", key="sub_user_id")
    check_subscription_button = st.button("Check Subscription")

    if check_subscription_button and user_id:
        subscription_status, expiry_date = check_subscription(user_id)

        if subscription_status:
            st.success(f"Your subscription is active until {expiry_date.strftime('%Y-%m-%d')}")
        else:
            st.warning(f"Your subscription has expired. Expiry Date: {expiry_date.strftime('%Y-%m-%d') if expiry_date else 'N/A'}")

            # Payment and subscription extension section
            st.markdown('<div class="payment-section">', unsafe_allow_html=True)
            st.write("Extend your subscription by making a payment.")
            if st.button("Extend Subscription (30 days for $10)"):
                # Placeholder for payment processing
                # Here, you would integrate with a payment gateway like Stripe or PayPal
                # For this example, we'll just simulate a successful payment
                extend_subscription(user_id, days=30)
                st.success("Your subscription has been extended by 30 days!")
            st.markdown('</div>', unsafe_allow_html=True)


def about_us_page():
    st.subheader("About Us")
    st.write("""
        E-Copyright is a copyright-focused assistant designed to provide prompt and reliable assistance with copyright policies and regulations. Hosted on the copyright government website, E-Copyright offers convenient access to essential copyright information, ensuring compliance and protection for individuals and businesses in the creative industry.

        **Features:**
        - **Prompt Recommendations:** Access a comprehensive prompt library for instant guidance and recommendations on copyright policy queries.
        - **24/7 Availability:** EthicalGuard is accessible at any time, providing round-the-clock support and assistance.
        - **Text Queries:** Users can input their copyright-related questions in natural language for quick and accurate responses.
        - **Ease of Use:** Enjoy a seamless navigation experience and effortless interaction through our user-friendly interface.
        - **Personalized Solutions:** Receive customized recommendations and strategies tailored to your individual copyright needs and concerns.

        At E-Copyright, we are committed to providing you with the tools and information necessary to navigate copyright regulations effectively. Whether you are an individual creator or a business in the creative industry, we are here to support you every step of the way.

        Explore E-Copyright today and ensure your creative work is protected and compliant with copyright laws. Let us assist you in simplifying the complexities of copyright, allowing you to focus on what you do best—creating and innovating.

        For more information and support, visit us at E-Copyright on the copyright government website.
    """)

def chatbot_page(conversation):
    # User input form
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("", key="input", placeholder="Enter your message here...", max_chars=200, label_visibility="collapsed")
        submit_button = st.form_submit_button("Send")
    st.markdown('</div>', unsafe_allow_html=True)

    # Process user input
    if submit_button and user_input:
        try:
            st.session_state.history.append({"role": "user", "content": user_input})
            response = conversation.predict(input=user_input)
            st.session_state.history.append({"role": "bot", "content": response})
        except Exception as e:
            st.error(f"An error occurred during conversation: {e}")

    # Display conversation history
    for message in st.session_state.history:
        role = "You" if message["role"] == "user" else "Bot"
        st.markdown(f'<div class="response"><strong>{role}:</strong> {message["content"]}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
