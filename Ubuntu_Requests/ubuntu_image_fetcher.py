import os
import requests
from urllib.parse import unquote, urlparse
from pathlib import Path

def fetch_image():
    """
    Ubuntu-Inspired Image Fetcher
    Prompts user for an image URL, downloads it, and saves it to Fetched_Images directory
    """
    print("=" * 50)
    print("Ubuntu Image Fetcher: I am because we are")
    print("=" * 50)
    
    # Prompt user for URL
    url = input("Please enter the URL of the image you want to fetch: ").strip()
    
    if not url:
        print("No URL provided. Operation cancelled.")
        return
    
    try:
        # Create directory if it doesn't exist
        os.makedirs("Fetched_Images", exist_ok=True)
        print("✓ Fetched_Images directory ready")
        
        # Fetch the image with proper headers to respect the server
        headers = {
            'User-Agent': 'Ubuntu-Image-Fetcher/1.0 (Educational Project)'
        }
        
        print("Connecting to the global community...")
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        
        # Check for HTTP errors
        response.raise_for_status()
        print("✓ Connection established successfully")
        
        # Determine filename
        filename = extract_filename(url, response)
        filepath = os.path.join("Fetched_Images", filename)
        
        # Save the image
        print(f"Downloading image: {filename}")
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"✓ Image successfully saved to: {filepath}")
        print("Thank you for participating in our global community!")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {str(e)}")
        print("Please check the URL and your internet connection.")
    
    except Exception as e:
        print(f"❌ An unexpected error occurred: {str(e)}")
    
    finally:
        print("=" * 50)
        print("Ubuntu: I am because we are")
        print("=" * 50)

def extract_filename(url, response):
    """
    Extract filename from URL or generate one if not available
    """
    # Try to get filename from Content-Disposition header
    content_disposition = response.headers.get('Content-Disposition', '')
    if 'filename=' in content_disposition:
        filename = content_disposition.split('filename=')[1].strip('"\'')
        return unquote(filename)
    
    # Try to extract from URL path
    parsed_url = urlparse(url)
    path = parsed_url.path
    if path and '/' in path:
        filename = path.split('/')[-1]
        if filename and '.' in filename:
            return unquote(filename)
    
    # Generate filename if none found
    content_type = response.headers.get('Content-Type', 'image/jpeg')
    extension = content_type.split('/')[-1]
    if extension == 'jpeg':
        extension = 'jpg'
    
    return f"downloaded_image.{extension}"

if __name__ == "__main__":
    fetch_image()