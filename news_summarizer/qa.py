# qa.py
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def answer_question(article: str, question: str, api_key: str) -> str:
    if not article.strip():
        return "No article available. Please paste a news article first."
    if not question.strip():
        return "Please enter a valid question."

    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            groq_api_key=api_key,
            temperature=0.1
        )

        prompt = PromptTemplate(
            input_variables=["article", "question"],
            template=(
                "You are an AI assistant helping a user understand a news article.\n"
                "Answer the user's question based strictly on the provided article content.\n\n"
                "Article:\n{article}\n\n"
                "Question: {question}\n\n"
                "Instructions:\n"
                "- If the answer can be found in the article, provide a clear and direct answer.\n"
                "- If the article does not contain enough information to answer the question, reply exactly with: "
                "'This information is not available in the provided article.'\n\n"
                "Answer:"
            )
        )

        chain = prompt | llm | StrOutputParser()
        return chain.invoke({
            "article": article[:6000],
            "question": question
        }).strip()

    except Exception as e:
        return f"Error answering question: {str(e)}"
