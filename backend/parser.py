import json
import pandas as pd
import xml.etree.ElementTree as ET


def parse_json(source):
    if isinstance(source, str):
        with open(source, "r", encoding="utf-8") as file:
            return json.load(file)
    return json.load(source)


def parse_csv(file):
    df = pd.read_csv(file)
    df = df.rename(
        columns={
            "ProductID": "product_id",
            "ProductName": "product_name",
            "Category": "category",
        }
    )
    return df


def parse_xml(file):
    tree = ET.parse(file)
    return tree.getroot()
