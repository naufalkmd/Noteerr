# 🚀 Deployment Guide for Noteerr

This guide covers multiple deployment options for distributing **Noteerr**.

## 📦 Option 1: PyPI (Recommended for Public Release)

PyPI (Python Package Index) is the standard way to distribute Python packages.

### Prerequisites

```bash
pip install build twine
```

### Steps

1. **Build the package:**

```bash
python -m build
```

This creates:
- `dist/noteerr-1.0.0.tar.gz` (source distribution)
- `dist/noteerr-1.0.0-py3-none-any.whl` (wheel distribution)

2. **Test upload to TestPyPI (optional but recommended):**

```bash
python -m twine upload --repository testpypi dist/*
```

3. **Upload to PyPI:**

```bash
python -m twine upload dist/*
```

You'll need a PyPI account. Create one at https://pypi.org/account/register/

4. **Users install with:**

```bash
pip install noteerr
```

### Update Version

To release a new version:
1. Update version in `setup.py` and `pyproject.toml`
2. Update `src/noteerr/__init__.py`
3. Tag the release: `git tag v1.0.1`
4. Rebuild and upload: `python -m build && twine upload dist/*`

---

## 🐙 Option 2: GitHub Releases

Perfect for open-source projects and beta testing.

### Steps

1. **Push to GitHub:**

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/noteerr.git
git push -u origin main
```

2. **Create a release tag:**

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

3. **Create GitHub Release:**
   - Go to https://github.com/yourusername/noteerr/releases
   - Click "Create a new release"
   - Select the tag v1.0.0
   - Add release notes
   - Upload distribution files from `dist/`

4. **Users install with:**

```bash
pip install git+https://github.com/yourusername/noteerr.git
```

Or for a specific version:

```bash
pip install git+https://github.com/yourusername/noteerr.git@v1.0.0
```

---

## 💻 Option 3: Standalone Executable (Windows/Mac/Linux)

Create a single executable file using PyInstaller.

### Prerequisites

```bash
pip install pyinstaller
```

### Build Executable

**For Windows:**

```bash
pyinstaller --onefile --name noteerr src/noteerr/cli.py
```

**For macOS/Linux:**

```bash
pyinstaller --onefile --name noteerr src/noteerr/cli.py
```

The executable will be in `dist/noteerr.exe` (Windows) or `dist/noteerr` (Unix).

### Distribution

- Zip the executable
- Upload to GitHub Releases
- Users download and add to PATH

**On Windows:**
```powershell
# Move to a permanent location
Move-Item noteerr.exe C:\tools\noteerr.exe

# Add to PATH
setx PATH "$env:PATH;C:\tools"
```

**On Unix:**
```bash
# Move to /usr/local/bin
sudo mv noteerr /usr/local/bin/
sudo chmod +x /usr/local/bin/noteerr
```

---

## 🐳 Option 4: Docker Container

For cross-platform deployment without Python installation.

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY setup.py .
COPY pyproject.toml .

RUN pip install -e .

# Volume for persistent data
VOLUME /root/.noteerr

ENTRYPOINT ["noteerr"]
```

### Build and Run

```bash
# Build image
docker build -t noteerr:latest .

# Create alias for easy use
echo 'alias noteerr="docker run -it -v ~/.noteerr:/root/.noteerr -v $(pwd):/work -w /work noteerr"' >> ~/.bashrc

# Use it
noteerr list
```

---

## 📱 Option 5: Homebrew (macOS/Linux)

Create a Homebrew formula for easy installation on macOS/Linux.

### Create Formula

Save as `noteerr.rb`:

```ruby
class Noteerr < Formula
  desc "Command error memory tool"
  homepage "https://github.com/yourusername/noteerr"
  url "https://github.com/yourusername/noteerr/archive/v1.0.0.tar.gz"
  sha256 "YOUR_SHA256_HERE"
  license "MIT"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/noteerr", "--version"
  end
end
```

### Usage

```bash
# Add tap
brew tap yourusername/noteerr

# Install
brew install noteerr
```

---

## 🌐 Option 6: Web API (Bonus)

Deploy a web API for team collaboration.

### Simple Flask API

```python
# api.py
from flask import Flask, request, jsonify
from noteerr.storage import Storage

app = Flask(__name__)
storage = Storage()

@app.route('/errors', methods=['GET'])
def get_errors():
    return jsonify([e.to_dict() for e in storage.get_all_entries()])

@app.route('/errors', methods=['POST'])
def add_error():
    data = request.json
    entry = storage.add_entry(**data)
    return jsonify(entry.to_dict()), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Deploy to:
- **Heroku**: `git push heroku main`
- **AWS Lambda**: Use Zappa or Serverless Framework
- **Railway**: Connect GitHub repo

---

## ✅ Recommended Deployment Strategy

**For Individual Use:**
- Install via pip from GitHub: `pip install git+https://github.com/...`

**For Public Release:**
1. Publish to PyPI: `pip install noteerr`
2. GitHub Releases for versioning
3. Create standalone executables for non-Python users

**For Team/Enterprise:**
- Deploy to private PyPI server (devpi)
- Or use Docker with shared volume
- Or deploy web API for centralized storage

---

## 📊 Quick Comparison

| Method | Ease | Distribution | Updates |
|--------|------|--------------|---------|
| PyPI | ⭐⭐⭐⭐⭐ | Public | Easy |
| GitHub | ⭐⭐⭐⭐ | Public/Private | Manual |
| Executable | ⭐⭐⭐ | Any | Manual |
| Docker | ⭐⭐⭐ | Any | Medium |
| Homebrew | ⭐⭐⭐⭐ | macOS/Linux | Easy |

---

## 🎯 Next Steps

1. Choose your deployment method
2. Update GitHub repository URL in `setup.py` and `README.md`
3. Build and test locally
4. Deploy!
5. Share with the community 🎉

For questions or issues, create an issue on GitHub!
