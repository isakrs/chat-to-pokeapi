## Technical Improvements Notes

- Consider using RAG for dynamic document retrieval when GPT models are not familiar with the API.
- Transitioning to a GraphQL API could reduce information overhead and streamline requests.
- Ensure that the NLP model, whether GPT or RAG, is synchronized with the latest API documentation to accurately determine relevant endpoints and data schema.
- Address the issue of handling large API responses that exceed the GPT context window by either using GraphQL to fetch more targeted data or by developing a mechanism to filter and condense data before processing.
