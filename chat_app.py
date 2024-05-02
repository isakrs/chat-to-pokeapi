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
    """Q1.yes.Q2: For this question:

    \n\n {question} \n\n

    Please provide the {API_NAME} endpoints I should use. 
    Also, for each endpoint say where in the response body I should look as a schema. 
    I need to know keys and lists. It should have a structure like this:

    [
        {
            "endpoint" : endpoint-url,
            "response-keys" : [
                "key1",
                "key10".[]."key3".[]."key5",
                ...
            ]
        },
        ...
    ]

    You answer strictly with this requested JSON"""
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
                    "For this question:\n\n" 
                    f"{question}\n\n"
                    f"Please provide the {API_NAME} endpoints I should use. "
                    "Also, for each endpoint say where in the response body I should look as a schema. "
                    "I need to know keys and lists. It should have a structure like this:\n\n"
                    "[\n"
                    "    {\n"
                    '        "endpoint" : "endpoint-url",\n'
                    '        "response-keys" : [\n'
                    '            "key1",\n'
                    '            "key10.[].key3.[].key5",\n'
                    '            "..." \n'
                    '        ]\n'
                    "    },\n"
                    "    ...\n"
                    "]\n\n"
                    "You answer strictly with this requested JSON and nothing else"
                )
            }
        ]
    }


    response = call_api(data)
    
    content = response["choices"][0]["message"]["content"]

    try:
        content = json.loads(content)
        endpoints = [e["endpoint"] for e in content]
        response_keys_list = [e["response-keys"] for e in content]
    except KeyError:
        # TODO: make the code more robust here and handle the error
        raise ValueError("The response body should have 'endpoint' and 'response-keys' keys.")

    # TODO: check if response is valid. if not, append system's answer to data messages and ask one more time for a valid answer.
    # API_URL should be in each endpoint.

    new_message = {
        "role": "assistant",
        "content": response["choices"][0]["message"]["content"]
    }
    data["messages"].append(new_message)

    return endpoints, response_keys_list, data


def get_endpoints(endpoints):
    """Call the API for each endpoint and return the responses."""
    responses = []
    for e in endpoints:
        r = requests.get(e)
        responses.append(r.json())
    return responses


def filter_response(response, response_keys):
    filtered_response = {}
    for key in response_keys:
        # Split keys on periods, which are used to navigate through the data structure
        keys = key.split(".")
        temp = response
        for k in keys:
            # Check if the current part of the key is a list index indicated by brackets '[]'
            if '[]' in k:
                list_key = k.split('[]')[0]
                # Ensure we're dealing with a list and it's not an empty path to a list
                if list_key and isinstance(temp, dict) and list_key in temp and isinstance(temp[list_key], list):
                    # Collect all items specified by the list index key
                    temp = [item.get(k.split('[]')[1], {}) for item in temp[list_key] if k.split('[]')[1] in item]
                else:
                    temp = [{}]
            elif k.isdigit():  # Handle direct list indices
                temp = temp[int(k)] if isinstance(temp, list) and int(k) < len(temp) else {}
            else:  # Handle dictionary keys
                temp = temp.get(k, {}) if isinstance(temp, dict) else {}
        # Store the filtered result for the current key
        filtered_response[key] = temp
    return filtered_response


def filter_responses(responses, response_keys_list):
    filtered_responses = []
    for r, keys in zip(responses, response_keys_list):
        filtered_responses.append(filter_response(r, keys))
    return filtered_responses



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
    endpoints, response_keys_list, data = gpt_q1_yes_q2(question)
    history.append({"gpt-data": data})
    responses = get_endpoints(endpoints)
    history.append({"api-responses": responses})

    # Filter the responses based on the response keys
    filtered_responses = filter_responses(responses, response_keys_list)
    history.append({"filtered-responses": filtered_responses})

    # # Check if additional endpoints are needed after initial response
    # additional_endpoints, data = gpt_q1_yes_q2_api_q3(question, endpoints, responses)
    # history.append({"gpt-data": data})
    # if additional_endpoints:
    #     more_responses = get_endpoints(additional_endpoints)
    #     history.append({"api-responses": more_responses})
    #     endpoints.extend(additional_endpoints) # Append additional endpoints
    #     responses.extend(more_responses)  # Append additional responses

    # Final interaction based on all collected data
    final_answer, data = q1_yes_q2_api_q3_api_q4(question, endpoints, filtered_responses)
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
