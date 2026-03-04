import requests
import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "config"))
from config import BASE_URL, RESPONSE_TIME_LIMIT_MS, REPORT_PATH

PASS = "PASS"
FAIL = "FAIL"
results = []

def log(tc_id, title, status, expected, actual, note=""):
    results.append({
        "TC ID": tc_id, "Title": title, "Status": status,
        "Expected": expected, "Actual": actual, "Note": note
    })
    icon = "✅" if status == PASS else "❌"
    print(f"{icon} [{tc_id}] {title} — {status}")

# ─── AUTH TESTS ───────────────────────────────────────────────────

def test_login_valid():
    r = requests.post(f"{BASE_URL}/auth/login",
                      json={"username": "emilys", "password": "emilyspass"})
    ok = r.status_code == 200 and "accessToken" in r.json()
    log("TC-001", "Login with valid credentials",
        PASS if ok else FAIL, "200 + accessToken",
        f"{r.status_code} | accessToken={'accessToken' in r.json()}")

def test_login_wrong_password():
    r = requests.post(f"{BASE_URL}/auth/login",
                      json={"username": "emilys", "password": "wrongpass"})
    ok = r.status_code in [400, 401]
    log("TC-002", "Login with wrong password",
        PASS if ok else FAIL, "400 or 401", str(r.status_code))

def test_login_missing_fields():
    r = requests.post(f"{BASE_URL}/auth/login", json={})
    ok = r.status_code in [400, 401, 422]
    log("TC-003", "Login with empty body",
        PASS if ok else FAIL, "400/401/422", str(r.status_code))

def test_login_wrong_username():
    import time; time.sleep(3)
    r = requests.post(f"{BASE_URL}/auth/login",
                      json={"username": "fakeuser999", "password": "fakepass"})
    ok = r.status_code in [400, 401]
    log("TC-004", "Login with non-existent username",
        PASS if ok else FAIL, "400 or 401", str(r.status_code))

def test_get_current_user():
    # Login first to get token
    r = requests.post(f"{BASE_URL}/auth/login",
                      json={"username": "emilys", "password": "emilyspass"})
    token = r.json().get("accessToken", "")
    r2 = requests.get(f"{BASE_URL}/auth/me",
                      headers={"Authorization": f"Bearer {token}"})
    ok = r2.status_code == 200 and "username" in r2.json()
    log("TC-005", "Get current user with valid token",
        PASS if ok else FAIL, "200 + username",
        f"{r2.status_code} | username={'username' in r2.json()}")

def test_get_current_user_no_token():
    r = requests.get(f"{BASE_URL}/auth/me")
    ok = r.status_code in [401, 403]
    log("TC-006", "Get current user without token",
        PASS if ok else FAIL, "401 or 403", str(r.status_code))

# ─── PRODUCT TESTS ────────────────────────────────────────────────

def test_get_products_list():
    r = requests.get(f"{BASE_URL}/products")
    data = r.json()
    products = data.get("products", [])
    ok = r.status_code == 200 and len(products) > 0
    log("TC-007", "Get all products",
        PASS if ok else FAIL, "200 + non-empty products list",
        f"{r.status_code} | count={len(products)}")

def test_get_single_product():
    r = requests.get(f"{BASE_URL}/products/1")
    ok = r.status_code == 200 and r.json().get("id") == 1
    log("TC-008", "Get single product by valid ID",
        PASS if ok else FAIL, "200 + id=1",
        f"{r.status_code} | id={r.json().get('id')}")

def test_get_nonexistent_product():
    r = requests.get(f"{BASE_URL}/products/99999")
    ok = r.status_code == 404
    log("TC-009", "Get product with invalid ID (99999)",
        PASS if ok else FAIL, "404 Not Found", str(r.status_code))

def test_product_schema():
    r = requests.get(f"{BASE_URL}/products/1")
    data = r.json()
    required = {"id", "title", "price", "category", "description"}
    missing = required - data.keys()
    ok = r.status_code == 200 and not missing
    log("TC-010", "Validate product response schema",
        PASS if ok else FAIL, f"Fields: {required}",
        f"Missing: {missing if missing else 'None'}", "Schema validation")

def test_search_products():
    import time; time.sleep(2)
    r = requests.get(f"{BASE_URL}/products/search?q=phone")
    data = r.json()
    ok = r.status_code == 200 and len(data.get("products", [])) > 0
    log("TC-011", "Search products by keyword 'phone'",
        PASS if ok else FAIL, "200 + matching results",
        f"{r.status_code} | results={len(data.get('products', []))}")

def test_filter_by_category():
    r = requests.get(f"{BASE_URL}/products/category/smartphones")
    ok = r.status_code == 200 and len(r.json().get("products", [])) > 0
    log("TC-012", "Filter products by category 'smartphones'",
        PASS if ok else FAIL, "200 + results", str(r.status_code))

def test_limit_products():
    r = requests.get(f"{BASE_URL}/products?limit=5")
    data = r.json()
    products = data.get("products", [])
    ok = r.status_code == 200 and len(products) == 5
    log("TC-013", "Get products with limit=5",
        PASS if ok else FAIL, "200 + exactly 5 products",
        f"{r.status_code} | count={len(products)}")

# ─── USER TESTS ───────────────────────────────────────────────────

def test_get_users():
    r = requests.get(f"{BASE_URL}/users")
    data = r.json()
    users = data.get("users", [])
    ok = r.status_code == 200 and len(users) > 0
    log("TC-014", "Get all users",
        PASS if ok else FAIL, "200 + non-empty users list",
        f"{r.status_code} | count={len(users)}")

def test_get_single_user():
    r = requests.get(f"{BASE_URL}/users/1")
    ok = r.status_code == 200 and r.json().get("id") == 1
    log("TC-015", "Get single user by valid ID",
        PASS if ok else FAIL, "200 + id=1",
        f"{r.status_code} | id={r.json().get('id')}")

def test_user_schema():
    r = requests.get(f"{BASE_URL}/users/1")
    data = r.json()
    required = {"id", "firstName", "lastName", "email", "age"}
    missing = required - data.keys()
    ok = r.status_code == 200 and not missing
    log("TC-016", "Validate user response schema",
        PASS if ok else FAIL, f"Fields: {required}",
        f"Missing: {missing if missing else 'None'}", "Schema validation")

# ─── PERFORMANCE & HEADERS ────────────────────────────────────────

def test_response_time():
    start = datetime.now()
    requests.get(f"{BASE_URL}/products")
    elapsed = (datetime.now() - start).total_seconds() * 1000
    ok = elapsed < RESPONSE_TIME_LIMIT_MS
    log("TC-017", f"Response time under {RESPONSE_TIME_LIMIT_MS}ms",
        PASS if ok else FAIL, f"< {RESPONSE_TIME_LIMIT_MS}ms",
        f"{elapsed:.0f}ms", "Performance check")

def test_content_type():
    r = requests.get(f"{BASE_URL}/products/1")
    ct = r.headers.get("Content-Type", "")
    ok = "application/json" in ct
    log("TC-018", "Content-Type is application/json",
        PASS if ok else FAIL, "application/json", ct)

def test_cart_schema():
    r = requests.get(f"{BASE_URL}/carts/1")
    data = r.json()
    required = {"id", "products", "total", "userId"}
    missing = required - data.keys()
    ok = r.status_code == 200 and not missing
    log("TC-019", "Validate cart response schema",
        PASS if ok else FAIL, f"Fields: {required}",
        f"Missing: {missing if missing else 'None'}")

def test_get_categories():
    r = requests.get(f"{BASE_URL}/products/categories")
    data = r.json()
    ok = r.status_code == 200 and isinstance(data, list) and len(data) > 0
    log("TC-020", "Get all product categories",
        PASS if ok else FAIL, "200 + non-empty list",
        f"{r.status_code} | count={len(data) if isinstance(data, list) else 'N/A'}")

# ─── REPORT ───────────────────────────────────────────────────────

def generate_report():
    total  = len(results)
    passed = sum(1 for r in results if r["Status"] == PASS)
    failed = total - passed
    pct    = (passed / total * 100) if total else 0
    ts     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "="*65)
    print("        API TEST EXECUTION REPORT — DummyJSON")
    print("="*65)
    print(f"  Run Time  : {ts}")
    print(f"  Total TCs : {total}")
    print(f"  Passed    : {passed}  ✅")
    print(f"  Failed    : {failed}  ❌")
    print(f"  Pass Rate : {pct:.1f}%")
    print("="*65)

    if failed:
        print("\n  FAILED TEST CASES:")
        for r in results:
            if r["Status"] == FAIL:
                print(f"  ❌ [{r['TC ID']}] {r['Title']}")
                print(f"      Expected : {r['Expected']}")
                print(f"      Actual   : {r['Actual']}")
    print("="*65 + "\n")

    os.makedirs("reports", exist_ok=True)
    report = {
        "run_timestamp": ts,
        "summary": {"total": total, "passed": passed,
                    "failed": failed, "pass_rate": f"{pct:.1f}%"},
        "results": results
    }
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)
    print(f"  📄 Report saved → {REPORT_PATH}\n")

    if failed > 0:
        sys.exit(1)

# ─── MAIN ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n🚀 Starting API Test Suite — DummyJSON API")
    print("="*65)

    tests = [
        test_login_valid, test_login_wrong_password,
        test_login_missing_fields, test_login_wrong_username,
        test_get_current_user, test_get_current_user_no_token,
        test_get_products_list, test_get_single_product,
        test_get_nonexistent_product, test_product_schema,
        test_search_products, test_filter_by_category,
        test_limit_products, test_get_users,
        test_get_single_user, test_user_schema,
        test_response_time, test_content_type,
        test_cart_schema, test_get_categories,
    ]

    import time
    for t in tests:
        try:
            t()
            time.sleep(3)
        except Exception as e:
            name = t.__name__.replace("test_", "").replace("_", " ").title()
            log("TC-ERR", name, FAIL, "No exception", str(e), "Unexpected error")

    generate_report()
