# Project: toggle_chrome_google_translate

Google Chrome lacks a single shortcut to toggle translations. This tool automates 
the Google Translate extension using a global hotkey.

* Required Extension: 
  https://chromewebstore.google.com/detail/google-translate/aapbdbdomjkkjkaonfhkkikfgjllcleb

### Configure Chrome
* Go to chrome://settings/?search=translate in Chrome
* Turn on 'Use Google Translate'
* Make sure it works: Click the icon, press right arrow key, press ESC key. 

### How it Works
The shortcut **Ctrl + Shift + X** automates three manual steps:
1. Click the extension icon.
2. Press **Right Arrow** (to toggle).
3. Press **Escape** (to close).

### How to Use
1. Pin the Google Translate extension in Chrome.
2. Run `toggle.bat`.
3. Press **Ctrl + Shift + X** in Chrome to toggle languages instantly.