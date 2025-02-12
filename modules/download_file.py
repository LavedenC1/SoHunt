import requests

def download_file(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except requests.exceptions.RequestException as e:
        file.write(f"Error downloading file: {e}")
        print(f"Error downloading file: {e}")
    except IOError as e:
        file.write(f"Error downloading file: {e}")
        print(f"Error writing to file: {e}")