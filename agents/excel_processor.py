"""Excel file processor with validation."""

import pandas as pd
from typing import Tuple, List, Dict, Optional
from utils.validators import (
    validate_phone_number,
    validate_date_format,
    validate_date_range,
    validate_customer_name,
    validate_file_size,
    validate_file_extension
)


class ExcelProcessor:
    """Handles Excel file parsing and validation."""

    REQUIRED_COLUMNS = {
        'customer_name': ['customer name', 'name', 'client name', 'member name'],
        'phone_number': ['contact', 'phone', 'phone number', 'mobile', 'mobile number'],
        'start_date': ['subscription start date', 'start date', 'join date', 'start'],
        'end_date': ['subscription end date', 'end date', 'expiry date', 'expiry', 'end']
    }

    def __init__(self):
        """Initialize processor."""
        self.df = None
        self.errors = []
        self.warnings = []

    def validate_file(self, uploaded_file) -> Tuple[bool, str]:
        """
        Validate uploaded file.
        Returns (is_valid, error_message).
        """
        # Check file extension
        is_valid, error = validate_file_extension(uploaded_file.name)
        if not is_valid:
            return False, error

        # Check file size
        is_valid, error = validate_file_size(uploaded_file.size)
        if not is_valid:
            return False, error

        return True, ""

    def find_column(self, possible_names: List[str], df_columns: List[str]) -> Optional[str]:
        """Find matching column name (case-insensitive)."""
        df_columns_lower = [col.lower().strip() for col in df_columns]

        for name in possible_names:
            if name.lower() in df_columns_lower:
                # Return original column name
                idx = df_columns_lower.index(name.lower())
                return df_columns[idx]

        return None

    def load_and_validate(self, uploaded_file) -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """
        Load Excel file and validate structure.
        Returns (is_valid, message, dataframe).
        """
        try:
            # Read Excel file
            self.df = pd.read_excel(uploaded_file, engine='openpyxl')

            # Check if empty
            if self.df.empty:
                return False, "Excel file is empty", None

            # Find required columns
            column_mapping = {}
            missing_columns = []

            for key, possible_names in self.REQUIRED_COLUMNS.items():
                found_column = self.find_column(possible_names, self.df.columns.tolist())
                if found_column:
                    column_mapping[key] = found_column
                else:
                    missing_columns.append(possible_names[0])

            # Check for missing columns
            if missing_columns:
                return False, f"Missing required columns: {', '.join(missing_columns)}", None

            # Rename columns to standard names
            rename_dict = {v: k for k, v in column_mapping.items()}
            self.df.rename(columns=rename_dict, inplace=True)

            return True, f"Successfully loaded {len(self.df)} rows", self.df

        except Exception as e:
            return False, f"Error reading Excel file: {str(e)}", None

    def validate_and_clean_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[Dict]]:
        """
        Validate and clean data.
        Returns (cleaned_dataframe, list_of_errors).
        """
        errors = []
        valid_rows = []

        for idx, row in df.iterrows():
            row_errors = []
            row_num = idx + 2  # Excel row number (1-indexed + header)

            # Validate customer name
            is_valid, error = validate_customer_name(row['customer_name'])
            if not is_valid:
                row_errors.append(f"Row {row_num}: {error}")
                continue

            # Validate phone number
            is_valid, error, formatted_phone = validate_phone_number(row['phone_number'])
            if not is_valid:
                row_errors.append(f"Row {row_num}: {error}")
                continue

            # Validate start date
            is_valid, error, start_date = validate_date_format(row['start_date'])
            if not is_valid:
                row_errors.append(f"Row {row_num}: Start date - {error}")
                continue

            # Validate end date
            is_valid, error, end_date = validate_date_format(row['end_date'])
            if not is_valid:
                row_errors.append(f"Row {row_num}: End date - {error}")
                continue

            # Validate date range
            is_valid, error = validate_date_range(start_date, end_date)
            if not is_valid:
                row_errors.append(f"Row {row_num}: {error}")
                continue

            # If all validations passed, add to valid rows
            if not row_errors:
                valid_rows.append({
                    'customer_name': str(row['customer_name']).strip(),
                    'phone_number': formatted_phone,
                    'subscription_start_date': start_date.strftime('%Y-%m-%d'),
                    'subscription_end_date': end_date.strftime('%Y-%m-%d'),
                })
            else:
                errors.extend(row_errors)

        # Create cleaned dataframe
        cleaned_df = pd.DataFrame(valid_rows) if valid_rows else pd.DataFrame()

        return cleaned_df, errors

    def process_file(self, uploaded_file) -> Tuple[bool, str, Optional[pd.DataFrame], List[str]]:
        """
        Complete file processing pipeline.
        Returns (success, message, cleaned_dataframe, errors).
        """
        # Validate file
        is_valid, error = self.validate_file(uploaded_file)
        if not is_valid:
            return False, error, None, [error]

        # Load file
        is_valid, message, df = self.load_and_validate(uploaded_file)
        if not is_valid:
            return False, message, None, [message]

        # Validate and clean data
        cleaned_df, errors = self.validate_and_clean_data(df)

        if cleaned_df.empty:
            return False, "No valid rows found after validation", None, errors

        success_message = f"✅ Processed {len(cleaned_df)} out of {len(df)} rows successfully"

        if errors:
            success_message += f"\n⚠️ {len(errors)} rows had errors and were skipped"

        return True, success_message, cleaned_df, errors
