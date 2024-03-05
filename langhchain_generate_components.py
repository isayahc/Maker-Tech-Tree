""" 
#TODO: make a agent that uses HUMAMN as a tool to get:
- Purpose of science experiment
- What fields of study do they already know of

#IDEA: Platform generate more indepth experiments by generaing a data set and generate / collect scienfic data

### Chatbot
the chatbot helps the BOUNTY_BOARD_CHAIN generate science experiments

### EXPERIMENT and Provide feedback on experiments

### Interrgration

- I need to intergrate this code into the app. This includes creating an id for each post, and potentially and a comment section for each "Experiment"
- I addition i need to generate a mostly pinecone retriever to geenrate scientific experiments from the "community vectore search"
- potentially have prenium users store their private data, but i may not implement this during the hackathon
"""

# https://python.langchain.com/docs/modules/model_io/output_parsers/types/structured
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers import ArxivRetriever, pubmed
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers import ArxivRetriever
from langchain.retrievers import PubMedRetriever
from langchain.retrievers import WikipediaRetriever
from operator import itemgetter
# import dotenv
import os
from dotenv import load_dotenv

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


# The scheme for creating experiments
experiment_schema = [
    ResponseSchema(name="Material", description="list of materials need to perfrom the experiments please be specific", type="list"),
]


maker_schema = [
    ResponseSchema(name="Material", description="The base components needed to create this items from scratch DIY This item must be exact and not an estimation", type="list"),
]

experiment_output_parser = StructuredOutputParser.from_response_schemas(experiment_schema)
maker_output_parser = StructuredOutputParser.from_response_schemas(maker_schema)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

format_instructions = experiment_output_parser.get_format_instructions()


experiment_prompt = PromptTemplate(
    template="You must generate well detailed science experiments.\n{format_instructions}\n{question}\n{context}",
    input_variables=["question"],
    partial_variables={"format_instructions": format_instructions},
    memory = memory
)

maker_prompt = PromptTemplate(
    template="You must generate a well detailed list of items for creating a given item from scratch. \
        Also describe the purpose for a text-to-3d model to use for extra context\n{format_instructions}\n{question}\n{context}",
    input_variables=["question"],
    partial_variables={"format_instructions": format_instructions},
    memory = memory
)


def join_strings(*args: str) -> str:
    """
    Join an arbitrary number of strings into one string.
    
    Args:
        *args: Variable number of strings to join.
    
    Returns:
        str: Joined string.
    """
    return ''.join(args)

def format_docs(docs):
    return "\n\n".join([join_strings(d.page_content, d.metadata['Entry ID'],d.metadata['Title'], ) for d in docs])


arxiv_retriever = ArxivRetriever(load_max_docs=2)

# model = ChatOpenAI(temperature=0)
model = ChatOpenAI(temperature=0,model="gpt-4")


arxiv_retriever = ArxivRetriever(load_max_docs=2)

pub_med_retriever = PubMedRetriever()

wikipedia_retriever = WikipediaRetriever()

arxiv_chain = (
    {"context": arxiv_retriever, "question": RunnablePassthrough()}
    | experiment_prompt
    | model
    | experiment_output_parser
)

pub_med_chain = (
    {"context": pub_med_retriever, "question": RunnablePassthrough()}
    | experiment_prompt
    | model
    | experiment_output_parser
)

wikipedia_chain = (
    {"context": wikipedia_retriever, "question": RunnablePassthrough()}
    | experiment_prompt
    | model
    | experiment_output_parser
)

maker_wikipedia_chain = (
    {"context": wikipedia_retriever, "question": RunnablePassthrough()}
    | maker_prompt
    | model
    | maker_output_parser
)




if __name__ == "__main__":


    # query = "how to create electronoic on a cellulose subtstrate"
    query = "A Microscope"

    # output = wikipedia_chain.invoke(query)
    output = maker_wikipedia_chain.invoke(query)
    x=0

