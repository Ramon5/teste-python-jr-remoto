from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.views import Response

from api import models, serializers
from api.integrations.github import GithubApi

# TODOS:
# 1 - Buscar organização pelo login através da API do Github
# 2 - Armazenar os dados atualizados da organização no banco
# 3 - Retornar corretamente os dados da organização
# 4 - Retornar os dados de organizações ordenados pelo score na listagem da API


class OrganizationViewSet(viewsets.ModelViewSet):

    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    lookup_field = "login"
    http_method_names = ["get","delete"]

    def __init__(self, *args, **kwargs):
        super(OrganizationViewSet, self).__init__(*args, **kwargs)
        self.github = GithubApi()

    def retrieve(self, request, login=None):
        payload, status_code = self._search_organization(login)

        serialized_response = {}

        if bool(payload):
            organization, _ = models.Organization.objects.update_or_create(**payload)
            serializer = self.serializer_class(organization)
            serialized_response = serializer.data

        return Response(serialized_response, status=status_code)

    def list(self, request):
        organizations = models.Organization.objects.all()

        serializer = self.serializer_class(organizations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, login):

        organization = get_object_or_404(models.Organization, login=login)

        self.perform_destroy(organization)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def _search_organization(self, login: str) -> (dict, int):
        """
            Busca a organização na api do github, se nao existir retorna 404
        """
        response = self.github.get_organization(login)
        public_members = self.github.get_organization_public_members(login)

        data = response.json()

        payload = {}

        if not data.get("message"):
            payload["login"] = data["login"]
            payload["name"] = data["name"]
            payload["score"] = public_members + data["public_repos"]

        return payload, response.status_code
