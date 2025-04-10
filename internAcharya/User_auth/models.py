from django.db import models
from django.core.validators import RegexValidator
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class custom_user(AbstractUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=now)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",
        blank=True
    )

    def __str__(self):
        return self.username

class user_profile(models.Model):
    user = models.OneToOneField(custom_user, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex='^\d{10}$', message="Contact number must be exactly 10 digits.")],
        unique=True,
        null=True
    )

    SKILL_CHOICES = [
        ("Java", "Java"),
        ("Python", "Python"),
        ("JavaScript", "JavaScript"),
        ("HTML", "HTML"),
        ("CSS", "CSS"),
        ("SQL", "SQL"),
    ]
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    skills = models.CharField(max_length=50, choices=SKILL_CHOICES, blank=True, null=True)
    certificates = models.FileField(upload_to='certificates/', blank=True, null=True)
    area_of_interest = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')

    def __str__(self):
        return self.full_name if self.full_name else self.user.username
  


class Application(models.Model):
    STATUS_CHOICES = [
        ('Under Review', 'Under Review'),
        ('Shortlisted', 'Shortlisted'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ]
    
    user = models.ForeignKey(custom_user, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex='^\d{10}$', message="Phone number must be exactly 10 digits.")]
    )
    address = models.TextField()
    skills = models.CharField(max_length=255)
    experience = models.IntegerField()
    preferred_technology = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    
    internship_role = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    resume = models.FileField(upload_to='resumes/')
    certificates = models.FileField(upload_to='certificates/', blank=True, null=True)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Under Review')
    

    def __str__(self):
        return f"{self.full_name} - {self.internship_role}"

    @classmethod
    def can_apply(cls, user):
        return user.applications.filter(status__in=['Under Review', 'Shortlisted', 'Interview Scheduled', 'Accepted']).count() < 4

class InternshipList(models.Model):
    role = models.CharField(max_length=100, default='Software Intern')  # 👈 default added
    location = models.CharField(max_length=100, default='Remote')        # 👈 default added
    company = models.CharField(max_length=100, default='Unknown')        # 👈 default added
    work_hours = models.CharField(
        max_length=20,
        choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time')],
        default='Full-time'                                              # 👈 default added
    )
    logo = models.ImageField(upload_to='company_logos/', default='company_logos/default.png')  # 👈 default added
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.role} at {self.company}"