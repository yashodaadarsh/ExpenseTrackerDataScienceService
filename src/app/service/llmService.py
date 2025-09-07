import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from entity.Expense import Expense # Assuming Expense is defined elsewhere

class LLMService:
    def __init__(self):
        load_dotenv()
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert extraction algorithm. "
                    "Only extract relevant information from the text. "
                    "If you do not know the value of an attribute asked to extract, "
                    "return null for the attribute's value."
                ),
                ("human", "{text}")
            ]
        )
        
        # Best practice: Retrieve the Google API key from the environment variable
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")

        # Switch to the free-tier-friendly model gemini-1.5-flash
        # This model has higher free-tier limits and is optimized for speed
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
            google_api_key=google_api_key
        )

        self.runnable = self.prompt | self.llm.with_structured_output(schema=Expense)

    def runLLM(self, message: str):   
        print("Invoking LLM with message:", message)
        try:
            ans = self.runnable.invoke({"text": message})
            print("Raw LLM response:", ans)
        except Exception as e:
            print("Error invoking LLM:", e)
            raise
        
        # Check if model_dump() is available before calling it
        if hasattr(ans, "model_dump"):
            return ans.model_dump()
        return ans
