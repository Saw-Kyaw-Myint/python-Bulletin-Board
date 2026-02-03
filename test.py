import os

import requests

# 1. Configuration
API_KEY = (
    "AIzaSyAb23qN_atKGGUwsp_bJbaWHx2Uoa-TMXw"  # Or use os.environ.get("GEMINI_API_KEY")
)
MODEL = "gemini-3-flash-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

# 2. Test Payload (A simple Python bug for Gemini to find)
sample_code = """
+def second_refresh():
+    try:
+        claims = get_jwt()
+        old_refresh_token = request.headers.get("X-refresh-token")
+        user_id = get_jwt_identity()
+        user = UserService.get_user(user_id)
+        user_data = auth_schema.dump(user)
+        if is_refresh_token_revoked(old_refresh_token):
+            return {"msg": "Refresh token invalid."}, 403
+        if not user:
+            return {"msg": "Invalid identity."}, 403
+        revoke_refresh_token(old_refresh_token)
+        new_access_token = create_access_token(
+            identity=str(user_id), additional_claims={"user": user_data}
+        )
+        remember_me = bool(claims.get("remember_me", False))
+        new_refresh_token = generate_and_save_refresh_token(user_id, remember_me)
+        resp = jsonify(access_token=new_access_token, refresh_token=new_refresh_token)
+        db.session.commit()
+        return resp, 200
+    except Exception as e:
+        log_handler("error", "Auth Controller : refresh =>", e)
+        db.session.rollback()
+        return jsonify({"msg": str(e)}), 500
+
"""

prompt = f"Review this Python code :\n{sample_code} and answer short line"

payload = {"contents": [{"parts": [{"text": prompt}]}]}

headers = {"Content-Type": "application/json", "x-goog-api-key": API_KEY}

# 3. Execution
print(f"🚀 Testing {MODEL}...")
try:
    response = requests.post(URL, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    print("\n✨ Gemini's Review:")
    print(data["candidates"][0]["content"]["parts"][0]["text"])

except Exception as e:
    print(f"❌ Failed: {e}")
    if "response" in locals():
        print(f"Response Body: {response.text}")
