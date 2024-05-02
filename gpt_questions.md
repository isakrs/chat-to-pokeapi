Q1: Is possible to use any information from the {API_NAME} to answer this question?
Question: \n\n {question} \n\n.
Answer strictly yes or no

Q1.no.Q2: Please answer in a fun and polite tone that this is a not a Pokeman related question.

Q1.yes.Q2:
List all the {API_NAME} endpoints you would like to call in order to answer the question.
Question: \n\n {question} \n\n.
Provide the full URL of the endpoint. {API_URL} should be part of each endpoint.
Answer strictly with comma separated values for the endpoints to call and nothing else

api-get

Q1.yes.Q2.api.Q3:
Based {API_NAME}'s endpoints and corresponding responses: \n\n
{[(e, r) for e,r in zip(endpoints, responses)]} \n\n
and the user's original question: \n\n {question} \n\n
please answer the user's question in a fun and polite tone.
