import os
import logging
import requests
import smtplib
from typing import Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from livekit.agents import function_tool, RunContext
from langchain_community.tools import DuckDuckGoSearchRun

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
