#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8080}"

format_json() {
  if command -v jq >/dev/null 2>&1; then
    jq .
  else
    python3 -c 'import json,sys; print(json.dumps(json.load(sys.stdin), indent=2))'
  fi
}

print_header() {
  printf '\n%s\n' "============================================================"
  printf '%s\n' "$1"
  printf '%s\n\n' "------------------------------------------------------------"
}

print_response() {
  echo "Response:"
  cat
}

print_header "Testing GET /health"
echo "Request: GET $BASE_URL/health"
curl -sS -X GET "$BASE_URL/health" | format_json
sleep 1

print_header "Testing GET /version"
echo "Request: GET $BASE_URL/version"
curl -sS -X GET "$BASE_URL/version" | format_json
sleep 1

print_header "Testing GET /env"
echo "Request: GET $BASE_URL/env"
curl -sS -X GET "$BASE_URL/env" | format_json
sleep 1

print_header "Testing POST /config"
echo "Request: POST $BASE_URL/config"
echo "Payload: {\"name\": \"database_url\", \"value\": \"postgres://example\"}"
curl -sS -X POST "$BASE_URL/config" \
  -H "Content-Type: application/json" \
  -d '{"name": "database_url", "value": "postgres://example"}' | format_json
sleep 1

print_header "Testing GET /config/database_url"
echo "Request: GET $BASE_URL/config/database_url"
curl -sS -X GET "$BASE_URL/config/database_url" | format_json
sleep 1

print_header "Testing DELETE /config/database_url"
echo "Request: DELETE $BASE_URL/config/database_url"
curl -sS -X DELETE "$BASE_URL/config/database_url" | format_json
sleep 1

printf '\n%s\n' "All tests completed."
