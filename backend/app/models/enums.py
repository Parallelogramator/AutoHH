# app/models/enums.py
import enum

class MatchStatusEnum(str, enum.Enum):
    NEW = "new"
    REVIEW = "review"
    APPLIED = "applied"
    REJECTED = "rejected"

class DocKindEnum(str, enum.Enum):
    RESUME = "resume"
    PROJECT = "project"
    CERTIFICATE = "cert"