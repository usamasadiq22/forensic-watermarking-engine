# Contributing to Forensic Watermarking Engine

Thank you for your interest in contributing to the Forensic Watermarking Engine project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful and professional in all interactions with other contributors and maintainers.

## How to Contribute

### 1. Report Bugs

- Check if the bug has already been reported in Issues
- Include:
  - Python version
  - Operating system
  - Error traceback
  - Steps to reproduce
  - Expected vs actual behavior

### 2. Suggest Enhancements

- Clearly describe the enhancement and use case
- Explain why this would be beneficial
- Provide examples if applicable

### 3. Submit Pull Requests

#### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/usamasadiq/forensic-watermarking-engine.git
cd forensic-watermarking-engine

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

#### Making Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit with clear messages:
   ```bash
   git commit -m "Add: Brief description of changes"
   ```

3. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request with:
   - Clear title and description
   - Reference to related issues
   - Explanation of changes

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and modular
- Maximum line length: 100 characters

### Example Function

```python
def detect_watermark_image(image_path: str) -> Dict[str, Any]:
    """
    Detect watermark in image file.
    
    Args:
        image_path (str): Path to image file
        
    Returns:
        Dict containing:
            - success (bool): Whether watermark was detected
            - sessionId (str): Extracted session identifier
            - confidence (float): Detection confidence 0-1
            - error (str): Error message if detection failed
            
    Raises:
        FileNotFoundError: If image file not found
        ValueError: If image format not supported
    """
    pass
```

## Testing

Before submitting a pull request:

```bash
# Test with sample images
python3 engine_api.py ./test_image.jpg

# Test with sample videos
python3 engine_api.py ./test_video.mp4

# Run linting
python3 -m flake8 engine.py engine_api.py
```

## Documentation

- Update README.md if adding new features
- Document API changes clearly
- Include usage examples
- Update docstrings for modified functions

## Commit Messages

Use clear, descriptive commit messages:

```
Add: New feature or enhancement
Fix: Bug fix
Docs: Documentation changes
Test: Adding tests
Refactor: Code restructuring
Perf: Performance improvements
```

Example:
```
git commit -m "Add: Support for HEIF image format in detection"
```

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add any new dependencies to requirements.txt
4. Follow the existing code style
5. Provide clear PR description
6. Link related issues

## Release Process

Maintainers will handle releases following semantic versioning:
- MAJOR: Breaking changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes

## Questions?

Open an issue for discussions or questions about the project.

---

Thank you for contributing!
