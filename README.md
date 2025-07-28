# Talk Sheet With Me

---

# 🧠 Sheet Talk – AI-Powered Excel Assistant

Simplifying spreadsheet workflows using natural language + Cohere API

---

## 🚀 Project Overview

**Sheet Talk** allows users to interact with Google Sheets using plain English commands. It sends these commands to a backend server, which uses an AI agent (powered by Cohere) to generate executable scripts, which are then dynamically run inside the sheet.

The goal: **Reduce Excel’s learning curve for professionals in hospitals and other institutions.**

---

## 🧑‍💻 Team Structure

| Name   | Role                   | Responsibilities                                                                 |
| ------ | ---------------------- | -------------------------------------------------------------------------------- |
| Goodn  | Principal Engineer     | Coordination, final review, user deployment                                      |
| Nathan | Lead Frontend Engineer | Building UI, linking frontend with backend, JavaScript logic in Google Sheets    |
| Navas  | Backend/AI Engineer    | Server setup, AI command interpretation using Cohere, script response generation |

---

## 🛠️ Project Setup

### 1. 📁 Frontend – Google Sheets Script (Nathan)

**Main Script File: `Code.gs`**

```javascript
function onOpen() {
  SpreadsheetApp.getUi().createMenu("SHEET TALK 😊")
    .addItem("Open Assistant", "openSheetTalk")
    .addToUi();
}

function openSheetTalk() {
  const html = HtmlService.createHtmlOutputFromFile("SheetTalk")
    .setWidth(400)
    .setHeight(300);
  SpreadsheetApp.getUi().showModalDialog(html, "SHEET TALK 😊");
}

// Core logic for executing scripts received from the server
function executeDynamicScript(script) {
  try {
    const func = new Function(script);
    const result = func();
    return result || "✅ Script executed successfully.";
  } catch (error) {
    return "❌ Error: " + error.message;
  }
}
```

**Next Steps:**

* Build `SheetTalk.html` to provide input field and send request via `google.script.run`.
* Connect user input to an API endpoint hosted by Navas.

---

### 2. 🌐 Backend – AI Agent Server (Navas)

**Stack Recommendation:**

* Express.js / FastAPI (Python)
* Use Cohere API for NLP-to-JavaScript translation
* Set up a `/generate` endpoint to receive user input and return a valid JS function

**Example Payload:**

```json
POST /generate
{
  "prompt": "Create a new column that sums column A and B"
}
```

**Response:**

```json
{
  "script": "function() { const sheet = SpreadsheetApp.getActiveSheet(); const data = sheet.getDataRange().getValues(); for (let i = 1; i < data.length; i++) { sheet.getRange(i + 1, 4).setValue(data[i][0] + data[i][1]); } }"
}
```

---

### 3. 🧪 Deployment – First Client (Goodn)

* Deploy MVP version to hospital staff
* Provide basic usage guide and onboarding
* Collect real feedback and submit notes to the team
* Document common user prompts to improve agent understanding

---

## 📦 Future Add-ons

* Voice interface via browser microphone
* Error logging and feedback collection
* User-defined macros saved for reuse
* OAuth login and personalization

---

## 📞 API Keys & Credentials (Private)

> Store your Cohere API key and any service tokens in a `.env` file or secret manager. **Never commit to version control.**

---

## 🧠 AI Prompting Guidelines

Use system-level prompts like:

> "You're an assistant for Google Sheets. Convert the user's request into a valid JavaScript function using SpreadsheetApp APIs. Only return the JavaScript code."

---

