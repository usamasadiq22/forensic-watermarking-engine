#!/usr/bin/env python3
"""
Unit tests for the Forensic Watermarking Engine

Run: python3 test_engine.py
Or:  python3 -m pytest test_engine.py -v
"""

import unittest
import os
import tempfile
import uuid
import numpy as np
from PIL import Image
import subprocess
import json

from engine import (
    embed_watermark,
    detect_watermark_image,
    detect_watermark_video,
    uuid_to_bytes,
    bytes_to_uuid,
)


class TestUUIDConversion(unittest.TestCase):
    """Test UUID to bytes conversion utilities"""
    
    def test_uuid_to_bytes_conversion(self):
        """Test converting UUID string to bytes"""
        session_uuid = str(uuid.uuid4())
        uuid_bytes = uuid_to_bytes(session_uuid)
        
        self.assertEqual(len(uuid_bytes), 16)
        self.assertIsInstance(uuid_bytes, bytes)
    
    def test_bytes_to_uuid_conversion(self):
        """Test converting bytes back to UUID string"""
        session_uuid = str(uuid.uuid4())
        uuid_bytes = uuid_to_bytes(session_uuid)
        recovered_uuid = bytes_to_uuid(uuid_bytes)
        
        self.assertEqual(session_uuid, recovered_uuid)
    
    def test_uuid_round_trip(self):
        """Test UUID conversion round trip"""
        original_uuid = str(uuid.uuid4())
        
        # Round trip: UUID -> bytes -> UUID
        uuid_bytes = uuid_to_bytes(original_uuid)
        recovered_uuid = bytes_to_uuid(uuid_bytes)
        
        self.assertEqual(original_uuid, recovered_uuid)


class TestEmbedding(unittest.TestCase):
    """Test watermark embedding functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Create test video file"""
        cls.temp_dir = tempfile.mkdtemp()
        cls.test_video = os.path.join(cls.temp_dir, 'test_video.mp4')
        
        # Create a simple test video using ffmpeg
        cmd = [
            'ffmpeg', '-f', 'lavfi', '-i', 'testsrc=duration=5:size=320x240:rate=1',
            '-pix_fmt', 'yuv420p', '-y', cls.test_video
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, timeout=30, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise unittest.SkipTest(f"FFmpeg not available or failed: {e}")
    
    def test_embed_watermark_success(self):
        """Test successful watermark embedding"""
        output_path = os.path.join(self.temp_dir, 'embedded_output.mp4')
        session_uuid = str(uuid.uuid4())
        
        result = embed_watermark(self.test_video, output_path, session_uuid)
        
        self.assertTrue(result.get('success'))
        self.assertEqual(result.get('sessionId'), session_uuid)
        self.assertTrue(os.path.exists(output_path))
    
    def test_embed_with_invalid_input(self):
        """Test embedding with non-existent input file"""
        output_path = os.path.join(self.temp_dir, 'output.mp4')
        session_uuid = str(uuid.uuid4())
        
        result = embed_watermark('/nonexistent/file.mp4', output_path, session_uuid)
        
        self.assertFalse(result.get('success'))
    
    def test_embed_generates_output_file(self):
        """Test that embedding creates output file"""
        output_path = os.path.join(self.temp_dir, 'generated_output.mp4')
        session_uuid = str(uuid.uuid4())
        
        # Ensure output doesn't exist yet
        if os.path.exists(output_path):
            os.remove(output_path)
        
        embed_watermark(self.test_video, output_path, session_uuid)
        
        self.assertTrue(os.path.exists(output_path), "Output file was not created")
        self.assertGreater(os.path.getsize(output_path), 0, "Output file is empty")


class TestDetectionVideo(unittest.TestCase):
    """Test watermark detection in videos"""
    
    @classmethod
    def setUpClass(cls):
        """Create test video with embedded watermark"""
        cls.temp_dir = tempfile.mkdtemp()
        cls.original_video = os.path.join(cls.temp_dir, 'original.mp4')
        cls.watermarked_video = os.path.join(cls.temp_dir, 'watermarked.mp4')
        
        # Create test video
        cmd = [
            'ffmpeg', '-f', 'lavfi', '-i', 'testsrc=duration=5:size=320x240:rate=1',
            '-pix_fmt', 'yuv420p', '-y', cls.original_video
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, timeout=30, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise unittest.SkipTest(f"FFmpeg not available: {e}")
        
        # Embed watermark
        cls.session_uuid = str(uuid.uuid4())
        embed_watermark(cls.original_video, cls.watermarked_video, cls.session_uuid)
    
    def test_detect_watermarked_video(self):
        """Test detecting watermark in watermarked video"""
        result = detect_watermark_video(self.watermarked_video)
        
        self.assertTrue(result.get('success'), "Failed to detect embedded watermark")
        self.assertEqual(result.get('sessionId'), self.session_uuid)
        self.assertGreaterEqual(result.get('confidence', 0), 0.5)
    
    def test_detect_original_video_no_watermark(self):
        """Test that original video has no watermark"""
        result = detect_watermark_video(self.original_video)
        
        self.assertFalse(result.get('success'), "Detected watermark in original (shouldn't happen)")
    
    def test_detect_invalid_video(self):
        """Test detection with non-existent file"""
        result = detect_watermark_video('/nonexistent/video.mp4')
        
        self.assertFalse(result.get('success'))


class TestDetectionImage(unittest.TestCase):
    """Test watermark detection in images"""
    
    @classmethod
    def setUpClass(cls):
        """Create test image"""
        cls.temp_dir = tempfile.mkdtemp()
        cls.test_image = os.path.join(cls.temp_dir, 'test_image.jpg')
        
        # Create a random test image
        img_array = np.random.randint(50, 200, (480, 640, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        img.save(cls.test_image)
    
    def test_detect_image_no_watermark(self):
        """Test detection on image with no watermark"""
        result = detect_watermark_image(self.test_image)
        
        # Result depends on image content, but should return a valid response
        self.assertIn('success', result)
        self.assertIn('confidence', result)
    
    def test_detect_invalid_image(self):
        """Test detection with non-existent image"""
        result = detect_watermark_image('/nonexistent/image.jpg')
        
        self.assertFalse(result.get('success'))


class TestCLIIntegration(unittest.TestCase):
    """Test command-line interface"""
    
    @classmethod
    def setUpClass(cls):
        """Create test video for CLI testing"""
        cls.temp_dir = tempfile.mkdtemp()
        cls.test_video = os.path.join(cls.temp_dir, 'cli_test.mp4')
        
        cmd = [
            'ffmpeg', '-f', 'lavfi', '-i', 'testsrc=duration=3:size=320x240:rate=1',
            '-pix_fmt', 'yuv420p', '-y', cls.test_video
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, timeout=30, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise unittest.SkipTest(f"FFmpeg not available: {e}")
    
    def test_cli_detect_command(self):
        """Test CLI detect command"""
        cmd = ['python3', 'engine_api.py', 'detect', '--input', self.test_video]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 1)  # Should fail (no watermark)
        
        # Verify JSON output
        output = json.loads(result.stdout)
        self.assertIn('success', output)
    
    def test_cli_embed_command(self):
        """Test CLI embed command"""
        output_path = os.path.join(self.temp_dir, 'cli_embedded.mp4')
        session_uuid = str(uuid.uuid4())
        
        cmd = [
            'python3', 'engine_api.py', 'embed',
            '--input', self.test_video,
            '--output', output_path,
            '--session', session_uuid
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        # Verify command succeeded
        self.assertEqual(result.returncode, 0)
        
        # Verify JSON output
        output = json.loads(result.stdout)
        self.assertTrue(output.get('success'))
        self.assertEqual(output.get('sessionId'), session_uuid)


def run_tests():
    """Run all tests with detailed output"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestUUIDConversion))
    suite.addTests(loader.loadTestsFromTestCase(TestEmbedding))
    suite.addTests(loader.loadTestsFromTestCase(TestDetectionVideo))
    suite.addTests(loader.loadTestsFromTestCase(TestDetectionImage))
    suite.addTests(loader.loadTestsFromTestCase(TestCLIIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit(run_tests())
