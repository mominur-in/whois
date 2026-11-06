import re
import socket
from datetime import datetime, timezone
from flask import Flask, request, jsonify
import whois
import whoisit

# -----------------------------------------------------------------------------
# DevHubX ORG Configuration & Constants
# -----------------------------------------------------------------------------
DEVHUBX_ORG_NAME = "DevHubX ORG"
DEVHUBX_ORG_SERVICE = "DevHubX ORG Domain WHOIS & RDAP API"
DEVHUBX_ORG_VERSION = "1.0.0"
DEVHUBX_ORG_PORT = 5001

devhubx_org_app = Flask(__name__)

# Bootstrap IANA RDAP registry endpoints for DevHubX ORG
whoisit.bootstrap()

DEVHUBX_ORG_DOMAIN_REGEX = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)


# -----------------------------------------------------------------------------
# DevHubX ORG Helper Functions
# -----------------------------------------------------------------------------
def devhubx_org_serialize_dates(devhubx_org_value):
    if isinstance(devhubx_org_value, list):
        return [
            devhubx_org_item.isoformat()
            if isinstance(devhubx_org_item, datetime)
            else str(devhubx_org_item)
            for devhubx_org_item in devhubx_org_value
        ]
    if isinstance(devhubx_org_value, datetime):
        return devhubx_org_value.isoformat()
    return devhubx_org_value


def devhubx_org_clean_domain(devhubx_org_raw_domain: str) -> str:
    devhubx_org_domain = devhubx_org_raw_domain.strip().lower()
    devhubx_org_domain = re.sub(r"^https?://", "", devhubx_org_domain)
    devhubx_org_domain = devhubx_org_domain.split("/")[0].split(":")[0]
    return devhubx_org_domain


@devhubx_org_app.after_request
def devhubx_org_add_headers(devhubx_org_response):
    """Injects DevHubX ORG branding into every HTTP response header."""
    devhubx_org_response.headers["X-Powered-By"] = DEVHUBX_ORG_NAME
    devhubx_org_response.headers["X-Organization-Service"] = DEVHUBX_ORG_SERVICE
    return devhubx_org_response


@devhubx_org_app.route("/api/whois", methods=["GET"])
def devhubx_org_lookup_whois():
    devhubx_org_raw_domain = request.args.get("domain", "")
    devhubx_org_domain = devhubx_org_clean_domain(devhubx_org_raw_domain)

    if not devhubx_org_domain or not DEVHUBX_ORG_DOMAIN_REGEX.match(devhubx_org_domain):
        return jsonify({
            "OurWebsite": DEVHUBX_ORG_NAME,
            "error": "Invalid or missing domain parameter."
        }), 400

    try:
        devhubx_org_ip_address = socket.gethostbyname(devhubx_org_domain)
    except socket.gaierror:
        devhubx_org_ip_address = None

    try:
        devhubx_org_w = whois.whois(devhubx_org_domain)
        devhubx_org_whois_data = {
            "domain_name": devhubx_org_w.domain_name,
            "registrar": devhubx_org_w.registrar,
            "whois_server": devhubx_org_w.whois_server,
            "creation_date": devhubx_org_serialize_dates(devhubx_org_w.creation_date),
            "expiration_date": devhubx_org_serialize_dates(devhubx_org_w.expiration_date),
            "updated_date": devhubx_org_serialize_dates(devhubx_org_w.updated_date),
            "name_servers": devhubx_org_w.name_servers,
            "status": devhubx_org_w.status,
            "emails": devhubx_org_w.emails,
            "org": devhubx_org_w.org,
            "country": devhubx_org_w.country,
            "dnssec": devhubx_org_w.dnssec,
        }
    except Exception as devhubx_org_err:
        devhubx_org_whois_data = {
            "error": f"WHOIS lookup failed: {str(devhubx_org_err)}"
        }

    devhubx_org_rdap_data = None
    try:
        devhubx_org_rdap_res = whoisit.domain(devhubx_org_domain, follow_related=False)
        devhubx_org_rdap_data = {
            "handle": devhubx_org_rdap_res.get("handle"),
            "name": devhubx_org_rdap_res.get("name"),
            "registrar": devhubx_org_rdap_res.get("entities", {}).get("registrar"),
            "registration_date": devhubx_org_serialize_dates(
                devhubx_org_rdap_res.get("registration_date")
            ),
            "expiration_date": devhubx_org_serialize_dates(
                devhubx_org_rdap_res.get("expiration_date")
            ),
            "last_changed_date": devhubx_org_serialize_dates(
                devhubx_org_rdap_res.get("last_changed_date")
            ),
            "nameservers": devhubx_org_rdap_res.get("nameservers"),
            "status": devhubx_org_rdap_res.get("status"),
        }
    except Exception:
        devhubx_org_rdap_data = None

    return jsonify({
        "OurWebSite": DEVHUBX_ORG_NAME,
        "service": DEVHUBX_ORG_SERVICE,
        "version": DEVHUBX_ORG_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": devhubx_org_domain,
        "resolved_ip": devhubx_org_ip_address,
        "whois": devhubx_org_whois_data,
        "rdap": devhubx_org_rdap_data
    })


if __name__ == "__main__":
    devhubx_org_app.run(debug=True, port=DEVHUBX_ORG_PORT)
