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

def create_html_file():
    """Create the index.html file"""
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emoji-Text converter</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            max-width: 800px;
            width: 100%;
            animation: slideUp 0.6s ease-out;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
        }

        .header h1 {
            color: #333;
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header p {
            color: #666;
            font-size: 1.1rem;
        }

        .converter-section {
            margin-bottom: 30px;
        }

        .input-group {
            margin-bottom: 20px;
        }

        .input-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
            font-size: 1.1rem;
        }

        .input-area {
            width: 100%;
            min-height: 120px;
            padding: 15px;
            border: 2px solid #e1e8ed;
            border-radius: 12px;
            font-size: 1.1rem;
            resize: vertical;
            transition: all 0.3s ease;
            font-family: inherit;
        }

        .input-area:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .button-group {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }

        .convert-btn {
            flex: 1;
            min-width: 150px;
            padding: 15px 25px;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .btn-auto {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
        }

        .btn-to-emoji {
            background: linear-gradient(45deg, #f093fb, #f5576c);
            color: white;
        }

        .btn-to-text {
            background: linear-gradient(45deg, #4facfe, #00f2fe);
            color: white;
        }

        .convert-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }

        .convert-btn:active {
            transform: translateY(-1px);
        }

        .convert-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .result-section {
            background: #f8fafc;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #e2e8f0;
        }

        .result-section h3 {
            margin-bottom: 15px;
            color: #333;
            font-size: 1.2rem;
        }

        .result-content {
            min-height: 60px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            font-size: 1.2rem;
            line-height: 1.5;
            word-wrap: break-word;
        }

        .loading {
            display: flex;
            align-items: center;
            gap: 10px;
            color: #666;
        }

        .spinner {
            width: 20px;
            height: 20px;
            border: 2px solid #f3f3f3;
            border-top: 2px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .error {
            color: #e53e3e;
            background: #fed7d7;
            padding: 10px;
            border-radius: 8px;
            margin-top: 10px;
        }

        .success {
            color: #38a169;
            background: #c6f6d5;
            padding: 10px;
            border-radius: 8px;
            margin-top: 10px;
        }

        .examples {
            margin-top: 30px;
            padding: 20px;
            background: rgba(102, 126, 234, 0.05);
            border-radius: 12px;
        }

        .examples h3 {
            color: #333;
            margin-bottom: 15px;
        }

        .example-item {
            margin-bottom: 10px;
            padding: 8px 12px;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .example-item:hover {
            background: #667eea;
            color: white;
            transform: translateX(5px);
        }

        .status {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 15px;
            background: #4facfe;
            color: white;
            border-radius: 8px;
            font-size: 0.9rem;
            z-index: 1000;
        }

        @media (max-width: 600px) {
            .container {
                padding: 20px;
            }

            .header h1 {
                font-size: 2rem;
            }

            .button-group {
                flex-direction: column;
            }

            .convert-btn {
                min-width: auto;
            }
        }
    </style>
</head>
<body>
    <div class="status">🟢 Server Running</div>
    
    <div class="container">
        <div class="header">
            <h1>🔄 TalkiMoji</h1>
            <p>Convert text to emojis or emojis to text</p>
        </div>

        <div class="converter-section">
            <div class="input-group">
                <label for="inputText">Enter text or emojis:</label>
                <textarea 
                    id="inputText" 
                    class="input-area" 
                    placeholder="Type your text here... e.g., 'I love pizza and music' or '🍕🎵❤️'"
                ></textarea>
            </div>

            <div class="button-group">
                <button class="convert-btn btn-auto" onclick="convertAuto()">
                    🔄 Convert
                </button>
                
            </div>
        </div>

        <div class="result-section">
            <h3>Result:</h3>
            <div id="resultContent" class="result-content">
                Results will appear here...
            </div>
        </div>

        <div class="examples">
            <h3>💡 Example inputs (click to try):</h3>
            <div class="example-item" onclick="setInput('I love coffee and coding')">
                📝 "I love coffee and coding"
            </div>
            <div class="example-item" onclick="setInput('🍕🎵❤️🌟')">
                😊 "🍕🎵❤️🌟"
            </div>
            <div class="example-item" onclick="setInput('Good morning sunshine')">
                📝 "Good morning sunshine"
            </div>
            <div class="example-item" onclick="setInput('🏠🚗✈️🏖️')">
                😊 "🏠🚗✈️🏖️"
            </div>
        </div>
    </div>

    <script>
        function setInput(text) {
            document.getElementById('inputText').value = text;
        }

        function showLoading() {
            const resultContent = document.getElementById('resultContent');
            resultContent.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <span>Converting...</span>
                </div>
            `;
        }

        function showResult(result) {
            const resultContent = document.getElementById('resultContent');
            if (result.success) {
                resultContent.innerHTML = `
                    <div>${result.result}</div>
                    <div class="success">✅ Conversion successful!</div>
                `;
            } else {
                resultContent.innerHTML = `
                    <div class="error">❌ ${result.error}</div>
                `;
            }
        }

        function disableButtons() {
            const buttons = document.querySelectorAll('.convert-btn');
            buttons.forEach(btn => btn.disabled = true);
        }

        function enableButtons() {
            const buttons = document.querySelectorAll('.convert-btn');
            buttons.forEach(btn => btn.disabled = false);
        }

        async function convertAuto() {
            const inputText = document.getElementById('inputText').value.trim();
            if (!inputText) {
                alert('Please enter some text or emojis first!');
                return;
            }

            showLoading();
            disableButtons();

            try {
                const response = await fetch('/convert', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        text: inputText,
                        mode: 'auto'
                    })
                });

                const result = await response.json();
                showResult(result);
            } catch (error) {
                showResult({success: false, error: 'Network error occurred'});
            } finally {
                enableButtons();
            }
        }

        async function convertToEmoji() {
            const inputText = document.getElementById('inputText').value.trim();
            if (!inputText) {
                alert('Please enter some text first!');
                return;
            }

            showLoading();
            disableButtons();

            try {
                const response = await fetch('/convert', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        text: inputText,
                        mode: 'to_emoji'
                    })
                });

                const result = await response.json();
                showResult(result);
            } catch (error) {
                showResult({success: false, error: 'Network error occurred'});
            } finally {
                enableButtons();
            }
        }

        async function convertToText() {
            const inputText = document.getElementById('inputText').value.trim();
            if (!inputText) {
                alert('Please enter some emojis first!');
                return;
            }

            showLoading();
            disableButtons();

            try {
                const response = await fetch('/convert', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        text: inputText,
                        mode: 'to_text'
                    })
                });

                const result = await response.json();
                showResult(result);
            } catch (error) {
                showResult({success: false, error: 'Network error occurred'});
            } finally {
                enableButtons();
            }
        }

        // Allow Ctrl+Enter to trigger auto convert
        document.getElementById('inputText').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && e.ctrlKey) {
                convertAuto();
            }
        });
    </script>
</body>
</html>'''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

def run_server():
    # Create HTML file
    create_html_file()
    
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
        print("📁 HTML file created: index.html")
        print("⭐ Click on the examples to test quickly!")
        print("🔍 Check the console for API request logs")
        print("\n🛑 Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✨ Server stopped successfully!")

if __name__ == "__main__":
    run_server()