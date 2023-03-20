curl "http://127.0.0.1:8000"
{"message":"Hello!"}

curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=64184588b4c148d792050b9f&password=secret&scope=&client_id=&client_secret='
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjc5MjIxMDg5fQ.YcKCZXfyqqQQDRmwSds0NcydBhq2PzXO-47WqCbC4Uw","token_type":"bearer"}

curl -X 'GET' \
  'http://127.0.0.1:8000/users/me/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NDE4NDU4OGI0YzE0OGQ3OTIwNTBiOWYiLCJleHAiOjE2NzkzMTUzODZ9.3iR2himf7kHY3F-wUWu_Txoj_e0CMbLsDQLQgKt7FrI'
{"username":"johndoe","email":"johndoe@example.com","full_name":"John Doe","disabled":false}⏎

curl -X 'GET' \
  'http://127.0.0.1:8000/users/me/items/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjc5MjI0NjA1fQ.WxzwsjIKj2jZ2u_6Ces2QGvqG2ItxRLGOyHlBVflRg8'
{"username":"johndoe","email":"johndoe@example.com","full_name":"John Doe","disabled":false,"hashed_password":"$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"}
