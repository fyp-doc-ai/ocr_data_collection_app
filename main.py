from flask import Flask, render_template, request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google.cloud import storage
import random
import os
import uuid
from googleapiclient.http import MediaIoBaseUpload

app = Flask(__name__)
# serve the static files from static folder
app.static_folder = 'static'

# Initialize Google Drive and Cloud Storage clients
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds/credentials.json'

drive_service = build('drive', 'v3')
storage_client = storage.Client()

# Google Drive folder ID containing text files
TEXT_FILES_FOLDER_ID = '1mc-ODRIGZM45OmJ-xzLMxmxkRRt62v2_'
# Google Drive folder ID for storing images
IMAGES_FOLDER_ID = '1P1eC9xyjhURfpV9LjiYh0f2vvFs46VDZ'

@app.route('/')
def index():
    # Get list of text files in the specified folder
    query = f"'{TEXT_FILES_FOLDER_ID}' in parents and trashed=false"
    page_token = None
    files = []
    while True:
        response = drive_service.files().list(q=query, fields="nextPageToken, files(id, name)", pageToken=page_token).execute()
        cur_files = response.get('files', [])
        files += cur_files
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    # Select a random text file
    if files:
        random_file = random.choice(files)
        file_id = random_file['id']
        file_name = random_file['name']

        # Read the content of the selected file
        file = drive_service.files().get_media(fileId=file_id).execute()
        content = file.decode('utf-8')
    else:
        content = 'No text files found in the specified folder.'

    return render_template('index.html', content=content, file_name=file_name)

def create_folder_if_unique(service, file_metadata):
  
  query = f"'{file_metadata['parents'][0]}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false and name = '{file_metadata['name']}'"
  results = service.files().list(q=query, fields="files(id, name)").execute()
  folders = results.get('files', [])
  
  if folders:
    return folders[0]['id']
  else:
    folder = service.files().create(body=file_metadata, fields='id').execute()
    return folder.get('id')
  
@app.route('/upload', methods=['POST'])
def upload():
    # Get the selected text file ID from the form data
    file_name = request.form.get('file_name')

    # Get the uploaded image file
    image_file = request.files['image']

    # Create a subfolder for the selected text file in the images folder
    file_metadata = {
        'name': file_name.split('.')[0],
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [IMAGES_FOLDER_ID]
    }

    folder_id = create_folder_if_unique(drive_service, file_metadata)

    # Generate a unique filename for the image
    image_ext = image_file.filename.split('.')[-1]
    image_name = f"{uuid.uuid4()}.{image_ext}"

    # Save the image in the subfolder for the selected text file
    file_metadata = {
        'name': image_name,
        'parents': [folder_id]
    }

    # Create a MediaIoBaseUpload object
    media = MediaIoBaseUpload(
        image_file,
        mimetype=image_file.content_type,
        resumable=True
    )

    drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return 'Image uploaded successfully!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)