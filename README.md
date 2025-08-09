<img width="3188" height="1202" alt="frame (3)" src="https://github.com/user-attachments/assets/517ad8e9-ad22-457d-9538-a9e62d137cd7" />


# The TalkiMOji 🎯

## Basic Details
### Team Name:Technova


### Team Members
- Team Lead: Emmanuel Biju - college of engineering MUnnar
- Member 2: Akshay Baiju - college of engineering MUnnar

### Project Description
TalkiMOji is a fun and interactive tool that instantly converts words into emojis and emojis back into words. Designed for both desktop and mobile, it makes chatting more expressive, playful, and universally understandable.

The Problem (that doesn't exist)
“People waste precious seconds typing words when they could just use emojis — and sometimes they see emojis but can’t tell what they mean.”

### The Solution (that nobody asked for)
“TalkiMOji instantly turns your boring words into expressive emojis, and your confusing emojis back into plain words — so you can speak fluent 😎🍕❤️ without ever opening the emoji keyboard.”

## Technical Details
### Technologies/Components Used
For Software:
- Languages used:Python,HTML,CSS,JavaScript
- Frameworks used:None (Vanilla implementation)
- Libraries used:Google Gemini API (generativelanguage.googleapis.com),Python requests library,Python http.server (BaseHTTPRequestHandler),Python re (Regular expressions),Python json
- Tools used:Vercel (for serverless deployment),GitHub (version control and repository hosting),Google AI Studio (for API key generation),Git (version control)

### Implementation
For Software:
Development Process:

Project Setup:

Created Python backend using http.server module for local development
Designed responsive HTML/CSS interface with gradient animations
Implemented JavaScript for client-side interactions


Core Functionality:

Built EmojiConverter class to handle API communication with Google Gemini
Implemented auto-detection using regex patterns to identify emojis vs text
Created conversion methods for bidirectional text↔emoji transformation
Added error handling and timeout management for API calls


User Interface:

Developed modern, mobile-responsive design with CSS animations
Created interactive example buttons for quick testing
Implemented loading states and success/error feedback
Added keyboard shortcuts (Ctrl+Enter) for better UX


API Integration:

Integrated Google Gemini API for intelligent text/emoji conversion
Configured proper request formatting and response parsing
Implemented retry logic and error handling for network issues


Deployment Adaptation:

Converted traditional server architecture to serverless functions for Vercel
Modified request handling from socketserver to BaseHTTPRequestHandler
Added CORS headers for cross-origin requests
Created Vercel configuration files (vercel.json, requirements.txt)


Testing & Optimization:

Tested conversion accuracy with various text inputs and emoji combinations
Optimized API call efficiency and response parsing
Validated responsive design across different screen sizes
Implemented proper error messaging for user feedback



Key Technical Decisions:

Used serverless architecture for scalability and cost-effectiveness
Implemented client-side state management without external frameworks
Chose Gemini API for its superior emoji interpretation capabilities
Designed mobile-first responsive interface for broader accessibility

# Installation
[commands]

# Run
* As of now we did't hosted the website so its running in local host 
for local host

1.Run the server:
bash : python server.py

2.Open your browser and go to http://localhost:8000

### Project Documentation
For Software:

# Screenshots (Add at least 3)


<img width="1920" height="1080" alt="Screenshot (165)" src="https://github.com/user-attachments/assets/eec28c96-d6c6-442d-8c5e-d102c4ca6030" />

*Main UI of the website*

<img width="1920" height="1080" alt="Screenshot (164)" src="https://github.com/user-attachments/assets/675af231-c412-441a-bf7a-fd72f498c5a3" />

*Emoji to text convertion*

<img width="1920" height="1080" alt="Screenshot (163)" src="https://github.com/user-attachments/assets/da03dd72-9a32-4ed7-ab5a-e0ecb0efb4a7" />

*Text to emoji convertion*

### Project Demo
# Video
https://drive.google.com/file/d/1GCQtF-BqtBXgqjirnXVcQHFu89fyjcJD/view?usp=sharing
*Working of the code where converting emoji to text and then text to image*


## Team Contributions
- Akshay Baiju:Collected datas and found ideas
- Emmanuel Biju:made those idea and datas into on web application
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--25-25?link=https%3A%2F%2Fwww.tinkerhub.org%2Fevents%2FQ2Q1TQKX6Q%2FUseless%2520Projects)



