# QueryAI – Intelligent Document Assistant

QueryAI is an AI-powered document question-answering application that allows users to upload PDF documents and ask natural-language questions about their content.

It uses a Retrieval-Augmented Generation (RAG) pipeline to retrieve relevant document context before generating responses with an LLM.

## Live Demo

https://query-ai-docs.vercel.app

## Features

- Upload PDF documents
- Extract and process document text
- Split documents into overlapping chunks
- Generate semantic embeddings
- Store and search embeddings using FAISS
- Retrieve relevant document context for user queries
- Generate context-aware answers using Gemini
- Display source page references
- Interactive React-based chat interface

## Tech Stack

### Frontend
- React.js
- Vite
- React Markdown

### Backend
- Python
- FastAPI
- LangChain
- PyPDF

### AI / RAG
- Gemini
- Gemini Embeddings
- FAISS
- Retrieval-Augmented Generation (RAG)

### Deployment
- Vercel
- Render

## Architecture

```text
React Frontend
      |
      v
FastAPI REST API
      |
      +---- PDF Processing
      |         |
      |         v
      |      Text Chunks
      |         |
      |         v
      |   Gemini Embeddings
      |         |
      |         v
      |       FAISS
      |
      v
Semantic Retrieval
      |
      v
Relevant Document Context
      |
      v
Gemini LLM
      |
      v
Context-Aware Answer