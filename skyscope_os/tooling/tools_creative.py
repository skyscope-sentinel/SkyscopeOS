from smolagents import tool
import os
import json
import lief
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from uncompyle6.main import decompile
from io import StringIO
from jinja2 import Environment, FileSystemLoader
import moviepy.editor as mpe
from gtts import gTTS

@tool
def analyze_binary(filepath: str) -> str:
    """Analyzes a binary file using lief and capstone."""
    try:
        binary = lief.parse(filepath)
        if not binary:
            return f"Error: Could not parse binary file at {filepath}"

        text = ""
        for section in binary.sections:
            text += f"Section {section.name}: size {section.size}\n"

        if binary.has_section('.text'):
            text_section = binary.get_section('.text')
            code = text_section.content
            md = Cs(CS_ARCH_X86, CS_MODE_64)
            text += "\nDisassembly of .text section (first 20 instructions):\n"
            for i in md.disasm(bytes(code), text_section.virtual_address):
                text += f"0x{i.address:x}:\t{i.mnemonic}\t{i.op_str}\n"
                if len(text.splitlines()) > 30:
                    break

        return text

    except Exception as e:
        return f"Error analyzing binary: {str(e)}"

@tool
def generate_website(template_dir: str, output_dir: str, context_json: str) -> str:
    """Generates a responsive website from a Jinja2 template and a JSON context."""
    try:
        context = json.loads(context_json)
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template('index.html')
        rendered_html = template.render(context)

        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, 'index.html'), 'w') as f:
            f.write(rendered_html)

        return f"Website successfully generated at {output_dir}/index.html"
    except json.JSONDecodeError:
        return "Error: Invalid JSON provided for context."
    except Exception as e:
        return f"Error generating website: {str(e)}"

@tool
def create_documentary_video(image_files_str: str, narration_text: str, output_file: str) -> str:
    """Creates a narrated documentary video from a list of images and a narration script."""
    try:
        image_files = image_files_str.split(',')
        clips = []
        for img_path in image_files:
            if os.path.exists(img_path.strip()):
                clips.append(mpe.ImageClip(img_path.strip()).set_duration(5))

        if not clips:
            return "Error: No valid image files found."

        video = mpe.concatenate_videoclips(clips, method="compose")

        tts = gTTS(text=narration_text, lang='en')
        audio_path = "temp_audio.mp3"
        tts.save(audio_path)

        audio = mpe.AudioFileClip(audio_path)
        final_video = video.set_audio(audio)
        final_video.write_videofile(output_file, fps=24, codec='libx264')

        os.remove(audio_path)

        return f"Documentary video successfully saved to {output_file}"
    except Exception as e:
        return f"Error creating video: {str(e)}"
