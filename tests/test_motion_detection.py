import unittest
import numpy as np
from app.motion_detection import detect_motion

class TestMotionDetection(unittest.TestCase):
    def test_detect_motion_no_motion(self):
        # Create two identical frames (no motion)
        frame1 = np.zeros((100, 100, 3), dtype=np.uint8)
        frame2 = np.zeros((100, 100, 3), dtype=np.uint8)
        
        self.assertFalse(detect_motion(frame1, frame2))

    def test_detect_motion_with_motion(self):
        # Create two different frames (motion)
        frame1 = np.zeros((100, 100, 3), dtype=np.uint8)
        frame2 = np.zeros((100, 100, 3), dtype=np.uint8)
        frame2[40:60, 40:60] = 255  # Add a white square
        
        self.assertTrue(detect_motion(frame1, frame2))

    def test_detect_motion_invalid_input(self):
        # Test with None input
        self.assertFalse(detect_motion(None, None))
        
        # Test with mismatched frame sizes
        frame1 = np.zeros((100, 100, 3), dtype=np.uint8)
        frame2 = np.zeros((50, 50, 3), dtype=np.uint8)
        self.assertFalse(detect_motion(frame1, frame2))

if __name__ == '__main__':
    unittest.main()
