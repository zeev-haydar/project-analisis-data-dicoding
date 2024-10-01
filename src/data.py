# data.py

from typing import Dict
import pandas as pd
import os

class Data:
    '''
    Data class provides data for widgets
    '''
    _data: Dict[str, pd.DataFrame]
    DATA_PATH: str = "./data/E-Commerce Public Dataset/"
    
    def __init__(self):
        self._data: Dict[str, pd.DataFrame] = {} 
        self._data["costumers"] = pd.read_csv(self.DATA_PATH + "customers_dataset.csv")
        self._data["geolocation"] = pd.read_csv(self.DATA_PATH + "geolocation_dataset.csv")
        self._data["order_items"] = pd.read_csv(self.DATA_PATH + "order_items_dataset.csv")
        self._data["order_payments"] = pd.read_csv(self.DATA_PATH + "order_payments_dataset.csv")
        self._data["order_reviews"] = pd.read_csv(self.DATA_PATH + "order_reviews_dataset.csv")
        self._data["orders"] = pd.read_csv(self.DATA_PATH + "orders_dataset.csv")
        self._data["product_category_name"] = pd.read_csv(self.DATA_PATH + "product_category_name_translation.csv")
        self._data["products"] = pd.read_csv(self.DATA_PATH + "products_dataset.csv")
        self._data["sellers"] = pd.read_csv(self.DATA_PATH + "sellers_dataset.csv")
        
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
    