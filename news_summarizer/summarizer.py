# summarizer.py
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def generate_summary(text: str, api_key: str) -> str:
    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            groq_api_key=api_key,
            temperature=0.3
        )

        prompt = PromptTemplate(
            input_variables=["article"],
            template=(
                "You are an expert news editor. "
                "Read the news article below and write a concise summary in 3 to 5 bullet points. "
                "Each bullet point should cover one key fact. Be clear and brief.\n\n"
                "Article:\n{article}\n\n"
                "Summary (bullet points):"
            )
        )

        chain = prompt | llm | StrOutputParser()
        return chain.invoke({"article": text[:6000]}).strip()

    except Exception as e:
        return f"Error generating summary: {str(e)}"
