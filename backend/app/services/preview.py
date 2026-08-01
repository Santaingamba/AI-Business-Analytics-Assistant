import csv
import openpyxl
from typing import List, Dict, Any, Tuple
from app.models.enums import FileType

class PreviewService:
    @classmethod
    def get_csv_preview(cls, file_path: str, delimiter: str = ',', encoding: str = 'utf-8', num_rows: int = 20) -> Tuple[List[str], List[List[Any]]]:
        headers = []
        data = []
        try:
            with open(file_path, mode='r', encoding=encoding) as f:
                reader = csv.reader(f, delimiter=delimiter)
                try:
                    headers = next(reader)
                except StopIteration:
                    return [], []
                    
                count = 0
                for row in reader:
                    data.append(row)
                    count += 1
                    if count >= num_rows:
                        break
        except Exception:
            pass
        return headers, data

    @classmethod
    def get_excel_preview(cls, file_path: str, num_rows: int = 20) -> Tuple[List[str], List[List[Any]]]:
        headers = []
        data = []
        try:
            wb = openpyxl.load_workbook(filename=file_path, read_only=True, data_only=True)
            sheet = wb.active
            
            count = 0
            for row in sheet.iter_rows(values_only=True):
                if count == 0:
                    headers = [str(cell) if cell is not None else "" for cell in row]
                else:
                    data.append(list(row))
                    if count >= num_rows:
                        break
                count += 1
        except Exception:
            pass
        return headers, data
        
    @classmethod
    def get_preview(cls, file_path: str, file_type: FileType, num_rows: int = 20) -> Tuple[List[str], List[List[Any]]]:
        if file_type == FileType.CSV:
            return cls.get_csv_preview(file_path, num_rows=num_rows)
        else:
            return cls.get_excel_preview(file_path, num_rows=num_rows)
