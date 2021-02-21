import pytest
import os
from unittest import mock
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from settings.factories import OrganizationFactory
from api.integrations.github import GithubApi

from api.models import Organization

pytestmark = pytest.mark.django_db


class TestOrganizationView:

    client = APIClient()
    github = GithubApi()

    @mock.patch.object(GithubApi, "get_organization", return_value={"login": "instruct-br", "name": "instruct", "score": 100})
    def test_should_retrieve_org_from_github_api(self, call_api):
        response = self.github.get_organization("instruct-br")

        assert call_api.called == True

        assert response["login"] == "instruct-br"
        assert response["name"] == "instruct"
        assert response["score"] == 100

    def test_should_list_orgs_saved_in_database(self):

        orgs = [
            OrganizationFactory.create(),
            OrganizationFactory.create(),
            OrganizationFactory.create(),
        ]

        response = self.client.get(reverse("organization-list"))
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == len(orgs)

    def test_should_return_organizations_ordered_by_major_score(self):
        orgs = [
            OrganizationFactory.create(score=10),
            OrganizationFactory.create(score=150),
            OrganizationFactory.create(score=5),
        ]

        max_score = max(orgs, key=lambda x:x.score)

        response = self.client.get(reverse("organization-list"))

        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0] == serialize_instance(max_score)

def serialize_instance(instance):
    return {
        "login": instance.login,
        "name": instance.name,
        "score": instance.score
    }