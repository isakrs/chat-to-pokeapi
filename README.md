# chat-to-pokeapi: Natural Language Interface to API

This project provides a natural language interface that allows users to interact with the [PokéAPI](https://pokeapi.co) through spoken or written questions. Users can ask questions such as "How many Pokémon are there?" or "List some blue pokemons", and the system translates these into specific API requests to fetch and display the information.

The solution is hosted on [Chat with PokéAPI](https://isakrs-chat-to-api.streamlit.app/).

## Features

- **API Interaction**: Connects to PokéAPI to retrieve data about Pokémon.
- **Natural Language Processing (NLP)**: Uses a GPT-4 model to interpret natural language queries and convert them into API requests.
- **User Interface**: A simple, user-friendly web interface built with Streamlit, allowing users to submit questions and view answers.
- **Error Handling**: Robust error handling to manage common issues like invalid queries and API connection errors.
- **Documentation**: Comprehensive documentation for setup and example queries.

## Prerequisites

- Python 3.8 or higher
- Pip
- An Azure account with access to GPT-3.5 or GPT-4 API

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/isakrs/chat-to-pokeapi.git
   cd chat-to-pokeapi.git
   ```

2. **Create and activate a virtual environment**

   - **For Windows**
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **For macOS and Linux**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root directory and add your Azure API key:

   ```
   API_KEY = "your_azure_api_key_here"
   API_URL = "your_azure_gpt_api_url_here"

   ```

5. **Run the application**
   ```bash
   streamlit run chat_app.py
   ```

## Usage

1. **Start the application** as described above.
2. **Open your web browser** and go to `http://localhost:8501`.
3. **Enter your query** in the text box provided and press "Send" to receive an answer.
4. **View past interactions** by clicking on "Show me what you did" to see a JSON representation of all queries and responses.

## Deploy to the Cloud

After testing your application locally, you can deploy it to Streamlit Cloud to make it accessible online. Follow these steps to deploy your application:

1. **Push your local changes**

   - Before pushing, ensure that your `.env` file is listed in your `.gitignore` to prevent any secrets from being uploaded to GitHub. This is crucial to maintain the security of your API keys and other sensitive information.
   - Confirm all other local changes are appropriately committed. Do not include actual secrets or sensitive data in these commits.
   - Push these changes to your GitHub repository:
     ```bash
     git add .
     git commit -m "Prepare for deployment"
     git push
     ```

2. **Set up Streamlit Cloud**

   - Visit [Streamlit Cloud](https://streamlit.io/cloud) and sign in with your GitHub account.
   - Click on the **New app** button, select your GitHub repository (`isakrs/chat-to-pokeapi` in this case), the branch you want to deploy (usually `main` or `master`), and the path to your Streamlit app file (`chat_app.py`).

3. **Configure secrets**

   - In the Streamlit Cloud interface, go to the **Settings** tab for your app and find the **Secrets** section.
   - Enter the necessary API keys and other sensitive information in the secrets management area. Use the same keys as in your `.env` file, but provide the actual values here:
     ```
     API_KEY = "your_azure_api_key_here"
     API_URL = "your_azure_gpt_api_url_here"
     ```
   - Streamlit Cloud uses these secrets to set environment variables internally, mimicking the behavior of your local `.env` file.

4. **Deploy your application**

   - After configuring the secrets, click **Deploy**. Streamlit Cloud will build and deploy your application based on the latest commit from the selected branch.
   - The deployment process may take a few minutes. You can monitor the progress in the **Logs** section.

5. **Monitor and maintain your application**

   - Once deployed, your application will be accessible at a unique Streamlit URL, which you can share with others.
   - Keep an eye on the application's performance and logs via the Streamlit Cloud dashboard.
   - For updates or changes to your application, simply push the changes to your GitHub repository. Streamlit Cloud will automatically redeploy your application.

6. **Manage application restarts and updates**
   - If you need to update the secrets or make changes that affect the environment variables, you may need to manually restart the application from the Streamlit Cloud dashboard to ensure the new settings take effect.

These steps provide a comprehensive guide to deploying and managing your application on Streamlit Cloud, ensuring it remains secure, up-to-date, and accessible to users.

## Examples

- "How many Pokémon are there?"
- "List all blue Pokémon."
- "What are the abilities of Pikachu?"

These queries demonstrate the types of questions you can ask and the information the interface can retrieve from the PokéAPI.

## Error Handling

The system is equipped to handle various errors, such as:

- Invalid questions that do not correspond to the data available in the API.
- API connection issues, providing clear error messages to the user.
- Handling unexpected input gracefully by informing users about the types of questions they can ask.

## Project Files Description

- **notes_to_self.md**: Contains technical improvement ideas and considerations for future enhancements of the NLP model and API interaction.
- **gpt_questions.md**: Documents the structure of question flows in the application, detailing how natural language queries are processed and translated into API requests.
- **test_cases.md**: Lists test cases used to ensure the application meets performance expectations and correctly handles both successful and failing query scenarios.

## Contributions

Contributions are welcome! Please open an issue to discuss your idea or submit a pull request.
