import io


def test_non_pdf_rejected(client, auth_headers):
    fake_file = io.BytesIO(b"this is not a pdf")
    res = client.post(
        "/analysis/",
        files={"file": ("resume.txt", fake_file, "text/plain")},
        data={"job_description": "Python developer needed"},
        headers=auth_headers,
    )
    assert res.status_code == 400
    assert "PDF" in res.json()["detail"]


def test_unauthenticated_analysis_rejected(client):
    fake_file = io.BytesIO(b"fake pdf content")
    res = client.post(
        "/analysis/",
        files={"file": ("resume.pdf", fake_file, "application/pdf")},
        data={"job_description": "Python developer needed"},
    )
    assert res.status_code == 401


def test_get_history_unauthenticated(client):
    res = client.get("/analysis/")
    assert res.status_code == 401


def test_get_history_authenticated(client, auth_headers):
    res = client.get("/analysis/", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)