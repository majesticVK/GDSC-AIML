import streamlit as st
from video import VideoGenerator
from langchain_groq import ChatGroq
import os

# Initialize ChatGroq LLM
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0.7,
    api_key="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"
)

video_gen = VideoGenerator(llm)

# Streamlit UI
st.title("AI Video and script Generator Chatbot 🎥")
st.write("Turn your creative ideas into stunning videos with AI!")

# Collect user input
idea = st.text_input("💡 Enter your creative idea:")
style = st.selectbox(
    "🎨 Select a video style:",
    ["Cartoon", "Realistic", "Minimalistic", "Abstract", "Futuristic", "Hand-drawn"]
)

if st.button("🚀 Generate Video"):

    
    if idea.strip() and style:
        with st.spinner("Generating your video... 🎬 This may take 2-5 minutes"):
            try:
                progress_bar = st.progress(0)
                
                # Generate storyboard
                result = video_gen.model.generate_storyboard_and_parameters(idea, style)
                progress_bar.progress(30)

                                # Display generated text
                st.subheader("Generated Storyboard 📝")
                st.write(result["storyboard"])
                
                with st.expander("📖 Scene Breakdown"):
                    scenes = [line.strip() for line in result["storyboard"].split("\n") if line.strip()]
                    for i, scene in enumerate(scenes, 1):
                        st.markdown(f"**Scene {i}:** {scene}")
            
                
                # Generate images
                scenes = [line.strip() for line in result["storyboard"].split("\n") if line.strip()]
                image_paths = video_gen.model.generate_images(scenes)
                progress_bar.progress(70)
                
                # Generate video
                output_file = f"{idea.replace(' ', '_')}_{style}.mp4"
                video_gen.generate_video_with_opencv(scenes, output_file)
                progress_bar.progress(100)
                
                # Display results
                st.success("🎉 Video generated successfully!")
                st.video(output_file)
                st.download_button("Download Video", output_file)
                
            except Exception as e:
                st.error(f"🚨 Generation failed: {str(e)}")
                st.error("Check the API key and input parameters")
    else:
        st.warning("Please enter both an idea and select a style before generating a video.")

# Footer
st.markdown("---\n🛠 Built with LangChain, ChatGroq, OpenCV, Streamlit, and Stability")
st.markdown("------- project by Vansh Kumar -------")