import uuid
from pathlib import Path
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from lexer import tokenize           
from parser import Parser            

st.set_page_config(
    page_title="Python Mini-Compiler",
    page_icon="🐍",
    layout="wide",
)

st.title("Python Mini-Compiler")

def build_ast_graph(node, parent_id=None, nodes=None, edges=None):
    if nodes is None:
        nodes, edges = [], []

    current_id = str(uuid.uuid4())

    if isinstance(node, tuple):
        label = str(node[0])
    elif isinstance(node, list):
        label = "LIST"
    else:
        label = str(node)

    nodes.append(
        Node(
            id=current_id,
            label=label,
            shape="box",
            size=250,
            font={"multi": True},
        )
    )

    if parent_id:
        edges.append(Edge(source=parent_id, target=current_id))

    if isinstance(node, tuple):
        for child in node[1:]:
            build_ast_graph(child, current_id, nodes, edges)
    elif isinstance(node, list):
        for item in node:
            build_ast_graph(item, current_id, nodes, edges)

    return nodes, edges

left, right = st.columns([3, 5])

with left:
    st.subheader("Input Code")

    code = ""

    uploaded = st.file_uploader("Upload a .py / .txt file", type=["py", "txt"])
    if uploaded is not None:
        code = uploaded.read().decode("utf-8")

    code = st.text_area(
        label="",
        value=code,
        height=350,
        placeholder="# Paste some code or upload a file →",
    )

    run = st.button("🔍  Tokenise & Parse", use_container_width=True)

if run:
    if not code.strip():
        st.warning("Please provide some code first.")
        st.stop()

    code = code.replace('\r\n', '\n').replace('\r', '\n')

    try:
        tokens = tokenize(code)
    except RuntimeError as err:
        st.error(f"Lexer error: {err}")
        st.stop()

    token_rows = [{"type": t[0], "lexeme": t[1]} for t in tokens]

    # AST
    try:
        parser = Parser(tokens)
        ast = parser.parse()
    except SyntaxError as err:
        st.error(f"Syntax error: {err}")
        st.stop()

    # Display
    with right:
        st.subheader("Tokens")
        st.table(token_rows)
        st.success(f"✅ Total Tokens: {len(tokens)}")

        st.subheader("AST – Visual tree")
        nodes, edges = build_ast_graph(ast)

        cfg = Config(
            width="100%",
            height=500,
            directed=True,
            hierarchical=True,
            physics=False,
            nodeHighlightBehavior=True,
        )

        agraph(nodes=nodes, edges=edges, config=cfg)

        st.markdown(
            """
            **Tips**
            * Drag nodes to reposition (physics is off for a neat tree).
            * Mouse-wheel to zoom.
            """,
            unsafe_allow_html=True,
        )

else:
    st.info(" Paste code (or upload), then hit **Tokenise & Parse**.")
