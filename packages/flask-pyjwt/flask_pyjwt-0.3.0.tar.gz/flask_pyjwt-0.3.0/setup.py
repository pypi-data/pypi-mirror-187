# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_pyjwt']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=1.1,<2.0',
 'PyJWT>=2.1.0,<3.0.0',
 'cryptography>=3.4.7,<4.0.0',
 'markupsafe==2.0.1',
 'python-dotenv>=0.17.1,<0.18.0']

setup_kwargs = {
    'name': 'flask-pyjwt',
    'version': '0.3.0',
    'description': 'Flask extension for creating, verifying, and requiring the presence of JWTs',
    'long_description': '###########\nFlask_PyJWT\n###########\n\nFlast_PyJWT is a flask extension for adding authentication and authorization via\nJWT tokens. Routes can be decorated to require JWT auth or refresh tokens, and can\nrequire the presence of additional claims and their values.\n\n************\nInstallation\n************\n\nFlask_PyJWT can be installed with ``pip``:\n\n.. code-block:: console\n\n    pip install Flask_PyJWT\n\nA python version of 3.8 or higher is officially supported. Other versions of Python 3.x\nmay work, but have not been tested.\n\nCurrently, only Flask 1.1.x is officially supported. Flask 2.x *may* work, but has not\nbeen tested.\n\n*************\nDocumentation\n*************\n\nDocumentation is hosted by `Read the Docs <https://readthedocs.org/>`_.\n\nYou can find documentation for Flask_PyJWT at `<https://flask-pyjwt.readthedocs.io/>`_\n\n*************\nConfiguration\n*************\n\nFlask_PyJWT\'s configuration variables are read from the Flask app\'s config and start\nwith the prefix "JWT\\_".\n\nRequired Values\n===============\n\nJWT_ISSUER\n----------\n\n(``str``): The issuer of JWTs. Usually your website/API\'s name.\n\nJWT_AUTHTYPE\n------------\n\n(``str``): The type of auth to use for your JWTs (HMACSHA256, HMACSHA512, RSA256, RSA512).\n\nAccepted Values:\n\n* HS256\n* HS512\n* RS256\n* RS512\n\nJWT_SECRET\n----------\n\n(``str`` | ``bytes``): The secret key or RSA private key to sign JWTs with.\n\nIf the ``JWT_AUTHTYPE`` is HS256 or HS512, a ``str`` is required.\nif the ``JWT_AUTHTYPE`` is RS256 or RS512, a ``bytes`` encoded RSA private key is required.\n\nOptional Values\n===============\n\nJWT_AUTHMAXAGE\n--------------\n\n(``int``): The maximum time, in seconds, that an auth JWT is considered valid.\n\nJWT_REFRESHMAXAGE\n-----------------\n(``int``): The maximum time, in seconds, that a refresh JWT is considered valid.\n\nJWT_PUBLICKEY\n-------------\n\n(``str`` | ``bytes``): The RSA public key used to verify JWTs with, if the ``JWT_AUTHTYPE``\nis set to RS256 or RS512.\n\n\n*************\nExample Usage\n*************\n\n.. code-block:: python\n\n    from Flask import flask, request\n    from Flask_PyJWT import auth_manager, current_token, require_token\n\n    app = Flask(__name__)\n    app.config["JWT_ISSUER"] = "Flask_PyJWT" # Issuer of tokens\n    app.config["JWT_AUTHTYPE"] = "HS256" # HS256, HS512, RS256, or RS512\n    app.config["JWT_SECRET"] = "SECRETKEY" # string for HS256/HS512, bytes (RSA Private Key) for RS256/RS512\n    app.config["JWT_AUTHMAXAGE"] = 3600\n    app.config["JWT_REFRESHMAXAGE"] = 604800\n\n    auth_manager = AuthManager(app)\n\n    # Create auth and refresh tokens with the auth_manager object\n    @app.route("/login", METHODS=["POST"])\n    def post_token():\n        username = request.form["username"]\n        password = request.form["password"]\n        # Some user authentication via username/password\n        if not valid_login(username, password):\n            return {"error": "Invalid login credentials"}, 401\n        # Retrieve some authorizations the user has, such as {"admin": True}\n        authorizations = get_user_authorizations(username)\n        # Create the auth and refresh tokens\n        auth_token = auth_manager.auth_token(username, authorizations)\n        refresh_token = auth_manager.refresh_token(username)\n        return {\n            "auth_token": auth_token.signed, \n            "refresh_token": refresh_token.signed\n        }, 200\n    \n    # Protect routes by requiring auth tokens\n    @app.route("/protected_route")\n    @require_token()\n    def protected_route():\n        return {"message": "You\'ve reached the protected route!"}, 200\n    \n    # Provision new auth tokens by requiring refresh tokens\n    @app.route("/refresh", method=["POST"])\n    @require_token("refresh")\n    def refresh_token_route():\n        username = current_token.sub\n        # Retrieve some authorizations the user has, such as {"admin": True}\n        authorizations = get_user_authorizations(username)\n        new_auth_token = auth_manager.auth_token(username, authorizations)\n        return {\n            "auth_token": new_auth_token.signed\n        }, 200\n    \n    # Require specific claims in auth or refresh tokens\n    # to match a route\'s rule variables\n    @app.route("/user_specific_route/<string:username>")\n    @require_token(sub="username")\n    def user_specific_route(username):\n        return {"message": f"Hello, {username}!"}, 200\n    \n    # Require arbitrary claims in auth or refresh tokens\n    @app.route("/custom_claim_route")\n    @require_token(custom_claim="Arbitrary Required Value")\n    def custom_claim_route():\n        return {"message": "You\'ve reached the custom claim route!"}, 200\n    \n    # Require authorizations to be present in an auth token\'s scope\n    @app.route("/admin_dashboard")\n    @require_token(scope={"admin": True})\n    def admin_dashboard():\n        return {"message": f"Hello admin!"}\n    \n    # Access the current token\'s information using current_token\n    @app.route("/token/info")\n    @require_token()\n    def extract_token_info():\n        return {\n            "token_type": current_token.token_type,\n            "subject": current_token.sub,\n            "scope": current_token.scope,\n            "claims": current_token.claims,\n            "is_signed": current_token.is_signed()\n            "signed_token": current_token.signed,\n        }\n\n    # Require authorization to be present in an auth token\'s scope or claims, but\n    # with the option to override those values with other claims\n    @app.route("/overridable_route/<string:username>")\n    @require_token(sub="username", override={"admin": True})\n    def overridable_route():\n        is_admin = current_token.claims.get("admin")\n        return {"message": f"Hello, {\'admin\' if is_admin else username}!"}, 200\n',
    'author': 'Carson Mullins',
    'author_email': 'septem151@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://flask-pyjwt.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
