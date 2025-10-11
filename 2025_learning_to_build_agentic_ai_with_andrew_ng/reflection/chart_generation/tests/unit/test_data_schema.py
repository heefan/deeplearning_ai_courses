"""
Unit tests for the Data Schema parser.

These tests verify the CSV schema parsing and data analysis functionality.
"""

import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path
from unittest.mock import patch

from src.utils.data_schema import DataSchema, ColumnInfo


class TestDataSchema:
    """Test cases for the Data Schema parser."""
    
    @pytest.fixture
    def sample_csv_data(self):
        """Create sample CSV data for testing."""
        data = {
            'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-02-01', '2024-03-01'],
            'time': ['08:00', '09:30', '10:15', '14:20', '16:45'],
            'cash_type': ['card', 'cash', 'card', 'card', 'cash'],
            'card': ['ANON-001', 'ANON-002', 'ANON-003', 'ANON-004', 'ANON-005'],
            'price': [3.50, 4.20, 2.80, 3.90, 4.10],
            'coffee_name': ['Latte', 'Cappuccino', 'Americano', 'Latte', 'Espresso']
        }
        return pd.DataFrame(data)
    
    @pytest.fixture
    def temp_csv_file(self, sample_csv_data):
        """Create temporary CSV file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            sample_csv_data.to_csv(f.name, index=False)
            yield f.name
        os.unlink(f.name)
    
    def test_initialization_success(self, temp_csv_file):
        """Test successful schema initialization."""
        schema = DataSchema(temp_csv_file)
        
        assert schema.csv_path == Path(temp_csv_file)
        assert schema.df is not None
        assert len(schema.columns) == 6
        assert 'date' in schema.columns
        assert 'coffee_name' in schema.columns
    
    def test_initialization_file_not_found(self):
        """Test initialization with non-existent file."""
        with pytest.raises(ValueError, match="Failed to load CSV file"):
            DataSchema("non_existent_file.csv")
    
    def test_get_column_info_success(self, temp_csv_file):
        """Test getting column information."""
        schema = DataSchema(temp_csv_file)
        
        col_info = schema.get_column_info('date')
        
        assert isinstance(col_info, ColumnInfo)
        assert col_info.name == 'date'
        assert col_info.dtype == 'object'
        assert len(col_info.sample_values) == 5
        assert col_info.null_count == 0
        assert col_info.unique_count == 5
    
    def test_get_column_info_not_found(self, temp_csv_file):
        """Test getting info for non-existent column."""
        schema = DataSchema(temp_csv_file)
        
        with pytest.raises(ValueError, match="Column 'nonexistent' not found"):
            schema.get_column_info('nonexistent')
    
    def test_get_description(self, temp_csv_file):
        """Test getting dataset description."""
        schema = DataSchema(temp_csv_file)
        
        description = schema.get_description()
        
        assert "Dataset:" in description
        assert "Shape: 5 rows, 6 columns" in description
        assert "Columns:" in description
        assert "date (object): 5 unique values" in description
        assert "coffee_name (object): 4 unique values" in description
    
    def test_get_sample_data(self, temp_csv_file):
        """Test getting sample data."""
        schema = DataSchema(temp_csv_file)
        
        sample_data = schema.get_sample_data(2)
        
        assert "2024-01-01" in sample_data
        assert "Latte" in sample_data
        assert "Cappuccino" in sample_data
    
    def test_get_date_range_success(self, temp_csv_file):
        """Test getting date range."""
        schema = DataSchema(temp_csv_file)
        
        date_range = schema.get_date_range()
        
        assert date_range is not None
        assert date_range['start'] == '2024-01-01'
        assert date_range['end'] == '2024-03-01'
    
    def test_get_date_range_no_date_column(self):
        """Test getting date range with no date column."""
        # Create CSV without date column
        data = {'name': ['A', 'B'], 'value': [1, 2]}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            pd.DataFrame(data).to_csv(f.name, index=False)
            try:
                schema = DataSchema(f.name)
                date_range = schema.get_date_range()
                assert date_range is None
            finally:
                os.unlink(f.name)
    
    def test_get_coffee_types(self, temp_csv_file):
        """Test getting coffee types."""
        schema = DataSchema(temp_csv_file)
        
        coffee_types = schema.get_coffee_types()
        
        assert len(coffee_types) == 4
        assert 'Latte' in coffee_types
        assert 'Cappuccino' in coffee_types
        assert 'Americano' in coffee_types
        assert 'Espresso' in coffee_types
    
    def test_get_coffee_types_no_column(self):
        """Test getting coffee types with no coffee_name column."""
        data = {'date': ['2024-01-01'], 'value': [1]}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            pd.DataFrame(data).to_csv(f.name, index=False)
            try:
                schema = DataSchema(f.name)
                coffee_types = schema.get_coffee_types()
                assert coffee_types == []
            finally:
                os.unlink(f.name)
    
    def test_get_quarterly_data_q1(self, temp_csv_file):
        """Test getting Q1 data."""
        schema = DataSchema(temp_csv_file)
        
        q1_data = schema.get_quarterly_data(2024, 1)
        
        assert len(q1_data) == 5  # All data is in Q1
        assert all(pd.to_datetime(q1_data['date']).dt.month.isin([1, 2, 3]))
    
    def test_get_quarterly_data_q2(self, temp_csv_file):
        """Test getting Q2 data (should be empty)."""
        schema = DataSchema(temp_csv_file)
        
        q2_data = schema.get_quarterly_data(2024, 2)
        
        assert len(q2_data) == 0
    
    def test_get_quarterly_data_invalid_quarter(self, temp_csv_file):
        """Test getting data for invalid quarter."""
        schema = DataSchema(temp_csv_file)
        
        with pytest.raises(ValueError, match="Quarter must be 1, 2, 3, or 4"):
            schema.get_quarterly_data(2024, 5)
    
    def test_get_quarterly_data_no_date_column(self):
        """Test getting quarterly data with no date column."""
        data = {'name': ['A'], 'value': [1]}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            pd.DataFrame(data).to_csv(f.name, index=False)
            try:
                schema = DataSchema(f.name)
                with pytest.raises(ValueError, match="No date column found"):
                    schema.get_quarterly_data(2024, 1)
            finally:
                os.unlink(f.name)
    
    def test_validate_query_valid(self, temp_csv_file):
        """Test query validation with valid query."""
        schema = DataSchema(temp_csv_file)
        
        valid_queries = [
            "Create a chart showing coffee sales in 2024",
            "Plot Q1 revenue data",
            "Show coffee sales visualization for 2024",
            "Create a graph of 2024 Q1 sales"
        ]
        
        for query in valid_queries:
            assert schema.validate_query(query) is True
    
    def test_validate_query_invalid(self, temp_csv_file):
        """Test query validation with invalid query."""
        schema = DataSchema(temp_csv_file)
        
        invalid_queries = [
            "What's the weather like?",
            "Calculate the square root of 16",
            "Show me a picture of a cat"
        ]
        
        for query in invalid_queries:
            assert schema.validate_query(query) is False
    
    def test_validate_query_edge_cases(self, temp_csv_file):
        """Test query validation with edge cases."""
        schema = DataSchema(temp_csv_file)
        
        # Empty query
        assert schema.validate_query("") is False
        
        # Query with only date terms
        assert schema.validate_query("2024 2025") is False
        
        # Query with only coffee terms
        assert schema.validate_query("coffee sales") is False
    
    def test_column_info_with_nulls(self):
        """Test column info with null values."""
        data = {
            'col1': ['A', 'B', None, 'D', 'E'],
            'col2': [1, 2, 3, 4, 5]
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            pd.DataFrame(data).to_csv(f.name, index=False)
            try:
                schema = DataSchema(f.name)
                col_info = schema.get_column_info('col1')
                
                assert col_info.null_count == 1
                assert col_info.unique_count == 4  # 4 non-null unique values
                assert len(col_info.sample_values) == 4  # Only non-null values
            finally:
                os.unlink(f.name)
    
    def test_get_sample_data_empty_dataframe(self):
        """Test getting sample data from empty dataframe."""
        data = {'col1': [], 'col2': []}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            pd.DataFrame(data).to_csv(f.name, index=False)
            try:
                schema = DataSchema(f.name)
                sample_data = schema.get_sample_data()
                assert "Empty DataFrame" in sample_data or len(sample_data.strip()) == 0
            finally:
                os.unlink(f.name)
