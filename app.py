import cohere
import os
import markdown
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

class Form(FlaskForm):
    text = StringField('Enter text to search', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = Form()
    co = cohere.ClientV2('your key')

    if form.validate_on_submit():
        text = form.text.data
        response = co.chat(
            model='command-a-03-2025',
            messages=[{'role': 'user', 'content': text}]
        )
        output = response.message.content[0].text
        output = markdown.markdown(output)
        return render_template('home.html', form=form, output=output)

    return render_template('home.html', form=form, output=None)

if __name__ == "__main__":
    app.run(debug=True)
