# 🐍 Python Mini-Compiler

An interactive web-based **Python Mini-Compiler** built using **Streamlit**. It tokenizes input code using a custom lexer, parses it into an AST (Abstract Syntax Tree), and visualizes it as a graph.

---

## ✨ Features

- **Lexer**: Tokenizes input code with support for numbers, identifiers, operators, keywords, and comments.
- **Parser**: Parses the token stream into an abstract syntax tree (AST).
- **AST Visualization**: Interactive tree using Streamlit AGraph.
- **Code Input Options**: Upload `.py`/`.txt` file or paste code manually.
- **Error Handling**: Catches and displays lexer and parser errors.

---

## 🛠️ Technology Stack

- **Python 3**
- **Streamlit** – Web interface
- **psutil** – (Used only in other system projects; not required here)
- **re** – Regular expressions for lexing
- **streamlit-agraph** – Graph-based AST visualization

---

## 📦 Installation

Install dependencies using:

```bash
pip install streamlit streamlit-agraph
```

---

## 🚀 How to Run

Ensure the following files are in the same folder:

- `app.py` – Streamlit UI
- `lexer.py` – Custom lexer
- `parser.py` – Recursive descent parser
- `input.py` – Sample code file (optional)

Then run:

```bash
streamlit run app.py
```

---

## 📁 File Structure

```
mini-compiler/
├── app.py          # Streamlit app to tokenize, parse, and visualize code
├── lexer.py        # Lexer to generate tokens from input
├── parser.py       # Parser that builds the AST
├── input.py        # Sample input code (used in standalone lexer/parser)
├── README.md       # Project documentation
```

---

## 📄 Example Code

```python
x = 10 + 5;
y = x * 2;

if y > 20 {
    print(y);
}
```

---

## 🛡️ Notes

- Only a subset of Python-like syntax is supported.
- Use semicolons to terminate statements.
- Parser currently handles: assignments, arithmetic expressions, `if` statements, and nested blocks.

---

Built for compiler designing and visualization practice.
