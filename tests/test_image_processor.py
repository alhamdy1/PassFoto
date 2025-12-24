"""
Unit tests for PassFoto image processor module.
"""

import unittest
import cv2
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from passfoto.image_processor import ImageProcessor


class TestImageProcessor(unittest.TestCase):
    """Test cases for ImageProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = ImageProcessor()
        # Create a test image (500x500 BGR image)
        self.test_image = np.zeros((500, 500, 3), dtype=np.uint8)
        self.test_image[:] = (100, 150, 200)  # Light color
    
    def test_init(self):
        """Test ImageProcessor initialization."""
        self.assertIsNotNone(self.processor)
        self.assertIsNotNone(self.processor.face_cascade)
        self.assertIsNotNone(self.processor.eye_cascade)
    
    def test_photo_sizes(self):
        """Test that standard photo sizes are defined."""
        self.assertIn("2x2 inch (US)", ImageProcessor.PHOTO_SIZES)
        self.assertIn("35x45 mm (EU)", ImageProcessor.PHOTO_SIZES)
        self.assertEqual(ImageProcessor.PHOTO_SIZES["2x2 inch (US)"], (600, 600))
    
    def test_auto_enhance(self):
        """Test auto enhancement."""
        result = self.processor.auto_enhance(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)
        self.assertEqual(result.dtype, np.uint8)
    
    def test_white_balance(self):
        """Test white balance correction."""
        result = self.processor.white_balance(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_sharpen(self):
        """Test image sharpening."""
        result = self.processor.sharpen(self.test_image, strength=1.0)
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_smooth_skin(self):
        """Test skin smoothing."""
        result = self.processor.smooth_skin(self.test_image, strength=30)
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_denoise(self):
        """Test denoising."""
        result = self.processor.denoise(self.test_image, strength=10)
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_adjust_brightness_contrast(self):
        """Test brightness and contrast adjustment."""
        # Test with positive values
        result = self.processor.adjust_brightness_contrast(
            self.test_image, brightness=10, contrast=10
        )
        self.assertEqual(result.shape, self.test_image.shape)
        
        # Test with negative values
        result = self.processor.adjust_brightness_contrast(
            self.test_image, brightness=-10, contrast=-10
        )
        self.assertEqual(result.shape, self.test_image.shape)
        
        # Test with zero values
        result = self.processor.adjust_brightness_contrast(
            self.test_image, brightness=0, contrast=0
        )
        self.assertEqual(result.shape, self.test_image.shape)
    
    def test_rotate_image(self):
        """Test image rotation."""
        # Test with angle
        result = self.processor.rotate_image(self.test_image, 10)
        self.assertIsNotNone(result)
        
        # Test with small angle (should return original)
        result = self.processor.rotate_image(self.test_image, 0.1)
        np.testing.assert_array_equal(result, self.test_image)
    
    def test_detect_face_no_face(self):
        """Test face detection with no face in image."""
        result = self.processor.detect_face(self.test_image)
        # Should return None when no face is found
        self.assertIsNone(result)
    
    def test_detect_eyes_no_eyes(self):
        """Test eye detection with no eyes in image."""
        result = self.processor.detect_eyes(self.test_image)
        # Should return empty list when no eyes are found
        self.assertEqual(result, [])
    
    def test_calculate_rotation_angle_no_face(self):
        """Test rotation angle calculation with no face."""
        result = self.processor.calculate_rotation_angle(self.test_image)
        # Should return 0 when no face is found
        self.assertEqual(result, 0.0)
    
    def test_auto_straighten_no_face(self):
        """Test auto straighten with no face in image."""
        result = self.processor.auto_straighten(self.test_image)
        # Should return original image when no face is found
        np.testing.assert_array_equal(result, self.test_image)
    
    def test_crop_to_face_no_face(self):
        """Test crop to face with no face in image."""
        result = self.processor.crop_to_face(self.test_image)
        # Should return original image when no face is found
        np.testing.assert_array_equal(result, self.test_image)
    
    def test_remove_red_eyes_no_face(self):
        """Test red eye removal with no face in image."""
        result = self.processor.remove_red_eyes(self.test_image)
        # Should return original image when no face is found
        np.testing.assert_array_equal(result, self.test_image)
    
    def test_change_background_no_face(self):
        """Test background change with no face in image."""
        result = self.processor.change_background(self.test_image)
        # Should return original image when no face is found
        np.testing.assert_array_equal(result, self.test_image)
    
    def test_resize_image(self):
        """Test image resizing."""
        result = self.processor.resize_image(self.test_image, "2x2 inch (US)")
        self.assertEqual(result.shape[:2], (600, 600))
        
        # Test with Custom size (should return original)
        result = self.processor.resize_image(self.test_image, "Custom")
        np.testing.assert_array_equal(result, self.test_image)
    
    def test_apply_all_enhancements(self):
        """Test applying all enhancements."""
        options = {
            'auto_straighten': True,
            'auto_enhance': True,
            'white_balance': True,
            'denoise': True,
            'smooth_skin': False,
            'sharpen': True,
            'remove_red_eyes': True
        }
        result = self.processor.apply_all_enhancements(self.test_image, options)
        self.assertEqual(result.shape, self.test_image.shape)
        self.assertEqual(result.dtype, np.uint8)
    
    def test_apply_all_enhancements_default_options(self):
        """Test applying all enhancements with default options."""
        result = self.processor.apply_all_enhancements(self.test_image)
        self.assertEqual(result.shape, self.test_image.shape)


if __name__ == '__main__':
    unittest.main()
