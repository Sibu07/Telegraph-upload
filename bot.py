from pyrogram import Client, filters
import requests
import os

# Initialize the Pyrogram client
api_id = 11405252
api_hash = "b1a1fc3dc52ccc91781f33522255a880"
bot_token = "6302362321:AAHkHBIm4ou9oIsGLFEsMDWFLzK-yCqGDqE"

app = Client("telegraph_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Print a message when the bot starts
print("Telegraph Bot has started!")

# Define a command handler for /start
@app.on_message(filters.command(["start"]))
def start(_, message):
    message.reply("Welcome to the Telegraph Bot! Send me a photo or video to get a permanent link.")

# Define an upload function
def upload_to_telegraph(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        return "File not found."

    # Determine the file type (image or video) based on the file extension
    file_extension = os.path.splitext(file_path)[1]
    media_type = "image" if file_extension in (".jpg", ".jpeg", ".png", ".gif") else "video"

    # Prepare the files for upload
    with open(file_path, 'rb') as file:
        files = {media_type: file}

        # Make the request to upload the file
        response = requests.post("https://telegra.ph/upload", files=files)

        # Parse the response JSON
        try:
            result = response.json()
            if 'error' in result:
                return "Upload failed."
            if media_type == "image":
                media_type_link = f"https://telegra.ph{result[0]['src']}"
            else:
                media_type_link = f"https://telegra.ph{result[0]['video_src']}"
            return media_type_link
        except Exception as e:
            return "An error occurred: " + str(e)

# Define a handler for media messages
@app.on_message(filters.media)
def handle_media(_, message):
    file_path = message.download()
    media_type = "image" if file_path.endswith((".jpg", ".jpeg", ".png", ".gif")) else "video"
    link = upload_to_telegraph(file_path)
    message.reply(f"Permanent {media_type} link: {link}")
    os.remove(file_path)  # Remove the downloaded file

# Start the bot
app.run()
