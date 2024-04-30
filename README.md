# chat-to-pokeapi Streamlit Application

Use natural language to communicate with the pokéapi.

This repository contains the source code for a simple Streamlit-based chat interface that interacts with an AI model via an API. The application allows users to input text, which is then sent to the AI model, and displays the response. It does not store any chat history and includes functionality to clear the chat window.

## Features

- Simple chat interface using Streamlit.
- Communication with AI model via a REST API.
- Input text box and response display.
- No storage of chat history.
- Functionality to clear the chat window.

## Live Application

The application is deployed and can be accessed at [https://isakrs-chat-to-api.streamlit.app/](https://isakrs-chat-to-api.streamlit.app/).

## Requirements

- Python 3.10
- Dependencies as listed in `requirements.txt`

## Local Setup

### Step 1: Clone the Repository

Clone the repository to your local machine by running:

```bash
git clone https://github.com/yourusername/your-repository.git
cd your-repository
```

### Step 2: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Step 3: Environment Configuration

This project uses environment variables stored in a TOML-formatted `.env` file to manage sensitive information like API keys and URLs. Ensure you have a `.env` file in your project root with the following format:

```toml
API_KEY = "your_api_key_here"
API_URL = "https://api_endpoint_url_here"
```

Replace `your_api_key_here` and `https://api_endpoint_url_here` with your actual API key and URL.

### Step 4: Run the Application

To run the application locally, use:

```bash
streamlit run app.py
```

This will start the Streamlit server, and you can view your application by navigating to `localhost:8501` in your web browser.

## Deployment

The application is deployed on Streamlit Cloud. For details on deploying your own Streamlit apps, see [Streamlit's documentation](https://docs.streamlit.io/knowledge-base/deploy).
