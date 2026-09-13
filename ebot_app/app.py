*** Begin Patch
*** Update File: ebot_app/app.py
@@
-from flask import Flask, request, jsonify, render_template
+from flask import Flask, request, jsonify, render_template
+from flask_cors import CORS
@@
-app = Flask(__name__)
+app = Flask(__name__)
+CORS(app)
@@
 if __name__ == '__main__':
     logger.info("Starting ebot v1.0.0")
     logger.info("Dashboard available at http://localhost:5000")
     app.run(debug=True, host='0.0.0.0', port=5000)
+
+@app.before_request
+def log_request_info():
+    logger.info("Incoming request: %s %s from %s", request.method, request.path, request.remote_addr)
*** End Patch
