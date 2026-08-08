import json
import pandas as pd
import xml.etree.ElementTree as ET


def parse_json(file):
    return json.load(file)


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
