from typing import List

from pydantic import BaseModel, Field


class OpenAccessInfo(BaseModel):
    """Information about the Open Access status of a paper."""
    is_oa: bool = Field(..., description="Whether the paper is Open Access")
    oa_status: str = Field(..., description="The status (e.g., gold, green, bronze, closed)")
    oa_url: str | None = Field(None, description="Direct URL to the full text PDF or HTML")
    version: str | None = Field(None, description="The version available (e.g., publishedVersion)")


class Paper(BaseModel):
    """Domain model representing a research paper."""
    doi: str = Field(..., description="Digital Object Identifier")
    title: str | None = Field(None, description="Title of the paper")
    authors: List[str] = Field(default_factory=list, description="List of author names")
    publication_date: str | None = Field(None, description="Date of publication in ISO 8601 format (YYYY-MM-DD)")
    publisher: str | None = Field(None, description="Publisher name")
    abstract: str | None = Field(None, description="Abstract of the paper")
    oa_info: OpenAccessInfo | None = Field(None, description="Open Access availability details")
