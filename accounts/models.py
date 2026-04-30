from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """Extended user profile with student information"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)

    # Student verification fields
    is_student = models.BooleanField(
        default=False, verbose_name='Are you a student?')
    institution_name = models.CharField(
        max_length=200, blank=True, verbose_name='Institution Name')
    student_id = models.CharField(
        max_length=50, blank=True, verbose_name='Student ID Number')
    is_verified = models.BooleanField(
        default=False, verbose_name='Student Verified')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def get_discount(self):
        """Return 40% discount if user is a verified student"""
        if self.is_student and self.is_verified:
            return 0.40
        return 0.00


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile automatically when a User is created"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save Profile when User is saved"""
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
