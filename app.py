import os
import cohere
import markdown
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-key')
co = cohere.ClientV2(os.environ['COHERE_API_KEY'])


class Form(FlaskForm):
    text = StringField('Enter text to search', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = Form()

    if form.validate_on_submit():
        text = form.text.data
        try:
            response = co.chat(
                model='command-a-03-2025',
                messages=[{'role': 'user', 'content': text}]
            )
            output = markdown.markdown(response.message.content[0].text)
        except Exception:
            app.logger.exception("Cohere request failed")
            output = "<p>Sorry, the demo is temporarily unavailable. Please try again later.</p>"
        return render_template('home.html', form=form, output=output)

    return render_template('home.html', form=form, output=None)


if __name__ == "__main__":
    app.run(debug=True)