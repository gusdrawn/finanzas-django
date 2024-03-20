from django import forms
from django.test import TestCase
from ..templatetags.form_tags import field_type, input_class

class ExampleForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        fields = ('name', 'password')

class FieldTypeTests(TestCase):
    # print("\nTest field type")
    def test_field_widget_type(self):
        form = ExampleForm()
        self.assertEquals(field_type(form['name']), 'TextInput')
        self.assertEquals(field_type(form['password']), 'PasswordInput')
class InputClassTests(TestCase):
    # print("\nTest input class")
    def test_unbound_field_initial_state(self):
        form = ExampleForm()
        self.assertEquals(input_class(form['name']), 'form-control ')

    def test_valid_bound_field(self):
        # print("\nTest valid bound field")
        form = ExampleForm({'name': 'john', 'password': '123'})
        self.assertEquals(input_class(form['name']), 'form-control is-valid')
    
    def test_invalid_bound_field(self):
        # print("\nTest invalid bound field")
        form = ExampleForm({'name': '', 'password': '123'})
        self.assertEquals(input_class(form['name']), 'form-control is-invalid')