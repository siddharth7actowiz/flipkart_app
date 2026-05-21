import pandas as pd
import os
from sqlalchemy import create_engine
from datetime import datetime

try:
    # ------- OUTPUT DIR -------
    output = r"D:\apps\flipkart\flipkart\pagesave\output"
    os.makedirs(output, exist_ok=True)

    # ----- TODAY'S DATE -----
    t_d = datetime.now().strftime("%Y-%m-%d")

    # Create DB connection
    engine = create_engine("mysql+pymysql://root:actowiz@localhost/flipkart")

    # Query data
    query = "SELECT * FROM product_data_flipkart2"
    df = pd.read_sql(query, engine)

    # Drop ID column
    df = df.drop(columns=["Id", "id"], errors="ignore")

    print("Shape:", df.shape)
    # 5. FIX is_sold_out
    if "is_sold_out" in df.columns:
        df["is_sold_out"] = pd.to_numeric(df["is_sold_out"], errors="coerce")

        df["is_sold_out"] = df["is_sold_out"].apply(
            lambda x: "TRUE" if x == 1 else
            "FALSE" if x == 0 else
            "N/A"
        )
    # 1. Replace NULL
    df = df.fillna("N/A")

    # 2. Replace empty strings
    df.replace(r'^\s*$', "N/A", regex=True, inplace=True)

    # 3. Replace [] and {}
    df.replace(["[]", "null", "{}"], "N/A", inplace=True)

    # 4. Replace 0 → N/A (object columns only)
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].replace(0, "N/A")


    # 6. Fix numeric columns
    cols_to_fix = [
        "average_rating",
        "total_ratings",
        "discount",
        "mrp",
        "number_of_ratings",
        "avg_rating","shipping_charges"
    ]

    for col in cols_to_fix:
        if col in df.columns:
            df[col] = df[col].replace(0, "N/A")

    # Save to Excel
    file_name = f"Flipkart_App_{t_d}.xlsx"
    output_file_path = os.path.join(output, file_name)

    df.to_excel(output_file_path, index=False)

    print(f"🎉🚀✅ Done (FINAL CLEAN VERSION SAVED TO 📁 {output_file_path}) 🏁🔥")

except Exception as e:
    print("❌ ERROR OCCURRED:")
    print(str(e))