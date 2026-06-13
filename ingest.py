import os
import pdfplumber

def load_documents(folder="documents"):
    docs = []
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if filename.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
        elif filename.endswith(".pdf"):
            with pdfplumber.open(filepath) as pdf:
                text = "\n\n".join(
                    p.extract_text() for p in pdf.pages if p.extract_text()
                )
        else:
            continue
        docs.append({"source": filename, "text": text})
    return docs

def clean_text(text):
    import re
    
    # Remove lines containing ad/promoted content keywords
    ad_keywords = [
    'Promoted', 'JumpCloud', 'TruGreen', 'USAA', 'monday.com',
    'guardianbikes', 'GuardianBike', 'washingtonpost', 'schwab', 'rxnt', 
    'Clickable image', 'Collapse video player', 'Thumbnail image', 'Sign Up', 
    'Shop Now', 'Learn More', 'Subscribe', '0:00', 'video player'
    ]
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        if not any(keyword.lower() in line.lower() for keyword in ad_keywords):
            cleaned_lines.append(line)
    text = '\n'.join(cleaned_lines)
    
    # Remove usernames and URLs
    text = re.sub(r'u/\w+', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\w+\.(com|org|net|gov)\b', '', text)
    
    # Remove noise
    text = re.sub(r'\bavatar\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Local Guide·[\d]+ reviews·[\d]+ photos', '', text)
    text = re.sub(r'\d+ more repl\w+', '', text)
    text = re.sub(r'\b\d+[ymdh] ago\b', '', text)
    text = re.sub(r'•', '', text)
    
    # Only remove 1-2 digit standalone numbers (vote counts), keep 3+ digit numbers like 210
    text = re.sub(r'(?<!\w)\d{1,2}(?!\w)', '', text)

    # Clean whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def chunk_text(text, chunk_size=400, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

if __name__ == "__main__":
    docs = load_documents()
    all_chunks = []
    for doc in docs:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned)
        for i, chunk in enumerate(chunks):
            all_chunks.append({"source": doc["source"], "chunk_index": i, "text": chunk})
    
    print(f"Total chunks: {len(all_chunks)}")
    print("\n--- 5 Sample Chunks ---")
    for chunk in all_chunks[:5]:
        print(f"\nSource: {chunk['source']}")
        print(f"Text: {chunk['text']}")
        print("-" * 40)