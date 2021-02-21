import pytest

from ..models import Organization

pytestmark = pytest.mark.django_db


class TestCaseOrganizationModel:

    @pytest.fixture
    def organization(self):
        return Organization.objects.create(
            login="test",
            name="test organization",
            score=100
        )

    def test_should_return_str_name_organization_name(self, organization):
        assert organization.__str__() == "<Organization: test organization>"

    def test_if_login_field_is_primary_key(self, organization):
        field = organization._meta.get_field("login")

        assert field.primary_key == True

    def test_login_label(self, organization):
        field_label = organization._meta.get_field("login").verbose_name

        assert field_label == "login"

    def test_login_max_length(self, organization):
        max_length = organization._meta.get_field("login").max_length

        assert max_length == 255

    def test_name_label(self, organization):
        field_label = organization._meta.get_field("name").verbose_name

        assert field_label == "name"

    def test_name_max_length(self, organization):
        max_length = organization._meta.get_field("name").max_length

        assert max_length == 255

    def test_score_label(self, organization):
        field_label = organization._meta.get_field("score").verbose_name

        assert field_label == "score"