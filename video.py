import cv2
import os
import tempfile
import numpy as np
from model import VideoGeneratorModel
from typing import Tuple
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)

class VideoGenerator:
    def __init__(self, llm):
        self.model = VideoGeneratorModel(llm)
        self.temp_dir = tempfile.TemporaryDirectory()

    def generate_video_with_opencv(self, scenes: list, output_file: str, fps: int = 24) -> str:
        try:
            image_files = self.model.generate_images(scenes)
            
            if not image_files:
                raise RuntimeError("No images generated")
            
            with Image.open(image_files[0]) as img:
                width, height = img.size

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
            
            if not video.isOpened():
                raise RuntimeError("Failed to initialize video writer")
            
            for img_path in image_files:
                if not os.path.exists(img_path):
                    raise FileNotFoundError(f"Image {img_path} not found")
                
                with Image.open(img_path) as pil_img:
                    frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                
                for _ in range(int(fps * 3)):
                    video.write(frame)
            
            video.release()
            logging.info(f"Video generated: {output_file}")
            return output_file
            
        except Exception as e:
            logging.error(f"Video generation error: {str(e)}")
            raise
        finally:
            for img_path in image_files:
                try:
                    os.remove(img_path)
                except:
                    pass

    def generate_video_pipeline(self, idea: str, style: str) -> Tuple[str, str]:
        try:
            result = self.model.generate_storyboard_and_parameters(idea, style)
            storyboard = result["storyboard"]
            scenes = [line.strip().split(":", 1)[-1].strip() 
                     if ":" in line else line.strip() 
                     for line in storyboard.split("\n") if line.strip()]
            
            if not scenes:
                raise ValueError("No scenes generated")
            
            output_file = f"{idea.replace(' ', '_')}_{style}.mp4"
            self.generate_video_with_opencv(scenes, output_file)
            
            return output_file, storyboard
        except Exception as e:
            logging.error(f"Pipeline error: {str(e)}")
            raise