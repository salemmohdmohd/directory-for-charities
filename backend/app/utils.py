from flask import jsonify, url_for

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def generate_sitemap(app):
    links = ['/admin/']
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if "/admin/" not in url:
                links.append(url)

    endpoint_details = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            methods = ', '.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
            endpoint_details.append(f"<li><a href='{url}' title='Methods: {methods}'><strong>{url}</strong></a> <span style='background:#eee;border-radius:3px;padding:2px 6px;font-size:0.9em;'>{methods}</span></li>")
    links_html = "\n".join(endpoint_details)
    return f"""
        <div style='text-align: center;'>
            <h2>API Endpoints</h2>
            <p>Click any endpoint to test it. Hover to see allowed methods.</p>
            <ul style='text-align: left;list-style: none;padding:0;'>
                {links_html}
            </ul>
        </div>
    """
