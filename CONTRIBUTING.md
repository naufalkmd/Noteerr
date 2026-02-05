# Contributing to Noteerr

Thank you for your interest in contributing to Noteerr! 🎉

## How to Contribute

### Reporting Bugs
- Use the GitHub issue tracker
- Include detailed steps to reproduce
- Mention your OS, Python version, and shell

### Suggesting Features
- Open a feature request issue
- Explain the use case clearly
- Provide example usage if possible

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow PEP 8 style guidelines
   - Add docstrings to functions
   - Keep commits focused and clear

4. **Test your changes**
   ```bash
   pip install -e .
   noteerr --help
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/noteerr.git
cd noteerr

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .

# Run noteerr
noteerr --version
```

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add comments for complex logic
- Write descriptive commit messages

## Testing

Before submitting:
- Test on your local machine
- Verify all commands work as expected
- Check that shell integration still works

## Questions?

Feel free to open an issue for any questions!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
