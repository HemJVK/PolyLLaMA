# llm.py
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import uvicorn
import cProfile
import pstats

app = FastAPI()

class MarathiQuestion(BaseModel):  # Pydantic model for validation
    question: str

# Initialize LLM and Prompt (do this ONCE)
try:
    llm = ChatOllama(model="llama3.1:8b", temperature=0.7)
    prompt = ChatPromptTemplate.from_messages([
        ("ai", "तुम्ही एक मदतनीस आहात."),
        ("human", "{question}"),
    ])
    memory = ConversationBufferMemory()
    marathi_chain = prompt | llm
    marathi_llm_chain = LLMChain(
    llm=llm, 
    prompt=prompt, # Use prompt here
    memory=memory, 
    output_key="answer"
)

except Exception as e:
    print(f"Error initializing LLM or prompt: {e}")
    llm = None
    prompt = None
    marathi_llm_chain = None

@app.post("/ask_marathi")
async def ask_marathi(request_data: MarathiQuestion):
    print("In Marati")# Use Pydantic model
    if llm is None or prompt is None or marathi_llm_chain is None:
        raise HTTPException(status_code=500, detail="LLM or prompt initialization failed.")

    try:
        pr = cProfile.Profile()
        pr.enable()  # Start profiling


        pr.disable()  # Stop profiling
        ps = pstats.Stats(pr)
        ps.sort_stats('time')  # Sort by time
        ps.print_stats(20)  # Print the top 20 time-consuming functions
        result = marathi_llm_chain.invoke({"question": request_data.question})
        return {"answer": result["answer"]}
    except Exception as e:
        import traceback  # Import the traceback module

        traceback.print_exc()  # Print the full traceback to the console

        print(f"Error during conversation: {e}")  # Keep this for a simpler message
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

if __name__ == "__main__":
    uvicorn.run(app="llm:app", host="0.0.0.0", port=8000, reload=False)