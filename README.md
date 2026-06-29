# 📄 DocuSense AI — AI-Powered Multilingual Document Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?style=flat-square&logo=streamlit)
![AWS](https://img.shields.io/badge/AWS-S3_&_DynamoDB-orange?style=flat-square&logo=amazonaws)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow?style=flat-square)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-black?style=flat-square&logo=github)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

> An AI-powered multilingual document intelligence platform that extracts text from scanned documents, classifies document types, summarizes content, performs semantic search, answers natural language questions, and securely stores documents using Amazon S3 with metadata managed in Amazon DynamoDB.

---

# 🎯 The Problem

Organizations process thousands of documents every day, including:

- National Identity Cards
- Certificates
- Invoices
- Reports
- Resumes
- Forms
- Academic Documents

Searching these documents manually is slow, repetitive, and prone to human error.

Many organizations also lack intelligent systems capable of understanding document content instead of simply storing files.

**DocuSense AI solves this problem** by combining OCR, Natural Language Processing (NLP), Semantic Search, Question Answering, and AWS Cloud services into one intelligent document management platform.

---

# ✨ Features

✅ OCR Text Extraction

✅ PDF Processing

✅ Language Detection

✅ Document Classification

✅ Information Extraction

✅ AI-powered Document Summarization

✅ Named Entity Recognition (NER)

✅ Question Answering

✅ Semantic Search

✅ Amazon S3 Cloud Storage

✅ Amazon DynamoDB Metadata Storage

✅ GitHub Actions Continuous Integration (CI)

---

# ☁️ Full AI Cloud Architecture

```text
                    User Uploads Document
                             │
                             ▼
                  Streamlit Web Application
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
 Amazon S3            OCR Extraction       PDF Processing
(File Storage)              │
                             ▼
                   Language Detection
                             ▼
                Document Classification
                             ▼
                Information Extraction
                             ▼
                   AI Summarization
                             ▼
              Named Entity Recognition
                             ▼
                 Semantic Search (FAISS)
                             ▼
                 Question Answering
                             ▼
              Amazon DynamoDB Metadata
```

---

# 🧠 AI Processing Pipeline

```text
Upload Document
       │
       ▼
OCR / PDF Extraction
       │
       ▼
Language Detection
       │
       ▼
Document Classification
       │
       ▼
Information Extraction
       │
       ▼
AI Summary
       │
       ▼
Named Entity Recognition
       │
       ▼
Semantic Search
       │
       ▼
Question Answering
       │
       ▼
Amazon S3 Upload
       │
       ▼
Amazon DynamoDB Storage
```

---

# 🛠️ Technology Stack

| Category | Technology | Purpose |
|-----------|------------|---------|
| **Programming Language** | Python 3.11 | Backend Development |
| **Web Framework** | Streamlit | Interactive Web Application |
| **OCR** | PyTesseract + OpenCV | Text Extraction |
| **PDF Processing** | PyPDF2 | PDF Reading |
| **Natural Language Processing** | Hugging Face Transformers | AI Summary & QA |
| **Semantic Search** | FAISS | Vector Similarity Search |
| **Language Detection** | langdetect | Detect Document Language |
| **Named Entity Recognition** | spaCy | Entity Extraction |
| **Cloud Storage** | Amazon S3 | Store Uploaded Documents |
| **NoSQL Database** | Amazon DynamoDB | Store Document Metadata |
| **Version Control** | Git | Source Code Management |
| **CI/CD** | GitHub Actions | Automatic Testing |
| **IDE** | Visual Studio Code | Development |

---

# 📊 System Workflow

```text
User
 │
 ▼
Upload Image / PDF
 │
 ▼
Extract Text
 │
 ▼
Analyze Document
 │
 ├────────► Detect Language
 │
 ├────────► Classify Document
 │
 ├────────► Extract Information
 │
 ├────────► Generate Summary
 │
 ├────────► Extract Named Entities
 │
 ├────────► Build Semantic Index
 │
 ├────────► Answer Questions
 │
 ▼
Store File → Amazon S3
 │
 ▼
Store Metadata → Amazon DynamoDB
 │
 ▼
Display Results to User
```

---

# 🌟 Key Highlights

- 📄 Intelligent document understanding
- 🌍 Multilingual document support
- 🤖 AI-powered document summarization
- 🔍 Semantic search using vector embeddings
- 💬 Natural language question answering
- ☁️ Secure cloud storage with Amazon S3
- 🗄️ Metadata management using Amazon DynamoDB
- ⚙️ Automated GitHub Actions CI pipeline
- 🚀 Modern interactive Streamlit interface
- 📚 Easily extensible architecture

---

# 🚀 Quick Start

## Prerequisites

Before running the project, ensure you have installed:

- Python 3.11+
- Git
- Visual Studio Code
- Tesseract OCR
- AWS CLI
- AWS Account
- Amazon S3 Bucket
- Amazon DynamoDB Table

---

# 📥 Clone Repository

```bash
git clone https://github.com/NavoSandeepani/DocuSense-AI.git

cd DocuSense-AI
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ☁️ Configure AWS

Configure AWS CLI.

```bash
aws configure
```

Enter the following:

```
AWS Access Key ID

AWS Secret Access Key

Region:
ap-southeast-2

Output:
json
```

---

# 🪣 Create Amazon S3 Bucket

Create an Amazon S3 bucket.

Example:

```
docusense-storage-navodya
```

This bucket securely stores uploaded documents.

---

# 🗄️ Create Amazon DynamoDB Table

Create a table using the following configuration.

**Table Name**

```
DocuSenseDocuments
```

**Partition Key**

```
document_id
```

**Type**

```
String
```

---

# ▶️ Run the Application

Start Streamlit.

```bash
streamlit run src/app.py
```

Open your browser:

```
http://localhost:8501
```

---

# 💻 How to Use DocuSense AI

### Step 1

Upload any supported document.

Supported file formats:

- PNG
- JPG
- JPEG
- PDF

---

### Step 2

The application automatically performs:

- OCR Text Extraction
- PDF Processing
- Language Detection
- Document Classification
- Information Extraction
- AI Summary
- Named Entity Recognition
- Semantic Search Indexing

---

### Step 3

Ask natural language questions.

Examples:

```
Who owns this document?

What is this document about?

Summarize this document.

What is the registration number?

When was this certificate issued?

Who issued this certificate?

What is the student's name?
```

---

### Step 4

The uploaded document is automatically stored in Amazon S3.

---

### Step 5

Document metadata is automatically stored in Amazon DynamoDB.

---

# 📁 Project Structure

```text
DocuSense-AI/
│
├── .github/
│   └── workflows/
│       └── python-ci.yml
│
├── docs/
│
├── src/
│   ├── app.py
│   ├── ocr.py
│   ├── pdf_extractor.py
│   ├── document_classifier.py
│   ├── information_extractor.py
│   ├── summarizer.py
│   ├── ner_extractor.py
│   ├── semantic_search.py
│   ├── question_answering.py
│   ├── s3_upload.py
│   ├── dynamodb.py
│   └── ...
│
├── tests/
│
├── requirements.txt
├── README.md
├── test_setup.py
└── .gitignore
```

---

# 📸 Application Screenshots

### 🏠 Home Page

```
docs/home.png
```

---

### 🤖 AI Summary

```
docs/summary.png
```

---

### 💬 Question Answering

```
docs/question_answering.png
```

---

### 🔍 Semantic Search

```
docs/search.png
```

---

### ☁️ Amazon S3

```
docs/s3_bucket.png
```

---

### 🗄️ Amazon DynamoDB

```
docs/dynamodb.png
```

---

# 🔒 AWS Security

The project follows AWS best practices.

✅ IAM User

✅ Amazon S3 Bucket Permissions

✅ Amazon DynamoDB Permissions

✅ AWS CLI Authentication

✅ Git Ignore for Credentials

AWS credentials are **never committed** to GitHub.

---

# 📤 Upload Workflow

```text
Upload Document
        │
        ▼
Save Temporary File
        │
        ▼
Upload to Amazon S3
        │
        ▼
Extract Text
        │
        ▼
AI Processing
        │
        ▼
Store Metadata
        │
        ▼
Amazon DynamoDB
        │
        ▼
Display Results
```

---

# 🤖 AI Capabilities

## 📄 OCR Text Extraction

Extracts text from:

- PNG Images
- JPG Images
- JPEG Images
- PDF Documents

---

## 🌍 Language Detection

Automatically identifies the language of uploaded documents.

Supported examples include:

- English
- Sinhala
- Tamil
- Other supported languages

---

## 🏷️ Document Classification

Automatically classifies uploaded documents into categories such as:

- National ID Card
- Resume / CV
- Certificate
- Invoice
- Report
- Academic Document
- Form

---

## 📌 Information Extraction

Extracts structured information from documents including:

- Person Names
- Organizations
- Dates
- Locations
- Registration Numbers
- Email Addresses
- Phone Numbers

---

## 🤖 AI Document Summary

Generates concise summaries using Hugging Face Transformer models.

Example:

```
This document is a university assignment discussing
Artificial Intelligence applications in healthcare...
```

---

## 🏷️ Named Entity Recognition (NER)

Automatically detects important entities.

Example:

```
PERSON

University of Jaffna

ORG

Sri Lanka

GPE

2026

DATE
```

---

## 🔍 Semantic Search

Searches documents based on meaning instead of exact keywords.

Example queries:

```
Machine Learning

University

Invoice Amount

Registration Number
```

---

## 💬 Question Answering

Ask natural language questions such as:

```
What is this document about?

Who owns this document?

What is the registration number?

Summarize this document.

When was it issued?

Who signed the document?
```

---

# ☁️ AWS Cloud Integration

## Amazon S3

Every uploaded document is automatically stored in Amazon S3.

Features:

- Cloud Storage
- Secure Upload
- Timestamp-based File Naming
- Highly Scalable Storage

---

## Amazon DynamoDB

Stores document metadata including:

- Document ID
- File Name
- Language
- Document Type
- Upload Time
- Amazon S3 Object Key

This enables efficient document management and retrieval.

---

# 🔄 GitHub Actions CI/CD

Every push to the **main** branch automatically executes the pipeline.

```
Developer Pushes Code
          │
          ▼
GitHub Repository
          │
          ▼
GitHub Actions
          │
          ├── Install Dependencies
          ├── Check Python Syntax
          ├── Test AWS Connection
          ├── Validate Project
          └── Build Successful
```

---

# 🧪 Testing

Run local tests using:

```bash
python test_setup.py
```

GitHub automatically validates every commit before deployment.

---

# 📈 Future Improvements

The following features are planned for future releases.

### ☁️ AWS

- Amazon Textract
- Amazon Comprehend
- Amazon Bedrock
- AWS Lambda
- Amazon API Gateway
- Amazon SNS Notifications

---

### 🤖 Artificial Intelligence

- Retrieval-Augmented Generation (RAG)
- Multi-document Question Answering
- Large Language Models (LLMs)
- AI Chat Assistant
- Document Recommendation System

---

### 🌐 Application

- User Authentication
- Role-Based Access Control
- Upload History
- Analytics Dashboard
- REST API (FastAPI)
- Mobile Application (Flutter)

---

### 🚀 Deployment

- Docker
- AWS EC2
- AWS ECS
- AWS App Runner
- Kubernetes
- Terraform Infrastructure

---

# 🎓 What I Learned

Developing **DocuSense AI** strengthened my practical knowledge in:

- Optical Character Recognition (OCR)
- Natural Language Processing (NLP)
- Semantic Search
- Question Answering Systems
- Document Intelligence
- Amazon S3
- Amazon DynamoDB
- AWS IAM
- GitHub Actions CI/CD
- Cloud-Based AI Applications

This project helped me understand how modern AI applications combine
machine learning, cloud computing, and software engineering to build
real-world intelligent document processing systems.

---

# 📬 Connect

**Navodya Sandeepani**

Final Year BSc (Hons) Computer Engineering Student

University of Jaffna

🇱🇰 Sri Lanka

---

### GitHub

https://github.com/NavoSandeepani

---

### LinkedIn

https://www.linkedin.com/in/navodya-mapa-684b83321/

---

📧 Email

navodyamapa444@gmail.com

---

Currently seeking internship opportunities in:

- Artificial Intelligence
- Machine Learning
- Data Science
- Cloud Engineering
- MLOps

Open to both remote and on-site opportunities.

---

# 📄 License

MIT License

Feel free to use, modify, and distribute this project for educational and research purposes.

---

<div align="center">

# 📄 DocuSense AI

### Intelligent Document Understanding using Artificial Intelligence and AWS Cloud

**Built with ❤️ using**

Python • Streamlit • Hugging Face • FAISS • OpenCV • PyTesseract • Amazon S3 • Amazon DynamoDB • GitHub Actions

⭐ If you found this project useful, consider giving it a star on GitHub!

</div>