import csv
import io
import openpyxl
from datetime import datetime
from typing import List, Dict, Any, Tuple
from app.models.enums import ColumnDataType

class SchemaExtractorService:
    @classmethod
    def detect_type(cls, values: List[str]) -> ColumnDataType:
        if not values:
            return ColumnDataType.UNKNOWN
            
        types = set()
        for v in values:
            if v is None or str(v).strip() == "":
                continue
            
            v_str = str(v).strip()
            
            # Boolean
            if v_str.lower() in ('true', 'false', 'yes', 'no', '1', '0') and len(values) > 1:
                types.add(ColumnDataType.BOOLEAN)
                continue
                
            # Integer
            try:
                int(v_str)
                types.add(ColumnDataType.INTEGER)
                continue
            except ValueError:
                pass
                
            # Float
            try:
                float(v_str)
                types.add(ColumnDataType.FLOAT)
                continue
            except ValueError:
                pass
                
            # Date / Datetime
            try:
                datetime.fromisoformat(v_str.replace('Z', '+00:00'))
                types.add(ColumnDataType.DATETIME)
                continue
            except ValueError:
                pass
                
            types.add(ColumnDataType.STRING)
            
        if len(types) == 0:
            return ColumnDataType.UNKNOWN
        if len(types) == 1:
            return types.pop()
        
        # Fallbacks for mixed
        if ColumnDataType.STRING in types:
            return ColumnDataType.STRING
        if ColumnDataType.FLOAT in types and ColumnDataType.INTEGER in types:
            return ColumnDataType.FLOAT
            
        return ColumnDataType.MIXED

    @classmethod
    def extract_from_csv(cls, file_path: str, delimiter: str = ',', encoding: str = 'utf-8', num_rows: int = 50) -> Tuple[List[Dict[str, Any]], int]:
        columns = []
        row_count = 0
        try:
            with open(file_path, mode='r', encoding=encoding) as f:
                reader = csv.reader(f, delimiter=delimiter)
                try:
                    headers = next(reader)
                    row_count += 1
                except StopIteration:
                    return [], 0
                
                # Clean headers
                headers = [str(h).strip() for h in headers]
                
                sample_data = {i: [] for i in range(len(headers))}
                
                for row in reader:
                    row_count += 1
                    if row_count <= num_rows + 1:
                        for i, val in enumerate(row):
                            if i < len(headers):
                                sample_data[i].append(val)
                                
        except Exception as e:
            raise ValueError(f"Failed to extract schema from CSV: {str(e)}")
            
        for i, header in enumerate(headers):
            samples = sample_data.get(i, [])
            detected_type = cls.detect_type(samples)
            sample_val_str = ", ".join([str(s) for s in samples[:3] if s])[:200]
            
            columns.append({
                "column_name": header or f"Column_{i}",
                "detected_data_type": detected_type,
                "position": i,
                "sample_values": sample_val_str,
                "is_nullable": any(s == "" or s is None for s in samples) if samples else True,
            })
            
        # Count remaining rows properly
        try:
            with open(file_path, mode='r', encoding=encoding) as f:
                row_count = sum(1 for row in f) - 1 # exclude header
        except:
            pass
            
        return columns, max(0, row_count)

    @classmethod
    def extract_from_excel(cls, file_path: str, num_rows: int = 50) -> Tuple[List[Dict[str, Any]], int]:
        columns = []
        try:
            wb = openpyxl.load_workbook(filename=file_path, read_only=True, data_only=True)
            sheet = wb.active
            
            headers = []
            sample_data = {}
            row_count = 0
            
            for row in sheet.iter_rows(values_only=True):
                if row_count == 0:
                    headers = [str(cell).strip() if cell is not None else f"Column_{i}" for i, cell in enumerate(row)]
                    sample_data = {i: [] for i in range(len(headers))}
                else:
                    if row_count <= num_rows:
                        for i, cell in enumerate(row):
                            if i < len(headers):
                                sample_data[i].append(cell)
                row_count += 1
                
        except Exception as e:
            raise ValueError(f"Failed to extract schema from Excel: {str(e)}")
            
        for i, header in enumerate(headers):
            samples = sample_data.get(i, [])
            detected_type = cls.detect_type(samples)
            sample_val_str = ", ".join([str(s) for s in samples[:3] if s is not None])[:200]
            
            columns.append({
                "column_name": header,
                "detected_data_type": detected_type,
                "position": i,
                "sample_values": sample_val_str,
                "is_nullable": any(s == "" or s is None for s in samples) if samples else True,
            })
            
        return columns, max(0, row_count - 1)
