import json
import os
import re
import uuid

from flask import Flask, Response, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["TEMPLATES_FOLDER"] = "/app/templates/"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_template():
    message = request.files["template"]
    fields_data = request.form["fields"]
    fields = json.loads(fields_data)

    template_id = str(uuid.uuid4())
    template_path = os.path.join(
        app.config["TEMPLATES_FOLDER"], secure_filename(template_id + ".html")
    )
    tmp_path = os.path.join(
        app.config["TEMPLATES_FOLDER"], str(uuid.uuid4())
    )
    message.save(tmp_path)

    # Prevent any injections
    jinja_objects = re.findall(r"{{(.*?)}}", open(tmp_path).read())
    for obj in jinja_objects:
        if not re.match(r"^[a-z ]+$", obj):
            # An oopsie whoopsie happened
            return Response(
                f"Upload failed for {tmp_path}. Injection detected.", status=400
            )

    # If file is injection-free, save it
    os.rename(tmp_path, template_path)
    with open(
        os.path.join(app.config["TEMPLATES_FOLDER"], f"{template_id}_form.html"), "w"
    ) as f:
        f.write(
            render_template(
                "form_template.html", fields=fields, template_id=template_id
            )
        )

    return redirect(url_for("render_form", template_id=template_id))

@app.route("/form/<template_id>", methods=["GET", "POST"])
def render_form(template_id):
    # On render
    if request.method == "POST":
        # Render the Jinja template with the provided data
        template = secure_filename(template_id + ".html")
        # Prevent hackers
        app.jinja_env.globals = {}
        # Set the parameters as globals
        for var_name, var_value in request.form.items():
            app.jinja_env.globals[var_name] = var_value
        # Render the template
        return render_template(template)
    # User just wants to GET
    return render_template(f"{template_id}_form.html", template_id=template_id)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
