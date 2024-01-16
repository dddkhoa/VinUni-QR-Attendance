import datetime
import json

from flask import request, render_template, session, url_for, jsonify
from pylti1p3.contrib.flask import (
    FlaskOIDCLogin,
    FlaskMessageLaunch,
    FlaskRequest,
    FlaskCacheDataStorage,
)
from pylti1p3.deep_link_resource import DeepLinkResource
from pylti1p3.exception import LtiException
from pylti1p3.grade import Grade
from pylti1p3.lineitem import LineItem
from pylti1p3.registration import Registration
from werkzeug.exceptions import Forbidden


from main import app, cache
from main.libs.utils import get_lti_config
from main.models.lti_config import LTIConfig


class ExtendedFlaskMessageLaunch(FlaskMessageLaunch):
    def validate_nonce(self):
        """
        Probably it is bug on "https://lti-ri.imsglobal.org":
        site passes invalid "nonce" value during deep links launch.
        Because of this in case of iss == http://imsglobal.org just skip nonce validation.
        """
        iss = self.get_iss()
        deep_link_launch = self.is_deep_link_launch()

        if iss == "http://imsglobal.org" and deep_link_launch:
            return self
        return super(ExtendedFlaskMessageLaunch, self).validate_nonce()

    def validate_deployment(self):
        iss = self._get_iss()
        deployment_id = self._get_deployment_id()
        tool_conf = get_lti_config(session["iss"], session["client_id"])

        # Find deployment.
        deployment = self._tool_config.find_deployment(iss, deployment_id)
        if deployment_id in tool_conf._config[iss][0]["deployment_ids"][0]:
            deployment = True
        if not deployment:
            raise LtiException("Unable to find deployment")

        return self


def get_launch_data_storage():
    return FlaskCacheDataStorage(cache)


@app.route("/login/", methods=["GET", "POST"])
def login():
    session["iss"] = request.values.get("iss")
    session["client_id"] = request.values.get("client_id")

    tool_conf = get_lti_config(session["iss"], session["client_id"])

    launch_data_storage = get_launch_data_storage()

    flask_request = FlaskRequest()

    target_link_uri = flask_request.get_param("target_link_uri")
    if not target_link_uri:
        raise Exception('Missing "target_link_uri" param')

    oidc_login = FlaskOIDCLogin(
        flask_request, tool_conf, launch_data_storage=launch_data_storage
    )
    return oidc_login.enable_check_cookies(
        main_msg="Your browser prohibits saving cookies in an iframe.",
        click_msg="Click here to open the application in a new tab.",
    ).redirect(target_link_uri)


@app.route("/launch/", methods=["POST"])
def launch():
    tool_conf = get_lti_config(session["iss"], session["client_id"])

    flask_request = FlaskRequest()
    launch_data_storage = get_launch_data_storage()
    message_launch = ExtendedFlaskMessageLaunch(
        flask_request, tool_conf, launch_data_storage=launch_data_storage
    )
    message_launch_data = message_launch.get_launch_data()

    session["is_deep_link_launch"] = message_launch.is_deep_link_launch()
    session["launch_id"] = message_launch.get_launch_id()
    session["launch_data"] = message_launch_data
    session["curr_user_name"] = message_launch_data.get('name', '')
    session["error"] = False

    return render_template("index.html", **session)


@app.route('/api/score/<launch_id>/<earned_score>/', methods=['POST'])
def score(launch_id, earned_score):
    tool_conf = get_lti_config(session["iss"], session["client_id"])
    flask_request = FlaskRequest()
    launch_data_storage = get_launch_data_storage()
    message_launch = FlaskMessageLaunch.from_cache(launch_id, flask_request, tool_conf,
                                                   launch_data_storage=launch_data_storage)

    resource_link_id = message_launch.get_launch_data() \
        .get('https://purl.imsglobal.org/spec/lti/claim/resource_link', {}).get('id')

    if not message_launch.has_ags():
        raise Forbidden("Don't have grades!")

    sub = message_launch.get_launch_data().get('sub')
    timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
    earned_score = int(earned_score)

    grades = message_launch.get_ags()
    sc = Grade()
    sc.set_score_given(earned_score) \
        .set_score_maximum(100) \
        .set_timestamp(timestamp) \
        .set_activity_progress('Completed') \
        .set_grading_progress('FullyGraded') \
        .set_user_id(sub)

    sc_line_item = LineItem()
    sc_line_item.set_tag('score') \
        .set_score_maximum(100) \
        .set_label('Score')
    if resource_link_id:
        sc_line_item.set_resource_id(resource_link_id)

    result = grades.put_grade(sc, sc_line_item)

    return jsonify({'success': True, 'result': result.get('body')})


@app.route('/jwks/', methods=['GET'])
def get_jwks():
    tool_conf = get_lti_config(session["iss"], session["client_id"])
    return jsonify({'keys': tool_conf.get_jwks()})


@app.route("/config/<key_id>/json", methods=["GET"])
def config_json(key_id):
    title = "VinUni QR Attendance LTI"

    public_jwk = LTIConfig.query.filter_by(id=key_id).first()
    public_jwk = json.loads(public_jwk.public_jwk)

    target_link_uri = url_for("launch", _external=True)
    oidc_initiation_url = url_for("login", _external=True)

    config = {
        "title": title,
        "scopes": [],
        "extensions": [
            {
                "platform": "canvas.instructure.com",
                "settings": {
                    "platform": "canvas.instructure.com",
                    "placements": [
                        {
                            "placement": "course_navigation",
                            "visibility": "admins",
                            "default": "disabled",
                            "message_type": "LtiResourceLinkRequest",
                            "target_link_uri": target_link_uri,
                        }
                    ],
                },
                "privacy_level": "public",
            }
        ],
        "public_jwk": public_jwk,
        # "description": description,
        "custom_fields": {
            "canvas_user_id": "$Canvas.user.id",
            "canvas_course_id": "$Canvas.course.id",
        },
        "target_link_uri": target_link_uri,
        "oidc_initiation_url": oidc_initiation_url,
    }

    return jsonify(config)
