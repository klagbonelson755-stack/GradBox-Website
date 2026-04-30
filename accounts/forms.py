from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    """Registration form with student verification"""
    email = forms.EmailField(
        required=True, help_text='Required. Enter a valid email address.')
    full_name = forms.CharField(
        max_length=100, required=True, help_text='Your full name')
    phone = forms.CharField(max_length=20, required=True,
                            help_text='Contact phone number')

    # Student fields
    is_student = forms.BooleanField(label='I am a student', required=False, widget=forms.CheckboxInput(attrs={
        'class': 'student-toggle',
        'onchange': 'toggleStudentFields()'
    }))
    institution_name = forms.CharField(
        max_length=200, required=False, label='Institution Name')
    student_id = forms.CharField(
        max_length=50, required=False, label='Student ID Number')

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'phone', 'password1',
                  'password2', 'is_student', 'institution_name', 'student_id']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        is_student = cleaned_data.get('is_student')
        institution_name = cleaned_data.get('institution_name')
        student_id = cleaned_data.get('student_id')

        if is_student and not institution_name:
            self.add_error('institution_name',
                           'Institution name is required for students')
        if is_student and not student_id:
            self.add_error('student_id', 'Student ID is required for students')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Update profile
            profile = user.profile
            profile.phone = self.cleaned_data.get('phone', '')
            profile.is_student = self.cleaned_data.get('is_student', False)
            profile.institution_name = self.cleaned_data.get(
                'institution_name', '')
            profile.student_id = self.cleaned_data.get('student_id', '')
            profile.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """Update user information"""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ProfileUpdateForm(forms.ModelForm):
    """Update profile information including student status"""

    class Meta:
        model = Profile
        fields = ['phone', 'is_student', 'institution_name', 'student_id']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        is_student = cleaned_data.get('is_student')
        institution_name = cleaned_data.get('institution_name')
        student_id = cleaned_data.get('student_id')

        if is_student and not institution_name:
            self.add_error('institution_name',
                           'Institution name is required for students')
        if is_student and not student_id:
            self.add_error('student_id', 'Student ID is required for students')

        return cleaned_data
