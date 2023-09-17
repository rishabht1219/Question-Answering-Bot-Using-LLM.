# Question-Answering-Bot-Using-LLM.
- A Question-Answer Bot powered by the Large Language Model (LLM) T5! 🤖
## Overview
This open-source project combines the capabilities of the T5 Transformer model with various data sources to create an intelligent question-answering bot. It is designed to provide concise and informative summaries in response to user queries. The bot utilizes multiple sources, including the Wikipedia Python API, Google search, Google snippet data, and the Google Knowledge Graph, to retrieve relevant information for answering questions.

## Key Features

- **Multi-Source Data Retrieval:** The bot fetches data from multiple sources, ensuring a comprehensive and accurate response to user queries.
- **Selection Algorithm with Similarity:** It employs a selection algorithm that calculates similarity scores between the user's query and data collected from all sources. This allows it to choose the best source with the       highest similarity score.
- **T5 Transformer Summarization:** The selected data is then fed into the T5 Transformer, which generates concise summaries for the user. It also provides a link to the source from which the data was obtained.
- **Built with FastAPI:** The bot's API is built using FastAPI, a modern web framework for Python, ensuring efficient and responsive interactions with users.
## Use Cases

- **Information Retrieval:** Quickly access detailed information from a variety of trusted sources.
- **Summarization:** Receive summarized answers to your questions, saving time while still gaining valuable insights.
- **Knowledge Enhancement:** Enhance your knowledge with accurate and reliable information from authoritative sources.
- **API Integration:** Seamlessly integrate the bot into your applications and services using the provided API.

To get started with the Question-Answering Bot, follow these steps:

1. Clone this repository to your local machine.
2. Install the necessary dependencies mentioned in the project's requirements.
3. Set up your API keys and credentials for the data sources (Google, Wikipedia).
4. Run the FastAPI application to start the bot.
5. Make API calls to the bot with your queries and receive summarized answers.
