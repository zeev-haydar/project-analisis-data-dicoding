import pandas as pd
from data import Data
import streamlit as st
import argparse
import seaborn as sns
import matplotlib.pyplot as plt

import geopandas as gpd
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
    
def display_paginated_dataframe(df, rows_per_page=10):
    total_rows = df.shape[0]
    total_pages = (total_rows // rows_per_page) + (1 if total_rows % rows_per_page > 0 else 0)

    # Create a select box or slider for pagination control
    current_page = st.selectbox('Select page:', range(1, total_pages + 1))

    # Calculate the start and end index for the current page
    start_idx = (current_page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page

    # Display the current page of the dataframe
    st.dataframe(df.iloc[start_idx:end_idx])
    
def main_app():
    data = Data()
    st.title("E-Commerce Public Dataset")
    
    # Create a select box for dataset selection
    dataset_names = list(data.get_datas().keys())
    
    with st.sidebar:
        st.write("# Navigate")
        # st.write("Overview")
        # st.write("Sales Information")
        menu_selected = st.radio("Select Section", ("Overview", "Sales Information", "About Customers"))
    
    # cols = st.columns(2)
    if menu_selected == "Overview":
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
    elif menu_selected == "Sales Information":
        data.get_data("product_category_name")["product_category_name_english"] = data.get_data("product_category_name")["product_category_name_english"].apply(lambda x: x.replace("_", " "))
        order_items_joined = pd.merge(data.get_data("order_items"), data.get_data("orders"), "inner", on="order_id")
        order_item_products = pd.merge(order_items_joined, data.get_data("products"), "inner", "product_id").merge(data.get_data("product_category_name"), "left", "product_category_name")
        order_item_counts = order_item_products.value_counts(subset="product_category_name_english").reset_index()
        order_item_counts_copy = order_item_counts.copy()
        order_item_counts_copy.columns = ["Product Category", "Total Orders"]
        st.markdown("# Sales Information")
        st.markdown("## Total Orders by Product Category")
        display_paginated_dataframe(order_item_counts_copy, rows_per_page=10)
        st.markdown("## Top 10 Most Ordered Products")
        top_10_products = order_item_counts_copy.iloc[:10]


        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # Bar chart on the first subplot (left)
        ax1.set_title("Most Bought Product Categories")
        ax1.bar(top_10_products["Product Category"], top_10_products["Total Orders"], width=0.8)
        ax1.set_xticklabels(top_10_products["Product Category"], rotation=45)
        ax1.set_ylabel('Count')

        # Pie chart on the second subplot (right)
        ax2.set_title("Product Category Distribution")
        ax2.pie(top_10_products["Total Orders"], 
                labels=top_10_products["Product Category"], 
                autopct='%1.1f%%', startangle=90)

        plt.tight_layout()
        st.pyplot(plt)
        
    elif menu_selected == "About Customers":
        
        geolocation_mean_lat_and_long = data.get_data("geolocation").groupby("geolocation_city")[["geolocation_lat", "geolocation_lng"]].agg(["mean"])
        geolocation_mean_lat_and_long.columns = geolocation_mean_lat_and_long.columns.get_level_values(0)

        cust_segs = pd.merge(data.get_data("customers"), geolocation_mean_lat_and_long.reset_index(), "inner", left_on="customer_city", right_on="geolocation_city")
        city_counts = cust_segs['customer_city'].value_counts().reset_index()
        city_counts.columns = ['customer_city', 'count']
        k = 20
        city_counts_top_k = city_counts.iloc[:k]

        # Set the figure size
        state_counts = cust_segs['customer_state'].value_counts().reset_index()
        st.markdown("## Customer Count by State")
        display_paginated_dataframe(state_counts, rows_per_page=10)
        plt.figure(figsize=(10, 8))

        # Plot horizontal barplot with Seaborn
        plt.barh(city_counts_top_k['customer_city'], city_counts_top_k['count'], color='skyblue')

        plt.gca().invert_yaxis()

        # Set title and labels
        # plt.title("Customer Count by City")
        plt.xlabel("Count")
        plt.ylabel("City")
        
        st.markdown("## Customer Count by City")
        st.pyplot(plt)
        
        gdf = gpd.read_file("./data/brazil/br_shp/br.shp")
        state_counts["customer_state_for_map_merge"] = state_counts['customer_state'].apply(lambda x: "BR"+str(x))
        
        brazil_map = gdf.merge(state_counts, left_on='id', right_on='customer_state_for_map_merge', how='inner')
        # print(brazil_map.isna().sum())

        plt.figure(figsize=(16, 16))
        ax = brazil_map.plot(column='count', cmap='PuRd', linewidth=1, edgecolor='0.6', legend=True, aspect=1.0)

        # Add a title
        plt.title('Customer Count by State in Brazil', fontsize=15)
        plt.axis('off')

        # Annotate state names on the map
        for x, y, label, count in zip(brazil_map.geometry.centroid.x, brazil_map.geometry.centroid.y, brazil_map['customer_state_for_map_merge'], brazil_map['count']):
            short_label = label[2:]
            font_color = 'white' if count > brazil_map['count'].quantile(0.97) else 'black'
            ax.annotate(short_label, xy=(x, y), horizontalalignment='center', fontsize=6, color=font_color, weight='bold')
        
        st.markdown("## Customer by States")
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