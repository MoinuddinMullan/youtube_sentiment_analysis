import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ml"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.preprocessing import clean_text, is_valid_comment

def test_clean_text_lowercases():
    assert clean_text("HELLO WORLD") == "hello world"

def test_clean_text_removes_urls():
    result = clean_text("Check this out https://example.com now")
    assert "http" not in result
    assert "example.com" not in result

def test_clean_text_removes_html():
    result = clean_text("<b>Bold</b> text")
    assert "<b>" not in result
    assert "bold text" in result

def test_clean_text_handles_non_string():
    result = clean_text(12345)
    assert isinstance(result, str)

def test_is_valid_comment_returns_false_for_empty():
    assert is_valid_comment("") is False
    assert is_valid_comment(None) is False
    assert is_valid_comment("a") is False

def test_is_valid_comment_returns_true_for_valid():
    assert is_valid_comment("Great video!") is True
