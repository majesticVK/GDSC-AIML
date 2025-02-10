from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field

storyboard_prompt = PromptTemplate(
    input_variables=["idea", "style"],
    template="""Generate a storyboard for a video about "{idea}" in {style} style.
Create 5-7 numbered scenes that visually tell the story. Format like:
1. Scene description
2. Scene description
..."""
)

parameters_prompt = PromptTemplate(
    input_variables=["storyboard", "style"],
    template="""Based on this storyboard in {style} style:
{storyboard}
Generate these parameters:
1. Visual Style: Colors, mood, elements
2. Duration: Video length
3. Resolution: 1080p or 4K"""
)

class Storyboard(BaseModel):
    scenes: list = Field(..., min_items=3)

class VideoParameters(BaseModel):
    visual_style: str
    duration: str
    resolution: str