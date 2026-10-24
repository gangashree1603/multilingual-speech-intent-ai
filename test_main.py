from main import clean_path, SECRET_RE


def test_paths():
    assert clean_path("src/app.py") == "src/app.py"
    assert clean_path("../etc/passwd") is None
    assert clean_path("/abs/x.py") == "abs/x.py"
    assert clean_path("a\\..\\b") is None
    assert clean_path(".env") is None and clean_path(".env.production") is None
    assert clean_path(".env.example") == ".env.example"
    assert clean_path("node_modules/x/index.js") is None and clean_path("server/key.pem") is None


def test_secret_detection():
    assert SECRET_RE.search("token=ghp_" + "a" * 36)
    assert not SECRET_RE.search("API_KEY=your-key-here")
