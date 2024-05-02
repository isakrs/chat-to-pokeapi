import streamlit as st
import requests
from dotenv import load_dotenv
import os
import json

API_NAME = "PokéAPI"
API_URL = "https://pokeapi.co/api/v2/"

# Load environment variables
load_dotenv()

# Retrieve API key and URL from environment
gpt_api_key = os.getenv("API_KEY")
gpt_api_url = os.getenv("API_URL")


def call_api(data):
    headers = {"Content-Type": "application/json", "api-key": gpt_api_key}
    response = requests.post(gpt_api_url, headers=headers, json=data)
    return response.json()


def gpt_q1(question):
    """Q1: Is possible to use any information from the {API_NAME} to answer this question? 
    
    Question: \n\n {question} \n\n. Answer yes or no."""
    data = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant who translates natural language into API calls. "
                    f"You are an expert on the {API_NAME}. "
                )
            },
            {
                "role": "user", 
                "content": (
                    f"Is possible to use any information from the {API_NAME} to answer this question? "
                    f"Question: \n\n {question} \n\n. "
                    "Answer strictly yes or no"
                )
            }
        ]
    }
    response = call_api(data)
    
    # TODO: check if response is valid. if not, append system's answer to data messages and ask one more time for a valid answer.
    
    is_api_question = response["choices"][0]["message"]["content"].strip().lower() == "yes"

    new_message = {
        "role": "assistant",
        "content": response["choices"][0]["message"]["content"]
    }
    data["messages"].append(new_message)

    return is_api_question, data


def gpt_q1_no_q2(question):
    """Q1.no.Q2: Please answer in a fun and polite tone that this is a not an API related question."""
    data = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant who translates natural language into API calls. "
                    f"You are an expert on the {API_NAME}. "
                )
            },
            {
                "role": "user", 
                "content": (
                    f"Is this a question that can be answered with {API_NAME}? Question: \n\n {question} \n\n. "
                    "Answer strictly yes or no"
                )
            },
            {
                "role": "assistant",
                "content": "no"
            },
            {
                "role": "user",
                "content": "Please answer in a fun and polite tone that this is a not an API related question."
            }
        ]
    }
    response = call_api(data)
    new_message = {
        "role": "assistant",
        "content": response["choices"][0]["message"]["content"]
    }
    data["messages"].append(new_message)
    answer = response["choices"][0]["message"]["content"]
    return answer, data


def gpt_q1_yes_q2(question):
    """Q1.yes.Q2: List all the {API_NAME} endpoints you would like to call in order to answer the question."""
    data = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant who translates natural language into API calls. "
                    f"You are an expert on the {API_NAME}. "
                )
            },
            {
                "role": "user", 
                "content": (
                    f"List all the {API_NAME} endpoints you would like to call in order to answer the question. "
                    f"Question: \n\n {question} \n\n. "
                    f"Provide the full URL of the endpoint. {API_URL} should be part of each endpoint. "
                    "Answer strictly with comma separated values for the endpoints to call and nothing else"
                )
            }
        ]
    }
    response = call_api(data)
    endpoints = response["choices"][0]["message"]["content"].split(',')

    # TODO: check if response is valid. if not, append system's answer to data messages and ask one more time for a valid answer.
    # API_URL should be in each endpoint.

    new_message = {
        "role": "assistant",
        "content": response["choices"][0]["message"]["content"]
    }
    data["messages"].append(new_message)

    return endpoints, data


def get_endpoints(endpoints):
    """Call the API for each endpoint and return the responses."""
    responses = []
    for e in endpoints:
        r = requests.get(e)
        responses.append(r.json())
    return responses


def gpt_q1_yes_q2_api_q3(question, endpoints, responses):
    """Q1.yes.Q2.api.Q3: 
    
    Based on the question: \n\n {question} \n\n
    
    and the {API_NAME} response(s): \n\n
     
    {(e, r)\n for e,r in zip(endpoints, responses)} \n\n
    
    are there any additional endpoints you would like to call? 
    Provide the full URL of the endpoint. {API_URL} should be part of each endpoint.
    Answer strictly with comma separated values for the endpoints to call and nothing else"""
    data = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant who translates natural language into API calls. "
                    f"You are an expert on the {API_NAME}. "
                )
            },
            {
                "role": "user", 
                "content": (
                    f"Based on the question: \n\n {question} \n\n"
                    f"and the {API_NAME} response(s): \n\n"
                    f"{[(e, r) for e,r in zip(endpoints, responses)]} \n\n"
                    "are there any additional endpoints you would like to call? "
                    f"Provide the full URL of the endpoint. {API_URL} should be part of each endpoint. "
                    "Answer strictly with comma separated values for the endpoints to call if yes, "
                    "otherwise answer no-more-endpoints"
                )
            }
        ]
    }
    response = call_api(data)

    new_message = {
        "role": "assistant",
        "content": response["choices"][0]["message"]["content"]
    }
    data["messages"].append(new_message)

    is_no_more_endpoints = response["choices"][0]["message"]["content"].strip().lower() == "no-more-endpoints"
    if is_no_more_endpoints:
        return [], data
    
    endpoints = response["choices"][0]["message"]["content"].split(',')

    # TODO: check if response is valid. if not, append system's answer to data messages and ask one more time for a valid answer.
    # API_URL should be in each endpoint.

    return endpoints, data


def q1_yes_q2_api_q3_api_q4(question, endpoints, responses):
    """Based on the user's original question:
    \n\n {question} \n\n
    and the response(s) from pokeAPI:
    \n\n {(e, r)\n for e,r in zip(endpoints, responses)} \n\n
    please answer the user in a fun and polite tone."""
    data = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant who translates natural language into API calls. "
                    f"You are an expert on the {API_NAME}. "
                )
            },
            {
                "role": "user", 
                "content": (
                    f"Based {API_NAME}'s endpoints and corresponding responses: \n\n"
                    f"{[(e, r) for e,r in zip(endpoints, responses)]} \n\n"
                    f"and the user's original question: \n\n {question} \n\n"
                    "please answer the user's question in a fun and polite tone."
                )
            }
        ]
    }
    response = call_api(data)

    new_message = {
        "role": "assistant",
        "content": response["choices"][0]["message"]["content"]
    }
    data["messages"].append(new_message)

    answer = response["choices"][0]["message"]["content"]

    return answer, data


def handle_query(question):
    """Handle the user's query."""
    # Append the user's question to the history
    history = []
    history.append({"question": question})

    # Determine if the question can be answered using the API
    is_api_question, data = gpt_q1(question)
    history.append({"gpt-data": data})
    if not is_api_question:
        # Handle no response, which is a fun and polite message about it not being an API question
        answer, data = gpt_q1_no_q2(question)
        history.append({"gpt-data": data})
        
        # Append the answer to the history
        history.append({"answer": answer})
        st.session_state["history"] = history

        return answer

    # Get the necessary endpoints to call if it's an API question
    endpoints, data = gpt_q1_yes_q2(question)
    history.append({"gpt-data": data})
    responses = get_endpoints(endpoints)
    history.append({"api-responses": responses})

    # Check if additional endpoints are needed after initial response
    additional_endpoints, data = gpt_q1_yes_q2_api_q3(question, endpoints, responses)
    history.append({"gpt-data": data})
    if additional_endpoints:
        more_responses = get_endpoints(additional_endpoints)
        history.append({"api-responses": more_responses})
        endpoints.extend(additional_endpoints) # Append additional endpoints
        responses.extend(more_responses)  # Append additional responses

    # Final interaction based on all collected data
    final_answer, data = q1_yes_q2_api_q3_api_q4(question, endpoints, responses)
    history.append({"gpt-data": data})

    # Append the final answer to the history
    history.append({"answer": final_answer})

    # Update chat history
    st.session_state["history"] = history

    return final_answer


### Streamlit UI ###
# Streamlit UI implementation
st.title(f"Chat with {API_NAME}")

# Textbox for user input
user_input = st.text_input("Ask a question:")

# History of all API interactions
if "history" not in st.session_state:
    st.session_state["history"] = []

# Handle user input
if st.button("Send"):
    if user_input:
        response = handle_query(user_input)
        st.write(f"AI: {response}")

# Clear chat history
if st.button("Clear Chat"):
    st.rerun()

# Show chat history
if st.button("Show me what you did"):
    st.json(st.session_state["history"])