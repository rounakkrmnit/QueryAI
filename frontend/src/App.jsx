import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [documentReady, setDocumentReady] = useState(false);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const uploadDocument = async () => {
    if (!file) {
      setUploadStatus("Please select a PDF first.");
      return;
    }

    if (file.type !== "application/pdf") {
      setUploadStatus("Only PDF files are supported.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

      try {
        setUploadStatus("Uploading and processing...");

        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/documents/upload`,
          {
            method: "POST",
            body: formData,
          }
        );

        const data = await response.json();

        if (!response.ok) {
        throw new Error(data.detail || "Upload failed.");
      }

      setUploadStatus(
        `Uploaded successfully — ${data.pages} page(s), ${data.chunks} chunk(s).`
      );

      setDocumentReady(true);
      setMessages([]);
    } catch (error) {
      setUploadStatus(error.message);
      setDocumentReady(false);
    }
  };

  const askQuestion = async () => {
    if (!question.trim() || loading) return;

    if (!documentReady) {
      setUploadStatus(
        "Please upload and process a PDF before asking a question."
      );
      return;
    }

    const currentQuestion = question.trim();

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: currentQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: currentQuestion,
          k: 3,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to get answer.");
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Error: ${error.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>QueryAI</h1>
        <p>Intelligent Document Assistant</p>
      </header>

      <main className="chat-container">
        <section className="upload-section">
          <h2>Upload a document</h2>

          <p>
            Upload a PDF to start asking questions about its content.
          </p>

          <div className="upload-box">
            <input
              type="file"
              accept=".pdf,application/pdf"
              onChange={(event) => {
                setFile(event.target.files[0]);
                setDocumentReady(false);
                setUploadStatus("");
                setMessages([]);
              }}
            />

            <button onClick={uploadDocument}>
              Upload PDF
            </button>
          </div>

          {file && (
            <p className="selected-file">
              Selected: {file.name}
            </p>
          )}

          {uploadStatus && (
            <p className="upload-status">
              {uploadStatus}
            </p>
          )}
        </section>

        <section className="chat-section">
          <div className="welcome">
            <h2>Ask questions about your document</h2>

            <p>
              Use natural language to find relevant information.
            </p>
          </div>

          <div className="messages">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`message ${message.role}`}
              >
                <strong>
                  {message.role === "user" ? "You" : "QueryAI"}
                </strong>

                <div className="message-content">
                  <ReactMarkdown>
                    {message.content}
                  </ReactMarkdown>
                </div>

                {message.sources && message.sources.length > 0 && (
                  <div className="sources">
                    <strong>Sources:</strong>

                    {[
                      ...new Set(
                        message.sources.map(
                          (source) => source.page_number
                        )
                      ),
                    ].map((pageNumber) => (
                      <span key={pageNumber}>
                        Page {pageNumber}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="message assistant">
                <strong>QueryAI</strong>
                <p>Thinking...</p>
              </div>
            )}
          </div>

          <div className="input-area">
            <input
              type="text"
              placeholder="Ask something about your document..."
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  askQuestion();
                }
              }}
              disabled={loading}
            />

            <button
              onClick={askQuestion}
              disabled={loading}
            >
              {loading ? "Thinking..." : "Ask"}
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;