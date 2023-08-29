import requests
import sys


def download_ipa_from_appcenter(api_token, owner_name, app_name, release_id):
    print(f"Fetching metadata for {release_id} build from App Center...")

    # App Center API endpoint
    api_endpoint = f"https://api.appcenter.ms/v0.1/apps/{owner_name}/{app_name}/releases/{release_id}"

    # Set headers
    headers = {
        "accept": "application/json",
        "X-API-Token": api_token
    }

    # Fetch the release details
    response = requests.get(api_endpoint, headers=headers)
    response.raise_for_status()

    # Extract the download URL from the response
    download_url = response.json().get('download_url')

    if not download_url:
        print("Download URL not found :(")
        raise ValueError("Download URL not found!")

    print("Determining download URL succeeded.")

    # Download the .ipa file
    response = requests.get(download_url, stream=True)
    response.raise_for_status()

    total_length = int(response.headers.get('content-length'))
    downloaded = 0

    print(f"Start downloading 29CM - iOS {release_id} build from App Center...")

    with open(f"{app_name}.ipa", 'wb') as ipa_file:
        for chunk in response.iter_content(chunk_size=8192):
            ipa_file.write(chunk)
            downloaded += len(chunk)
            percentage = 100.0 * downloaded / total_length
            sys.stdout.write(f"\r{percentage:.1f}% downloaded")
            sys.stdout.flush()
    print("\nDownload complete!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py RELEASE_ID")
        sys.exit(1)

    API_TOKEN = requests.get(f"http://192.168.103.13:50/qa/personal/test_environment").json().get('API_TOKEN')
    OWNER_NAME = "29CM"
    APP_NAME = "29CM-iOS"
    RELEASE_ID = sys.argv[1]

    download_ipa_from_appcenter(API_TOKEN, OWNER_NAME, APP_NAME, RELEASE_ID)