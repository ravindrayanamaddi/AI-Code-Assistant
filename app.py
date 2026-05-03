import re
import os
import tempfile
import subprocess

import streamlit as st

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


# --------------------------------------------------
# 1. Streamlit Page Setup
# --------------------------------------------------

st.set_page_config(
    page_title="AI Code Assistant",
    page_icon="💻",
    layout="wide"
)

st.title("💻 AI Code Assistant")
st.write("Generate correct Python code, explanation, and test cases using RAG.")


# --------------------------------------------------
# 2. User Input
# --------------------------------------------------

user_query = st.text_area(
    "Enter your coding request",
    placeholder="Example: Write a Python function to check if a number is prime"
)

run_code_option = st.checkbox("Run generated code")


# --------------------------------------------------
# 3. Create Vector Database
# --------------------------------------------------

@st.cache_resource
def create_vector_db():
    # Use a RELATIVE path (important for Streamlit Cloud)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "data")

    documents = []

    # Load all supported files safely
    for file in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, file)

        try:
            if file.endswith(".txt"):
                loader = TextLoader(file_path, encoding="utf-8")

            elif file.endswith(".pdf"):
                loader = PyPDFLoader(file_path)

            else:
                print(f"Skipping unsupported file: {file}")
                continue

            docs = loader.load()
            documents.extend(docs)

        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")

    if not documents:
        raise RuntimeError("No documents loaded. Check your /data folder.")

    return documents


# --------------------------------------------------
# 4. Extract Code, Explanation, Tests from RAG Context
# --------------------------------------------------

def extract_section(text, start_label, end_labels):
    pattern = rf"{start_label}:\s*(.*?)(?=" + "|".join([rf"{label}:" for label in end_labels]) + r"|$)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return ""


def build_answer_from_context(context, query):
    query = query.lower()

    examples = context.split("Example")
    best_match = None
    best_score = 0

    query_words = set(query.replace("write", "")
                      .replace("python", "")
                      .replace("function", "")
                      .replace("to", "")
                      .split())

    for example in examples:
        example_words = set(example.lower().split())
        score = len(query_words.intersection(example_words))

        if score > best_score:
            best_score = score
            best_match = example

    if not best_match or best_score == 0:
        return None, None, None

    code = extract_section(best_match, "Code", ["Explanation", "Test Cases"])
    explanation = extract_section(best_match, "Explanation", ["Test Cases"])
    test_cases = extract_section(best_match, "Test Cases", [])

    return code, explanation, test_cases

# --------------------------------------------------
# 5. Code Quality Check
# --------------------------------------------------

def is_valid_python_code(code):
    try:
        compile(code, "<string>", "exec")
        return True, "Valid Python code"
    except SyntaxError as e:
        return False, str(e)


# --------------------------------------------------
# CLEAN CODE BEFORE EXECUTION
# --------------------------------------------------

def clean_code_block(text):
    """
    Removes unwanted sections like Example, Task, etc.
    Keeps only valid Python code.
    """
    lines = text.split("\n")

    clean_lines = []

    for line in lines:
        if line.strip().startswith("Example"):
            break
        if line.strip().startswith("Task"):
            break

        clean_lines.append(line)

    return "\n".join(clean_lines).strip()


# --------------------------------------------------
# RUN PYTHON CODE
# --------------------------------------------------

def run_python_code(code, test_cases=""):
    # Clean code and test cases
    code = clean_code_block(code)
    test_cases = clean_code_block(test_cases)

    final_code = code + "\n\n" + test_cases

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".py",
        mode="w",
        encoding="utf-8"
    ) as temp_file:
        temp_file.write(final_code)
        temp_file_path = temp_file.name

    try:
        result = subprocess.run(
            ["python", temp_file_path],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.stderr:
            return "ERROR:\n" + result.stderr

        if result.stdout:
            return "OUTPUT:\n" + result.stdout

        return "Code executed successfully."

    except subprocess.TimeoutExpired:
        return "ERROR: Code execution timed out."


# --------------------------------------------------
# 7. Load RAG Components
# --------------------------------------------------

with st.spinner("Loading vector database..."):
    vector_db = create_vector_db()
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})


# --------------------------------------------------
# 8. Generate Response
# --------------------------------------------------

if st.button("Generate"):
    if not user_query.strip():
        st.warning("Please enter a coding request.")
    else:
        with st.spinner("Retrieving best matching program..."):
            retrieved_docs = retriever.invoke(user_query)

            context = "\n\n".join(
                [doc.page_content for doc in retrieved_docs]
            )

            code, explanation, test_cases = build_answer_from_context(context, user_query)

        if not code:
            st.error(
                "No matching code found in knowledge base. "
                "Add this problem to python_examples.txt."
            )
            st.stop()

        valid, message = is_valid_python_code(code)

        if not valid:
            st.error("Retrieved code has syntax error:")
            st.code(message)
            st.stop()

        st.subheader("Generated Python Code")
        st.code(code, language="python")

        st.subheader("Explanation")
        st.write(explanation)

        st.subheader("Test Cases")
        st.code(test_cases, language="python")

        with st.expander("Retrieved RAG Context"):
            st.write(context)

        if run_code_option:
            st.subheader("Code Execution Result")
            result = run_python_code(code, test_cases)
            st.code(result)
