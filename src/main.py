from data import Data
import streamlit as st
import argparse
import seaborn as sns
import matplotlib.pyplot as plt

from widgets import *


def example():
    st.title("Custom Widget Builder with Streamlit")

    create_container(
        child=lambda: build_text("This is a styled container", style={"background-color": "#007bff", "color": "white", "padding": "10px"}),
    )

    create_rows([
        lambda: create_buttons("Button 1", on_click=lambda: st.write("Button 1 clicked!")),
        lambda: create_buttons("Button 2", on_click=lambda: st.write("Button 2 clicked!")),
        lambda: create_buttons("Button 3", on_click=lambda: st.write("Button 3 clicked!")),
    ])

    create_container(
        child=lambda: create_columns([
            lambda: build_text("Column 1", style={"font-size": "20px"}),
            lambda: build_text("Column 2", style={"font-size": "18px", "color": "gray"}),
        ])
    )

    create_tabs(
        tab_names=["Tab 1", "Tab 2"],
        children=[
            lambda: build_text("Content for Tab 1"),
            lambda: build_text("Content for Tab 2"),
        ]
    )

    create_selectbox(
        options=["Option 1", "Option 2", "Option 3"],
        label="Select an option",
        on_select=lambda x: st.write(f"You selected: {x}")
    )
    
def main_app():
    data = Data()
    st.title("E-Commerce Public Dataset")
    
    # Create a select box for dataset selection
    dataset_names = list(data.get_datas().keys())
    
    with st.sidebar:
        st.write("# Navigate")
        # st.write("Overview")
        # st.write("Sales Information")
        overview_selected = st.radio("Select Section", ("Overview", "Sales Information"))
    
    # cols = st.columns(2)
    if overview_selected == "Overview":
        selected_dataset = st.selectbox("Select a dataset", dataset_names)
        
        st.write(f"Showing data for: **{selected_dataset}**")
        if selected_dataset:
            df = data.get_data(selected_dataset)
            
            # Handle object-type columns separately to avoid serialization issues
            try:
                # Convert only non-numeric columns to string
                non_numeric_columns = df.select_dtypes(include=['object']).columns.tolist()
                
                for col in non_numeric_columns:
                    df[col] = df[col].astype(str)  # Force string type for Arrow compatibility
                    
                st.dataframe(df)
            except Exception as e:
                st.write(f"Error displaying dataframe: {e}")
            
            st.write("Data Summary")
            st.dataframe(df.describe(include="all"))
            
            # Select a column for distribution plot
            column_names = df.select_dtypes(include=['number']).columns.tolist()
            selected_column = st.selectbox("Select a column for distribution plot", column_names)
            
            if selected_column:
                st.write(f"### Distribution of {selected_column}")
                
                # Plotting the distribution
                plt.figure(figsize=(10, 6))
                sns.histplot(df[selected_column], kde=True, bins=30)
                plt.title(f'Distribution of {selected_column}')
                plt.xlabel(selected_column)
                plt.ylabel('Frequency')
                st.pyplot(plt)
    
    
def main(run_example: bool = False):
    if run_example:
        example()
    else:
        main_app()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Streamlit App")
    parser.add_argument('--example', action='store_true', help='Run the example dashboard')
    args = parser.parse_args()
    
    # Run the main function with the example flag
    main(run_example=args.example)