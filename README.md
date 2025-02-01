# URL Cleaner

## Overview
The URL Cleaner project includes two main components:
1. **CLI Tool (Python)** - A command-line interface tool to clean and sanitize URLs.
2. **Browser Extension (JavaScript)** - A browser extension that automatically cleans URLs while browsing.

These tools are designed to remove unnecessary query parameters and tracking information from URLs to improve privacy and simplify URL sharing.

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [CLI Tool](#cli-tool)
  - [Browser Extension](#browser-extension)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- **Privacy-Focused:** Removes tracking parameters from URLs.
- **Multi-Platform:** Available as a CLI tool and a browser extension.
- **Customizable:** Ability to specify which parameters to remove.

---

## Installation

### CLI Tool (Python)
1. **Clone the repository**:
   ```bash
   git clone https://github.com/makalin/URL-Cleaner.git
   cd URL-Cleaner
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### CLI Tool
The CLI tool allows you to clean URLs directly from the command line.

#### Usage
```bash
python url-cleaner-python.py <url>
```

#### Example
```bash
python url-cleaner-python.py "https://example.com?utm_source=google&utm_medium=cpc"
```
**Output:**
```
https://example.com
```

#### Requirements
- Python 3.x
- **Required Library:** pyperclip (automatically installed via `requirements.txt`)

---

### Browser Extension
The browser extension automatically cleans URLs as you navigate the web.

#### Installation
1. Open your web browser (Chrome or any Chromium-based browser).
2. Go to `chrome://extensions/`.
3. Enable **Developer mode**.
4. Click **Load unpacked** and select the folder containing the extension files.

#### Usage
- The extension automatically cleans URLs in the background.
- No user interaction is required.

#### Customization
- Open the extension's background script or configuration file to add or remove URL parameters to be filtered.

---

## Development

### For CLI Tool
1. **Run Tests**:
   ```bash
   python url-cleaner-python.py "https://example.com?test=true"
   ```
2. **Add Custom Cleaning Rules**:
   - Update the `url-cleaner-python.py` file to customize which parameters to remove.

### For Browser Extension
1. **Load Extension**:
   - Follow the installation steps in [Browser Extension](#browser-extension).
2. **Modify Code**:
   - Make changes to `url-cleaner.js` or `extension-files.js` as needed.
   
---

## Contributing
1. **Fork the repository**.
2. **Create a new branch** (`git checkout -b feature-name`).
3. **Make your changes** and **commit them** (`git commit -m 'Add new feature'`).
4. **Push your branch** (`git push origin feature-name`).
5. **Create a Pull Request**.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact
For questions or suggestions, feel free to create an issue on the GitHub repository.

