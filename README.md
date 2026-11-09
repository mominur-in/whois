# 🌐 DevHubX ORG — Domain WHOIS & RDAP API

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-REST_API-black?logo=flask&logoColor=white)
![Website](https://img.shields.io/badge/Organization-DevHubX_ORG-orange)
![Version](https://img.shields.io/badge/Version-1.0.0-brightgreen)

A fast, lightweight REST API built with Python and Flask by **DevHubX ORG** that fetches comprehensive domain intelligence. It combines traditional **Port 43 WHOIS** lookups, modern **IANA RDAP (Registration Data Access Protocol)** data, and **IPv4 DNS resolution** into a single unified JSON response without requiring third-party API keys.

---

## ✨ Features

- **Dual Lookup Engine:** Queries both legacy WHOIS servers (`python-whois`) and modern IANA RDAP endpoints (`whoisit`).
- **Automatic Input Sanitization:** Strips protocols (`http://`, `https://`), paths, and ports automatically from raw domain inputs.
- **DNS IPv4 Resolution:** Resolves the target domain's active IPv4 address via socket lookup.
- **ISO-8601 Date Normalization:** Standardizes registration, expiration, and last-updated timestamps across registries.
- **DevHubX ORG Branding:** Injects custom organization metadata into both JSON payloads and HTTP response headers (`X-Powered-By` & `X-Organization-Service`).

---

## 📁 Project Structure

```text
.
├── src/
│   └── app.py          # Main DevHubX ORG Flask application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/mominur-in/whois.git
cd whois
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install Flask python-whois whoisit gunicorn
```

*(Optional)* Save dependencies to `requirements.txt`:

```bash
pip freeze > requirements.txt
```

### 4. Run the Application

**Development Mode:**

```bash
python src/app.py
```

The server will start on `http://127.0.0.1:5001`.

**Production Mode (with Gunicorn):**

```bash
gunicorn -w 4 -b 0.0.0.0:5001 src.app:devhubx_org_app
```

---

## 📡 API Reference

### Lookup Domain Information

```http
GET /api/whois?domain={domain_name}
```

#### Query Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `domain` | `string` | **Yes** | The domain name or URL to query (e.g., `google.com` or `https://example.org/path`). |

---

### Example Request

```bash
curl -i "[http://127.0.0.1:5001/api/whois?domain=google.com](http://127.0.0.1:5001/api/whois?domain=google.com)"
```

### Example Successful Response (`200 OK`)

**HTTP Headers:**

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Powered-By: DevHubX ORG
X-Organization-Service: DevHubX ORG Domain WHOIS & RDAP API
```

**JSON Body:**

```json
{
  "MyWebSite": "DevHubX ORG",
  "service": "DevHubX ORG Domain WHOIS & RDAP API",
  "version": "1.0.0",
  "timestamp": "2026-11-06T06:25:00.000000+00:00",
  "query": "google.com",
  "resolved_ip": "142.250.190.46",
  "whois": {
    "country": "US",
    "creation_date": "1997-09-15T04:00:00",
    "dnssec": "unsigned",
    "domain_name": ["GOOGLE.COM", "google.com"],
    "emails": [
      "abusecomplaints@markmonitor.com",
      "whoisrequest@markmonitor.com"
    ],
    "expiration_date": "2028-09-14T04:00:00",
    "name_servers": [
      "NS1.GOOGLE.COM",
      "NS2.GOOGLE.COM",
      "NS3.GOOGLE.COM",
      "NS4.GOOGLE.COM"
    ],
    "org": "Google LLC",
    "registrar": "MarkMonitor, Inc.",
    "status": [
      "clientDeleteProhibited ([https://www.icann.org/epp#clientDeleteProhibited](https://www.icann.org/epp#clientDeleteProhibited))",
      "clientTransferProhibited ([https://www.icann.org/epp#clientTransferProhibited](https://www.icann.org/epp#clientTransferProhibited))",
      "clientUpdateProhibited ([https://www.icann.org/epp#clientUpdateProhibited](https://www.icann.org/epp#clientUpdateProhibited))"
    ],
    "updated_date": "2019-09-09T15:39:04",
    "whois_server": "whois.markmonitor.com"
  },
  "rdap": {
    "expiration_date": "2028-09-14T04:00:00+00:00",
    "handle": "2138514_DOMAIN_COM-VRSN",
    "last_changed_date": "2019-09-09T15:39:04+00:00",
    "name": "GOOGLE.COM",
    "nameservers": [
      "NS1.GOOGLE.COM",
      "NS2.GOOGLE.COM",
      "NS3.GOOGLE.COM",
      "NS4.GOOGLE.COM"
    ],
    "registration_date": "1997-09-15T04:00:00+00:00",
    "registrar": ["MarkMonitor Inc."],
    "status": [
      "client delete prohibited",
      "client transfer prohibited",
      "client update prohibited"
    ]
  }
}
```

### Example Error Response (`400 Bad Request`)

Returned when the `domain` parameter is missing or fails domain regex validation:

```json
{
  "MyWebSite": "DevHubX ORG",
  "error": "Invalid or missing domain parameter."
}
```

---

## 🛠️ Built With

- **[Flask](https://flask.palletsprojects.com/)** — Micro web framework for Python
- **[python-whois](https://pypi.org/project/python-whois/)** — Traditional WHOIS client and parser
- **[whoisit](https://pypi.org/project/whoisit/)** — Python RDAP client bootstrapped with IANA registries

---

## 📄 License & Credits

Developed and maintained by **DevHubX ORG**.  
Distributed under the MIT License.
