import os
from dotenv import load_dotenv

load_dotenv()

# Application (client) ID of app registration
CLIENT_ID = os.getenv("CLIENT_ID")

# Application's generated client secret: never check this into source control!
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


# AUTHORITY = "https://login.microsoftonline.com/common"  # For multi-tenant app
AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('TENANT_ID', 'common')}"

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
# The absolute URL must match the redirect URI you set
# in the app's registration in the Azure portal.

ENDPOINT = (
    "https://graph.microsoft.com/v1.0/users"  # This resource requires no admin consent
)

SCOPE = [
    "User.ReadBasic.All",
    "OnlineMeetings.ReadWrite",
    "OnlineMeetingRecording.Read.All",
    "OnlineMeetingTranscript.Read.All",
]

# Tells the Flask-session extension to store sessions in the filesystem
SESSION_TYPE = "filesystem"