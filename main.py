# Imports
import os
import streamlit as st
from apikey import apikey
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

# Define OpenAI API KEY
os.environ['OPENAI_API_KEY'] = apikey

# Define Satirical Template 
sat_template = PromptTemplate(
    input_variables=['input'],
    template="Be as satirical and witty as possible,\
              make jokes about the user input,\
              act goofy, not required to be helpful, \
              most important is to be funny and original, \
              with an emphasis on satirical responses \
              USER INPUT: {input}"
)

# Memory
sat_memory = ConversationBufferMemory(input_key="input", memory_key="chat_history")

# Language Model
llm = OpenAI(temperature=0.9)

# Satirical Response Generation Chain
sat_chain = LLMChain(llm=llm, prompt=sat_template, memory=sat_memory)

# Define Generated and Past Chat Arrays
if 'generated' not in st.session_state: 
    st.session_state['generated'] = []

if 'past' not in st.session_state: 
    st.session_state['past'] = []

# Title and Description
st.title("satGPT")
st.write("An OpenAI chatGPT trained to be as satirical and jokingly as possible")

# CSS for chat bubbles
chat_bubble_style = """
    .user-bubble {
        background-color: #DCF8C6;
        color: #1C824C;
        padding: 8px 12px;
        border-radius: 15px;
        display: inline-block;
        max-width: 70%;
    }
    
    .gpt-bubble {
        background-color: #F3F3F3;
        color: #404040;
        padding: 8px 12px;
        border-radius: 15px;
        display: inline-block;
        max-width: 70%;
        text-align: right;
    }
"""

# Apply CSS style
st.write(f'<style>{chat_bubble_style}</style>', unsafe_allow_html=True)

# User input
input_text = st.text_input('Enter message for satGPT')

if st.button('Send Message') and input_text:
    with st.spinner('Generating response...'):
        try:
            # Generate satirical response
            response = sat_chain.run(input_text)

            # Store conversation
            st.session_state.past.append(input_text)
            st.session_state.generated.append(response)

            # Display conversation in reverse order
            for i in range(len(st.session_state.past)-1, -1, -1):
                st.write(f'<div class="gpt-bubble">{st.session_state.generated[i]}</div>', unsafe_allow_html=True)
                st.write(f'<div class="user-bubble">{st.session_state.past[i]}</div>', unsafe_allow_html=True)
                st.write("")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
