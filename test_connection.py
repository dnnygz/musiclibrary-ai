#!/usr/bin/env python3
"""
Script para probar la conexión con la AI API
Asegúrate de que la AI API esté corriendo en http://localhost:8000
"""

import requests
import json
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_health_check() -> bool:
    """Test health check endpoint"""
    print("1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"❌ Health check failed (HTTP {response.status_code})")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {str(e)}")
        return False

def test_describe_playlist() -> bool:
    """Test describe playlist endpoint"""
    print("\n2️⃣ Testing Describe Playlist...")
    payload = {
        "songs": [
            {
                "id": "1",
                "title": "Bohemian Rhapsody",
                "artist": "Queen",
                "album": "A Night at the Opera",
                "genre": "Rock",
                "year": 1975,
                "duration": 354
            }
        ]
    }
    try:
        response = requests.post(
            f"{BASE_URL}/describe-playlist",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            print("✅ Describe playlist passed")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"❌ Describe playlist failed (HTTP {response.status_code})")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Describe playlist failed: {str(e)}")
        return False

def test_recommend_songs() -> bool:
    """Test recommend songs endpoint"""
    print("\n3️⃣ Testing Recommend Songs...")
    payload = {
        "current_songs": [
            {
                "id": "1",
                "title": "Bohemian Rhapsody",
                "artist": "Queen",
                "genre": "Rock",
                "year": 1975,
                "duration": 354
            }
        ],
        "number_of_recommendations": 3
    }
    try:
        response = requests.post(
            f"{BASE_URL}/recommend-songs",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            print("✅ Recommend songs passed")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"❌ Recommend songs failed (HTTP {response.status_code})")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Recommend songs failed: {str(e)}")
        return False

def test_generate_playlist_name() -> bool:
    """Test generate playlist name endpoint"""
    print("\n4️⃣ Testing Generate Playlist Name...")
    payload = {
        "songs": [
            {
                "id": "1",
                "title": "Bohemian Rhapsody",
                "artist": "Queen",
                "genre": "Rock",
                "year": 1975,
                "duration": 354
            }
        ],
        "style": "creative"
    }
    try:
        response = requests.post(
            f"{BASE_URL}/generate-name",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            print("✅ Generate playlist name passed")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"❌ Generate playlist name failed (HTTP {response.status_code})")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Generate playlist name failed: {str(e)}")
        return False

def test_analyze_mood() -> bool:
    """Test analyze mood endpoint"""
    print("\n5️⃣ Testing Analyze Mood...")
    payload = {
        "songs": [
            {
                "id": "1",
                "title": "Bohemian Rhapsody",
                "artist": "Queen",
                "genre": "Rock",
                "year": 1975,
                "duration": 354
            }
        ]
    }
    try:
        response = requests.post(
            f"{BASE_URL}/analyze-mood",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            print("✅ Analyze mood passed")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"❌ Analyze mood failed (HTTP {response.status_code})")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Analyze mood failed: {str(e)}")
        return False

def test_semantic_search() -> bool:
    """Test semantic search endpoint"""
    print("\n6️⃣ Testing Semantic Search...")
    payload = {
        "query": "upbeat songs for running in the morning",
        "limit": 5
    }
    try:
        response = requests.post(
            f"{BASE_URL}/semantic-search",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            print("✅ Semantic search passed")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"❌ Semantic search failed (HTTP {response.status_code})")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Semantic search failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing MusicLibrary AI API Connection")
    print("=" * 50)
    
    results = []
    
    # Test health check first
    results.append(("Health Check", test_health_check()))
    
    # Only continue if health check passes
    if not results[0][1]:
        print("\n❌ Health check failed. Is the AI API running?")
        print(f"   Expected URL: {BASE_URL}")
        sys.exit(1)
    
    # Run other tests
    results.append(("Describe Playlist", test_describe_playlist()))
    results.append(("Recommend Songs", test_recommend_songs()))
    results.append(("Generate Playlist Name", test_generate_playlist_name()))
    results.append(("Analyze Mood", test_analyze_mood()))
    results.append(("Semantic Search", test_semantic_search()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

