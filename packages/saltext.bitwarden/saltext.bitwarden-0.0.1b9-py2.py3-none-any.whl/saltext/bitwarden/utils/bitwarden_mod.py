"""
Bitwarden util module
"""
import json
import logging
import os
import subprocess
import urllib.parse

import humps
import pyotp
import salt.utils.files
import salt.utils.http
import salt.utils.url
import validators

log = logging.getLogger(__name__)

# Standard bitwarden cli client location
DEFAULT_CLI_PATH = "bw"
DEFAULT_CLI_CONF_DIR = "/etc/salt/.bitwarden"
DEFAULT_VAULT_API_URL = "http://localhost:8087"

# Standard CLI arguments
cli_standard_args = [
    "--response",
    "--nointeraction",
]


# Prefix that is appended to all log entries
LOG_PREFIX = "bitwarden:"


def _get_headers():  # pylint: disable=C0116
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    return headers


def _validate_opts(opts=None, opts_list=None):  # pylint: disable=C0116
    if isinstance(opts_list, list):
        for opt in opts_list:
            if opt == "cli_path":
                if not opts.get("cli_path") or not os.path.isfile(opts["cli_path"]):
                    opts["cli_path"] = DEFAULT_CLI_PATH
            elif opt == "cli_conf_dir":
                if not opts.get("cli_conf_dir"):
                    opts["cli_conf_dir"] = DEFAULT_CLI_CONF_DIR
            elif opt == "vault_url":
                if opts.get("vault_url"):
                    if not validators.url(opts["vault_url"]):
                        log.error(
                            '%s Supplied Bitwarden vault URL "%s" is malformed',
                            LOG_PREFIX,
                            opts.get("vault_url"),
                        )
                        return {
                            "Error": f'Supplied Bitwarden vault URL "{opts.get("vault_url")}" is malformed'
                        }
                else:
                    log.error("%s No Bitwarden vault URL specified", LOG_PREFIX)
                    return {"Error": "No Bitwarden vault URL specified"}
            elif opt == "email":
                if opts.get("email"):
                    if not validators.email(opts["email"]):
                        log.error(
                            '%s Value for email "%s" is not a valid email address',
                            LOG_PREFIX,
                            opts.get("email"),
                        )
                        return {
                            "Error": f'Value for email "{opts.get("email")}" is not a valid email address'
                        }
                else:
                    log.error("%s No email address supplied", LOG_PREFIX)
                    return {"Error": "No email address supplied"}
            elif opt == "password":
                if opts.get("password"):
                    if not isinstance(opts["password"], str):
                        log.error('%s Value for "password" must be a string', LOG_PREFIX)
                        return {"Error": 'Value for "password" must be a string'}
                else:
                    log.error("%s No password supplied", LOG_PREFIX)
                    return {"Error": "No password supplied"}
            elif opt == "vault_api_url":
                if opts.get("vault_api_url"):
                    if not validators.url(opts["vault_api_url"]):
                        log.error(
                            '%s Supplied Bitwarden CLI REST API URL "%s" is malformed',
                            LOG_PREFIX,
                            opts.get("vault_api_url"),
                        )
                        return {
                            "Error": f'Supplied Bitwarden CLI REST API URL "{opts.get("vault_api_url")}" is malformed'
                        }
                else:
                    log.error("%s No Bitwarden CLI REST API URL specified", LOG_PREFIX)
                    return {"Error": "No Bitwarden CLI REST API URL specified"}
            elif opt == "public_api_url":
                if opts.get("public_api_url"):
                    if not validators.url(opts["public_api_url"]):
                        log.error(
                            '%s Supplied Bitwarden Public API URL "%s" is malformed',
                            LOG_PREFIX,
                            opts.get("public_api_url"),
                        )
                        return {
                            "Error": f'Supplied Bitwarden Public API URL "{opts.get("public_api_url")}" is malformed'
                        }
                else:
                    log.error("%s No Bitwarden Public API URL specified", LOG_PREFIX)
                    return {"Error": "No Bitwarden Public API URL specified"}
            elif opt == "client_id":
                if opts.get("client_id"):
                    client_id_list = opts.get("client_id").split(".")
                    if client_id_list[0] != "user" or not validators.uuid(client_id_list[1]):
                        log.error(
                            '%s Supplied client_id "%s" is malformed',
                            LOG_PREFIX,
                            opts.get("client_id"),
                        )
                        return {
                            "Error": f'Supplied client_id "{opts.get("client_id")}" is malformed'
                        }
                else:
                    log.error("%s No client_id specified", LOG_PREFIX)
                    return {"Error": "No client_id specified"}
            elif opt == "client_secret":
                if opts.get("client_secret"):
                    if (
                        not isinstance(opts["client_secret"], str)
                        or len(opts["client_secret"]) != 30
                    ):
                        log.error(
                            '%s Value for "client_secret" must be a 30 character string',
                            LOG_PREFIX,
                        )
                        return {"Error": 'Value for "client_secret" must be a 30 character string'}
                else:
                    log.error("%s No client_secret supplied", LOG_PREFIX)
                    return {"Error": "No client_secret supplied"}
            elif opt == "org_client_id":
                if opts.get("org_client_id"):
                    org_client_id_list = opts.get("org_client_id").split(".")
                    if org_client_id_list[0] != "organization" or not validators.uuid(
                        org_client_id_list[1]
                    ):
                        log.error(
                            '%s Supplied org_client_id "%s" is malformed',
                            LOG_PREFIX,
                            opts.get("org_client_id"),
                        )
                        return {
                            "Error": f'Supplied org_client_id "{opts.get("org_client_id")}" is malformed'
                        }
                else:
                    log.error("%s No org_client_id specified", LOG_PREFIX)
                    return {"Error": "No org_client_id specified"}
            elif opt == "org_client_secret":
                if opts.get("org_client_secret"):
                    if (
                        not isinstance(opts["org_client_secret"], str)
                        or len(opts["org_client_secret"]) != 30
                    ):
                        log.error(
                            '%s Value for "org_client_secret" must be a 30 character string',
                            LOG_PREFIX,
                        )
                        return {
                            "Error": 'Value for "org_client_secret" must be a 30 character string'
                        }
                else:
                    log.error("%s No org_client_secret supplied", LOG_PREFIX)
                    return {"Error": "No org_client_secret supplied"}
            else:
                log.error("%s Invalid configuration option specified for validation", LOG_PREFIX)
                return {"Error": "Invalid configuration option specified for validation"}

        # Everything should be good, return configuration options
        return opts

    log.error("%s Invalid configuration option specified for validation", LOG_PREFIX)
    return {"Error": "Invalid configuration option specified for validation"}


def login(opts=None):
    """
    Login to Bitwarden vault

    opts
        Dictionary containing the following keys:

        cli_path: ``None``
            The path to the bitwarden cli binary on the local system. If set to ``None``
            the module will use ``bw`` (Unix-like) or ``bw.exe`` (Windows) from the Salt
            user's `PATH`.

        cli_conf_dir: ``None``
            The path specifying a folder where the Bitwarden CLI will store configuration
            data.

        vault_url: ``https://bitwarden.com``
            The URL for the Bitwarden vault.

        email: ``None``
            The email address of the Bitwarden account to use.

        client_id: ``None``
            The OAUTH client_id

        client_secret: ``None``
            The OAUTH client_secret

    Returns ``True`` if successful or a dictionary containing an error if unsuccessful
    """
    config = _validate_opts(
        opts=opts, opts_list=["cli_path", "cli_conf_dir", "email", "client_id", "client_secret"]
    )
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}

    command = ["login", config["email"], "--apikey"]

    run = [config["cli_path"]] + command + cli_standard_args

    env = os.environ

    env["BW_CLIENTID"] = config["client_id"]
    env["BW_CLIENTSECRET"] = config["client_secret"]
    # Required due to https://github.com/bitwarden/cli/issues/381
    env["BITWARDENCLI_APPDATA_DIR"] = config["cli_conf_dir"]

    process = subprocess.Popen(run, env=env, stdout=subprocess.PIPE, universal_newlines=True)
    result = json.loads(process.communicate()[0])

    if result["success"]:
        log.debug(result["data"]["title"])
        return True
    elif "You are already logged in" in result["message"]:
        log.debug("%s %s", LOG_PREFIX, result["message"])
        return True
    else:
        log.error("%s %s", LOG_PREFIX, result["message"])
        return {"Error": humps.decamelize(result["message"])}

    return False


def logout(opts=None):
    """
    Logout of Bitwarden vault

    opts
        Dictionary containing the following keys:

        cli_path: ``None``
            The path to the bitwarden cli binary on the local system. If set to ``None``
            the module will use ``bw`` (Unix-like) or ``bw.exe`` (Windows) from the Salt
            user's ``PATH``.

        cli_conf_dir: ``None``
            The path specifying a folder where the Bitwarden CLI will store configuration
            data.

    Returns ``True`` if successful or ``False`` if unsuccessful
    """
    config = _validate_opts(opts=opts, opts_list=["cli_path", "cli_conf_dir"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}

    command = [
        "logout",
    ]

    run = [config["cli_path"]] + command + cli_standard_args

    env = os.environ

    # Required due to https://github.com/bitwarden/cli/issues/381
    env["BITWARDENCLI_APPDATA_DIR"] = config["cli_conf_dir"]

    process = subprocess.Popen(run, env=env, stdout=subprocess.PIPE, universal_newlines=True)
    result = json.loads(process.communicate()[0])

    if result["success"]:
        log.debug(result["data"]["title"])
        return True
    elif "You are not logged in" in result["message"]:
        log.debug(result["message"])
        return True

    return False


def lock(opts=None):
    """
    Lock the Bitwarden vault

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    Returns ``True`` if successful or ``False`` if unsuccessful
    """
    config = _validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    lock_url = f"{vault_api_url}/lock"
    lock_results = {}
    lock_ret = salt.utils.http.query(lock_url, method="POST", header_dict=headers, decode=True)
    # Check status code for API call
    if "error" in lock_ret:
        log.error(
            '%s API query failed for "lock", status code: %s, error %s',
            LOG_PREFIX,
            lock_ret["status"],
            lock_ret["error"],
        )
        return False
    else:
        lock_results = json.loads(lock_ret["body"])
        if lock_results.get("success"):
            return True

    return False


def unlock(opts=None):
    """
    Unlock the Bitwarden vault

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

        password: ``None``
            The master password for the Bitwarden vault.

    Returns ``True`` if successful or ``False`` if unsuccessful
    """
    config = _validate_opts(opts=opts, opts_list=["vault_api_url", "password"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    unlock_url = f"{vault_api_url}/unlock"
    unlock_data = {"password": config["password"]}
    unlock_results = {}
    unlock_ret = salt.utils.http.query(
        unlock_url, method="POST", data=json.dumps(unlock_data), header_dict=headers, decode=True
    )
    # Check status code for API call
    if "error" in unlock_ret:
        log.error(
            '%s API query failed for "unlock", status code: %s, error %s',
            LOG_PREFIX,
            unlock_ret["status"],
            unlock_ret["error"],
        )
        return False
    else:
        unlock_results = json.loads(unlock_ret["body"])
        if unlock_results.get("success"):
            return True

    return False


def get_item(opts=None, item_id=None):
    """
    Get item from Bitwarden vault

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    item_id
        The object's item_id (UUID)

    Returns a dictionary containing the item if successful or ``False`` if unsuccessful
    """
    config = _validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    if not validators.uuid(item_id):
        log.error('%s Value for "item_id" must be a UUID', LOG_PREFIX)
        return False
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    item_url = f"{vault_api_url}/object/item/{item_id}"
    item_results = {}
    item_ret = salt.utils.http.query(item_url, method="GET", header_dict=headers, decode=True)
    # Check status code for API call
    if "error" in item_ret:
        log.error(
            '%s API query failed for "get_item", status code: %s, error %s',
            LOG_PREFIX,
            item_ret["status"],
            item_ret["error"],
        )
        return False
    else:
        item_results = json.loads(item_ret["body"])
        if item_results.get("success"):
            return humps.decamelize(item_results["data"])

    return False


def sync(opts=None):
    """
    Sync Bitwarden vault

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    Returns ``True`` if successful or ``False`` if unsuccessful
    """
    config = _validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    sync_url = f"{vault_api_url}/sync"
    sync_results = {}
    sync_ret = salt.utils.http.query(sync_url, method="POST", header_dict=headers, decode=True)
    # Check status code for API call
    if "error" in sync_ret:
        log.error(
            '%s API query failed for "sync", status code: %s, error %s',
            LOG_PREFIX,
            sync_ret["status"],
            sync_ret["error"],
        )
        return False
    else:
        sync_results = json.loads(sync_ret["body"])
        if sync_results.get("success"):
            return True

    return False


def get_status(opts=None):
    """
    Get status of Bitwarden vault (using the Vault Management REST API)

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    Returns a dictionary containing the vault status if successful or ``False`` if unsuccessful
    """
    config = _validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    status_url = f"{vault_api_url}/status"
    status_results = {}
    status_ret = salt.utils.http.query(status_url, method="GET", header_dict=headers, decode=True)
    # Check status code for API call
    if "error" in status_ret:
        log.error(
            '%s API query failed for "status", status code: %s, error %s',
            LOG_PREFIX,
            status_ret["status"],
            status_ret["error"],
        )
        return False
    else:
        status_results = json.loads(status_ret["body"])
        if status_results.get("success"):
            return humps.decamelize(status_results["data"]["template"])

    return False


def get_status_cli(opts=None):
    """
    Get status of Bitwarden vault (using the `bw` CLI client)

    opts
        Dictionary containing the following keys:

        cli_path: ``None``
            The path to the bitwarden cli binary on the local system. If set to ``None``
            the module will use ``bw`` (Unix-like) or ``bw.exe`` (Windows) from the Salt
            user's `PATH`.

        cli_conf_dir: ``None``
            The path specifying a folder where the Bitwarden CLI will store configuration
            data.

    Returns a dictionary containing the vault status if successful or ``False`` if unsuccessful
    """
    config = _validate_opts(opts=opts, opts_list=["cli_path", "cli_conf_dir"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}

    command = ["status"]

    run = [config["cli_path"]] + command + cli_standard_args

    env = os.environ

    # Required due to https://github.com/bitwarden/cli/issues/381
    env["BITWARDENCLI_APPDATA_DIR"] = config["cli_conf_dir"]

    process = subprocess.Popen(run, env=env, stdout=subprocess.PIPE, universal_newlines=True)
    result = json.loads(process.communicate()[0])

    if result["success"]:
        return humps.decamelize(result["data"]["template"])

    return False


def generate_password(
    opts=None, uppercase=None, lowercase=None, numeric=None, special=None, length=None
):
    """
    Generate a passphrase

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    uppercase
        Include uppercase characters in the password (boolean)

    lowercase
        Include lowercase characters in the password (boolean)

    numeric
        Include numbers in the password (boolean)

    special
        Include special characters in the password (boolean)

    length
        Number of characters in the password (integer >= 5)

    Returns a string containing the generated password if successful or ``False`` if unsuccessful
    """
    config = _validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    params = {}
    if uppercase is not None:
        if not isinstance(uppercase, bool):
            log.error('%s Value for "uppercase" must be a boolean.', LOG_PREFIX)
            return False
        elif uppercase:
            params["uppercase"] = "true"
    if lowercase is not None:
        if not isinstance(lowercase, bool):
            log.error('%s Value for "lowercase" must be a boolean.', LOG_PREFIX)
            return False
        elif lowercase:
            params["lowercase"] = "true"
    if numeric is not None:
        if not isinstance(numeric, bool):
            log.error('%s Value for "numeric" must be a boolean.', LOG_PREFIX)
            return False
        elif numeric:
            params["number"] = "true"
    if special is not None:
        if not isinstance(special, bool):
            log.error('%s Value for "special" must be a boolean.', LOG_PREFIX)
            return False
        elif special:
            params["special"] = "true"
    if length is not None:
        if not isinstance(length, int):
            log.error('%s Value for "length" must be an integer.', LOG_PREFIX)
            return False
        elif length:
            params["length"] = str(length)
        if length < 5:
            log.error("%s Password length must be at least 5 characters.", LOG_PREFIX)
            return False
    if params:
        params = urllib.parse.urlencode(params)
        params = "?" + params
    else:
        params = ""
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    generate_url = f"{vault_api_url}/generate{params}"
    generate_results = {}
    generate_ret = salt.utils.http.query(
        generate_url, method="GET", header_dict=headers, decode=True
    )
    # Check status code for API call
    if "error" in generate_ret:
        log.error(
            '%s API query failed for "generate_password", status code: %s, error %s',
            LOG_PREFIX,
            generate_ret["status"],
            generate_ret["error"],
        )
        return False
    else:
        generate_results = json.loads(generate_ret["body"])
        if generate_results.get("success"):
            return generate_results["data"]["data"]

    return False


def generate_passphrase(
    opts=None, words=None, separator=None, capitalize=None, number=None
):  # pylint: disable=C0116
    """
    Generate a passphrase

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    words
        Number of words in the passphrase (integer >= 3)

    separator
        Separator character in the passphrase

    capitalize
        Title-case the passphrase (boolean)

    number
        Include numbers in the passphrase (boolean)

    Returns a string containing the generated passphrase if successful or ``False`` if unsuccessful
    """
    config = _validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    params = {"passphrase": "true"}
    if words is not None:
        if not isinstance(words, int):
            log.error('%s Value for "words" must be an integer.', LOG_PREFIX)
            return False
        else:
            params["words"] = str(words)
        if words < 3:
            log.error("%s Passphrase length must be at least 3 words.", LOG_PREFIX)
            return False
    if separator is not None:
        if not isinstance(separator, str):
            log.error('%s Value for "separator" must be a string.', LOG_PREFIX)
            return False
        else:
            params["separator"] = separator
        if len(separator) != 1:
            log.error("%s Separator must be a single character.", LOG_PREFIX)
            return False
    if capitalize is not None:
        if not isinstance(capitalize, bool):
            log.error('%s Value for "capitalize" must be a boolean.', LOG_PREFIX)
            return False
        elif capitalize:
            params["capitalize"] = "true"
    if number is not None:
        if not isinstance(number, bool):
            log.error('%s Value for "number" must be a boolean.', LOG_PREFIX)
            return False
        elif number:
            params["includeNumber"] = "true"
    if params:
        params = urllib.parse.urlencode(params)
        params = "?" + params
    else:
        params = ""
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    generate_url = f"{vault_api_url}/generate{params}"
    generate_results = {}
    generate_ret = salt.utils.http.query(
        generate_url, method="GET", header_dict=headers, decode=True
    )
    # Check status code for API call
    if "error" in generate_ret:
        log.error(
            '%s API query failed for "generate_passphrase", status code: %s, error %s',
            LOG_PREFIX,
            generate_ret["status"],
            generate_ret["error"],
        )
        return False
    else:
        generate_results = json.loads(generate_ret["body"])
        if generate_results.get("success"):
            return generate_results["data"]["data"]

    return False


def get_template(opts=None, template_type=None):  # pylint: disable=C0116
    """
    Get a template

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    template_type
        Type of template to retrieve. (One of: "item", "item.field", "item.login.url", "item.card",
        item.identity", item.securenote, "folder", "collection", "item-collections", "org-collection")

    profile
        Profile to use (optional)

    Returns a dictionary containing the template if successful or ``False`` if unsuccessful
    """
    config = _validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    if template_type not in (
        "item",
        "item.field",
        "item.login.url",
        "item.card",
        "item.identity",
        "item.securenote",
        "folder",
        "collection",
        "item-collections",
        "org-collection",
    ):
        log.error(
            '%s Value for "template_type" must be one of:  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s.',
            LOG_PREFIX,
            "item",
            "item.field",
            "item.login.url",
            "item.card",
            "item.identity",
            "item.securenote",
            "folder",
            "collection",
            "item-collections",
            "org-collection",
        )
        return False
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    template_url = f"{vault_api_url}/object/template/{template_type}"
    template_results = {}
    template_ret = salt.utils.http.query(
        template_url, method="GET", header_dict=headers, decode=True
    )
    # Check status code for API call
    if "error" in template_ret:
        log.error(
            '%s API query failed for "get_template", status code: %s, error %s',
            LOG_PREFIX,
            template_ret["status"],
            template_ret["error"],
        )
        return False
    else:
        template_results = json.loads(template_ret["body"])
        if template_results.get("success"):
            return humps.decamelize(template_results["data"]["template"])

    return False


def get_fingerprint(opts=None):  # pylint: disable=C0116
    """
    Display user fingerprint

    opts
        Dictionary containing the following keys:

        vault_api_url: ``http://localhost:8087``
            The URL for the Bitwarden Vault Management API.

    Returns a string containing the fingerprint if successful or ``False`` if unsuccessful
    """
    config = _validate_opts(opts=opts, opts_list=["vault_api_url"])
    if not config:
        log.error("%s Invalid configuration supplied", LOG_PREFIX)
        return {"Error": "Invalid configuration supplied"}
    elif config.get("Error"):
        log.error("%s %s", LOG_PREFIX, config["Error"])
        return {"Error": config["Error"]}
    headers = _get_headers()
    vault_api_url = config["vault_api_url"]
    fingerprint_url = f"{vault_api_url}/object/fingerprint/me"
    fingerprint_results = {}
    fingerprint_ret = salt.utils.http.query(
        fingerprint_url, method="GET", header_dict=headers, decode=True
    )
    # Check status code for API call
    if "error" in fingerprint_ret:
        log.error(
            '%s API query failed for "get_fingerprint", status code: %s, error %s',
            LOG_PREFIX,
            fingerprint_ret["status"],
            fingerprint_ret["error"],
        )
        return False
    else:
        fingerprint_results = json.loads(fingerprint_ret["body"])
        if fingerprint_results.get("success"):
            return humps.decamelize(fingerprint_results["data"]["data"])

    return False


def get_totp(seed=None):
    """
    Get the current TOTP value

    seed
        TOTP seed

    Returns a string if successful or ``False`` if unsuccessful
    """

    if seed is not None:
        if not isinstance(seed, str):
            log.error('%s Value for "seed" must be a string.', LOG_PREFIX)
            return False
    else:
        log.error('%s Value for "seed" must be a string.', LOG_PREFIX)

    totp = pyotp.TOTP(seed)

    if totp:
        return totp.now()

    return False
