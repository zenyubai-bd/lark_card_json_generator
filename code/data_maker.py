import pandas as pd
import json

video_table = pd.read_csv("video_table.csv")
video_table = video_table[video_table["In Product Table"]==1]

def clean_data(df):
    """
    This function aims to clean the column names to prepare the transformation to json
    """
    df = df[["Product Name", "Video Link", "handle", "Product Category", "Product TTS Link"]]
    df = df.rename(columns={
        "Product Name":     "product_name",
        "Video Link":       "video_link",
        "handle":           "creator_handle",
        "Product Category": "product_category",
        "Product TTS Link": "product_link"
    })
    df = df.dropna(subset=["product_link"])
    df = df.drop_duplicates(subset=["product_name"])
    # df = df[df["product_name"].notna()]
    return df

def dislike_videos(pop_row):
    """
    This function is used to delete the selected rows and regenerate json template for card generation
    Args:
        df: original dataframe
        pop_row: the row that want to be deleted
    """
    pop_row = [int(x)-1 for x in pop_row if int(x)<=5]
    video_table.drop(pop_row, inplace=True)
    video_table.reset_index(drop=True, inplace=True)
    print("video_dropped")
    return video_table

def get_json():
    """
    this function select top 5 videos based on video GMV and product GMV
    output: json template feeding to Feishu Card
    """
    df_selected = video_table[:5]
    df_selected = clean_data(df_selected)

    data_list = df_selected.to_dict(orient="records")
    df_selected = {"product_description": data_list}
    print("json_selected")
    #template_variables  = json.dumps(df_selected, indent=4, ensure_ascii=False)
    return df_selected
