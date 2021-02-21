import os

import requests


class GithubApi:
    API_URL = os.environ.get("GITHUB_API_URL", "https://api.github.com")
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

    def __init__(self):
        self.headers = {"Authorization": f"token {self.GITHUB_TOKEN}"}
        self.url = lambda login: f"{self.API_URL}/orgs/{login}"

    def get_organization(self, login: str):
        """Busca uma organização no Github

        :login: login da organização no Github
        """
        return requests.get(self.url(login), headers=self.headers)

    def get_organization_public_members(self, login: str) -> int:
        """Retorna todos os membros públicos de uma organização

        :login: login da organização no Github
        """
        response = requests.get(
            f"{self.url(login)}/public_members", headers=self.headers
        )

        return len(response.json())
