import json
import pandas as pd

import os
import shutil

from get_img_key import *
from get_product_img import *


def clean_data(df):
    """
    This function aims to clean the column names to prepare the transformation to json
    """
    #get unique product_id
    df = df.drop_duplicates(subset=["product_id"])
    df = df.drop_duplicates(subset=["handle"])

    df = df[["Product Name", "Video Link", "handle", "Product Category", "Product TTS Link"]]
    df = df.rename(columns={
        "Product Name":     "product_name",
        "Video Link":       "video_link",
        "handle":           "creator_handle",
        "Product Category": "product_category",
        "Product TTS Link": "product_link"
    })
    df = df.reset_index(drop=True)
    return df

def get_json(df):
    """
    this function needs top 5 videos based on video GMV and product GMV
    output: json template feeding to Feishu Card
    """
    data_list = df.to_dict(orient="records")
    df_result = data_list
    # df_result = {"product_description": data_list}
    #template_variables  = json.dumps(df_selected, indent=4, ensure_ascii=False)
    return df_result



def main():
    PATH = os.getcwd()
    
    # remove existing img_folder if it exists
    img_folder_path = "img_folder"
    shutil.rmtree(os.path.join(PATH, img_folder_path), ignore_errors=True)  # Clear existing images
    os.mkdir(os.path.join(PATH, img_folder_path))  # Create img_folder

    # get cleaned product_infos
    data = pd.read_csv("video_table.csv")
    cleaned_df = clean_data(data)
    cleaned_df["img_key"] = "" # Initialize img_key column

    # get product images
    for index, row in cleaned_df.iterrows():
        product_link = row["product_link"]
        product_name = row["product_name"]
        filename = os.path.join(PATH, img_folder_path, f"{index}.jpg")
        img = download_image(product_link, filename)
        img_key = {"img_key": get_img_key(img)}
        cleaned_df.at[index, "img_key"] = img_key  # Add img_key to

    json_template = get_json(cleaned_df)
    print(json.dumps(json_template, indent=4, ensure_ascii=False))  # For testing purposes

    # export to txt file
    with open("template.txt", "w", encoding="utf-8") as f:
        json.dump(json_template, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()

