from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import render, redirect
from users.models import CustomUser, Gender
from clubs.models import AddressModel, PlaceModel, ClubModel
from clubs.tests.test_views import createTestUser, logTestClientIn,createTestClub
from teams.tests.test_views import createTestTeam
from members.models import Membership


def getUser():
    #Max
    return CustomUser.objects.get(pk=1)

def createGenders():
    #Max
    Gender.objects.create(gender='männlich')
    Gender.objects.create(gender='weiblich')
    Gender.objects.create(gender='divers')

def createTestMembership(user):
    #Max
    club                            = ClubModel.objects.get(clubname='fcbayern')
    mem                             = Membership.addMember(club=club,user=user)


class TestUsersViews(TestCase):
    #Tutorial: https://www.youtube.com/watch?v=hA_VxnxCHbo

    def setUp(self):
        self.signup                 = reverse('signup')
        self.login                  = redirect('login')
        self.template_signup        = 'registration/signup.html'
    

    def test_SignUpView_get(self):
        #Autor: Max
        #Prüfung der Funktion bei Get-Request

        response                    = self.client.get(self.signup)

        #Statuscode 200 Bedeutung: "HTTP_200_OK"
        self.assertEquals(response.status_code, 200)
        #Prüfung ob korrektes Template genutzt wird
        self.assertTemplateUsed(response, self.template_signup)


    def test_SignUpView_post(self):
        #Autor: Max
        #test der Post Methode, für den Falls, das die Bedingung "if form.is_valid():" nicht erfüllt ist

        response                    = self.client.post(self.signup)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_signup)

        createGenders()

        self.login_template         = 'registration/login.html'
        response                    = self.client.post(self.signup, 
        data={"email":"manageyourclub@web.de",
        "password1":"TaxiKing",
        "password2":"TaxiKing", 
        "Vorname":"Test", 
        "Nachname":"User",
        "Geburtstag":"2000-01-01",
        "Geschlecht":"1",
        "Postleitzahl":"65199",
        "Ort":"Wiesbaden",
        "Straße":"Sesamstraße",
        "Hausnummer":"1"}, follow = True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.login_template)


    def test_showUserData_with_user_view(self):
        #Autor: Max
        #Überprüfung ob der showUserData richtig dargestellt wird
        logTestClientIn(self.client)
        self.showUserData           = reverse('userData')
        response                    = self.client.get(self.showUserData, follow = True)
        self.showUserData_template  = 'userData.html'

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.showUserData_template)


    
    def test_showUserData_without_user_view(self):
        #Autor: Max
        #Überprüfung ob showUserData nur eingeloggt möglich
        self.showUserData           = reverse('userData')
        response                    = self.client.get(self.showUserData, follow = True)
        self.login_template         = 'registration/login.html'

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.login_template)
    
    

    def test_login_view(self):
        #Autor: Max
        #Überprüfung ob der showUserData richtig dargestellt wird
        self.login                  = reverse('login')
        response                    = self.client.get(self.login)
        self.login_template         = 'registration/login.html'

        #Test Aufbau der Seite
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.login_template)
        logTestClientIn(self.client)

        #test Login
        response                    = self.client.get(self.login)
        self.assertTrue(response.context['user'].is_active)



    def test_deleteuser_view(self):
        #Autor: Max
        #Überprüfung ob der deleteUser View  richtig dargestellt wird
        self.deleteUser             = reverse('deleteuser')
        response                    = self.client.get(self.deleteUser)
        self.delete_template        = 'delete_account.html'

        logTestClientIn(self.client)
        response                    = self.client.get(self.deleteUser )

        #Test Aufbau der Seite
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.delete_template)

    def test_deleteuser_without_user_view(self):
        #Autor: Max
        #Überprüfung ob der deleteUser View  richtig dargestellt wird
        self.deleteUser             = reverse('deleteuser')
        response                    = self.client.get(self.deleteUser)
        self.login_template         = 'registration/login.html'

        response                    = self.client.get(self.deleteUser, follow=True )

        #Test Aufbau der Seite
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.login_template)

    def test_ActivateAccount_view(self):
        #Autor: Max
        #Überprüfung ob der ActivateAccount bei falschem Token richtig dargestellt wird/ richtiger Token wird über Frontend Tests abgedeckt
        context = {
            "uidb64":"mud", 
            "token":"trash",
        }
        self.activate               = reverse('activate', kwargs=context)
        response                    = self.client.get(self.activate, follow = True)
        self.login_template         = 'registration/login.html'

        #Test Aufbau der Seite
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.login_template)


    def test_edit_profile_view_not_logged_in(self):
        #Autor: Max
        #Seite Profil Ändern nur Aufrufbar, wenn eingeloggt
        self.edit_profile           = reverse('edit_profile')
        response                    = self.client.get(self.edit_profile, follow = True)
        self.login_template         = 'registration/login.html'

        #Test Aufbau der Seite
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.login_template)

    
    def test_edit_profile_view_logged_in_no_Data_change(self):
        #Autor: Max
        #Seite Profil Ändern nur Aufrufbar, wenn eingeloggt
        self.edit_profile           = reverse('edit_profile')
        logTestClientIn(self.client)
        response                    = self.client.get(self.edit_profile, follow = True)
        self.edit_profile_template         = 'edit_profile.html'
        self.home_template                 = 'home.hmtl'

        #Test Aufbau der Seite
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.edit_profile_template)



    def test_edit_profile_view_logged_in_no_Data_change(self):
        #Autor: Max
        #Test änderung von Daten

        self.edit_profile                  = reverse('edit_profile')
        self.edit_profile_template         = 'edit_profile.html'
        self.home_template                 = 'home.html'

        logTestClientIn(self.client)
        createTestClub()
        createTestMembership(getUser())

        response                    = self.client.post(self.edit_profile, 
        data={"email":"testuser@email.de",
        "Vorname":"Test", 
        "Nachname":"User",
        "Geschlecht":"1",
        "postcode":"12345",
        "village":"München",
        "streetAddress":"Teststraße",
        "houseNumber":"95b"}, follow = True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.home_template)