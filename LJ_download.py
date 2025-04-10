import requests
import re
import os
from tqdm import tqdm
import time
from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type

# Define a retry decorator
retry_decorator = retry(
    wait=wait_fixed(5),  # Wait 5 seconds between retries
    stop=stop_after_attempt(3),  # Stop after 3 attempts
    retry=retry_if_exception_type((requests.RequestException,))  # Retry on request exceptions
)

@retry_decorator
def download_file(url, destination_folder):
    # Send a GET request to the URL
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the filename from the Content-Disposition header
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            filename_match = re.findall('filename="(.+)"', content_disposition)
            if filename_match:
                filename = filename_match[0]
            else:
                filename = "downloaded_file"
        else:
            filename = "downloaded_file"

        # Define the full path to save the file
        file_path = os.path.join(destination_folder, filename)

        # Check if the file already exists
        if os.path.exists(file_path):
            print(f"File already exists: {file_path}")
            return

        # Get the total file size for the progress bar
        total_size = int(response.headers.get('content-length', 0))

        # Write the content to a temporary file with a progress bar
        temp_file_path = file_path + ".part"
        with open(temp_file_path, 'wb') as file, tqdm(
            desc=filename,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                bar.update(len(chunk))

        # Rename the temporary file to the final filename
        os.rename(temp_file_path, file_path)
        print(f"Downloaded and saved: {file_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

# Example usage
base_url = "http://59.175.109.173:8888/luojiadatas/"
start_number = 3581
end_number = 12256
destination_folder = "downloads"  # Specify the folder where files will be saved

# Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

for number in range(start_number, end_number + 1):
    url = f"{base_url}{number}/resource/1?userId=34540"
    download_file(url, destination_folder)
    time.sleep(2)  # Rate limiting: wait 2 seconds between downloads
