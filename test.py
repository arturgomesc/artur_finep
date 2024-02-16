import os
import logging
from PyPDF2 import PdfReader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)


def read_pdf_file(file_path):
    try:
        pdf_reader = PdfReader(file_path)
        document_text = "".join(page.extract_text() + "\n" for page in pdf_reader.pages if page.extract_text())
        return document_text
    except Exception as e:
        logging.error(f"Erro ao processar o arquivo {file_path}: {e}")
        return None


def extract_pdf_texts(directory):
    pdf_texts = []
    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            complete_path = os.path.join(directory, file)
            document_text = read_pdf_file(complete_path)
            if document_text:
                pdf_texts.append(document_text)
    return pdf_texts


def save_txt_file(text_content, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for text in text_content:
            file.write(text + "\n\n")


directory_pdfs = "/home/artur/Documentos/arquivos_dnx/finep/artur_finep/normas_regulamentadoras"
texts = extract_pdf_texts(directory_pdfs)

file_path_txt = "/home/artur/Documentos/arquivos_dnx/finep/artur_finep/txt_content/textos.txt"
save_txt_file(texts, file_path_txt)

if not texts:
    logging.info("Nenhum texto foi extraído dos PDFs.")
else:
    loader = TextLoader("txt_content/textos.txt", encoding="utf-8")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)

    # new_db = FAISS.load_local("txt_content/faiss_index", embeddings)

    # new_db.save_local("txt_content")

    query = "Queimaduras em ambiente de trabalho"
    docs = db.similarity_search(query)
    print(docs)
