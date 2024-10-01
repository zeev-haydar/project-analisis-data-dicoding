from typing import Dict, Callable, List
import streamlit as st

def create_style_sheets(**kwargs):
    style_string: str = ""
    for key, value in kwargs.items():
        style_string += f"{key}: {value}; "
    return style_string

def create_container(child: Callable[[], None] = None, style: Dict[str, str] = None):
    container_style = create_style_sheets(**style) if style else ""
    
    st.markdown(f"<div style='{container_style}'>", unsafe_allow_html=True)
    if child is not None:
        child()  # Render the child content inside the container
    st.markdown("</div>", unsafe_allow_html=True)

def build_text(text: str, style: Dict[str, str] = None):
    text_style = create_style_sheets(**style) if style else ""
    st.markdown(f"<p style='{text_style}'>{text}</p>", unsafe_allow_html=True)
    
def create_rows(children: List[Callable[[], None]]):
    cols = st.columns(len(children))
    for i, child in enumerate(children):
        with cols[i]:
            child()

def create_columns(children: List[Callable[[], None]]):
    for child in children:
        child()

def create_buttons(label: str, on_click: Callable[[], None] = None):
    if st.button(label):
        if on_click:
            on_click()

def create_sidebar(child: Callable[[], None] = None, style: Dict[str, str] = None):
    sidebar_style = create_style_sheets(**style) if style else ""
    st.sidebar.markdown(f"<div style='{sidebar_style}'>", unsafe_allow_html=True)
    if child:
        child()
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

def create_tabs(tab_names: List[str], children: List[Callable[[], None]]):
    selected_tab = st.selectbox("Select Tab", tab_names)
    for i, tab_name in enumerate(tab_names):
        if selected_tab == tab_name:
            children[i]()

def create_selectbox(options: List[str], label: str = "Choose an option", on_select: Callable[[str], None] = None):
    selected_option = st.selectbox(label, options)
    if on_select:
        on_select(selected_option)
