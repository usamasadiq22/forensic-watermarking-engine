"""
CLI wrapper called by watermarkService.js via child_process.spawn

Usage (Video):
  python3 engine_api.py embed --input /path/in.mp4 --output /path/out.mp4 --session <uuid>
  python3 engine_api.py detect --input /path/suspected_leak.mp4

Usage (Image):
  python3 engine_api.py embed-image --input /path/in.jpg --output /path/out.jpg --session <uuid>
  python3 engine_api.py detect-image --input /path/suspected_leak.jpg
"""

import sys
import json
import argparse
from engine import (
    embed_watermark,
    detect_watermark,
    embed_watermark_image,
    detect_watermark_image,
)


def main():
    parser = argparse.ArgumentParser(description='SCDS Watermark CLI (Video & Image)')
    parser.add_argument('action', choices=['embed', 'detect', 'embed-image', 'detect-image'])
    parser.add_argument('--input',   required=True,  help='Input video/image path')
    parser.add_argument('--output',  required=False, help='Output path (embed only)')
    parser.add_argument('--session', required=False, help='Session UUID (embed only)')
    args = parser.parse_args()

    if args.action == 'embed':
        if not args.output or not args.session:
            result = {'success': False, 'message': '--output and --session are required for embed'}
        else:
            result = embed_watermark(args.input, args.output, args.session)
    
    elif args.action == 'detect':
        result = detect_watermark(args.input)
    
    elif args.action == 'embed-image':
        if not args.output or not args.session:
            result = {'success': False, 'message': '--output and --session are required for embed-image'}
        else:
            result = embed_watermark_image(args.input, args.output, args.session)
    
    elif args.action == 'detect-image':
        result = detect_watermark_image(args.input)

    # Write JSON to stdout — Node.js parses this
    print(json.dumps(result))
    sys.exit(0 if result.get('success') else 1)


if __name__ == '__main__':
    main()
