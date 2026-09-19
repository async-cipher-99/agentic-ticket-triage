# Agentic Ticket Triage

<p align="center">
  <strong>Configurable, Multi-Tenant LLM Agent for Intelligent Customer-Support Ticket Triage</strong>
</p>

<p align="center">
  An end-to-end machine-learning system for classifying support tickets, selecting tools, applying tenant-specific policies, and producing structured triage decisions.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Qwen](https://img.shields.io/badge/Qwen-2.5--1.5B-7C3AED?style=for-the-badge)
![PyTorch](https://img.shields.io/badge/PyTorch-ML%20Training-EE4C2C?style=for-the-badge\&logo=pytorch\&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Transformers-FFD21E?style=for-the-badge\&logo=huggingface\&logoColor=black)
![PEFT](https://img.shields.io/badge/PEFT-LoRA%20%2F%20QLoRA-FF6F00?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge\&logo=docker\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)
![YAML](https://img.shields.io/badge/YAML-Configuration-CB171E?style=for-the-badge\&logo=yaml\&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI-2088FF?style=for-the-badge\&logo=github-actions\&logoColor=white)
![Weights & Biases](https://img.shields.io/badge/Weights%20%26%20Biases-Experiment%20Tracking-FFBE00?style=for-the-badge\&logo=weightsandbiases\&logoColor=black)

</p>

---

## Table of Contents

* [Overview](#overview)
* [Why This Project](#why-this-project)
* [Key Features](#key-features)
* [System Architecture](#system-architecture)
* [End-to-End Workflow](#end-to-end-workflow)
* [Agentic Ticket Triage](#agentic-ticket-triage)
* [Multi-Tenant Architecture](#multi-tenant-architecture)
* [Tenant Configuration](#tenant-configuration)
* [Machine Learning Pipeline](#machine-learning-pipeline)
* [Base Model](#base-model)
* [LoRA Fine-Tuning](#lora-fine-tuning)
* [QLoRA and 4-Bit Quantization](#qlora-and-4-bit-quantization)
* [Training Configuration](#training-configuration)
* [Dataset Generation](#dataset-generation)
* [Data Preparation](#data-preparation)
* [Project Structure](#project-structure)
* [Technology Stack](#technology-stack)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Clone the Repository](#clone-the-repository)
* [Create a Virtual Environment](#create-a-virtual-environment)
* [Install Dependencies](#install-dependencies)
* [Dataset Workflow](#dataset-workflow)
* [Training Workflow](#training-workflow)
* [Evaluation](#evaluation)
* [Testing](#testing)
* [Running the API](#running-the-api)
* [Docker](#docker)
* [Configuration](#configuration)
* [Adding a New Tenant](#adding-a-new-tenant)
* [Development Workflow](#development-workflow)
* [Reproducibility](#reproducibility)
* [Troubleshooting](#troubleshooting)
* [Limitations](#limitations)
* [Future Improvements](#future-improvements)
* [Contributing](#contributing)
* [License](#license)
* [Author](#author)

---

# Overview

**Agentic Ticket Triage** is a machine-learning and LLM-based customer-support automation system designed to transform unstructured support tickets into structured, actionable triage decisions.

Instead of treating ticket triage as a simple text-classification problem, the project models the workflow as an **agentic system**.

The system can combine:

* Natural-language understanding
* Ticket classification
* Urgency detection
* Tenant-specific labels
* Tool selection
* Tool execution
* Knowledge-base lookup
* Business-policy handling
* Confidence-based escalation
* Structured outputs
* Configurable multi-tenant behavior

The architecture is designed so that the underlying model can be adapted to different organizations without rewriting the entire application.

Each tenant can define its own:

* Supported languages
* Ticket categories
* Labels
* Urgency levels
* Available tools
* Business rules
* Escalation behavior
* Confidence requirements

This makes the project suitable as a foundation for experimenting with **LLM-powered customer-support agents and enterprise ticket-routing workflows**.

---

# Why This Project?

Traditional ticket-routing systems commonly depend on:

1. Manually written rules
2. Fixed categories
3. Hard-coded business logic
4. A single workflow for every organization

That approach becomes difficult to maintain when different organizations have different support processes.

For example, a manufacturing company may need:

* Warranty classification
* Parts-order lookup
* Manufacturing-specific escalation

while an e-commerce organization may need:

* Order tracking
* Refund lookup
* Shipping classification
* Billing workflows

Agentic Ticket Triage addresses this problem by separating **tenant-specific configuration** from the core processing system.

The result is a system where the same underlying architecture can operate against different business configurations.

---

# Key Features

## 🤖 LLM-Powered Ticket Understanding

The system uses **Qwen/Qwen2.5-1.5B-Instruct** as the base language model.

The model is configured for task-specific fine-tuning rather than relying entirely on generic pretrained behavior.

---

## 🎯 Ticket Classification

Incoming support messages can be mapped into structured ticket labels defined by the active tenant.

This allows organizations to maintain their own support taxonomy.

---

## 🚨 Urgency Detection

The system supports urgency information as part of the triage process.

Urgency can be combined with business rules and confidence thresholds to determine whether a ticket can continue through the automated workflow or should be escalated.

---

## 🧰 Tool-Using Agent

The project is designed around an agentic workflow where the model can select tools relevant to a support request.

Examples include:

* Order-status lookup
* Refund lookup
* Knowledge-base search

The available tools are tenant-specific rather than globally hard-coded.

---

## 🏢 Multi-Tenant Configuration

Different organizations can use different configurations without changing the core application.

Included tenant examples include:

* `acme_corp`
* `globex_manufacturing`

---

## 🌍 Multi-Language Configuration

Tenant configurations can specify supported languages.

This makes it possible to adapt the same architecture to organizations serving customers in different linguistic environments.

---

## ⚠️ Confidence-Based Escalation

The system can use confidence thresholds and tenant-defined policies to determine when an automated decision should be escalated.

This is important in customer-support environments where uncertain automated decisions should not always be treated as final.

---

## 🧪 Automated Testing

The repository includes a dedicated `tests/` directory for validating project behavior.

The project can therefore be tested independently from model-training workflows.

---

## 🐳 Docker Support

The repository includes a Dockerfile for running the serving application inside a container.

The container is configured around Python 3.11 and exposes port `8000`.

---

## 📊 Experiment Tracking

The training configuration supports **Weights & Biases (W&B)** reporting for experiment tracking.

The configured training run name is:

```text
ticket-triage-tool-use
```

---

# System Architecture

At a high level, the system follows this architecture:

```text
                         ┌─────────────────────────┐
                         │    Incoming Support     │
                         │         Ticket          │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │   Tenant Configuration  │
                         │                         │
                         │  • Labels               │
                         │  • Languages            │
                         │  • Tools                │
                         │  • Policies             │
                         │  • Escalation Rules     │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │      LLM / Agent        │
                         │                         │
                         │ Qwen2.5-1.5B-Instruct   │
                         │       + LoRA/QLoRA      │
                         └────────────┬────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
             ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
             │ Classification│  │ Tool Choice │  │   Urgency   │
             │    / Labels   │  │             │  │   Analysis  │
             └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
                    │                │                 │
                    │                ▼                 │
                    │       ┌────────────────┐         │
                    │       │ Tenant Tools   │         │
                    │       │                │         │
                    │       │ • KB Search    │         │
                    │       │ • Order Lookup │         │
                    │       │ • Refund Lookup│         │
                    │       └───────┬────────┘         │
                    │               │                  │
                    └───────────────┼──────────────────┘
                                    ▼
                         ┌─────────────────────────┐
                         │ Business Rules &        │
                         │ Confidence Evaluation   │
                         └────────────┬────────────┘
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                         ▼                         ▼
                 ┌───────────────┐         ┌───────────────┐
                 │ Automated     │         │ Human /        │
                 │ Triage Result │         │ Escalation     │
                 └───────────────┘         └───────────────┘
```

---

# End-to-End Workflow

The complete workflow can be understood as the following sequence:

### 1. Ticket ingestion

A customer-support message enters the system as unstructured text.

Example:

```text
"My order hasn't arrived yet and I need to know where it is."
```

---

### 2. Tenant selection

The system loads the configuration associated with the organization.

The configuration determines the rules under which the ticket should be processed.

---

### 3. Ticket understanding

The LLM analyzes the ticket and extracts the information required for triage.

This can include:

* Ticket category
* Relevant labels
* Urgency
* Tool requirements
* Other structured information required by the workflow

---

### 4. Tool selection

If additional information is required, the agent can select an appropriate configured tool.

For example:

```text
Ticket
  ↓
Order-related request
  ↓
order_status tool
  ↓
Retrieve order information
```

---

### 5. Business-policy evaluation

The result can then be evaluated against tenant-specific policies.

This is important because two organizations can have different rules for handling similar tickets.

---

### 6. Confidence and escalation

If the system is sufficiently confident and the request satisfies the configured policy, it can proceed with automated triage.

If confidence is insufficient or a policy requires human intervention, the ticket can be escalated.

---

### 7. Structured result

The final output is represented as structured triage information suitable for downstream customer-support systems.

---

# Agentic Ticket Triage

The main distinction between a conventional classifier and this project is the **agentic workflow**.

A conventional classifier might simply produce:

```text
category = refund
```

An agentic system can instead reason about the operational workflow:

```text
Incoming ticket
       ↓
Identify request
       ↓
Determine category
       ↓
Determine urgency
       ↓
Determine whether external information is required
       ↓
Select an appropriate tenant tool
       ↓
Apply tenant-specific policy
       ↓
Determine whether escalation is necessary
       ↓
Return structured triage result
```

This architecture makes the project closer to an **LLM-powered support operations system** than a standalone text classifier.

---

# Multi-Tenant Architecture

A major design goal of the project is to avoid hard-coding every organization's support workflow into Python code.

Instead, tenant-specific behavior is represented through YAML configuration.

Conceptually:

```text
                    Core Application
                          │
            ┌─────────────┴─────────────┐
            │                           │
            ▼                           ▼
     Acme Corp Config          Globex Manufacturing
            │                           │
            ▼                           ▼
       Tools + Rules               Tools + Rules
       Labels + Policy             Labels + Policy
       Languages                   Languages
```

This means the application can maintain a shared processing architecture while allowing individual organizations to define their own operational behavior.

---

# Tenant Configuration

Tenant configurations are stored under:

```text
configs/tenants/
```

Current repository examples include:

```text
configs/
└── tenants/
    ├── acme_corp.yaml
    └── globex_manufacturing.yaml
```

---

## Acme Corp

The Acme configuration demonstrates a tenant with:

* English/Spanish language support
* Ticket labels
* Multiple urgency levels
* Tool definitions
* Order-status functionality
* Refund lookup
* Knowledge-base search
* Confidence-based escalation
* Refund-related business policy configuration

This demonstrates how an organization can define support behavior without modifying the core model pipeline.

---

## Globex Manufacturing

The Globex Manufacturing configuration demonstrates how the same architecture can support a different industry.

Its configuration includes:

* English/German/French language support
* Manufacturing-specific labels
* Warranty-related support workflows
* Parts-order handling
* Tenant-specific tools
* Tenant-specific escalation behavior

This is useful for demonstrating that the system is designed around configurable workflows rather than a single fixed support taxonomy.

---

# Machine Learning Pipeline

The machine-learning workflow can be viewed as:

```text
Raw / Generated Ticket Data
            │
            ▼
     Data Preparation
            │
            ▼
    Processed Training Data
            │
            ▼
 Qwen2.5-1.5B-Instruct
            │
            ▼
       LoRA / QLoRA
            │
            ▼
   Fine-Tuning Workflow
            │
            ▼
     Saved Model Output
            │
            ▼
       Evaluation
            │
            ▼
     Serving / Inference
```

---

# Base Model

The configured base model is:

```text
Qwen/Qwen2.5-1.5B-Instruct
```

The model is loaded through the Hugging Face ecosystem and adapted for the ticket-triage/tool-use task.

The configuration uses a maximum sequence length of:

```text
2048 tokens
```

This provides substantially more context than a short classification-only pipeline and is useful for ticket conversations and structured task instructions.

---

# LoRA Fine-Tuning

The project uses **Low-Rank Adaptation (LoRA)** to fine-tune the language model efficiently.

The configured parameters are:

| Parameter      |                                  Value |
| -------------- | -------------------------------------: |
| Rank (`r`)     |                                   `16` |
| Alpha          |                                   `32` |
| Dropout        |                                 `0.05` |
| Bias           |                                 `none` |
| Task type      |                            `CAUSAL_LM` |
| Target modules | `q_proj`, `k_proj`, `v_proj`, `o_proj` |

Rather than updating every parameter of the base model, LoRA introduces trainable low-rank adapters into selected model components.

This reduces the number of parameters that need to be trained and makes task-specific adaptation more practical.

---

# QLoRA and 4-Bit Quantization

The training configuration also enables QLoRA-style 4-bit loading.

Configured options include:

```yaml
load_in_4bit: true
bnb_4bit_quant_type: "nf4"
bnb_4bit_compute_dtype: "bfloat16"
bnb_4bit_use_double_quant: true
```

### NF4

The project uses **NormalFloat 4-bit (NF4)** quantization for loading the base model.

### BF16 computation

The configured computation datatype is:

```text
bfloat16
```

### Double quantization

Double quantization is enabled to further reduce memory overhead.

Together, these techniques make it possible to experiment with fine-tuning a relatively capable language model with substantially lower memory requirements than full-precision full-parameter training.

---

# Training Configuration

The main training configuration is located at:

```text
configs/train_config.yaml
```

Current settings include:

| Setting                  | Value                        |
| ------------------------ | ---------------------------- |
| Base model               | `Qwen/Qwen2.5-1.5B-Instruct` |
| Maximum sequence length  | `2048`                       |
| Processed data directory | `data/processed/acme_corp`   |
| LoRA rank                | `16`                         |
| LoRA alpha               | `32`                         |
| LoRA dropout             | `0.05`                       |
| Quantization             | 4-bit                        |
| Quantization type        | NF4                          |
| Compute dtype            | BF16                         |
| Epochs                   | `3`                          |
| Per-device batch size    | `2`                          |
| Gradient accumulation    | `8`                          |
| Learning rate            | `2e-4`                       |
| Warmup ratio             | `0.03`                       |
| Logging interval         | `10` steps                   |
| Save strategy            | Epoch                        |
| Evaluation strategy      | Epoch                        |
| Output directory         | `outputs/tool_use_agent`     |
| Experiment tracker       | Weights & Biases             |
| Run name                 | `ticket-triage-tool-use`     |

The configuration is intentionally separated from the training implementation so that training behavior can be changed without rewriting the training code.

---

# Dataset Generation

The repository includes:

```text
generate_large_dataset.py
```

This script is dedicated to generating a larger synthetic dataset for the project.

The script is substantial enough to form its own data-generation pipeline and is designed around support-ticket examples and the structured information required by the agentic workflow.

The dataset-generation stage is important because machine-learning experiments require consistent training examples covering the supported ticket categories, urgency levels, tools, and workflows.

---

# Data Preparation

The project also contains preprocessing logic that converts source JSONL records into training-ready rows.

A typical source record contains information such as:

```json
{
  "text": "Customer support ticket text",
  "gold_labels": ["some_label"],
  "gold_urgency": "medium"
}
```

The preparation process transforms the source into a simplified training representation containing:

```json
{
  "text": "Customer support ticket text",
  "labels": "some_label",
  "urgency": "medium"
}
```

The preparation workflow:

1. Reads JSONL records.
2. Skips empty lines.
3. Parses each JSON object.
4. Extracts ticket text.
5. Converts the label list into a string representation.
6. Preserves urgency.
7. Creates missing output directories.
8. Writes processed records as JSONL.

This provides a clean boundary between raw/generated data and the training pipeline.

---

# Project Structure

The repository is organized around configuration, data, source code, tests, and deployment.

```text
agentic-ticket-triage/
│
├── .github/
│   └── workflows/
│       └── ...
│
├── configs/
│   ├── tenants/
│   │   ├── acme_corp.yaml
│   │   └── globex_manufacturing.yaml
│   │
│   └── train_config.yaml
│
├── data/
│   ├── raw/
│   └── processed/
│
├── github/
│   └── ...
│
├── src/
│   ├── ...
│   └── serving/
│       └── app.py
│
├── tests/
│   └── ...
│
├── Dockerfile
├── generate_large_dataset.py
├── requirements.txt
└── README.md
```

### `configs/`

Contains model-training configuration and tenant-specific configuration.

### `configs/tenants/`

Contains organization-specific support workflows.

### `data/`

Contains raw and processed datasets used throughout the ML pipeline.

### `src/`

Contains the main application and machine-learning implementation.

### `src/serving/`

Contains the application serving layer.

### `tests/`

Contains automated tests for validating project behavior.

### `generate_large_dataset.py`

Generates the larger synthetic dataset used for experimentation.

### `Dockerfile`

Defines the containerized serving environment.

### `requirements.txt`

Defines the Python dependencies required by the project.

---

# Technology Stack

## Core Language

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square\&logo=python\&logoColor=white)

Python is used throughout the machine-learning pipeline, data processing, configuration handling, and serving layer.

---

## Language Model

![Qwen](https://img.shields.io/badge/Qwen-2.5--1.5B-7C3AED?style=flat-square)

The project uses:

```text
Qwen/Qwen2.5-1.5B-Instruct
```

as its configured base instruction-following model.

---

## Deep Learning

![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square\&logo=pytorch\&logoColor=white)

PyTorch provides the underlying deep-learning framework used by the model training ecosystem.

---

## Transformers

![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Transformers-FFD21E?style=flat-square\&logo=huggingface\&logoColor=black)

Hugging Face tooling is used for working with the language model and transformer training ecosystem.

---

## Parameter-Efficient Fine-Tuning

![PEFT](https://img.shields.io/badge/PEFT-LoRA%20%2F%20QLoRA-FF6F00?style=flat-square)

PEFT techniques are used to adapt the base language model without requiring full-parameter fine-tuning.

---

## API Serving

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square\&logo=fastapi\&logoColor=white)

The serving layer uses FastAPI.

The Docker configuration starts the application with:

```bash
uvicorn src.serving.app:app --host 0.0.0.0 --port 8000
```

---

## Containerization

![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square\&logo=docker\&logoColor=white)

Docker provides a reproducible serving environment.

The current Dockerfile uses:

```text
python:3.11-slim
```

and exposes port:

```text
8000
```

---

## Configuration

![YAML](https://img.shields.io/badge/YAML-CB171E?style=flat-square\&logo=yaml\&logoColor=white)

YAML is used for:

* Training configuration
* Tenant configuration
* Model configuration
* Tool configuration
* Business-policy configuration

---

## Experiment Tracking

![Weights & Biases](https://img.shields.io/badge/W%26B-FFBE00?style=flat-square\&logo=weightsandbiases\&logoColor=black)

Training is configured to report experiments to Weights & Biases.

---

# Prerequisites

Before running the project locally, install:

* Python 3.11+
* Git
* pip
* A compatible environment for the selected ML dependencies
* Docker, if you want to use the containerized serving workflow

For GPU-based model training, ensure that your hardware and installed PyTorch environment support the selected quantization and BF16 configuration.

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/Aardess/agentic-ticket-triage.git
cd agentic-ticket-triage
```

---

# Create a Virtual Environment

## Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

## Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Verify the environment:

```bash
python --version
```

---

# Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Then install the project requirements:

```bash
pip install -r requirements.txt
```

If you are setting up the serving environment only, the Dockerfile also installs the serving-related packages required by the API application.

---

# Dataset Workflow

The project separates dataset generation and processing from model training.

A typical workflow is:

```text
Generate Dataset
      ↓
Raw Dataset
      ↓
Prepare / Process Data
      ↓
Processed Dataset
      ↓
Training
      ↓
Evaluation
```

---

# Generate the Dataset

The repository includes:

```text
generate_large_dataset.py
```

Run it from the repository root:

```bash
python generate_large_dataset.py
```

After generation, inspect the resulting files under the appropriate `data/` directory.

If you modify the generator or its output location, update the downstream configuration accordingly.

---

# Training Data Preparation

The preprocessing stage converts the raw JSONL records into the format expected by the training pipeline.

The general pattern is:

```text
data/raw/
     │
     ▼
preprocessing
     │
     ▼
data/processed/
```

The current training configuration points to:

```text
data/processed/acme_corp
```

Make sure the processed dataset exists at the location expected by the training configuration before starting fine-tuning.

---

# Training Workflow

The training configuration is stored at:

```text
configs/train_config.yaml
```

Before training, verify:

```yaml
model:
  base_model: "Qwen/Qwen2.5-1.5B-Instruct"
```

and:

```yaml
training:
  output_dir: "outputs/tool_use_agent"
```

The configured training process uses:

* Qwen 2.5 1.5B Instruct
* LoRA adapters
* 4-bit QLoRA loading
* NF4 quantization
* BF16 computation
* Gradient accumulation
* Epoch-level evaluation
* W&B experiment reporting

The repository's training implementation should be invoked using the training entry point provided under `src/`.

---

# Evaluation

Evaluation should be performed against data that was not used for parameter updates.

A recommended workflow is:

```text
Training Dataset
       │
       ▼
Fine-Tuning
       │
       ▼
Saved Adapter / Model
       │
       ▼
Evaluation Dataset
       │
       ▼
Metrics + Error Analysis
```

Evaluation should consider more than whether the model generates plausible text.

For a ticket-triage system, useful evaluation dimensions include:

* Label correctness
* Urgency correctness
* Tool-selection correctness
* Structured-output validity
* Escalation behavior
* Tenant-policy compliance
* Failure cases
* Unsupported requests

When adding new evaluation metrics, keep the evaluation dataset isolated from training data to avoid misleading results.

---

# Testing

The repository includes a dedicated:

```text
tests/
```

directory.

Run the test suite from the repository root:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

To stop after the first failure:

```bash
pytest -x
```

To run a specific test file:

```bash
pytest tests/<test_file>.py -v
```

To run a specific test:

```bash
pytest tests/<test_file>.py::test_name -v
```

## Recommended Verification Sequence

After cloning the repository, a practical verification workflow is:

```bash
python --version
pip install -r requirements.txt
pytest -v
```

If the tests pass, continue with the data-generation and model workflow.

---

# Testing the Serving Layer

The API can be tested after starting the application.

Run:

```bash
uvicorn src.serving.app:app --reload --host 0.0.0.0 --port 8000
```

The application should then listen on:

```text
http://localhost:8000
```

FastAPI also provides interactive API documentation when enabled by the application:

```text
http://localhost:8000/docs
```

and OpenAPI documentation can be available at:

```text
http://localhost:8000/openapi.json
```

The exact available endpoints should be verified from the current `src.serving.app` implementation.

---

# Running the API

Start the development server with:

```bash
uvicorn src.serving.app:app --reload --host 0.0.0.0 --port 8000
```

Or use:

```bash
python -m uvicorn src.serving.app:app --reload --host 0.0.0.0 --port 8000
```

The production-style command used by the Docker image is:

```bash
uvicorn src.serving.app:app --host 0.0.0.0 --port 8000
```

---

# Docker

The repository includes a Dockerfile based on:

```text
python:3.11-slim
```

The container:

1. Creates `/app`
2. Installs the serving dependencies
3. Copies `src/`
4. Copies `configs/`
5. Copies `data/`
6. Exposes port `8000`
7. Starts the FastAPI application

## Build the Image

From the repository root:

```bash
docker build -t agentic-ticket-triage .
```

## Run the Container

```bash
docker run --rm -p 8000:8000 agentic-ticket-triage
```

The API should then be accessible through:

```text
http://localhost:8000
```

---

# Configuration

The project deliberately separates configuration from application logic.

The main configuration locations are:

```text
configs/
├── train_config.yaml
└── tenants/
    ├── acme_corp.yaml
    └── globex_manufacturing.yaml
```

This separation makes experimentation easier.

For example, training parameters can be changed without modifying the application implementation.

---

# Training Configuration Reference

The following values are currently configured:

```yaml
model:
  base_model: "Qwen/Qwen2.5-1.5B-Instruct"
  max_seq_length: 2048

data:
  processed_dir: "data/processed/acme_corp"

lora:
  r: 16
  lora_alpha: 32
  lora_dropout: 0.05
  target_modules:
    - q_proj
    - k_proj
    - v_proj
    - o_proj
  bias: "none"
  task_type: "CAUSAL_LM"

qlora:
  load_in_4bit: true
  bnb_4bit_quant_type: "nf4"
  bnb_4bit_compute_dtype: "bfloat16"
  bnb_4bit_use_double_quant: true

training:
  output_dir: "outputs/tool_use_agent"
  num_train_epochs: 3
  per_device_train_batch_size: 2
  gradient_accumulation_steps: 8
  learning_rate: 2.0e-4
  warmup_ratio: 0.03
  logging_steps: 10
  save_strategy: "epoch"
  eval_strategy: "epoch"
  report_to:
    - wandb
  run_name: "ticket-triage-tool-use"
```

---

# Adding a New Tenant

One of the major advantages of the architecture is the ability to create another tenant configuration.

Create a new file:

```text
configs/tenants/my_company.yaml
```

The configuration can define organization-specific behavior such as:

```text
Supported languages
        +
Ticket labels
        +
Urgency levels
        +
Available tools
        +
Business policies
        +
Confidence thresholds
        +
Escalation behavior
```

The goal is to keep tenant-specific rules in configuration instead of duplicating application code.

---

# Development Workflow

A recommended development workflow is:

```text
1. Clone repository
        ↓
2. Create virtual environment
        ↓
3. Install dependencies
        ↓
4. Run tests
        ↓
5. Generate / update dataset
        ↓
6. Prepare processed data
        ↓
7. Update configuration
        ↓
8. Train / fine-tune
        ↓
9. Evaluate
        ↓
10. Run serving layer
        ↓
11. Test inference
        ↓
12. Build Docker image
```

This workflow keeps data, training, evaluation, and deployment stages separate.

---

# Reproducibility

The project keeps important experiment parameters inside configuration files rather than scattering them across source code.

For reproducible experiments, record:

* Base model
* Dataset version
* Tenant configuration
* LoRA configuration
* Quantization configuration
* Learning rate
* Batch size
* Gradient accumulation
* Number of epochs
* Evaluation dataset
* Output model/adapters
* W&B run

The training configuration provides a central place to track the most important model-training parameters.

---

# Troubleshooting

## `ModuleNotFoundError`

Make sure the virtual environment is active:

```bash
python -m pip install -r requirements.txt
```

Then retry the command.

---

## `pytest` is not recognized

Run:

```bash
python -m pytest
```

instead of:

```bash
pytest
```

---

## Port 8000 is already in use

Use another port:

```bash
uvicorn src.serving.app:app --host 0.0.0.0 --port 8001
```

Then access:

```text
http://localhost:8001
```

---

## Model Download or Hugging Face Errors

The first model-loading operation may require downloading the configured model.

Check:

* Internet connectivity
* Hugging Face access
* Available disk space
* Available RAM/VRAM
* Correct Python environment
* Installed transformer/quantization dependencies

---

## GPU / Quantization Issues

The training configuration uses:

```text
4-bit quantization
NF4
bfloat16
```

If your hardware does not support the selected computation mode, the training environment may require adjustment.

Do not change the quantization settings blindly; make sure the replacement configuration is compatible with your hardware and installed PyTorch stack.

---

## Dataset Path Errors

The training configuration currently expects processed data under:

```text
data/processed/acme_corp
```

If your generated data is located elsewhere, either:

1. Move/process the data into the expected location, or
2. Update `configs/train_config.yaml`.

---

# Limitations

This repository is primarily an engineering and machine-learning project for experimenting with agentic ticket triage.

Important limitations include:

* Synthetic/generated data may not represent the full diversity of real customer-support traffic.
* Model predictions should be evaluated before being used in production.
* Tenant configuration quality directly affects system behavior.
* Tool integrations shown in configuration are part of the agentic design and should be connected to real business systems only with appropriate validation and authorization.
* Automated escalation decisions should be validated against the requirements of the organization using the system.
* Small language models can produce incorrect or incomplete outputs, particularly for ambiguous tickets.
* Fine-tuning does not eliminate the need for inference-time validation.

---

# Future Improvements

Potential extensions include:

* Real customer-support dataset integration
* Larger evaluation suites
* Human-in-the-loop review
* Retrieval-augmented generation
* Persistent conversation context
* More production tool integrations
* Authentication and authorization
* Request tracing
* Structured observability
* Model versioning
* Dataset versioning
* Automated evaluation dashboards
* More extensive multilingual evaluation
* Advanced guardrails for tool execution
* Production-grade deployment
* Kubernetes support
* Distributed inference
* Model benchmarking across multiple LLM families

---

# Security Considerations

When adapting this project for production, treat tools as privileged operations.

A production implementation should consider:

* Authentication
* Authorization
* Tool-level permissions
* Input validation
* Output validation
* Rate limiting
* Secret management
* Audit logging
* Sensitive-data handling
* Tenant isolation
* Safe failure behavior

In particular, an LLM should not be treated as an authorization mechanism.

A model deciding that a tool is appropriate should not automatically grant permission to perform a sensitive business operation.

---

# Contributing

Contributions are welcome.

A typical contribution workflow is:

```bash
git clone https://github.com/Aardess/agentic-ticket-triage.git
cd agentic-ticket-triage
```

Create a feature branch:

```bash
git checkout -b feature/my-improvement
```

Make your changes and run the test suite:

```bash
python -m pytest -v
```

Then commit:

```bash
git add .
git commit -m "Add my improvement"
```

Push the branch:

```bash
git push origin feature/my-improvement
```

Open a pull request describing:

* What changed
* Why it changed
* How it was tested
* Any configuration changes
* Any model/data implications

---

# License

If this repository has not yet been assigned a license, add a `LICENSE` file before publishing it as an open-source project.

For example, a project owner may choose an appropriate license such as MIT, Apache-2.0, or another license based on the intended usage terms.

---

# Author

**Aardess**

GitHub:

[github.com/Aardess](https://github.com/Aardess)

Repository:

[github.com/Aardess/agentic-ticket-triage](https://github.com/Aardess/agentic-ticket-triage)

---

# Project Summary

**Agentic Ticket Triage** combines modern LLM fine-tuning techniques with configurable agent workflows to create a flexible customer-support triage system.

The project demonstrates several important machine-learning engineering concepts in one repository:

* LLM application development
* Qwen-based model integration
* Parameter-efficient fine-tuning
* LoRA
* QLoRA
* 4-bit quantization
* Synthetic dataset generation
* Data preprocessing
* Multi-tenant configuration
* Tool-oriented agent workflows
* Confidence-based escalation
* Experiment tracking
* Automated testing
* FastAPI serving
* Docker containerization

The architecture intentionally separates the **model**, **training configuration**, **tenant configuration**, **data pipeline**, **agent behavior**, and **serving layer**, making the project easier to extend and experiment with.

---

<p align="center">
  <strong>Built with Python, Qwen, PyTorch, LoRA/QLoRA, FastAPI, Docker, and modern ML engineering practices.</strong>
</p>
