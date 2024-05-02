## Question Flow in the Application

- **Q1**: "Is it possible to use any information from the {API_NAME} to answer this question?"
  - **Answer**: Strictly yes or no.
- **Q1.no.Q2**: Informs the user in a fun and polite tone that the query is not related to the API.
- **Q1.yes.Q2**: Requests a list of all necessary {API_NAME} endpoints to answer the question.
- **api-get**: Fetches data from the specified API endpoints.
- **Q1.yes.Q2.api.Q3**: Generates a user-friendly response based on API data and the original query.
