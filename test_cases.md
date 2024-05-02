test_cases

max reponse time should be 5 seconds.

# Successful questions

Q: How many pokemons are there?
A: There are 1302. Make sure this number is in the answer.

Q: What is the api call to pokeapi to answer this question? How many pokemons are there?
A: Should answer with an API endpoint and 1302. It should also provide a url.

Q: How many blue pokemons are there?
A: Should be between 100-200.

Q: List some blue pokemons
A: A list of blue pokemons.

Q: Give me some stats on Usain Bolt
A: Should be answer saying that this is not a relevant question for the API

Q: What are the names of the names of the top 10 most famous pokemons.
A: Name of ten pokemons are provided, or that this is not a relevant question.

Q: What are the names of the characters in Star Wars?
A: It should be a polite answer and it should be clear that this is not a pokemon related question.

Q: Could you tell a joke about Pikachu?
A: No, it did not fit with an API request.

Q: Could you tell a joke about picatou?
A: No, it did not fit with an API request. Note the wrong name in the question.

#### Failing questions

Q: What are Pikachu's abilities?
A: Should give some abilities.
Currently: KeyError. However, it is actually failing due to too big max_tokens

Q: Give me some stats on Pikachu
A: Should have more than 3 numerical details
Currently: failing due to too large response

Q: Pichatou or something is a name of a pokemon. What is the real name and can you tell me something about this pokemon?
A: Should provide some statics on Picatou and the correct name of this pokemon, Pikachu.
Currently: failing, JSONDecodeError. Unsure why yet.

Q: Tell me something about two pokemons
A: Make sure you get the name of two pokemons and some information on both of them
Currently: failing, line 139

Q1: Give me some stats on Pikachu
A1: Should have more than 3 numerical details
Q2: What is iconic sound?
A2: Should sound should be described
Currently: History functionality is yet not written
