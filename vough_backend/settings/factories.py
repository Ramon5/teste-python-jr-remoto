import factory
from factory import fuzzy
from factory.django import DjangoModelFactory
from api.models import Organization


class OrganizationFactory(DjangoModelFactory):

    login = factory.Sequence(lambda n: 'login%d' % n)
    name = factory.Faker("name")
    score = fuzzy.FuzzyInteger(0)

    class Meta:
        model = Organization
        django_get_or_create = ("login",)