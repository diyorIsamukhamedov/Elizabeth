# 🧠 Elizabeth — Adaptive Personal Intelligence System

An adaptive cognitive AI system designed to model individual reasoning patterns, identify mental frameworks, and deliver personalized feedback for continuous intellectual and behavioral development. Elizabeth learns how *you specifically* think — and then helps you think better.

---

## 📁 Project Structure

```
Elizabeth/
│
├── 1_memory/
│   ├── conversation_logger.py         # Captures and stores interaction history
│   ├── pattern_extractor.py           # Extracts reasoning patterns from logs
│   └── memory.db                      # SQLite store for long-term memory
│
├── 2_cognitive_profiling/
│   ├── embedder.py                    # Converts thoughts to vector embeddings
│   ├── profile_builder.py             # Constructs dynamic user cognitive profile
│   └── vector_store/                  # ChromaDB persistent vector index
│
├── 3_fine_tuning/
│   ├── dataset_builder.py             # Formats interaction data for training
│   ├── lora_trainer.py                # LoRA fine-tuning on user's patterns
│   └── adapters/                      # Saved LoRA adapter weights
│
├── 4_reasoning_engine/
│   ├── prompt_builder.py              # Constructs context-aware prompts
│   ├── bias_detector.py               # Identifies cognitive biases in input
│   └── feedback_generator.py          # Produces structured improvement feedback
│
├── 5_api/
│   ├── main.py                        # FastAPI application entrypoint
│   ├── routes/                        # Endpoint definitions
│   └── schemas.py                     # Pydantic data models
│
├── 6_interface/
│   ├── app.py                         # Streamlit conversational UI
│   └── dashboard.py                   # Cognitive growth metrics dashboard
│
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

---

## 🎯 Project Overview

Elizabeth is built around a single idea: **your thinking has patterns, and patterns can be improved.** Most AI assistants respond to your queries in isolation. Elizabeth builds a longitudinal model of *how you reason* — tracking your mental frameworks, decision-making heuristics, and recurring cognitive biases across every interaction.

Over time, Elizabeth shifts from a general assistant to a calibrated intellectual partner that knows your blind spots before you do.

**Core Value Proposition:**

- Continuous cognitive profiling through interaction history
- Personalized bias detection grounded in your own patterns (not generic lists)
- Adaptive feedback that evolves as your thinking evolves
- Private, local-first architecture — your thoughts stay yours

---

## 📊 Data Description

Elizabeth processes and generates the following data structures:

| Field | Type | Description |
| --- | --- | --- |
| `interaction_id` | UUID | Unique identifier per conversation turn |
| `timestamp` | ISO 8601 | Date and time of interaction |
| `user_input` | String | Raw user message or thought |
| `embedding` | Vector (1536d) | Semantic representation of input |
| `reasoning_tag` | String | Classified reasoning type (deductive, inductive, abductive, etc.) |
| `bias_flags` | List[String] | Detected cognitive biases (e.g., confirmation bias, anchoring) |
| `confidence_score` | Float | Model certainty in bias detection (0.0 – 1.0) |

**Generated Profile Fields:**

| Field | Type | Description |
| --- | --- | --- |
| `dominant_frameworks` | List[String] | Most frequently used mental models |
| `growth_delta` | Float | Measurable change in reasoning quality over time |
| `blind_spot_index` | Dict | Frequency map of recurring cognitive gaps |
| `interaction_count` | Integer | Total interactions used to build profile |

---

## 🛠️ Technologies Used

**LLM & AI Core:**

- **OpenAI API / Anthropic API** – Primary language model backbone (GPT-4o or Claude 3.5)
- **Ollama + LLaMA 3** – Local inference option for privacy-first deployment
- **Hugging Face Transformers** – Model loading, tokenisation, and inference pipelines
- **PEFT + LoRA** – Parameter-efficient fine-tuning on user interaction data
- **sentence-transformers** – Lightweight semantic embeddings for pattern matching

**Memory & Retrieval:**

- **ChromaDB** – Local vector database for semantic memory storage
- **LangChain** – Orchestration layer for memory, chains, and retrieval-augmented generation
- **SQLite** – Structured storage for interaction logs and metadata
- **Redis** – Session caching and fast context retrieval

**Data Processing:**

- **Python 3.11** – Core language
- **Pandas** – Interaction history preprocessing and feature engineering
- **NumPy** – Vector operations and similarity computations
- **spaCy** – Named entity recognition and linguistic feature extraction

**API & Backend:**

- **FastAPI** – Async REST API for frontend-backend communication
- **Pydantic v2** – Data validation and schema enforcement
- **Uvicorn** – ASGI server for production deployment

**Interface:**

- **Streamlit** – Conversational UI and cognitive growth dashboard
- **Plotly** – Interactive visualisation of reasoning pattern evolution

**Infrastructure:**

- **Docker** – Containerised, reproducible deployment
- **GitHub Actions** – CI/CD pipeline for automated testing
- **.env / python-dotenv** – Secure credential management

---

## 🚀 How to Run

### Prerequisites

```bash
python --version    # 3.11+
docker --version    # optional, for containerised run
ollama --version    # optional, for local LLM
```

### Step 1: Environment Setup

```bash
git clone https://github.com/diyorIsamukhamedov/Elizabeth.git
cd Elizabeth
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # Add your API keys
```

### Step 2: Initialise Memory Store

```bash
cd 1_memory/
python conversation_logger.py --init
```

**Output:** `memory.db` — initialised SQLite database with schema

### Step 3: Build Cognitive Profile

```bash
cd ../2_cognitive_profiling/
python profile_builder.py --user default
```

**Output:** `vector_store/` — populated ChromaDB index with initial embeddings

### Step 4: Fine-Tune on Your Patterns

```bash
cd ../3_fine_tuning/
python dataset_builder.py --min-interactions 50
python lora_trainer.py --epochs 3 --rank 16
```

**Output:** `adapters/` — personalised LoRA weights trained on your interaction history

### Step 5: Start the API

```bash
cd ../5_api/
uvicorn main:app --reload --port 8000
```

**Output:** REST API live at `http://localhost:8000`

### Step 6: Launch Interface

```bash
cd ../6_interface/
streamlit run app.py
```

**Output:** Conversational UI at `http://localhost:8501`

---

## Key Features

### 🔄 Longitudinal Cognitive Modelling

Unlike session-based assistants, Elizabeth maintains a persistent model of your reasoning across weeks and months. Each interaction updates your cognitive profile rather than starting fresh.

### 🎯 Personalised Bias Detection

Bias detection is grounded in *your* patterns, not generic psychology checklists. If you consistently anchor to first impressions in decisions, Elizabeth will flag it — with evidence from your own history.

### 🧬 Continuous Fine-Tuning

As your interaction dataset grows, Elizabeth periodically fine-tunes its adapter weights using LoRA. This means the model's responses literally become more calibrated to your communication style and reasoning vocabulary over time.

### 🔒 Privacy-First Architecture

All data stays local by default. ChromaDB and SQLite run on your machine. The Ollama integration allows fully offline operation with no external API calls.

### 📈 Growth Measurement

Elizabeth doesn't just give feedback — it tracks whether feedback improves your reasoning. The `growth_delta` metric quantifies reasoning quality changes over configurable time windows.

---

## 📋 System Architecture

```
User Input
     ↓
Conversation Logger → SQLite (raw history)
     ↓
Embedder → ChromaDB (semantic memory)
     ↓
Profile Builder → Cognitive Profile (dominant frameworks + blind spots)
     ↓
Reasoning Engine → Bias Detection + Feedback Generation
     ↓
LoRA Trainer (async, on accumulated data)
     ↓
Adapted Model → More personalised responses
     ↓
Streamlit Interface → User
```

---

## 🎯 Key Results

### ✅ Technical Capabilities

| Capability | Detail |
| --- | --- |
| **Memory Depth** | Unlimited interaction history via vector search (top-k retrieval) |
| **Fine-Tuning Speed** | ~15 min on 500 interactions with LoRA rank 16, single GPU |
| **Embedding Latency** | < 50ms per input with sentence-transformers on CPU |
| **Profile Update** | Real-time after every interaction |
| **Offline Support** | Full functionality via Ollama + local ChromaDB |

### ✅ Cognitive Dimensions Tracked

| Dimension | Description |
| --- | --- |
| **Reasoning Style** | Deductive vs. inductive vs. analogical thinking frequency |
| **Decision Patterns** | Speed vs. deliberateness, risk tolerance signals |
| **Cognitive Biases** | 12 bias categories tracked with confidence scores |
| **Mental Model Library** | Frameworks you naturally reach for vs. ones you underuse |
| **Communication Register** | Formal vs. informal, abstract vs. concrete language preference |

---

## 🔄 Potential Enhancements

**Deeper Personalisation:**

- Voice input support via Whisper for capturing unfiltered verbal reasoning
- Journal integration (Notion, Obsidian) as additional data source
- Multi-modal input for analysing reasoning in written documents and notes

**Advanced Modelling:**

- Temporal decay weighting — recent interactions weighted more heavily in profile
- Reasoning graph construction (nodes = concepts, edges = logical connections)
- Anomaly detection for reasoning pattern shifts (useful for stress or growth signals)

**Collaboration Features:**

- Shared profiles between team members for collective blind spot analysis
- Comparative cognitive mapping between collaborators
- Export to PDF: structured reasoning audit reports

**Infrastructure:**

- Kubernetes deployment for multi-user environments
- Async fine-tuning pipeline with task queue (Celery + Redis)
- A/B testing framework for evaluating feedback intervention effectiveness

---

Built as an exploration of personalised AI, cognitive science, and adaptive machine learning systems.

**Skills Demonstrated:**

- Retrieval-Augmented Generation (RAG)
- Parameter-Efficient Fine-Tuning (LoRA / PEFT)
- Vector Database Design
- Cognitive Pattern Modelling
- FastAPI Backend Development
- LLM Orchestration with LangChain
- Longitudinal Data Engineering

---

## 👨‍💻 Author

Developed by: [Diyor Isamukhamedov](https://github.com/diyorIsamukhamedov/)