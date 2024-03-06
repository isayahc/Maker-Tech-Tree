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


response_schemas = [
    ResponseSchema(name="Material", description="The base components needed to create this items from scratch DIY This item must be exact and not an estimation, also make sure each output has the obejcts name in context", type="list"),
    ResponseSchema(name="Fields_of_study", description="List the field of study this can be used for", type="list"),
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

format_instructions = output_parser.get_format_instructions()


prompt = maker_prompt = PromptTemplate(
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


retriver = arxiv_retriever = ArxivRetriever(load_max_docs=2)

pub_med_retriever = PubMedRetriever()

wikipedia_retriever = WikipediaRetriever()

arxiv_chain = (
    {"context": arxiv_retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | output_parser
)

pub_med_chain = (
    {"context": pub_med_retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | output_parser
)

wikipedia_chain = (
    {"context": wikipedia_retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | output_parser
)




if __name__ == "__main__":
    query = "MicroScope"
    pub_med_data = pub_med_chain.invoke(query)
    wiki_data = wikipedia_chain.invoke(query)

    x=0