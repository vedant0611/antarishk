from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.retrievers import EnsembleRetriever
from langchain.vectorstores import FAISS
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}

def context_prompt(retriever_prompt,gemini_embeddings):
    contextualize_q_prompt  = ChatPromptTemplate.from_messages(
        [
            ("system", retriever_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    vectordb = FAISS.load_local("assets/exoplanet_1", gemini_embeddings,allow_dangerous_deserialization=True)
    # Create a retriever for querying the vector database
    retriever = vectordb.as_retriever(score_threshold=0.7)

    vectordb1 = FAISS.load_local("assets/exoplanet_2", gemini_embeddings,allow_dangerous_deserialization=True)
    retriever1= vectordb1.as_retriever(score_threshold=0.7)

    vectordb2 = FAISS.load_local("assets/exoplanet_3", gemini_embeddings,allow_dangerous_deserialization=True)
    retriever2= vectordb2.as_retriever(score_threshold=0.7)

    vectordb3 = FAISS.load_local("assets/exoplanet_4", gemini_embeddings,allow_dangerous_deserialization=True)
    retriever3= vectordb3.as_retriever(score_threshold=0.7)

    vectordb4 = FAISS.load_local("assets/exoplanet_5", gemini_embeddings,allow_dangerous_deserialization=True)
    retriever4= vectordb4.as_retriever(score_threshold=0.7)

    vectordb5 = FAISS.load_local("assets/exoplanet_6", gemini_embeddings,allow_dangerous_deserialization=True)
    retriever5 = vectordb5.as_retriever(score_threshold=0.7)

    ensemble_retriever = EnsembleRetriever(
        retrievers=[retriever, retriever1, retriever2,retriever3,retriever4,retriever5], weights=[100, 100,100,100,100,100]
    )

    return ensemble_retriever,contextualize_q_prompt 

def qa_chain(system_prompt,model):
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"), # Added context to the human message
        ]
    )

    question_answer_chain = create_stuff_documents_chain(model, qa_prompt)

    return question_answer_chain

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def conversational_rag(rag_chain):

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    return conversational_rag_chain
