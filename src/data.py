# data.py

from typing import Dict
import pandas as pd
import os

class Data:
    '''
    Data class provides data for widgets (Singleton implementation)
    '''
    _instance = None
    _data: Dict[str, pd.DataFrame]
    data_path: str
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Data, cls).__new__(cls)
        return cls._instance

    def __init__(self, data_path = "./data/E-Commerce Public Dataset/"):
        if not hasattr(self, "_initialized"):  # To avoid re-initialization
            self.data_path = data_path
            self._data: Dict[str, pd.DataFrame] = {} 
            self._data["customers"] = pd.read_csv(self.data_path + "customers_dataset.csv")
            self._data["geolocation"] = pd.read_csv(self.data_path + "geolocation_dataset.csv")
            self._data["order_items"] = pd.read_csv(self.data_path + "order_items_dataset.csv")
            self._data["order_payments"] = pd.read_csv(self.data_path + "order_payments_dataset.csv")
            self._data["order_reviews"] = pd.read_csv(self.data_path + "order_reviews_dataset.csv")
            self._data["orders"] = pd.read_csv(self.data_path + "orders_dataset.csv")
            self._data["product_category_name"] = pd.read_csv(self.data_path + "product_category_name_translation.csv")
            self._data["products"] = pd.read_csv(self.data_path + "products_dataset.csv")
            self._data["sellers"] = pd.read_csv(self.data_path + "sellers_dataset.csv")
            self._initialized = True  # Mark as initialized to prevent re-execution of __init__

    def get_data(self, name: str):
        '''
        Returns the dataframe associated with the given name
        
        Parameters:
        name (str): the name of the dataframe to be returned
        
        Returns:
        pd.DataFrame: the dataframe associated with the given name
        '''
        return self._data[name]
    
    def get_datas(self):
        return self._data
