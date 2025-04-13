import logging
import os

import pandas as pd

from src.domain.reader.base_reader import BaseReader


class PandasReader(BaseReader):
    """
    PandasReader uses pandas to read various file types including parquet, csv, json,
    HTML, XML, pickle, HDF, and Feather.

    The convert method reads the file based on its extension and returns a dictionary
    (list of records) representing the tabular data. For HTML files, which may contain
    multiple tables, it returns the first table found.

    Supported file extensions (case-insensitive): parquet, csv, json, html, xml, pickle,
        hdf, feather.
    """

    def convert(self, file_path: str) -> str | dict:
        """
        Reads a file at the given path using pandas based on the file extension and converts
        the tabular data into a dictionary (list of row dictionaries).

        Args:
            file_path (str): The path to the file to be read.

        Returns:
            dict or list: A dictionary representing the DataFrame's records (list of dictionaries).
                (This output is typically a list of dictionaries.)

        Raises:
            ValueError: If the file extension is not supported.
            Exception: If an error occurs during reading.
        """
        # Extract file extension and normalize (remove the dot and make lowercase)
        ext = os.path.splitext(file_path)[1].lower()
        if ext.startswith("."):
            ext = ext[1:]

        supported = {
            "parquet",
            "csv",
            "json",
            "html",
            "xml",
            "pickle",
            "hdf",
            "feather",
        }
        if ext not in supported:
            raise ValueError(f"Unsupported file extension: {ext}")

        try:
            if ext == "html":
                # read_html returns a list of DataFrames; pick the first one
                df_list = pd.read_html(file_path)
                text = []
                for df in df_list:
                    text.append(df)
                return text
            elif ext == "xml":
                # Requires pandas version 1.3+ which supports pd.read_xml
                df = pd.read_xml(file_path)
            elif ext == "csv":
                df = pd.read_csv(file_path)
            elif ext == "parquet":
                df = pd.read_parquet(file_path)
            elif ext == "json":
                df = pd.read_json(file_path)
            elif ext == "pickle":
                df = pd.read_pickle(file_path)
            elif ext == "hdf":
                df = pd.read_hdf(file_path)
            elif ext == "feather":
                df = pd.read_feather(file_path)
            else:
                raise ValueError(f"File type {ext} is not supported")
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {e}")
            raise e

        # Convert the DataFrame to a dictionary (list of records) and return.
        return df.to_dict(orient="records")
