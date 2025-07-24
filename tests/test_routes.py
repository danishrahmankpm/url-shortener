import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_shorten_valid_url(client):
    response = client.post('/api/shorten', json={"url": "https://example.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert "short_code" in data
    assert data["short_url"].endswith(data["short_code"])

def test_shorten_invalid_url(client):
    response = client.post('/api/shorten', json={"url": "invalid-url"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid URL"

def test_redirect_and_click_tracking(client):
    # Step 1: Shorten URL
    post_resp = client.post('/api/shorten', json={"url": "https://example.com"})
    short_code = post_resp.get_json()["short_code"]

    # Step 2: Redirect
    redirect_resp = client.get(f"/{short_code}", follow_redirects=False)
    assert redirect_resp.status_code == 302
    assert redirect_resp.headers["Location"] == "https://example.com"

    # Step 3: Stats
    stats_resp = client.get(f"/api/stats/{short_code}")
    stats = stats_resp.get_json()
    assert stats["url"] == "https://example.com"
    assert stats["clicks"] == 1
    assert "created_at" in stats

def test_redirect_invalid_code(client):
    response = client.get("/noexist123", follow_redirects=False)
    assert response.status_code == 404

def test_stats_invalid_code(client):
    response = client.get("/api/stats/noexist123")
    assert response.status_code == 404
