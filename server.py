#!/usr/bin/env python3
import http.server
import socketserver
import json
import urllib.parse
import requests
import re
import threading
from datetime import datetime

# Configuration
PORT = 8000
GEMINI_API_KEY = "AIzaSyBkmE5uE-UfT--3bh_s3hHCgqu2L5_ZzL8"  # Your actual API key

class EmojiConverter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        self.headers = {'Content-Type': 'application/json'}
    
    def text_to_emoji(self, text):
        """Convert text to emojis"""
        try:
            prompt_text = (
                f"Convert the following text to appropriate emojis. "
                f"Keep the meaning intact and use relevant emojis that represent the text. "
                f"If it's a sentence, convert each meaningful word to emojis. "
                f"Only respond with emojis, no explanations: '{text}'"
            )
            
            payload = {
                "contents": [{"parts": [{"text": prompt_text}]}]
            }
            
            print(f"Making API request for text_to_emoji: {text}")
            response = requests.post(self.url, headers=self.headers, data=json.dumps(payload), timeout=30)
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"API Response: {result}")
                
                if 'candidates' in result and len(result['candidates']) > 0:
                    emoji_result = result['candidates'][0]['content']['parts'][0]['text'].strip()
                    return {"success": True, "result": emoji_result, "type": "emoji"}
                else:
                    return {"success": False, "error": "No candidates in API response"}
            else:
                error_text = response.text
                print(f"API Error: {response.status_code} - {error_text}")
                return {"success": False, "error": f"API Error {response.status_code}: {error_text}"}
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return {"success": False, "error": f"Network error: {str(e)}"}
        except Exception as e:
            print(f"General error: {e}")
            return {"success": False, "error": f"Error: {str(e)}"}
    
    def emoji_to_text(self, emoji_text):
        """Convert emojis to text"""
        try:
            prompt_text = (
                f"Convert the following emojis to meaningful text/words. "
                f"Interpret what the emojis represent and provide a clear, readable text. "
                f"Be concise and accurate: '{emoji_text}'"
            )
            
            payload = {
                "contents": [{"parts": [{"text": prompt_text}]}]
            }
            
            print(f"Making API request for emoji_to_text: {emoji_text}")
            response = requests.post(self.url, headers=self.headers, data=json.dumps(payload), timeout=30)
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"API Response: {result}")
                
                if 'candidates' in result and len(result['candidates']) > 0:
                    text_result = result['candidates'][0]['content']['parts'][0]['text'].strip()
                    return {"success": True, "result": text_result, "type": "text"}
                else:
                    return {"success": False, "error": "No candidates in API response"}
            else:
                error_text = response.text
                print(f"API Error: {response.status_code} - {error_text}")
                return {"success": False, "error": f"API Error {response.status_code}: {error_text}"}
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return {"success": False, "error": f"Network error: {str(e)}"}
        except Exception as e:
            print(f"General error: {e}")
            return {"success": False, "error": f"Error: {str(e)}"}
    
    def auto_detect_and_convert(self, input_text):
        """Auto-detect if input contains emojis or is text, then convert accordingly"""
        emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", 
            flags=re.UNICODE
        )
        
        if emoji_pattern.search(input_text):
            return self.emoji_to_text(input_text)
        else:
            return self.text_to_emoji(input_text)

# Initialize converter
converter = EmojiConverter(GEMINI_API_KEY)

class EmojiServerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('index.html', 'r', encoding='utf-8') as f:
                self.wfile.write(f.read().encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/convert':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                text = data.get('text', '').strip()
                mode = data.get('mode', 'auto')
                
                if not text:
                    result = {"success": False, "error": "No text provided"}
                elif mode == 'auto':
                    result = converter.auto_detect_and_convert(text)
                elif mode == 'to_emoji':
                    result = converter.text_to_emoji(text)
                elif mode == 'to_text':
                    result = converter.emoji_to_text(text)
                else:
                    result = {"success": False, "error": "Invalid mode"}
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_response = {"success": False, "error": f"Server error: {str(e)}"}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server():
    # Test API key first
    print("🧪 Testing Gemini API key...")
    test_result = converter.text_to_emoji("hello")
    if test_result["success"]:
        print("✅ API key is working!")
    else:
        print(f"❌ API key test failed: {test_result['error']}")
        print("🔑 Please check your API key is correct and has Gemini API access")
    
    # Start server
    with socketserver.TCPServer(("", PORT), EmojiServerHandler) as httpd:
        print("🚀 Emoji Converter Server Starting...")
        print(f"🌐 Server running at: http://localhost:{PORT}")
        print("📁 Make sure index.html file is in the same directory")
        print("⭐ Click on the examples to test quickly!")
        print("🔍 Check the console for API request logs")
        print("\n🛑 Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✨ Server stopped successfully!")

if __name__ == "__main__":
    run_server()
