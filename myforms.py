from wtforms import Form, BooleanField, StringField, TextField, validators


class myNewItem(Form):
    name = TextField('Name', [validators.Length(min=4, max=30)])
