from django.forms import ModelForm, CharField, Textarea, Form, EmailField, ValidationError
from log.models import Log, LogItem, Comment, LogCustomFieldValue, LogCustomField
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class LogForm(ModelForm):

  def clean_initial_elo(self):
    data = self.cleaned_data['initial_elo']
    if data > 5000 or data < 0:
      raise ValidationError("Please enter a reasonable Elo value")
    return data

  def clean_initial_games_won(self):
    data = self.cleaned_data['initial_games_won']
    if data > 50000 or data < 0:
      raise ValidationError("Please enter a reasonable number of games")
    return data

  def clean_initial_games_lost(self):
    data = self.cleaned_data['initial_games_lost']
    if data > 50000 or data < 0:
      raise ValidationError("Please enter a reasonable number of games")
    return data

  def clean_initial_games_left(self):
    data = self.cleaned_data['initial_games_left']
    if data > 50000 or data < 0:
      raise ValidationError("Please enter a reasonable number of games")
    return data

  class Meta:
    model = Log
    fields = ('summoner_name', 'region', 'initial_elo', 'initial_games_won', 'initial_games_lost', 'initial_games_left', 'show_on_public_list')

class LogItemForm(ModelForm):
  def __init__(self, *args, **kwargs):
    from log.custom_fields.types import FieldTypes
    super(LogItemForm, self).__init__(*args, **kwargs)
    self.custom_fields = {}

    if self.instance:
      for field in self.instance.log.logcustomfield_set.all():

        # using exceptions for program flow, yikes
        try:
          # works on editing
          value = self.instance.logcustomfieldvalue_set.get(custom_field=field)
          self.fields[field.name] = field.get_form_field(required=True, initial=value.get_value())
          self.custom_fields[field.name] = field
        except ObjectDoesNotExist:
          # works on adding a new item
          self.fields[field.name] = field.get_form_field(required=True)
          self.custom_fields[field.name] = field

  def clean_elo(self):
    data = self.cleaned_data['elo']
    if data > 5000 or data < 0:
      raise ValidationError("Please enter a reasonable Elo value")
    return data

  def save(self, force_insert=False, force_update=False, commit=True):
    o = super(LogItemForm, self).save(commit=False)
    
    is_new = self.instance.id == None

    if commit:
      o.save()
    
    for field in self.custom_fields:
      # insert
      if is_new:
        value = LogCustomFieldValue(custom_field=self.custom_fields[field], log_item=self.instance)
      else:
        try:
          value = self.instance.logcustomfieldvalue_set.get(custom_field=self.custom_fields[field])
        except:
          print("Could not find LogCustomFieldValue for field '%s'" % self.custom_fields[field])
          return False
        
      print("Saving value '%s' for field '%s'" % (self.cleaned_data[field], field))
      value.set_value(self.cleaned_data[field])
      value.save()

  class Meta:
    model = LogItem
    fields = ('outcome',)

class SignupForm(ModelForm):
  class Meta:
    model = User
    fields = ('username', 'password', 'email')

class CommentForm(ModelForm):
  text = CharField(
      max_length = 1000,
      widget = Textarea,
      error_messages={'max_length': u'Please write no more than 1000 characters!'}
  )

  class Meta:
    model = Comment
    fields = ('text',)

class ResendActivationForm(Form):
  email = EmailField(required=True)
