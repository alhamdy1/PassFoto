"""
Image processing module for PassFoto application.
Contains all image enhancement and correction functions.
"""

import cv2
import numpy as np
from PIL import Image
import math


class ImageProcessor:
    """Main class for processing and enhancing passport photos."""
    
    # Standard passport photo sizes (width x height in pixels at 300 DPI)
    PHOTO_SIZES = {
        "2x2 inch (US)": (600, 600),
        "35x45 mm (EU)": (413, 531),
        "35x35 mm": (413, 413),
        "33x48 mm (Indonesia)": (390, 567),
        "51x51 mm": (602, 602),
        "Custom": None
    }
    
    def __init__(self):
        """Initialize the image processor."""
        self.face_cascade = None
        self.eye_cascade = None
        self._load_cascades()
    
    def _load_cascades(self):
        """Load Haar cascade classifiers for face and eye detection."""
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            self.eye_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_eye.xml'
            )
        except Exception as e:
            print(f"Warning: Could not load cascade classifiers: {e}")
    
    def load_image(self, file_path):
        """
        Load an image from file.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            numpy.ndarray: The loaded image in BGR format
        """
        image = cv2.imread(file_path)
        if image is None:
            raise ValueError(f"Could not load image from {file_path}")
        return image
    
    def save_image(self, image, file_path, quality=95):
        """
        Save an image to file.
        
        Args:
            image: Image array to save
            file_path: Destination path
            quality: JPEG quality (0-100)
        """
        if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
            cv2.imwrite(file_path, image, [cv2.IMWRITE_JPEG_QUALITY, quality])
        elif file_path.lower().endswith('.png'):
            cv2.imwrite(file_path, image, [cv2.IMWRITE_PNG_COMPRESSION, 9])
        else:
            cv2.imwrite(file_path, image)
    
    def detect_face(self, image):
        """
        Detect face in the image.
        
        Args:
            image: Input image in BGR format
            
        Returns:
            tuple: (x, y, w, h) of the detected face, or None if not found
        """
        if self.face_cascade is None:
            return None
            
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        
        if len(faces) == 0:
            return None
        
        # Return the largest face detected
        largest_face = max(faces, key=lambda f: f[2] * f[3])
        return tuple(largest_face)
    
    def detect_eyes(self, image, face_rect=None):
        """
        Detect eyes in the image.
        
        Args:
            image: Input image in BGR format
            face_rect: Optional face rectangle to limit search area
            
        Returns:
            list: List of (x, y, w, h) tuples for detected eyes
        """
        if self.eye_cascade is None:
            return []
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        if face_rect is not None:
            x, y, w, h = face_rect
            roi_gray = gray[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            # Adjust coordinates to full image
            eyes = [(ex + x, ey + y, ew, eh) for (ex, ey, ew, eh) in eyes]
        else:
            eyes = self.eye_cascade.detectMultiScale(gray)
            eyes = [tuple(e) for e in eyes]
        
        return eyes
    
    def calculate_rotation_angle(self, image):
        """
        Calculate the rotation angle needed to straighten the face.
        
        Args:
            image: Input image in BGR format
            
        Returns:
            float: Rotation angle in degrees
        """
        face = self.detect_face(image)
        if face is None:
            return 0.0
        
        eyes = self.detect_eyes(image, face)
        
        if len(eyes) < 2:
            return 0.0
        
        # Sort eyes by x coordinate
        eyes = sorted(eyes, key=lambda e: e[0])
        
        # Get center of each eye
        eye1_center = (eyes[0][0] + eyes[0][2] // 2, eyes[0][1] + eyes[0][3] // 2)
        eye2_center = (eyes[1][0] + eyes[1][2] // 2, eyes[1][1] + eyes[1][3] // 2)
        
        # Calculate angle
        dx = eye2_center[0] - eye1_center[0]
        dy = eye2_center[1] - eye1_center[1]
        
        angle = math.degrees(math.atan2(dy, dx))
        
        return angle
    
    def rotate_image(self, image, angle):
        """
        Rotate the image by the specified angle.
        
        Args:
            image: Input image in BGR format
            angle: Rotation angle in degrees
            
        Returns:
            numpy.ndarray: Rotated image
        """
        if abs(angle) < 0.5:
            return image
        
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        # Calculate new image bounds
        cos = abs(rotation_matrix[0, 0])
        sin = abs(rotation_matrix[0, 1])
        new_width = int(height * sin + width * cos)
        new_height = int(height * cos + width * sin)
        
        # Adjust rotation matrix
        rotation_matrix[0, 2] += (new_width - width) / 2
        rotation_matrix[1, 2] += (new_height - height) / 2
        
        rotated = cv2.warpAffine(
            image, 
            rotation_matrix, 
            (new_width, new_height),
            borderMode=cv2.BORDER_REPLICATE
        )
        
        return rotated
    
    def auto_straighten(self, image):
        """
        Automatically straighten the image based on face detection.
        
        Args:
            image: Input image in BGR format
            
        Returns:
            numpy.ndarray: Straightened image
        """
        angle = self.calculate_rotation_angle(image)
        return self.rotate_image(image, angle)
    
    def adjust_brightness_contrast(self, image, brightness=0, contrast=0):
        """
        Adjust brightness and contrast of the image.
        
        Args:
            image: Input image in BGR format
            brightness: Brightness adjustment (-100 to 100)
            contrast: Contrast adjustment (-100 to 100)
            
        Returns:
            numpy.ndarray: Adjusted image
        """
        brightness = int((brightness - 0) * (255 - (-255)) / (100 - (-100)) + (-255))
        contrast = int((contrast - 0) * (127 - (-127)) / (100 - (-100)) + (-127))
        
        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                highlight = 255
            else:
                shadow = 0
                highlight = 255 + brightness
            alpha = (highlight - shadow) / 255
            gamma = shadow
            image = cv2.addWeighted(image, alpha, image, 0, gamma)
        
        if contrast != 0:
            f = 131 * (contrast + 127) / (127 * (131 - contrast))
            alpha = f
            gamma = 127 * (1 - f)
            image = cv2.addWeighted(image, alpha, image, 0, gamma)
        
        return image
    
    def auto_enhance(self, image):
        """
        Automatically enhance the image using histogram equalization.
        
        Args:
            image: Input image in BGR format
            
        Returns:
            numpy.ndarray: Enhanced image
        """
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        
        # Convert back to BGR
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    def white_balance(self, image):
        """
        Apply automatic white balance correction.
        
        Args:
            image: Input image in BGR format
            
        Returns:
            numpy.ndarray: Color-corrected image
        """
        result = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        avg_a = np.average(result[:, :, 1])
        avg_b = np.average(result[:, :, 2])
        
        result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
        
        return cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    
    def remove_red_eyes(self, image):
        """
        Detect and remove red eyes from the image.
        
        Args:
            image: Input image in BGR format
            
        Returns:
            numpy.ndarray: Image with red eyes corrected
        """
        result = image.copy()
        face = self.detect_face(image)
        
        if face is None:
            return result
        
        eyes = self.detect_eyes(image, face)
        
        for (ex, ey, ew, eh) in eyes:
            eye_region = result[ey:ey+eh, ex:ex+ew]
            
            b, g, r = cv2.split(eye_region)
            
            # Find red pixels
            bg = cv2.add(b, g)
            mask = ((r > 150) & (r > bg)).astype(np.uint8) * 255
            
            # Replace red with average of blue and green
            mean = (b.astype(np.float32) + g.astype(np.float32)) / 2
            eye_region[:, :, 2] = np.where(mask, mean, r).astype(np.uint8)
        
        return result
    
    def smooth_skin(self, image, strength=30):
        """
        Apply skin smoothing effect while preserving details.
        
        Args:
            image: Input image in BGR format
            strength: Smoothing strength (0-100)
            
        Returns:
            numpy.ndarray: Image with smoothed skin
        """
        # Apply bilateral filter for edge-preserving smoothing
        d = max(1, strength // 10)
        sigma_color = strength * 2
        sigma_space = strength // 2
        
        smoothed = cv2.bilateralFilter(image, d, sigma_color, sigma_space)
        
        return smoothed
    
    def sharpen(self, image, strength=1.0):
        """
        Sharpen the image.
        
        Args:
            image: Input image in BGR format
            strength: Sharpening strength (0.0 to 3.0)
            
        Returns:
            numpy.ndarray: Sharpened image
        """
        kernel = np.array([
            [-1, -1, -1],
            [-1, 9 + strength, -1],
            [-1, -1, -1]
        ]) / (1 + strength)
        
        sharpened = cv2.filter2D(image, -1, kernel)
        
        return sharpened
    
    def denoise(self, image, strength=10):
        """
        Remove noise from the image.
        
        Args:
            image: Input image in BGR format
            strength: Denoising strength (1-30)
            
        Returns:
            numpy.ndarray: Denoised image
        """
        return cv2.fastNlMeansDenoisingColored(image, None, strength, strength, 7, 21)
    
    def crop_to_face(self, image, size_name="35x45 mm (EU)", padding_percent=50):
        """
        Crop the image to center on the face with standard passport photo proportions.
        
        Args:
            image: Input image in BGR format
            size_name: Name of the target photo size
            padding_percent: Extra padding around the face (percentage)
            
        Returns:
            numpy.ndarray: Cropped image
        """
        face = self.detect_face(image)
        
        if face is None:
            # If no face detected, return the original image
            return image
        
        x, y, w, h = face
        
        # Get target aspect ratio
        if size_name in self.PHOTO_SIZES and self.PHOTO_SIZES[size_name]:
            target_w, target_h = self.PHOTO_SIZES[size_name]
            aspect_ratio = target_w / target_h
        else:
            aspect_ratio = 35 / 45  # Default passport ratio
        
        # Calculate crop dimensions
        face_center_x = x + w // 2
        face_center_y = y + h // 2
        
        # Add padding
        padding = int(max(w, h) * padding_percent / 100)
        
        crop_h = h + 2 * padding
        crop_w = int(crop_h * aspect_ratio)
        
        # Make sure the face is properly positioned (usually slightly above center)
        crop_y = face_center_y - int(crop_h * 0.4)
        crop_x = face_center_x - crop_w // 2
        
        # Ensure crop area is within image bounds
        img_h, img_w = image.shape[:2]
        
        crop_x = max(0, min(crop_x, img_w - crop_w))
        crop_y = max(0, min(crop_y, img_h - crop_h))
        
        # Adjust crop dimensions if they exceed image bounds
        if crop_x + crop_w > img_w:
            crop_w = img_w - crop_x
        if crop_y + crop_h > img_h:
            crop_h = img_h - crop_y
        
        cropped = image[crop_y:crop_y + crop_h, crop_x:crop_x + crop_w]
        
        # Resize to target dimensions
        if size_name in self.PHOTO_SIZES and self.PHOTO_SIZES[size_name]:
            target_size = self.PHOTO_SIZES[size_name]
            cropped = cv2.resize(cropped, target_size, interpolation=cv2.INTER_LANCZOS4)
        
        return cropped
    
    def change_background(self, image, new_color=(255, 255, 255), threshold=30):
        """
        Change the background color of the image.
        
        Args:
            image: Input image in BGR format
            new_color: New background color in BGR format
            threshold: Color difference threshold for background detection
            
        Returns:
            numpy.ndarray: Image with new background
        """
        result = image.copy()
        
        # Create a mask using GrabCut algorithm
        face = self.detect_face(image)
        
        if face is None:
            return result
        
        mask = np.zeros(image.shape[:2], np.uint8)
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)
        
        # Define rectangle around the face with padding
        x, y, w, h = face
        padding = int(max(w, h) * 0.5)
        rect = (
            max(0, x - padding),
            max(0, y - padding),
            min(image.shape[1], w + 2 * padding),
            min(image.shape[0], h + 2 * padding)
        )
        
        try:
            cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
        except cv2.error:
            return result
        
        # Create mask where 0 and 2 are background, 1 and 3 are foreground
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        
        # Apply new background color
        background = np.full(image.shape, new_color, dtype=np.uint8)
        result = image * mask2[:, :, np.newaxis] + background * (1 - mask2[:, :, np.newaxis])
        
        return result.astype(np.uint8)
    
    def resize_image(self, image, size_name):
        """
        Resize image to standard passport photo size.
        
        Args:
            image: Input image in BGR format
            size_name: Name of the target size
            
        Returns:
            numpy.ndarray: Resized image
        """
        if size_name not in self.PHOTO_SIZES or self.PHOTO_SIZES[size_name] is None:
            return image
        
        target_size = self.PHOTO_SIZES[size_name]
        return cv2.resize(image, target_size, interpolation=cv2.INTER_LANCZOS4)
    
    def apply_all_enhancements(self, image, options=None):
        """
        Apply all enhancements based on options.
        
        Args:
            image: Input image in BGR format
            options: Dictionary of enhancement options
            
        Returns:
            numpy.ndarray: Fully enhanced image
        """
        if options is None:
            options = {
                'auto_straighten': True,
                'auto_enhance': True,
                'white_balance': True,
                'denoise': True,
                'smooth_skin': False,
                'sharpen': True,
                'remove_red_eyes': True
            }
        
        result = image.copy()
        
        if options.get('auto_straighten', True):
            result = self.auto_straighten(result)
        
        if options.get('denoise', True):
            result = self.denoise(result, strength=10)
        
        if options.get('auto_enhance', True):
            result = self.auto_enhance(result)
        
        if options.get('white_balance', True):
            result = self.white_balance(result)
        
        if options.get('remove_red_eyes', True):
            result = self.remove_red_eyes(result)
        
        if options.get('smooth_skin', False):
            result = self.smooth_skin(result, strength=30)
        
        if options.get('sharpen', True):
            result = self.sharpen(result, strength=0.5)
        
        return result
