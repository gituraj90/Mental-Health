from django.db import models
from django.contrib.auth.models import User  # Optional, if you want to track logged-in users

class MentalHealthSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    stress_level = models.CharField(max_length=20)
    diagnosed = models.CharField(max_length=50)
    symptoms = models.TextField()  # comma-separated values
    other_issues = models.TextField(blank=True, null=True)
    total_score = models.IntegerField(default=0)  # NEW: Score based on answers
    ai_feedback = models.TextField(blank=True, null=True)  # NEW: Gemini AI-generated feedback
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class YouTubeVideo(models.Model):
    link = models.URLField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.link
    
    
    

