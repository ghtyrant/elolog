from django.forms import IntegerField
from django.forms import ValidationError
from log.custom_fields.customfield import CustomField

class NumberField(IntegerField, CustomField):
  def __init__(self, *args, **kwargs):
    super(NumberField, self).__init__(*args, **kwargs)

  def convert_value(self, value):
    try:
      self.validate(value)
    except ValidationError:
      return ""

    return value

  def render(self, value):
    return "%s" % (value,)

# rendering of this is done in views.py
class EloField(NumberField):
  def __init__(self, *args, **kwargs):
    super(EloField, self).__init__(*args, **kwargs)

  def validate(self, value):
    super(EloField, self).validate(value)

    if value < 0:
      raise ValidationError("Please enter a reasonable Elo value")

  def convert_value(self, value):
    try:
      self.validate(int(value))
    except (ValueError, ValidationError):
      return "0"

    return value

  def render(self, elo_gain, elo):
    return "%d (%s)" % (elo_gain, elo)
