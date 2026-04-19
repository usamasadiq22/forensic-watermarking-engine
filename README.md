# Forensic Watermarking Engine

A Python-based watermark detection system for identifying embedded watermarks in images and videos. Designed for content leak traceability and forensic analysis in secure content delivery systems.

## Features

- **Image Watermark Detection**: Support for PNG, JPG, BMP, GIF, WebP formats
- **Video Watermark Detection**: Support for MP4, MOV, AVI, MKV, FLV, WMV formats
- **Confidence Scoring**: Returns watermark detection confidence (0-1 scale)
- **Session ID Extraction**: Identifies embedded session identifiers for leaker tracking
- **Node.js Integration**: Easy integration with JavaScript/TypeScript backends via child_process
- **Forensic Analysis**: Extract and analyze embedded watermark data

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Install Dependencies

```bash
pip3 install -r requirements.txt
```

### Supported Packages

- `invisible-watermark`: Core watermark detection library
- `opencv-python-headless`: Video frame extraction (headless for server environments)
- `numpy`: Array processing
- `scipy`: Scientific computing utilities

## Quick Start

### Detect Watermark in Image

```python
from engine import detect_watermark_image

result = detect_watermark_image('/path/to/image.jpg')
print(result)
# Output: {'success': True, 'sessionId': 'uuid-here', 'confidence': 0.95}
```

### Detect Watermark in Video

```python
from engine import detect_watermark_video

result = detect_watermark_video('/path/to/video.mp4')
print(result)
# Output: {'success': True, 'sessionId': 'uuid-here', 'confidence': 0.92}
```

### Command Line Usage

```bash
python3 engine_api.py /path/to/file.jpg
# Output: {"success": true, "sessionId": "550e8400-e29b-41d4-a716-446655440000", "confidence": 0.95}
```

### Node.js/JavaScript Integration

```javascript
const { spawn } = require('child_process');

const detectWatermark = (filePath) => {
  return new Promise((resolve, reject) => {
    const python = spawn('python3', ['engine_api.py', filePath]);
    
    let output = '';
    python.stdout.on('data', (data) => {
      output += data.toString();
    });
    
    python.on('close', (code) => {
      if (code === 0) {
        resolve(JSON.parse(output));
      } else {
        reject(new Error('Watermark detection failed'));
      }
    });
  });
};

// Usage
detectWatermark('./suspected_leak.jpg')
  .then(result => console.log(result))
  .catch(err => console.error(err));
```

## API Response Format

### Success Response

```json
{
  "success": true,
  "sessionId": "550e8400-e29b-41d4-a716-446655440000",
  "confidence": 0.95,
  "type": "invisible-watermark"
}
```

### Failure Response

```json
{
  "success": false,
  "error": "No watermark detected or invalid file format",
  "confidence": 0
}
```

## File Structure

```
forensic-watermarking-engine/
├── engine.py              # Core watermark detection implementation
├── engine_api.py          # Python API wrapper for command-line and external integration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Core Components

### engine.py

Main detection engine with the following functions:

- **`detect_watermark_image(image_path)`**: Detects watermark in image files
  - Supported formats: PNG, JPG, JPEG, BMP, GIF, WebP
  - Returns: Dict with success status, sessionId, and confidence score
  
- **`detect_watermark_video(video_path)`**: Detects watermark in video files
  - Supported formats: MP4, MOV, AVI, MKV, FLV, WMV
  - Extracts and analyzes key frames
  - Returns: Dict with best detection result from all frames

### engine_api.py

Wrapper for external integration:

- **`main()`**: Command-line entry point
- Accepts file path as argument
- Returns JSON formatted result
- Handles file validation and error reporting
- Designed for integration with Node.js backends

## Performance Considerations

- **Image Processing**: ~100-500ms per image
- **Video Processing**: ~5-30 seconds depending on resolution and duration
- **Memory Usage**: ~500MB-2GB depending on file size
- **Supported File Sizes**: Up to 500MB (configurable)
- **Concurrent Processing**: Run multiple instances for parallel detection

## Security Notes

⚠️ **Important for Production Deployment:**

- Always validate file paths before processing to prevent directory traversal
- Implement rate limiting for public-facing endpoints
- Run in sandboxed/containerized environment for untrusted input
- Clear temporary files after processing to avoid disk space issues
- Log all detection attempts for audit trails and forensic investigation
- Implement authentication for watermark detection endpoints
- Use HTTPS for transmitting sensitive watermark data

## Use Cases

### Content Leak Investigation
Identify and track leaked content by extracting embedded session IDs that reveal which user accessed the content.

### Digital Rights Management (DRM)
Verify authenticity of digital media and prevent unauthorized distribution.

### Forensic Analysis
Analyze suspected leaked content to determine source and identify unauthorized users.

### Compliance & Audit
Maintain audit trails of content access and distribution for regulatory compliance.

## Integration Examples

### Secure Content Delivery System (SCDS)

This engine is designed to integrate with SCDS to:
1. Detect watermarks in suspected leaked content
2. Extract embedded session IDs for leaker identification
3. Correlate with access logs for incident investigation
4. Support forensic analysis of content breaches
5. Generate forensic reports for legal proceedings

### Backend Integration

For NestJS/Express backends:

```typescript
import { spawn } from 'child_process';

class WatermarkService {
  async detectWatermark(filePath: string) {
    return new Promise((resolve, reject) => {
      const python = spawn('python3', [
        './engines/forensic-watermarking-engine/engine_api.py',
        filePath
      ]);

      let output = '';
      python.stdout.on('data', (data) => {
        output += data.toString();
      });

      python.on('close', (code) => {
        if (code === 0) {
          resolve(JSON.parse(output));
        } else {
          reject(new Error('Detection failed'));
        }
      });
    });
  }
}
```

## Performance Optimization

### For Large-Scale Deployments

- Use containerization (Docker) for isolated execution
- Implement job queuing (Bull, Celery) for async processing
- Cache detection results for identical files
- Parallelize video frame processing
- Monitor resource usage and implement autoscaling

## Troubleshooting

### "No module named 'invisible_watermark'"
```bash
pip3 install invisible-watermark --upgrade
```

### "No module named 'cv2'"
```bash
pip3 install opencv-python-headless
```

### Permission Denied Errors
```bash
chmod +x engine.py
chmod +x engine_api.py
```

### Out of Memory for Large Videos
Reduce video processing by sampling fewer frames or using lower resolution extraction.

## Testing

```bash
# Test with a sample image
python3 engine_api.py ./test_image.jpg

# Test with a sample video
python3 engine_api.py ./test_video.mp4
```

## License

MIT License - See LICENSE file for details

## Author

Usama Sadiq

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support & Issues

For bugs, questions, or feature requests, please create an issue in the GitHub repository.

## Citation

If you use this engine in your research or production system, please cite:

```
Forensic Watermarking Engine
Usama Sadiq
https://github.com/yourusername/forensic-watermarking-engine
```

## Related Projects

- [invisible-watermark](https://github.com/ShieldMnt/invisible-watermark) - Core watermarking library
- [OpenCV](https://opencv.org/) - Computer vision library for video processing
- [NumPy](https://numpy.org/) - Numerical computing library

---

**Version**: 1.0.0  
**Last Updated**: April 2026
