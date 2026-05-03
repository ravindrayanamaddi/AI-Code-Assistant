# 💻 AI Code Assistant 

## 🚀 Project Overview

AI Code Assistant is a Generative AI project that converts natural language coding queries into working Python code using:

* Retrieval-Augmented Generation (RAG)
* Vector Database (FAISS)
* NLP-based query understanding

The system retrieves relevant coding examples from a knowledge base and generates accurate code, explanations, and test cases.

---

## 🧠 Features

* 🔍 Semantic search using FAISS vector database
* 🧾 Code generation from natural language queries
* 📚 Uses custom knowledge base (`python_examples.txt`)
* 🧪 Automatic test case generation
* ⚡ Code execution inside the app
* 🖥️ Interactive UI using Streamlit

---

## 🛠️ Tech Stack

* Python
* LangChain
* FAISS
* Hugging Face Embeddings
* Streamlit
* NLP

---

## 📂 Project Structure

```
AI Code Assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── knowledge_base/
│   └── python_examples.txt
└── venv/
```

---

## ⚙️ Installation

### 1. Clone the repository

```
git clone https://github.com/your-username/ai-code-assistant.git
cd ai-code-assistant
```

### 2. Create virtual environment

```
python -m venv venv
```

Activate:

**Windows**

```
venv\Scripts\activate
```

**Git Bash**

```
source venv/Scripts/activate
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

## 🧪 Example Inputs

Try these queries:

```
Check if a number is prime
Reverse a string
Find second largest number in a list
Binary search
Flatten a nested list
```

---

## 📸 Output

The system generates:

* ✅ Python Code
* ✅ Explanation
* ✅ Test Cases
* ✅ Execution Result

---

## ⚠️ Limitations

* Works only for problems available in `python_examples.txt`
* Accuracy depends on knowledge base quality
* Not a full LLM-based solution (RAG-only approach)

---

## 🔥 Future Improvements

* Integrate LLM (OpenAI / Hugging Face)
* Support unseen queries
* Add more coding problems (100+)
* Improve semantic matching
* Deploy on cloud (Streamlit Cloud / AWS)

---

## 💼 Resume Description

Built an AI Code Assistant using RAG and FAISS vector database to generate Python code from natural language queries. Implemented semantic search using embeddings and developed a Streamlit-based interactive interface with code execution capabilities.

---

## 👨‍💻 Author

Ravindra Yanamaddi

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
