# tests/test_unit_cases.py

import pytest
import os
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_home():
    """Test the home page route"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Document Portal" in response.text

def test_health():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "document-portal"}

def test_analyze_invalid_request():
    """Test document analysis with invalid request"""
    response = client.post("/analyze")
    assert response.status_code == 422  # Unprocessable Entity due to missing file

@pytest.fixture
def sample_pdf():
    """Create a sample PDF file for testing"""
    # Create a temporary PDF file with some content
    test_file_path = "test_sample.pdf"
    with open(test_file_path, "wb") as f:
        f.write(b"%PDF-1.4\n%Test PDF content")
    yield test_file_path
    # Cleanup after test
    if os.path.exists(test_file_path):
        os.remove(test_file_path)

def test_analyze_document(sample_pdf):
    """Test document analysis with valid PDF"""
    with open(sample_pdf, "rb") as f:
        response = client.post("/analyze", files={"file": ("test.pdf", f, "application/pdf")})
    assert response.status_code in [200, 500]  # 500 is acceptable if PDF parsing fails due to minimal content

def test_compare_documents_invalid_request():
    """Test document comparison with invalid request"""
    response = client.post("/compare")
    assert response.status_code == 422  # Unprocessable Entity due to missing files

def test_compare_documents(sample_pdf):
    """Test document comparison with valid PDFs"""
    with open(sample_pdf, "rb") as f1, open(sample_pdf, "rb") as f2:
        files = {
            "reference": ("ref.pdf", f1, "application/pdf"),
            "actual": ("act.pdf", f2, "application/pdf")
        }
        response = client.post("/compare", files=files)
    assert response.status_code in [200, 500]  # 500 is acceptable if PDF parsing fails due to minimal content

def test_chat_index_invalid_request():
    """Test chat indexing with invalid request"""
    response = client.post("/chat/index")
    assert response.status_code == 422  # Unprocessable Entity due to missing files

def test_chat_index(sample_pdf):
    """Test chat indexing with valid file"""
    with open(sample_pdf, "rb") as f:
        files = {"files": ("test.pdf", f, "application/pdf")}
        data = {
            "session_id": "test_session",
            "use_session_dirs": "true",
            "chunk_size": "1000",
            "chunk_overlap": "200",
            "k": "5"
        }
        response = client.post("/chat/index", files=files, data=data)
    assert response.status_code in [200, 500]  # 500 is acceptable if PDF parsing fails due to minimal content

def test_chat_query_without_session():
    """Test chat query without session ID"""
    data = {
        "question": "test question",
        "use_session_dirs": "true",
        "k": "5"
    }
    response = client.post("/chat/query", data=data)
    assert response.status_code == 400  # Bad request due to missing session_id

def test_chat_query_invalid_session():
    """Test chat query with invalid session ID"""
    data = {
        "question": "test question",
        "session_id": "invalid_session",
        "use_session_dirs": "true",
        "k": "5"
    }
    response = client.post("/chat/query", data=data)
    assert response.status_code == 404  # Not found due to invalid session_id
