import re
import hashlib
import openai
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

import os
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class PII:
    def __init__(self, df):
        self.pii_cols = None
        self.df = df
        pass

    def identify_pii(self):        
        column_name = self.df.columns.values

        prompt = f"""Here is a list of of columns present in my data: {column_name}. 
                    Your goal is to identify columns which could potentially contain PII data. 
                    From the given list of columns I shared, return the column names which could have PII. 
                    Give the result in the form of Python string (no individual quotes for strings), seperated by comma in the exact case as the original column names I gave
                    No preamble"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": prompt
                }
            ]   
        )
        self.pii_cols = response.choices[0].message.content.split(", ")
        return self.pii_cols
    

    def mask_pii(self):
        if self.pii_cols is None:
            raise ValueError("No PII columns identified. Run `identify_pii` first.")

        def mask_value(value, field_type):
            if pd.isna(value):  
                return value

            value = str(value)  

            if field_type == "email":
                parts = value.split("@")
                return parts[0][0] + "*****@" + parts[1] if len(parts) > 1 else "*****"

            elif field_type == "phone":
                value = re.sub(r'\D', '', value)
                return re.sub(r"(\d{2})\d{6}(\d{2})", r"\1******\2", value)  # Keep first & last 2 digits

            elif field_type in ["ssn", "passport", "credit_card"]:
                return "****-****-****-" + value[-4:]  # Keep last 4 digits

            elif field_type == "home_address":
                parts = value.split(",")
                if len(parts) >= 3:
                    return "**** " + parts[0].split()[1] + ", " + ", ".join(parts[1:])  # Mask house number
                return "**** " + value

            elif field_type == "name":
                return value[0] + "****"  # Keep first letter only

            elif field_type == "hash":
                return hashlib.sha256(value.encode()).hexdigest()  # Irreversible hashing

            else:
                return "*****"  # Default fully redact
        
        # Define common patterns to infer PII type
        column_patterns = {
            "email": ["email", "e-mail"],
            "phone": ["phone", "mobile", "contact", 'phone number'],
            "ssn": ["ssn", "social security", "social security number"],
            "passport": ["passport"],
            "credit_card": ["card number", "credit", "debit"],
            "home_address": ["address", "street", "residence"],
            "name": ["name", "full name"],
            "hash": ["token", "unique_id"]
        }

        def infer_pii_type(col_name):
            """Infer the type of PII based on column name patterns"""
            col_lower = col_name.lower()
            for pii_type, patterns in column_patterns.items():
                if any(pattern in col_lower for pattern in patterns):
                    return pii_type
            return "default"


        for col in self.pii_cols:
            pii_type = infer_pii_type(col)
            self.df[col] = self.df[col].apply(lambda x: mask_value(x, pii_type))

        return self.df
    
    def exclude_columns(self, columns):
        for column in columns:
            self.pii_cols.remove(column)   
