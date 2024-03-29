from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session,
    jsonify,
)

from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError


from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from app import create_app,db,login_manager,bcrypt
from models import User
from forms import login_form,register_form
from cryptography.fernet import Fernet
import os
import tempfile
from ansible_sdk.executors import AnsibleSubprocessJobExecutor, AnsibleSubprocessJobOptions
from example_common import run_one_stdout, run_one_events, run_many


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = create_app()
secret_key = os.getenv('MASTER_KEY', 'MASTERKEY123')

@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.html", title="Home")


@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html",
        form=form,
        text="Login",
        title="Login",
        btn_action="Login"
        )



# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        fernet = Fernet(secret_key.encode())
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data
            ansible_vault = form.ansible_vault.data
            
            newuser = User(
                username=username,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd),
                ansible_vault=fernet.encrypt(ansible_vault.encode()),
            )
    
            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")
    return render_template("auth.html",
        form=form,
        text="Create account",
        title="Register",
        btn_action="Register account"
        )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/run')
async def run_playbook():
    fernet = Fernet(secret_key.encode())
    # print(fernet.decrypt(current_user.ansible_vault))
    tf = tempfile.NamedTemporaryFile(delete=False)
    with open(tf.name, "w") as f:
        f.write(fernet.decrypt(current_user.ansible_vault).decode())

    with open(os.path.join(os.getcwd(), 'datadir', 'env', 'cmdline'), 'w') as f:
        f.write(f"--vault-password-file={tf.name}")

    executor = AnsibleSubprocessJobExecutor()
    executor_options = AnsibleSubprocessJobOptions()
    job_options = {
        'datadir': '/home/vagrant/flask_app/datadir',
        'playbook': 'pb.yml'
    }

    ret = await run_one_stdout(executor, executor_options, job_options=job_options)
    tf.close()
    os.unlink(tf.name)
    return jsonify(ret)



if __name__ == "__main__":
    app.run(debug=True)
