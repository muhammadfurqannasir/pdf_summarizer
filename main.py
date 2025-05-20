import streamlit as st
from pypdf import PdfReader
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import tempfile
import os
# Add local nltk_data path
nltk_data_path = "D:\try\nltk_data"
nltk.data.path.append(nltk_data_path)

# Function to extract text from a PDF
def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        all_text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
        return all_text if all_text.strip() else "No readable text found in the PDF."
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"An error occurred: {e}"

# Function to summarize text
def summarize_text(text, max_sentences=30):
    if not text.strip():
        return "No content to summarize."

    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)

    freq_table = {}
    for word in words:
        word = word.lower()
        if word.isalpha() and word not in stop_words:
            freq_table[word] = freq_table.get(word, 0) + 1

    sentences = sent_tokenize(text)
    sentence_scores = {}
    for sentence in sentences:
        for word in freq_table:
            if word in sentence.lower():
                sentence_scores[sentence] = sentence_scores.get(sentence, 0) + freq_table[word]

    ranked_sentences = sorted(sentence_scores.items(), key=lambda item: item[1], reverse=True)
    top_sentences = [sentence for sentence, _ in ranked_sentences[:max_sentences]]
    summary = " ".join(top_sentences)
    return summary if summary.strip() else "The text could not be summarized meaningfully."

def main():
    st.title("PDF Text Extractor and Summarizer")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            file_path = temp_file.name

        st.info(f"File uploaded successfully. Processing: {uploaded_file.name}")

        text = extract_text_from_pdf(file_path)

        if text.startswith("Error") or text == "No readable text found in the PDF.":
            st.error(text)
        else:
            st.subheader("Extracted Text:")
            st.text(text)

            st.subheader("Summary:")
            max_sentences = st.slider("Maximum Summary Sentences", min_value=1, max_value=50, value=10, step=1)
            summary = summarize_text(text, max_sentences=max_sentences)
            st.write(summary)

        os.remove(file_path)

if __name__ == "__main__":
    main()
