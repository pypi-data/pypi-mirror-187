import requests


def get_github_avatar(github_username: str):
    """
    Get user avatar from a specific GitHub user

    :param github_username: str with GitHub username
    :return: str with avatar link
    """
    url = f'https://api.github.com/users/{github_username}'
    response = requests.get(url)
    return response.json()['avatar_url']


if __name__ == '__main__':
    print(get_github_avatar('mauriciodoerr'))
