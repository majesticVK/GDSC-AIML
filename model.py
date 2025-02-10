from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import storyboard_prompt, parameters_prompt
import requests
import uuid
import os
from PIL import Image, ImageDraw, ImageFont
from typing import List
from io import BytesIO
import textwrap

class VideoGeneratorModel:
    def __init__(self, llm):
        """
        Initialize the VideoGeneratorModel with an LLM.
        
        Args:
            llm: The language model to use for generating storyboards and parameters.
        """
        self.llm = llm
        self.storyboard_chain = LLMChain(
            llm=self.llm,
            prompt=storyboard_prompt,
            output_key="storyboard"
        )
        self.parameters_chain = LLMChain(
            llm=self.llm,
            prompt=parameters_prompt,
            output_key="parameters"
        )

    def generate_storyboard_and_parameters(self, idea: str, style: str) -> dict:
        """
        Generate a storyboard and video parameters based on the given idea and style.
        
        Args:
            idea (str): The idea for the video.
            style (str): The visual style of the video.
        
        Returns:
            dict: A dictionary containing the generated storyboard and parameters.
        """
        try:
            # Generate storyboard
            storyboard = self.storyboard_chain.run(idea=idea, style=style)
            
            # Generate video parameters
            parameters = self.parameters_chain.run(storyboard=storyboard, style=style)
            
            return {
                "storyboard": storyboard,
                "parameters": parameters
            }
        except Exception as e:
            print(f"Error generating storyboard and parameters: {str(e)}")
            raise

    def generate_images(self, scenes: List[str]) -> List[str]:
        """
        Generate images for each scene using a free API or fallback text images.
        
        Args:
            scenes (List[str]): A list of scene descriptions.
        
        Returns:
            List[str]: A list of file paths to the generated images.
        """
        image_paths = []
        for i, scene in enumerate(scenes):
            try:
                # Use Stability AI API
                response = requests.post(
                    "https://api.stability.ai/v2beta/stable-image/generate/sd3",
                    headers={
                        "Authorization": f"Bearer {os.getenv('STABILITY_API_KEY')}",
                        "Accept": "image/png"
                    },
                    files={"none": ''},
                    data={
                        "prompt": scene,
                        "model": "sd3",
                        "output_format": "png",
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    filename = f"scene_{i}.png"
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    image_paths.append(filename)
                else:
                    raise Exception(f"API Error {response.status_code}")
                    
            except Exception as e:
                print(f"Scene {i+1} generation failed: {str(e)}")
                image_paths.append(self.create_text_image(scene, i))
        
        return image_paths

    def create_text_image(self, scene: str, index: int) -> str:
        """
        Create a fallback text-based image for a scene.
        
        Args:
            scene (str): The scene description.
            index (int): The scene index.
        
        Returns:
            str: The file path to the generated fallback image.
        """
        try:
            img = Image.new('RGB', (1024, 768), color=(30, 30, 30))
            draw = ImageDraw.Draw(img)
            
            # Try to load font
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Wrap text
            lines = []
            for line in scene.split(', '):
                lines.extend(textwrap.wrap(line, width=40))
            
            # Draw text
            y = 100
            for line in lines:
                draw.text((100, y), line, font=font, fill=(255, 255, 0))
                y += 40
            
            # Save to bytes buffer
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            
            # Save to file
            filename = f"fallback_{index}.png"
            with open(filename, "wb") as f:
                f.write(buffer.getvalue())
            
            return filename
        except Exception as e:
            print(f"Error creating fallback image: {str(e)}")
            raise