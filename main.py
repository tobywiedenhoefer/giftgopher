# base packages

# PyPi packages
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def splash():
    """
    Splash page for user.
    """
    return render_template('splash.html', title="Gift Gopher")


if __name__ == "__main__":
    app.run(
        debug=True
    )