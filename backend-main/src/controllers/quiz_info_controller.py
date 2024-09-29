from src.helpers.index import quiz_info_helper
from src.helpers.index import info_image_helpers
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import src.helpers.index as helper

helper.initializaion()

template = """" You are an assistant for generating quiz
    Use the following pieces of retrieved context to generate response you can also use your own information in combination to help generate quizes
    In all the cases generate the question answers pair for the quiz.
    "\n\n"
{context1}

{context2}

{context3}

{context4}

{context5}

{context6}
Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

template_info = """
    You are an assistant for generating responses. 
    Use the following pieces of retrieved context to generate response.
    you can also use your own information in combination to help generate response.
    Provide the answer in about 150-200 words
    Provide the response in great detail.
    Provide the answer in a language according to the age.
    \n\n
    \n\n
{context1}

{context2}

{context3}

{context4}

{context5}

{context6}
Question: {question}
"""
prompt_info = ChatPromptTemplate.from_template(template_info)

def generate_quiz(data):
    gemini_embeddings, model =helper.models()
    age = data['age']
    input_query =  f"Generate a multiple-choice quiz about exoplanets with 10 questions for a {age}-year-old."
    input_query += """Each question should have a question, field (a short label that describes the topic of the question), customOptions (an array with four answer choices), and correctAnswer (the correct answer from the options).
The response should be provided in the following JSON format:
[
    {
        "question": "What is an exoplanet?",
        "field": "exoplanetDefinition",
        "customOptions": [
            "A planet that orbits a star outside our solar system",
            "A moon of Jupiter",
            "A star that is dying",
            "A comet passing through"
        ],
        "correctAnswer": "A planet that orbits a star outside our solar system"
    },
    {
        "question": "Which method is commonly used to detect exoplanets?",
        "field": "detectionMethod",
        "customOptions": [
            "Radial velocity",
            "Astrometry",
            "Transit method",
            "All of the above"
        ],
        "correctAnswer": "All of the above"
    }
]

Above is the example for your reference, please provide the response in same format. Generate the quiz in story telling format where each question is a tep to formation and completion of story. The stpry format should be engaging for the users to learn and have fun.
"""
    retriever,retriever1,retriever2,retriever3,retriever4,retriever5 = quiz_info_helper.context(gemini_embeddings)
    chain = (
        {"context1": retriever,
         "context2": retriever1,
         "context3": retriever2,
         "context4": retriever3,
         "context5": retriever4,
         "context6": retriever5,
         "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    result = chain.invoke(input_query)
    result
    print(result)
    return {"result":result},200

def generate_info(data):
    planet = data['planet']
    age = data['age']
    info_query = f"what is {planet}. Explain like you are explaining it to a {age} year old. Generate the response in a story telling format where the info is explained through a story for better engagement and understanding."
    gemini_embeddings, model =helper.models()
    retriever,retriever1,retriever2,retriever3,retriever4,retriever5 = quiz_info_helper.context(gemini_embeddings)
    chain = (
        {"context1": retriever,
         "context2": retriever1,
         "context3": retriever2,
         "context4": retriever3,
         "context5": retriever4,
         "context6": retriever5,
         "question": RunnablePassthrough()}
        | prompt_info
        | model
        | StrOutputParser()
    )
    result = chain.invoke(info_query)
    result
    print(result)
    random_image_url = info_image_helpers.get_random_image_url()
    
    if random_image_url:
        print(f"Random Image URL: {random_image_url}")
    else:
        print("No images found in the bucket.")
    return {"result":result, "image_url":random_image_url},200


