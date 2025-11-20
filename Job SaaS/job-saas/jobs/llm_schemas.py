from typing import Optional
from pydantic import BaseModel, Field


class JobListing(BaseModel):
    title: str = Field(..., description='A meaningful title representing this job listing.')
    job_url: str = Field(..., description='Link to the job listing.')
    job_type: Optional[str] = Field(..., description='The type of the job (full-time, part-time, internship etc.)')
    level: Optional[str] = Field(..., description='The level of the position (entry level, senior level etc.)')
    summary: Optional[str] = Field(..., description='A short and concise summary of the job')
    salary: Optional[str] = Field(..., description='The salary that is specified')
    posted: Optional[str] = Field(..., description='When the job was posted')
    applicants: Optional[int] = Field(..., description='How many applicants the job already has.')


class JobListings(BaseModel):
    listings: list[JobListing]