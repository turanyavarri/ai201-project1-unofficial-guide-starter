import os
from dotenv import load_dotenv
load_dotenv()
from groq import Groq
import gradio as gr
from embed import build_vector_store, retrieve

# Load vector store and model
print("Loading vector store...")
collection, model = build_vector_store()

# Set up Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def ask(question):
    # Retrieve top 5 relevant chunks
    results = retrieve(question, model, collection)
    
    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    
    # Build context from retrieved chunks
    context = ""
    sources = []
    for chunk, meta in zip(chunks, metadatas):
        context += f"Source: {meta['source']}\n{chunk}\n\n"
        if meta['source'] not in sources:
            sources.append(meta['source'])
    
    # Build grounded prompt
    prompt = f"""You are a helpful assistant answering questions about Rutgers University dining.
Answer the question using ONLY the information provided in the documents below.
If the documents do not contain enough information to answer the question, say "I don't have enough information on that."
Do not use any outside knowledge.

Documents:
{context}

Question: {question}
Answer:"""

    # Call Groq LLM
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    answer = response.choices[0].message.content
    return answer, sources

def handle_query(question):
    answer, sources = ask(question)
    sources_text = "\n".join(f"• {s}" for s in sources)
    return answer, sources_text

# Build Gradio UI
with gr.Blocks(title="Rutgers Dining Guide") as demo:
    gr.Markdown("# 🍽️ Rutgers Unofficial Dining Guide")
    gr.Markdown("Ask anything about Rutgers dining halls, meal plans, and food locations.")
    
    inp = gr.Textbox(label="Your question", placeholder="e.g. Which dining hall is the best?")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=4)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()