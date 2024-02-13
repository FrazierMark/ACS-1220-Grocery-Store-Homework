from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from grocery_app.models import GroceryStore, GroceryItem, ItemCategory
from grocery_app.extensions import db
from wtforms.validators import DataRequired, Length, URL, InputRequired

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=80, message='Must be between 5 and 180 characters.')])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=200, message='Must be between 5 and 180 characters.')])
    submit = SubmitField('Submit')
    

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=80, message='Must be between 5 and 180 characters.')])
    price = StringField('Price', validators=[DataRequired()])
    category = SelectField('Category', choices=ItemCategory.choices(), validators=[InputRequired('A category is required!'), Length(min=3, max=180, message='Must be between 5 and 180 characters.')])
    photo_url = StringField('Photo_url', validators=[InputRequired('A photo URL is required!'), URL('Please enter a valid URL.')])
    store = QuerySelectField('Store', query_factory=lambda: GroceryStore.query, allow_blank=False, get_label='title', validators=[InputRequired('A store is required!')])
    submit = SubmitField('Submit')
    
