import pandas as pd
import streamlit as st
from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_ollama import ChatOllama

# Streamlit web app configuration
st.set_page_config(page_title="Ollama Chatbot", page_icon="⚛", layout="centered")


# Funtion to read file
def read_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)


# Building the streamlit application:

# Streamlit page title
st.title("Personal Chatbot")

# Intialising chat history - to ensure access to previous conversation
if (
    "chat_history" not in st.session_state
):  # Check if chat history is not in session state and create a new one
    st.session_state.chat_history = []

# Initiate the dataframe in the session state in the same way as chat history
if "df" not in st.session_state:
    st.session_state.df = None

# Building the upload file widget
uploaded_file = st.file_uploader("Choose a file to upload", type=["csv", "xlsx", "xls"])

# Saving the file in the session state
if uploaded_file:
    st.session_state.df = read_data(uploaded_file)
    st.write("DataFrame Preview:")
    st.dataframe(st.session_state.df.head())

# Displaying the chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Creating input field for user to type in
user_prompt = st.chat_input("Ask me something...")

if user_prompt:
    # Adding user's message to chat history
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # loading the LLM
    llm = ChatOllama(
        model="deepseek-r1:8b", temperature=0.5
    )  # Temperature decides randomness of the response

    # Creating the agent:

    # We send the LLM, df and user prompt to the agent. The LLM will then generate the python code to carry out the task defined by user prompt. The agent will then execute the code and return the output.

    pandas_df_agent = create_pandas_dataframe_agent(
        llm,
        st.session_state.df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        allow_dangerous_code=True,
    )

    messages = [
        {"role": "system", "content": "You are an helpful assistent."},
        *st.session_state.chat_history,
    ]

    response = pandas_df_agent.invoke(messages)

    assistant_response = response["output"]

    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_response}
    )

    # Display the LLM's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
