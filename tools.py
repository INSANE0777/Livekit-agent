import os
import logging
import requests
import smtplib
import base64
import json
from typing import Optional, List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from livekit.agents import function_tool, RunContext
from langchain_community.tools import DuckDuckGoSearchRun
import google.generativeai as genai

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Setup Google API
def setup_google_api():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.error("GOOGLE_API_KEY must be set in .env file")
        return None
    genai.configure(api_key=api_key)
    return True

@function_tool()
async def get_weather(context: RunContext, city: str) -> str:
    """Get the weather in a given city"""
    try:
        response = requests.get(f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logger.info(f"Weather for {city}: {response.text}")
            return response.text.strip()
        else:
            logger.error(f"Failed to fetch weather for {city}")
            return f"Sorry, I couldn't fetch the weather for {city} right now."
    except Exception as e:
        logger.error(f"Error fetching weather for {city}: {e}")
        return f"Sorry, I couldn't fetch the weather for {city} right now."

@function_tool()
async def search_web(context: RunContext, query: str) -> str:
    """Search the web for information"""
    try:
        result = DuckDuckGoSearchRun().run(tool_input=query)
        logger.info(f"Search results for {query}: {result}")
        return result
    except Exception as e:
        logger.error(f"Error searching the web for {query}: {e}")
        return f"Sorry, I couldn't search the web for {query} right now."

@function_tool()
async def send_email(context: RunContext, to: str, subject: str, message: str, cc_email: Optional[str] = None) -> str:
    """
    Send an email
    Args:
        to: The email address of the recipient
        subject: The subject of the email
        message: The body of the email
        cc_email: The email address of the cc recipient (optional)
    """
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv("GMAIL_PASSWORD")

        if not gmail_user or not gmail_password:
            logger.error("GMAIL_USER and GMAIL_PASSWORD must be set")
            return "Error: GMAIL_USER and GMAIL_PASSWORD must be set"

        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to
        msg['Subject'] = subject
        recipients = [to]

        if cc_email:
            msg['Cc'] = cc_email
            recipients.append(cc_email)

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(gmail_user, gmail_password)

        text = msg.as_string()
        server.sendmail(gmail_user, recipients, text)
        server.quit()

        logger.info(f"Email sent successfully to {to}")
        return f"Email sent successfully to {to}"

    except smtplib.SMTPAuthenticationError:
        logger.error("Gmail authentication failed")
        return "Email sending failed: Authentication error. Please check your Gmail credentials."

    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred: {e}")
        return f"Email sending failed: SMTP error - {str(e)}"

    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return f"An error occurred while sending email: {str(e)}"

@function_tool()
async def generate_image(context: RunContext, prompt: str, output_file: str = "generated_image.png") -> str:
    """
    Generate an image using Google's Imagen API
    Args:
        prompt: Text description of the image to generate
        output_file: Filename to save the generated image (default: generated_image.png)
    """
    try:
        if not setup_google_api():
            return "Error: GOOGLE_API_KEY must be set in .env file"
            
        # Configure the model
        generation_config = {
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32,
        }
        
        # Use Gemini Pro Vision model for image generation
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # Check if the response contains image data
        if hasattr(response, 'candidates') and response.candidates:
            # Extract image data (base64 encoded)
            image_data = response.candidates[0].content.parts[0].text
            
            # Decode base64 image data
            image_bytes = base64.b64decode(image_data)
            
            # Save the image to a file
            with open(output_file, 'wb') as f:
                f.write(image_bytes)
                
            logger.info(f"Image generated and saved to {output_file}")
            return f"Image successfully generated and saved to {output_file}"
        else:
            logger.error("Failed to generate image: No image data in response")
            return "Sorry, I couldn't generate the image right now."
            
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return f"An error occurred while generating the image: {str(e)}"

@function_tool()
async def generate_website(context: RunContext, title: str, content: str, output_file: str = "index.html") -> str:
    """
    Generate a simple HTML website and save it to a file
    Args:
        title: The title of the website
        content: The main content of the website (can include HTML markup)
        output_file: Filename to save the generated HTML (default: index.html)
    """
    try:
        # Create a simple HTML template
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }}
        h1 {{
            color: #333;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }}
        footer {{
            margin-top: 30px;
            text-align: center;
            font-size: 0.8em;
            color: #777;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="content">
        {content}
    </div>
    <footer>
        <p>Generated by Friday AI Assistant</p>
    </footer>
</body>
</html>
"""
        
        # Write the HTML to a file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_template)
            
        logger.info(f"Website generated and saved to {output_file}")
        return f"Website successfully generated and saved to {output_file}"
        
    except Exception as e:
        logger.error(f"Error generating website: {e}")
        return f"An error occurred while generating the website: {str(e)}"