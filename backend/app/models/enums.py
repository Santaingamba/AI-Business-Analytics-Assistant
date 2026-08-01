from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    ANALYST = "ANALYST"

class Status(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    LOCKED = "LOCKED"
    SUSPENDED = "SUSPENDED"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"

class FileType(str, Enum):
    CSV = "CSV"
    EXCEL = "EXCEL"

class ProcessingStatus(str, Enum):
    UPLOADING = "UPLOADING"
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"
    
class Visibility(str, Enum):
    PRIVATE = "PRIVATE"
    ORGANIZATION = "ORGANIZATION"
    PUBLIC = "PUBLIC"

class ColumnDataType(str, Enum):
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"
    STRING = "STRING"
    DATE = "DATE"
    DATETIME = "DATETIME"
    CATEGORICAL = "CATEGORICAL"
    MIXED = "MIXED"
    UNKNOWN = "UNKNOWN"

class AIConversationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"

class MessageRole(str, Enum):
    USER = "USER"
    AI = "AI"
    SYSTEM = "SYSTEM"

class InsightCategory(str, Enum):
    REVENUE = "REVENUE"
    CUSTOMER = "CUSTOMER"
    PRODUCT = "PRODUCT"
    TREND = "TREND"
    ANOMALY = "ANOMALY"
    DATA_QUALITY = "DATA_QUALITY"
    GENERAL = "GENERAL"

class ImportanceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class RecommendationStatus(str, Enum):
    NEW = "NEW"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    IMPLEMENTED = "IMPLEMENTED"
