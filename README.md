
# 🧠📅 Meeting Room Booking Assistant

A simple and intelligent AI agent for **finding and reserving meeting rooms** in an office setting. Built with **LangGraph**, **Streamlit**, **SQLite**, and powered by **LLama 3.1-8B-Instant** through the **Groq API**, this assistant handles **availability checks**, **conflict resolution**, and **room feature matching**—all through natural language.

## 🔍 Project Description

This project demonstrates how to build an intelligent meeting room booking system that leverages an LLM-powered agent to handle scheduling tasks interactively. The assistant understands room availability, features, and can automatically resolve scheduling conflicts through natural language reasoning and real-time database queries.

The solution uses:

* 🧩 **LangGraph** for defining stateful agent logic and transitions
* 🧠 **Groq API** to access **LLama 3.1-8B-Instant** for natural language understanding and decision-making
* 🗃️ **SQLite** as the booking database backend
* 🖼️ **Streamlit** for an intuitive user interface

## 🛠️ Features

* 💡 Natural language room booking
* 📆 Real-time room availability checking
* ❌ Conflict resolution based on existing reservations
* 🏷️ Room filtering by features (e.g., capacity, equipment)
* ✅ Auto-booking when a suitable room is found
* 🧠 Powered by LLM (LLama 3.1-8B-Instant via Groq API)

## 🚀 Architecture Overview

```
User --> Streamlit UI --> LangGraph Agent Node --> LLM (via Groq API)
                                      |
                                      +--> SQLite Room Booking DB
```

### 🔄 Agent Workflow & State Transitions (via LangGraph)

1. **User Request** → Parses intent and desired time/room features
2. **Availability Check** → Queries the SQLite DB
3. **Conflict Detection** → Uses LLM to evaluate overlaps
4. **Booking Decision** → If available, proceed to book; else, suggest alternatives
5. **Booking Confirmation** → Finalize the reservation in the DB

## 🧠 Agent Responsibilities

| Agent Node        | Responsibility                          |
| ----------------- | --------------------------------------- |
| Intent Parser     | Understand user query and extract needs |
| Room Matcher      | Query DB for matching rooms             |
| Conflict Resolver | Detect and handle scheduling conflicts  |
| Booking Executor  | Perform DB write after confirmation     |

## 🔌 External System Integrations

* **SQLite** – Room booking database
* **Groq API** – Access to LLama-3.1-8B-Instant LLM
* *(Optional: Integrate calendar APIs like Google Calendar for extended functionality)*

## 🖥️ Technologies Used

* `LangGraph` – for agent and workflow definition
* `Streamlit` – interactive UI
* `SQLite` – simple and lightweight room booking database
* `Groq API` – blazing-fast inference for LLM queries

## 🧪 Error Handling

* Missing input validation (e.g., no date provided)
* Handles large overlapping meeting conflicts
* Suggests alternate rooms/times if the preferred option is unavailable
* Graceful fallback if LLM response is incomplete or ambiguous

## 📋 Justification for LangGraph

LangGraph was chosen for its:

* ✅ **Built-in state management**
* ✅ **Graph-based workflow control**
* ✅ **Fine-grained decision logic** through modular agents
* ✅ Seamless integration with external APIs and databases

This framework allows us to chain LLM outputs to real actions (query, decision, DB insert) in a maintainable, explainable graph structure.

