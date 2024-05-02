# Technical improvements notes

- If the GPT would not be familiar with the API you use RAG instead. and send the docs and the source code to be embedded.

- If the API is a GraphQL API it would speed up the process significantly. Less informaiton is sent around and fewer and shorter requests would be sent the GPT without information loss.

- The GPT or the RAG must be up to dates with the docs and the docs must be up to date. Otherwise, which endpoints to ask where in the payload to look will fail.

- Now the chat does not handle responses from the api which are bigger than what can be sent to the gpt. This would be solve by either a GPT that could handle a longer context window, by using graphql or some other way filtering out only the relevant information from the response.
