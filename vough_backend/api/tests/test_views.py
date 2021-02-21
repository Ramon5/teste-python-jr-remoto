import pytest
import os
from unittest import mock
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from django.urls import reverse

from settings.factories import OrganizationFactory
from api.integrations.github import GithubApi

from api.views import OrganizationViewSet
from api.models import Organization

pytestmark = pytest.mark.django_db


class TestOrganizationView:

    client = APIClient()
    github = GithubApi()
    factory = APIRequestFactory()

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

        request = self.factory.get('/', '', content_type='application/json')
        response = OrganizationViewSet.as_view({'get':'list'})(request)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(orgs)

