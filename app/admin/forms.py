from flask_wtf import Form
from flask_wtf.file import FileRequired
from flask_wtf.file import FileField
from wtforms.fields.simple import SubmitField


class PhotoForm(Form):

    photo = FileField(
        label='Upload your file here',
        validators=[FileRequired()],
    )
    submit_button = SubmitField(
        label='Save file'
    )

