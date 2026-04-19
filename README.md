# Forensic Watermarking Engine

A Python-based watermark embedding and detection system for secure content distribution and forensic analysis. Embed session identifiers into videos for leak traceability and detect watermarks in suspected leaked content to identify the source.

## Features

### Watermark Embedding
- **Video Watermark Embedding**: Embed UUID session identifiers into MP4, MOV, AVI, MKV videos
- **Frame-based Embedding**: Configurable embedding frequency (every Nth frame for performance optimization)
- **H.264 Compression Resistant**: Watermark survives H.264 re-encoding with zero bit error rate (BER=0.000)
- **Real-time Performance**: 1.4x real-time throughput with optimized frame sampling
- **Session ID Tracking**: Embed unique session UUIDs for viewer identification and leak attribution

### Watermark Detection
- **Video Watermark Detection**: Detect embedded watermarks in MP4, MOV, AVI, MKV, FLV, WMV formats
- **Image Watermark Detection**: Support for PNG, JPG, BMP, GIF, WebP formats
- **Confidence Scoring**: Returns watermark detection confidence (0-1 scale)
- **Session ID Extraction**: Recover embedded session identifiers for leaker tracking
- **Majority Voting**: Frame-based voting for accurate UUID recovery across video frames

### Integration & Analysis
- **Node.js Integration**: Easy integration with JavaScript/TypeScript backends via child_process
- **Forensic Analysis**: Extract and analyze embedded watermark data
- **UUID Management**: Automatic conversion between UUID and binary formats

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

### Embed Watermark in Video

```python
from engine import embed_watermark
import uuid

# Generate unique session ID for viewer
session_uuid = str(uuid.uuid4())
print(f"Session UUID: {session_uuid}")

# Embed watermark into video
result = embed_watermark(
    input_video_path='/path/to/input.mp4',
    output_video_path='/path/to/output_watermarked.mp4',
    session_uuid=session_uuid
)
print(result)
# Output: {'success': True, 'sessionId': 'uuid-here', 'message': 'Watermark embedded successfully'}
```

### Detect Watermark in Video

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

Main watermarking engine with embedding and detection functions:

#### Embedding Functions
- **`embed_watermark(input_video_path, output_video_path, session_uuid)`**: Embed UUID watermark into video
  - Supports: MP4, MOV, AVI, MKV input formats
  - Embeds UUID in every Nth frame (configurable via `EMBED_EVERY_N_FRAMES`)
  - Converts to MJPEG AVI for processing, then to H.264 MP4 output
  - Returns: Dict with success status and session ID
  
#### Detection Functions
- **`detect_watermark_image(image_path)`**: Detects watermark in image files
  - Supported formats: PNG, JPG, JPEG, BMP, GIF, WebP
  - Returns: Dict with success status, sessionId, and confidence score
  
- **`detect_watermark_video(video_path)`**: Detects watermark in video files
  - Supported formats: MP4, MOV, AVI, MKV, FLV, WMV
  - Extracts and analyzes key frames
  - Uses majority voting for UUID recovery
  - Returns: Dict with best detection result from all frames

#### Helper Functions
- **`uuid_to_bytes(session_uuid)`**: Convert UUID string to 16 raw bytes
- **`bytes_to_uuid(raw_bytes)`**: Convert 16 raw bytes back to UUID string
- **`_get_video_props(cap)`**: Extract video properties (fps, resolution, frame count)
- **`_mp4_to_mjpeg_avi(mp4_path, avi_path)`**: Convert MP4 to MJPEG AVI for processing
- **`_avi_to_mp4(avi_path, mp4_path)`**: Convert MJPEG AVI to H.264 MP4 for output

### engine_api.py

Wrapper for external integration:

- **`main()`**: Command-line entry point
- Accepts file path as argument
- Returns JSON formatted result
- Handles file validation and error reporting
- Designed for integration with Node.js backends

## Configuration

### Environment Variables

Configure embedding and detection behavior via environment variables:

```bash
# Embedding: Embed watermark in every Nth frame
# Lower N = more frames watermarked = better detection but slower
# Higher N = faster but fewer frames for voting
export WM_EMBED_EVERY_N=10

# Embedding: H.264 encoding quality (default: 18)
# CRF range: 0-51 (0=lossless, 18=high quality, 28=default, 51=worst quality)
# Do not go above 23 or watermark may not survive re-encoding
export WM_H264_CRF=18

# Temporary working directory for video processing
export WM_TEMP_DIR=/tmp/scds_wm
```

### Example with Custom Configuration

```python
import os
os.environ['WM_EMBED_EVERY_N'] = '5'  # Embed in every 5th frame (slower but better)
os.environ['WM_H264_CRF'] = '22'      # Lower quality for faster encoding

from engine import embed_watermark
result = embed_watermark(input_path, output_path, session_uuid)
```

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

### Secure Content Distribution with Leak Traceability
1. **Embed**: Add unique session UUID watermark to video when delivering to viewer
2. **Monitor**: If leaked content appears, detect and extract the session UUID
3. **Identify**: Cross-reference UUID with access logs to identify the leaker
4. **Respond**: Take appropriate action against the identified unauthorized user

### Content Leak Investigation
Identify and track leaked content by extracting embedded session IDs that reveal which user accessed the content.

### Digital Rights Management (DRM)
Verify authenticity of digital media and prevent unauthorized distribution by embedding ownership information.

### Forensic Analysis
Analyze suspected leaked content to determine source and identify unauthorized users through watermark extraction.

### Compliance & Audit
Maintain audit trails of content access and distribution for regulatory compliance by embedding session metadata.

## Workflow Example: End-to-End Leak Traceability

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: VIEWER ACCESSES CONTENT (Embed Watermark)              │
├─────────────────────────────────────────────────────────────────┤
│ 1. User authenticates and requests premium content              │
│ 2. Backend generates unique session UUID                        │
│ 3. Original video watermarked with session UUID                 │
│ 4. Watermarked video delivered to viewer                        │
│ 5. Session UUID + viewer info logged in database                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: CONTENT LEAKED (Suspected Leaked File Found)            │
├─────────────────────────────────────────────────────────────────┤
│ 1. Copyright team discovers leaked content online               │
│ 2. Download suspected leaked file                               │
│ 3. Submit to forensic investigation endpoint                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: FORENSIC ANALYSIS (Detect Watermark)                   │
├─────────────────────────────────────────────────────────────────┤
│ 1. Detection engine processes leaked file                       │
│ 2. Extracts embedded session UUID from frames                   │
│ 3. Returns confidence score and session ID                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: LEAKER IDENTIFICATION & ACTION                          │
├─────────────────────────────────────────────────────────────────┤
│ 1. Backend queries access logs using session UUID               │
│ 2. Identifies which user accessed during that session           │
│ 3. Correlates IP, device, and timestamp data                    │
│ 4. Confirms match with forensic evidence                        │
│ 5. Takes action: Account suspension, legal notice, etc.         │
└─────────────────────────────────────────────────────────────────┘
```

## Integration Examples

### Secure Content Delivery System (SCDS)

This engine is designed to integrate with SCDS to:

**Embedding Pipeline** (When serving content to viewer):
1. User authenticates and requests premium content
2. Backend generates unique session UUID
3. `embed_watermark()` called to add UUID to video
4. Watermarked video delivered to viewer
5. Session metadata logged for later correlation

**Detection Pipeline** (When investigating leaked content):
1. Suspected leaked content submitted to investigation endpoint
2. `detect_watermark_video()` processes the file
3. Extracts embedded session UUID with confidence score
4. Backend correlates UUID with access logs
5. Identifies leaker from viewer session data
6. Generates forensic report with evidence

### Backend Integration

For NestJS/Express backends:

```typescript
import { spawn } from 'child_process';
import { v4 as uuidv4 } from 'uuid';

class WatermarkService {
  // Embed watermark when delivering content to viewer
  async embedWatermark(inputPath: string, outputPath: string, sessionId?: string) {
    const uuid = sessionId || uuidv4();
    
    return new Promise((resolve, reject) => {
      const python = spawn('python3', [
        './engines/forensic-watermarking-engine/engine.py',
        'embed',
        inputPath,
        outputPath,
        uuid
      ]);

      let output = '';
      python.stdout.on('data', (data) => {
        output += data.toString();
      });

      python.on('close', (code) => {
        if (code === 0) {
          resolve({ success: true, sessionId: uuid, outputPath });
        } else {
          reject(new Error('Embedding failed'));
        }
      });
    });
  }

  // Detect watermark when investigating leaked content
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
