# 🤖 AI Meeting Notes Analyzer

An AI-powered meeting analysis application built using **Python, Gemini, LangChain, LangGraph, and Streamlit**.

The application takes a meeting transcript and automatically converts it into structured meeting insights including:

- 📝 Meeting Summary
- 🎯 Key Discussion Topics
- ✅ Action Items
- 👤 Task Owners
- 🔥 Priority Levels
- 🧠 LLM-based Evaluation
- 📊 Automated Evaluation Metrics

The project demonstrates how to build a **production-oriented GenAI application using a multi-agent LangGraph workflow with automated LLM evaluation**.

---

## 🚀 Project Objective

In real-world organizations, meetings generate a large amount of information, but important decisions, action items, and ownership can easily be missed.

This project addresses that problem by automatically analyzing meeting transcripts and generating structured meeting notes.

### Input

A meeting transcript such as:

```text
Product Manager: We have received several complaints about
the mobile app crashing during login.

Mobile Developer: I will review the Android login module.

QA Tester: I will prepare a detailed bug report.

Backend Developer: I will verify the authentication API.
```

### Output

```text
Meeting Summary
---------------
The team discussed a critical Android login crash affecting
multiple customers and investigated potential authentication
API and mobile application issues.

Key Topics
----------
1. Android login crash
2. Authentication API
3. Backend deployment
4. Root cause investigation

Action Items
------------
1. Review Android login module
   Owner: Mobile Developer
   Priority: High

2. Prepare detailed bug report
   Owner: QA Tester
   Priority: High

3. Verify authentication API
   Owner: Backend Developer
   Priority: High
```

---

# 🏗️ Architecture

```text
                        User
                          │
                          ▼
                  ┌───────────────┐
                  │   Streamlit   │
                  │      UI       │
                  └───────┬───────┘
                          │
                          ▼
                  Meeting Transcript
                          │
                          ▼
                  ┌───────────────┐
                  │   LangGraph   │
                  │   Workflow    │
                  └───────┬───────┘
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
    Topic Agent     Summary Agent     Action Agent
                                             │
                                             ▼
                                      Priority Agent
                                             │
                                             ▼
                                    Final Report Agent
                                             │
                                             ▼
                                  Structured Meeting Notes
                                             │
                                             ▼
                                   LLM-as-a-Judge
                                             │
                                             ▼
                                      Quality Scores
```

---

# 🧠 LangGraph Workflow

The application uses a multi-step LangGraph workflow.

```text
START
  │
  ▼
Input Transcript
  │
  ▼
Topic Extraction Agent
  │
  ▼
Meeting Summary Agent
  │
  ▼
Action Item Extraction Agent
  │
  ▼
Action Items Found?
  │
  ├────────────── No ──────────────► Final Output
  │
  ▼ Yes
Priority Classification Agent
  │
  ▼
Final Output
  │
  ▼
END
```

## Agents

### 1. Topic Extraction Agent

Identifies the main discussion topics from the transcript.

### 2. Meeting Summary Agent

Creates a concise 3–5 sentence summary of the meeting.

### 3. Action Item Agent

Extracts:

- Task description
- Task owner

If an owner is not mentioned:

```text
Owner: Not specified
```

### 4. Priority Agent

Classifies task priority based on urgency and deadlines.

Supported levels:

```text
High
Medium
Low
```

The agent considers phrases such as:

- urgently
- immediately
- today
- by tomorrow
- this week
- within the next hour
- critical

### 5. Conditional Routing

If no action items are detected, the priority agent is skipped.

```text
Action Items
     │
     ├── None ──► Skip Priority Agent
     │
     └── Found ─► Priority Agent
```

---

# 🖥️ Streamlit Application

The project provides a Streamlit interface where users can:

- Paste meeting transcripts
- Upload transcript files
- Analyze meetings
- View summaries
- View key topics
- View action items
- View task owners
- View priorities
- Evaluate generated output
- Download reports

---

# 📊 LLM Evaluation

The project includes an **LLM-as-a-Judge evaluation framework**.

Instead of only checking whether the generated text exactly matches expected text, the application evaluates the semantic quality of the generated meeting report.

The evaluation process:

```text
Original Transcript
        │
        ├───────────────┐
        │               │
        ▼               ▼
Reference Output    AI Generated Output
        │               │
        └───────┬───────┘
                ▼
          Gemini Judge
                │
                ▼
        Structured Scores
```

## Evaluation Criteria

### Summary Quality

Evaluates:

- Accuracy
- Relevance
- Completeness
- Conciseness

Score:

```text
1 – 5
```

### Action Item Quality

Evaluates whether important tasks were correctly identified.

### Owner Accuracy

Checks whether the extracted owner matches the person responsible in the transcript.

### Priority Accuracy

Checks whether task priority is supported by urgency and deadlines in the transcript.

### Overall Quality

Evaluates whether the generated report is useful for a real project manager.

---

# 📈 Deterministic Evaluation Metrics

The project also includes deterministic evaluation metrics.

Current metrics include:

```text
Topic Recall
Action Item Recall
Owner Accuracy
Priority Accuracy
Semantic Similarity
```

Example:

```text
Topic Recall:        91%
Action Recall:       87%
Owner Accuracy:      94%
Priority Accuracy:   90%
LLM Overall Score:   4.4 / 5
```

The evaluation framework can be extended with additional metrics and test cases.

---

# 🧪 Testing

The project includes unit tests for the workflow and evaluation components.

Run:

```bash
pytest
```

The application also tests different meeting scenarios, including:

### Normal meeting

Meeting contains action items with clearly identified owners.

### No-action meeting

The workflow should skip priority classification.

### Missing-owner meeting

Tasks without explicitly mentioned owners should be classified as:

```text
Owner: Not specified
```

### Urgent meeting

The priority agent should identify urgent tasks as high priority.

---

# 📂 Project Structure

```text
ai-meeting-notes-analyzer/
│
├── app/
│   ├── agents/
│   │   ├── topic_agent.py
│   │   ├── summary_agent.py
│   │   ├── action_agent.py
│   │   └── priority_agent.py
│   │
│   ├── graph/
│   │   └── workflow.py
│   │
│   ├── prompts/
│   │
│   ├── models.py
│   ├── state.py
│   ├── llm.py
│   └── config.py
│
├── evaluation/
│   ├── datasets/
│   │   └── meeting_cases.py
│   │
│   ├── evaluators/
│   │   ├── topic_evaluator.py
│   │   ├── action_evaluator.py
│   │   ├── priority_evaluator.py
│   │   ├── semantic_evaluator.py
│   │   └── llm_judge.py
│   │
│   └── run_evaluation.py
│
├── tests/
│   ├── test_agents.py
│   ├── test_workflow.py
│   └── test_evaluation.py
│
├── streamlit_app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Gemini | Large Language Model |
| LangChain | LLM integration |
| LangGraph | Agent/workflow orchestration |
| Pydantic | Structured output validation |
| Streamlit | User interface |
| NumPy | Evaluation calculations |
| Pytest | Unit testing |
| Git | Version control |
| GitHub | Source code management |

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone <your-github-repository-url>
```

Move into the project:

```bash
cd ai-meeting-notes-analyzer
```

## 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Configuration

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

Never commit `.env` to GitHub.

Use `.env.example` as a template:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

---

# ▶️ Run the Application

Start Streamlit:

```bash
streamlit run streamlit_app.py
```

The application will open in your browser.

---

# 🧪 Run Evaluation

Run the evaluation framework:

```bash
python -m evaluation.run_evaluation
```

Run the LLM-as-a-Judge:

```bash
python -m evaluation.run_llm_judge
```

---

# 📋 Example Evaluation

Example evaluation output:

```text
==============================
LLM AS JUDGE
==============================

Summary: 5/5
Accurate and concise summary.

Action Items: 4/5
Most important tasks identified.

Owners: 5/5
Owners correctly extracted.

Priority: 4/5
Urgent tasks correctly prioritized.

Overall: 4.5/5
Highly useful meeting report.
```

---

# 🔐 Security Considerations

API keys and secrets should never be committed to GitHub.

The project uses environment variables:

```text
.env
```

and excludes them through:

```text
.gitignore
```

For production deployments, secrets should be managed through a secure secret-management solution.

---

# 🚀 Future Enhancements

- [ ] PDF transcript upload
- [ ] DOCX transcript upload
- [ ] Audio-to-text meeting transcription
- [ ] Speaker identification
- [ ] Meeting history
- [ ] PostgreSQL persistence
- [ ] User authentication
- [ ] Multi-user support
- [ ] Email action-item reminders
- [ ] Calendar integration
- [ ] Slack/Teams integration
- [ ] FastAPI backend
- [ ] Docker deployment
- [ ] CI/CD pipeline
- [ ] LangSmith tracing
- [ ] Production evaluation dashboard
- [ ] Human feedback loop
- [ ] RAG-based meeting history
- [ ] Multi-language meeting support

---

# 🎯 Key GenAI Concepts Demonstrated

### LLM Application Development

- Prompt engineering
- Gemini integration
- Structured outputs
- Pydantic validation

### Agentic AI

- LangGraph
- Multi-agent workflow
- State management
- Conditional routing
- Agent specialization

### RAG / Embeddings Concepts

- Embedding-based semantic similarity
- Evaluation using embeddings

### LLM Evaluation

- Reference-based evaluation
- Deterministic metrics
- Semantic evaluation
- LLM-as-a-Judge
- Evaluation datasets
- Quality scoring

### Software Engineering

- Modular architecture
- Unit testing
- Error handling
- Environment configuration
- Git/GitHub
- Streamlit application development

---

# 💡 What I Learned

This project demonstrates an important principle in GenAI development:

> Building an LLM application is not only about generating good responses. It is also about measuring, testing, evaluating, and continuously improving the quality of those responses.

The project combines:

```text
LLM
 +
LangGraph
 +
Structured Outputs
 +
Testing
 +
Evaluation
 +
LLM-as-a-Judge
 +
Streamlit
```

to create an end-to-end GenAI application.

---

# 👩‍💻 Author

**Priyanka Chila**

AI/GenAI Engineer | Python | LangGraph | LLM | RAG | Agentic AI
