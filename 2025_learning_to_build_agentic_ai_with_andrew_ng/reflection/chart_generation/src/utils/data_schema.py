"""
Data schema parser for the coffee sales dataset.

This module provides utilities for parsing and understanding the structure
of the coffee_sales.csv dataset.
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ColumnInfo:
    """Information about a dataset column."""
    name: str
    dtype: str
    sample_values: List[str]
    null_count: int
    unique_count: int


class DataSchema:
    """
    Parser and analyzer for the coffee sales dataset schema.
    
    This class provides methods to understand the structure and content
    of the coffee_sales.csv dataset for use in agent prompts.
    """
    
    def __init__(self, csv_path: str):
        """
        Initialize the data schema parser.
        
        Args:
            csv_path: Path to the coffee_sales.csv file
        """
        self.csv_path = Path(csv_path)
        self.df: Optional[pd.DataFrame] = None
        self.columns: List[str] = []
        self._load_data()
    
    def _load_data(self) -> None:
        """Load and analyze the CSV data."""
        try:
            self.df = pd.read_csv(self.csv_path)
            self.columns = list(self.df.columns)
        except Exception as e:
            raise ValueError(f"Failed to load CSV file {self.csv_path}: {e}")
    
    def get_column_info(self, column_name: str) -> ColumnInfo:
        """
        Get detailed information about a specific column.
        
        Args:
            column_name: Name of the column to analyze
            
        Returns:
            ColumnInfo containing column details
            
        Raises:
            ValueError: If column doesn't exist
        """
        if column_name not in self.columns:
            raise ValueError(f"Column '{column_name}' not found in dataset")
        
        column_data = self.df[column_name]
        
        # Get sample values (non-null)
        sample_values = column_data.dropna().head(5).astype(str).tolist()
        
        return ColumnInfo(
            name=column_name,
            dtype=str(column_data.dtype),
            sample_values=sample_values,
            null_count=int(column_data.isnull().sum()),
            unique_count=int(column_data.nunique())
        )
    
    def get_description(self) -> str:
        """
        Get a comprehensive description of the dataset.
        
        Returns:
            String description of the dataset structure and content
        """
        if self.df is None:
            return "Dataset not loaded"
        
        description = f"Dataset: {self.csv_path.name}\n"
        description += f"Shape: {self.df.shape[0]} rows, {self.df.shape[1]} columns\n\n"
        
        description += "Columns:\n"
        for col in self.columns:
            col_info = self.get_column_info(col)
            description += f"- {col} ({col_info.dtype}): {col_info.unique_count} unique values"
            if col_info.null_count > 0:
                description += f", {col_info.null_count} nulls"
            description += "\n"
        
        return description
    
    def get_sample_data(self, n_rows: int = 3) -> str:
        """
        Get sample data from the dataset.
        
        Args:
            n_rows: Number of sample rows to return
            
        Returns:
            String representation of sample data
        """
        if self.df is None:
            return "No data available"
        
        sample_df = self.df.head(n_rows)
        return sample_df.to_string(index=False)
    
    def get_date_range(self) -> Optional[Dict[str, str]]:
        """
        Get the date range of the dataset.
        
        Returns:
            Dictionary with 'start' and 'end' dates, or None if no date column
        """
        if 'date' not in self.columns:
            return None
        
        try:
            date_col = pd.to_datetime(self.df['date'])
            return {
                'start': date_col.min().strftime('%Y-%m-%d'),
                'end': date_col.max().strftime('%Y-%m-%d')
            }
        except Exception:
            return None
    
    def get_coffee_types(self) -> List[str]:
        """
        Get list of unique coffee types in the dataset.
        
        Returns:
            List of unique coffee type names
        """
        if 'coffee_name' not in self.columns:
            return []
        
        return self.df['coffee_name'].dropna().unique().tolist()
    
    def get_quarterly_data(self, year: int, quarter: int) -> pd.DataFrame:
        """
        Get data for a specific quarter.
        
        Args:
            year: Year to filter
            quarter: Quarter (1-4) to filter
            
        Returns:
            Filtered DataFrame for the specified quarter
        """
        if 'date' not in self.columns:
            raise ValueError("No date column found in dataset")
        
        try:
            # Convert date column to datetime
            df_with_dates = self.df.copy()
            df_with_dates['date'] = pd.to_datetime(df_with_dates['date'])
            
            # Filter by year and quarter
            year_data = df_with_dates[df_with_dates['date'].dt.year == year]
            
            if quarter == 1:
                quarter_data = year_data[year_data['date'].dt.month.isin([1, 2, 3])]
            elif quarter == 2:
                quarter_data = year_data[year_data['date'].dt.month.isin([4, 5, 6])]
            elif quarter == 3:
                quarter_data = year_data[year_data['date'].dt.month.isin([7, 8, 9])]
            elif quarter == 4:
                quarter_data = year_data[year_data['date'].dt.month.isin([10, 11, 12])]
            else:
                raise ValueError("Quarter must be 1, 2, 3, or 4")
            
            return quarter_data
            
        except Exception as e:
            raise ValueError(f"Failed to filter quarterly data: {e}")
    
    def validate_query(self, query: str) -> bool:
        """
        Validate if a query can be answered with this dataset.
        
        Args:
            query: User query to validate
            
        Returns:
            True if query seems valid for this dataset
        """
        query_lower = query.lower()
        
        # Check for relevant keywords
        relevant_keywords = [
            'coffee', 'sales', 'revenue', 'price', 'date', 'quarter',
            'chart', 'plot', 'graph', 'visualization'
        ]
        
        has_relevant_keywords = any(keyword in query_lower for keyword in relevant_keywords)
        
        # Check for date-related terms
        date_terms = ['2024', '2025', 'q1', 'q2', 'q3', 'q4', 'quarter']
        has_date_terms = any(term in query_lower for term in date_terms)
        
        return has_relevant_keywords and has_date_terms
