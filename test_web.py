
import sys
import os
sys.path.append(os.getcwd())
from backend.tools import web_search

def test_web():
    print("Testing web_search for Tamil Nadu groundwater schemes...")
    res = web_search("latest groundwater schemes Tamil Nadu 2025")
    print(res)

if __name__ == "__main__":
    test_web()
