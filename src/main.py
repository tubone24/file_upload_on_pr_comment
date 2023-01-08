import base64

import requests


GITHUB_API_URL = 'https://api.github.com'
AUTHOR_NAME = 'github-actions[bot]'
AUTHOR_EMAIL = 'github-actions[bot]@users.noreply.github.com'


def _get_github_image_url(self, filename):
    return (
        f'https://github.com/{os.environ["GITHUB_REPOSITORY"]}/raw'
        f'/{os.environ["BRANCH_NAME"]}/file-uploader/{filename}'
    )

def _upload_file(self, filename, file_data):
    url = (
        f'{GITHUB_API_URL}/repos/{os.environ["GITHUB_REPOSITORY"]}'
        f'/contents/file-uploader/{filename}'
    )
    data = {
        'message': (
            '[file upload] Added file for '
            f'PR #{os.environ["GITHUB_PULL_REQUEST_NUMBER"]}'
        ),
        'content': base64.b64encode(file_data).decode("utf-8"),
        'branch': os.environ["BRANCH_NAME"],
        'author': {
            'name': AUTHOR_NAME,
            'email': AUTHOR_EMAIL
        },
        'committer': {
            'name': AUTHOR_NAME,
            'email': AUTHOR_EMAIL
        }
    }

    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'authorization': f'Bearer {os.environ["GITHUB_TOKEN"]}'
    }

    response = requests.put(
        url,
        headers=headers,
        json=data
    )

    if response.status_code in [200, 201]:
        link = self._get_github_image_url(filename)
        print_message(f'Image "{filename}" Uploaded to "{link}"')
        return link
    else:
        print("error")
        return None

def main():
    filename = os.environ["FILE_NAME"]
    with open(os.environ["FILE_PATH"], "rb") as f:
        _upload_file(filename, f.read())
    