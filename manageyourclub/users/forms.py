from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django import forms
from users.models import CustomUser, Gender
from clubs.models import PlaceModel

class EditProfileForm(UserChangeForm):
    #Jonas
    template_name='/edit_profile'
    
    streetAddress = forms.CharField(max_length=20, label='Straße')
    houseNumber = forms.CharField(max_length=5, label='Hausnummer')
    postcode = forms.IntegerField(max_value=99999, min_value=0, label='PLZ')
    village = forms.CharField(max_length=20, label='Ort')

    class Meta:
        model = CustomUser
        fields = ('Vorname', 'Nachname', 'email', 'Geschlecht')

    def save(self, commit=True): # Author: Tobias
        """
            Findet den Benutzer mit dem übergebenen initial und 
            überschreibt dessen Daten mit den Daten aus dem Formular.
        """
        instance = super().save(commit=False) 

        return instance.editAddress(
            self.cleaned_data['streetAddress'],
            self.cleaned_data['houseNumber'],
            self.cleaned_data['postcode'],
            self.cleaned_data['village'],
        )

#https://stackoverflow.com/questions/53461410/make-user-email-unique-django/53461823
class CreateCustomUserForm(UserCreationForm):
    #Max

    #Declarierung der Benötigten Datenfelder zur Erstellung eines CustomUsers
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    Vorname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    Nachname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    Geburtstag = forms.CharField(label='Geburtstag (yyyy-mm-dd)', widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    Geschlecht = forms.ModelChoiceField(label='Geschlecht', queryset=Gender.objects.all())
    Postleitzahl = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'number'}))
    Ort = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    Straße = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    Hausnummer = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'number'}))

    #Anpassung der Passwort Feldnamen für die Anzeige im Formular  
    password1.label="Passwort"
    password2.label="Passwort bestätigen"
    class Meta:
        model = CustomUser 
        fields = ['email','password1','password2', 'Vorname', 'Nachname','Geburtstag','Geschlecht','Postleitzahl','Ort','Straße','Hausnummer']

    def save(self, commit=True): # Author: Tobias
        "speichert die vom Nutzer eingegebenen Daten"
        instance = super().save(commit=False) 

        return instance.saveAddress(
            self.cleaned_data['Straße'],
            self.cleaned_data['Hausnummer'],
            self.cleaned_data['Postleitzahl'],
            self.cleaned_data['Ort'],
        )

class CustomPasswordChangeForm(PasswordChangeForm):
    #Max

    #benötige Felder für die Änderung eines Passwortes
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))

    #Anpassung der Passwort Feldnamen für die Anzeige im Formular  
    old_password.label="altes Passwort"
    new_password1.label="neues Passwort"
    new_password2.label="neues Passwort bestätigen"
    class Meta:
        model = CustomUser
    fields = ['old_password','new_password1','new_password2']

class UserDeleteForm(forms.ModelForm):
    #Jonas
    class Meta:
        model = CustomUser
        fields = []
