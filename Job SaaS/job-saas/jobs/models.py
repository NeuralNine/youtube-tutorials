from django.db import models
from django.contrib.auth.models import User


class LLMResult(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('ready', 'Ready')
    ]

    title = models.CharField(max_length=256)
    prompt = models.TextField()
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='pending')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='llm_results')


class JobListingResult(models.Model):
    title = models.CharField(max_length=1024)
    job_url = models.CharField(max_length=1024)
    job_type = models.CharField(max_length=1024, null=True, blank=True)
    level = models.CharField(max_length=1024, null=True, blank=True)
    summary = models.CharField(max_length=1024, null=True, blank=True)
    salary = models.CharField(max_length=1024, null=True, blank=True)
    posted = models.CharField(max_length=1024, null=True, blank=True)
    applicants = models.IntegerField(null=True, blank=True)

    llm_result = models.ForeignKey(LLMResult, on_delete=models.CASCADE, related_name='job_listing_results')


class Snapshot(models.Model):
    snapshot_id = models.CharField(max_length=256)
    ready = models.BooleanField()
    data = models.JSONField()

    llm_result = models.ForeignKey(LLMResult, on_delete=models.CASCADE, related_name='snapshots')
