from __future__ import annotations
from pydantic import BaseModel, Field

class SipParseRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1_000_000)

class InvestigationRequest(BaseModel):
    title: str = Field(min_length=3, max_length=160)
    description: str = Field(min_length=5, max_length=12_000)
    kind: str = Field(default="investigation", pattern="^(investigation|bug|feature|refactor|documentation|security)$")
    source_paths: list[str] = Field(default_factory=list, max_length=100)
