from django import forms


class UploadProfileImage(forms.Form):
    """
    The form used to upload profile image for current user.
    """

    picture = forms.ImageField(max_length=300*1024)
