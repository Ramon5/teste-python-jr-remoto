from django.db import models


class Organization(models.Model):
    login = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    score = models.IntegerField()

    class Meta:
        ordering = ["-score"]
        indexes = [
            models.Index(fields=["name",]),
        ]

    def __str__(self):
        return f"<Organization: {self.name}>"
