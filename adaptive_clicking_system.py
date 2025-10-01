#!/usr/bin/env python3
"""
Adaptive Clicking System for GlobalExam AI
==========================================

This system handles the fact that different question types have answers
in completely different locations:

1. True/False - Fixed positions
2. Multiple Choice - Fixed positions  
3. Remake phrase - Dynamic positions (need to find text)
4. Drag & drop - Dynamic positions (need to find elements)
5. Fill blanks - Dynamic input field positions

The system will:
- Detect question type from screen content
- Use appropriate clicking strategy for each type
- Find dynamic answer positions using image recognition
- Fall back to coordinate-based clicking when needed
"""

import pyautogui
import cv2
import numpy as np
import time
import re
from PIL import Image, ImageDraw
import pytesseract
from typing import List, Tuple, Dict, Optional

class AdaptiveClickingSystem:
    """
    Smart clicking system that adapts to different question layouts
    """
    
    def __init__(self):
        # Configure PyAutoGUI
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.2
        
        # Fixed coordinates for standard question types
        self.fixed_coordinates = {
            'true_false': {
                'true': [(850, 600), (920, 640), (800, 580)],
                'false': [(1050, 600), (1120, 640), (1000, 580)]
            },
            'multiple_choice': {
                'a': [(400, 500), (450, 520), (380, 480)],
                'b': [(400, 550), (450, 570), (380, 530)],
                'c': [(400, 600), (450, 620), (380, 580)],
                'd': [(400, 650), (450, 670), (380, 630)]
            }
        }
        
        # Text patterns to identify question types
        self.question_patterns = {
            'true_false': [
                r'true.*false',
                r'vrai.*faux',
                r'correct.*incorrect',
                r'right.*wrong'
            ],
            'multiple_choice': [
                r'[A-D]\)',
                r'choose.*option',
                r'select.*answer'
            ],
            'remake_phrase': [
                r'remake.*phrase',
                r'rearrange.*words',
                r'put.*order',
                r'organize.*sentence'
            ],
            'drag_drop': [
                r'drag.*drop',
                r'match.*items',
                r'connect.*pairs'
            ],
            'fill_blank': [
                r'fill.*blank',
                r'complete.*sentence',
                r'type.*answer'
            ]
        }
        
        print("[ADAPTIVE] Adaptive clicking system initialized")
    
    def capture_screen(self) -> np.ndarray:
        """Capture current screen as numpy array"""
        try:
            screenshot = pyautogui.screenshot()
            return np.array(screenshot)
        except Exception as e:
            print(f"[ERROR] Screen capture failed: {e}")
            return None
    
    def extract_text_from_screen(self, image: np.ndarray) -> str:
        """Extract text from screen using OCR"""
        try:
            # Convert to PIL Image for tesseract
            pil_image = Image.fromarray(image)
            
            # Extract text
            text = pytesseract.image_to_string(pil_image, lang='eng+fra')
            return text.lower()
            
        except Exception as e:
            print(f"[ERROR] OCR failed: {e}")
            return ""
    
    def detect_question_type(self, screen_text: str) -> str:
        """
        Detect question type from screen text
        
        Args:
            screen_text: Text extracted from screen
            
        Returns:
            Question type string
        """
        print(f"[DETECT] Analyzing screen text...")
        
        # Check each pattern type
        for question_type, patterns in self.question_patterns.items():
            for pattern in patterns:
                if re.search(pattern, screen_text, re.IGNORECASE):
                    print(f"[DETECT] Found {question_type} pattern: {pattern}")
                    return question_type
        
        # Fallback detection based on visual elements
        return self.detect_by_visual_elements()
    
    def detect_by_visual_elements(self) -> str:
        """Detect question type by looking for visual elements"""
        print("[DETECT] Using visual element detection...")
        
        screen = self.capture_screen()
        if screen is None:
            return 'multiple_choice'  # Default fallback
        
        # Convert to grayscale for analysis
        gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
        
        # Look for button-like elements
        # True/False usually has 2 large buttons
        # Multiple choice has 4 smaller buttons
        # Other types have scattered elements
        
        # Find contours (potential buttons)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Analyze contour sizes and positions
        button_like_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if 1000 < area < 50000:  # Button-sized areas
                x, y, w, h = cv2.boundingRect(contour)
                if 50 < w < 300 and 20 < h < 100:  # Button-like dimensions
                    button_like_contours.append((x, y, w, h))
        
        print(f"[DETECT] Found {len(button_like_contours)} button-like elements")
        
        # Classify based on button count and layout
        if len(button_like_contours) == 2:
            return 'true_false'
        elif len(button_like_contours) >= 4:
            return 'multiple_choice'
        else:
            return 'remake_phrase'  # Dynamic layout
    
    def find_clickable_text(self, target_text: str, screen: np.ndarray) -> List[Tuple[int, int]]:
        """
        Find clickable text elements on screen
        
        Args:
            target_text: Text to find and click
            screen: Screen image as numpy array
            
        Returns:
            List of (x, y) coordinates where text was found
        """
        print(f"[SEARCH] Looking for clickable text: '{target_text}'")
        
        try:
            # Convert to PIL for tesseract
            pil_image = Image.fromarray(screen)
            
            # Get detailed OCR data with bounding boxes
            ocr_data = pytesseract.image_to_data(pil_image, output_type=pytesseract.Output.DICT)
            
            found_positions = []
            
            # Search through OCR results
            for i in range(len(ocr_data['text'])):
                text = ocr_data['text'][i].strip().lower()
                confidence = int(ocr_data['conf'][i])
                
                if confidence > 30 and target_text.lower() in text:
                    x = ocr_data['left'][i] + ocr_data['width'][i] // 2
                    y = ocr_data['top'][i] + ocr_data['height'][i] // 2
                    
                    found_positions.append((x, y))
                    print(f"[FOUND] '{text}' at ({x}, {y}) confidence: {confidence}")
            
            return found_positions
            
        except Exception as e:
            print(f"[ERROR] Text search failed: {e}")
            return []
    
    def find_input_fields(self, screen: np.ndarray) -> List[Tuple[int, int]]:
        """
        Find input fields on screen
        
        Args:
            screen: Screen image as numpy array
            
        Returns:
            List of (x, y) coordinates of input fields
        """
        print("[SEARCH] Looking for input fields...")
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
            
            # Look for rectangular input field shapes
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            input_positions = []
            
            for contour in contours:
                # Check if contour looks like an input field
                x, y, w, h = cv2.boundingRect(contour)
                
                # Input fields are typically wide and not too tall
                if w > 100 and 20 < h < 60 and w/h > 3:
                    center_x = x + w // 2
                    center_y = y + h // 2
                    input_positions.append((center_x, center_y))
                    print(f"[FOUND] Input field at ({center_x}, {center_y})")
            
            return input_positions
            
        except Exception as e:
            print(f"[ERROR] Input field search failed: {e}")
            return []
    
    def click_answer(self, question_type: str, answer: str) -> bool:
        """
        Click answer using appropriate strategy for question type
        
        Args:
            question_type: Type of question detected
            answer: Answer to click/type
            
        Returns:
            True if click was successful
        """
        print(f"\n[CLICK] Answering {question_type} question: {answer}")
        
        screen = self.capture_screen()
        if screen is None:
            return False
        
        try:
            if question_type == 'true_false':
                return self._click_true_false(answer)
            
            elif question_type == 'multiple_choice':
                return self._click_multiple_choice(answer)
            
            elif question_type == 'remake_phrase':
                return self._click_remake_phrase(answer, screen)
            
            elif question_type == 'fill_blank':
                return self._click_fill_blank(answer, screen)
            
            elif question_type == 'drag_drop':
                return self._click_drag_drop(answer, screen)
            
            else:
                print(f"[ERROR] Unknown question type: {question_type}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Click failed: {e}")
            return False
    
    def _click_true_false(self, answer: str) -> bool:
        """Click True/False using fixed coordinates"""
        answer = answer.lower()
        
        if answer not in ['true', 'false', 'vrai', 'faux']:
            # Convert common variations
            if answer in ['yes', 'oui', 'correct', '1']:
                answer = 'true'
            elif answer in ['no', 'non', 'incorrect', '0']:
                answer = 'false'
            else:
                print(f"[ERROR] Invalid T/F answer: {answer}")
                return False
        
        # Normalize to true/false
        if answer in ['vrai', 'yes', 'oui', 'correct', '1']:
            answer = 'true'
        elif answer in ['faux', 'no', 'non', 'incorrect', '0']:
            answer = 'false'
        
        coordinates = self.fixed_coordinates['true_false'].get(answer, [])
        
        for i, (x, y) in enumerate(coordinates):
            print(f"[CLICK] Trying T/F coordinate {i+1}: ({x}, {y})")
            
            pyautogui.moveTo(x, y, duration=0.3)
            time.sleep(0.2)
            pyautogui.click()
            time.sleep(0.5)
            
            # Simple validation - check if something changed
            if self._validate_click():
                print(f"[SUCCESS] T/F click successful")
                return True
        
        print(f"[FAILED] All T/F coordinates failed")
        return False
    
    def _click_multiple_choice(self, answer: str) -> bool:
        """Click Multiple Choice using fixed coordinates"""
        answer = answer.lower()
        
        if answer not in ['a', 'b', 'c', 'd']:
            print(f"[ERROR] Invalid MC answer: {answer}")
            return False
        
        coordinates = self.fixed_coordinates['multiple_choice'].get(answer, [])
        
        for i, (x, y) in enumerate(coordinates):
            print(f"[CLICK] Trying MC coordinate {i+1}: ({x}, {y})")
            
            pyautogui.moveTo(x, y, duration=0.3)
            time.sleep(0.2)
            pyautogui.click()
            time.sleep(0.5)
            
            if self._validate_click():
                print(f"[SUCCESS] MC click successful")
                return True
        
        print(f"[FAILED] All MC coordinates failed")
        return False
    
    def _click_remake_phrase(self, answer: str, screen: np.ndarray) -> bool:
        """Click words for remake phrase questions"""
        print(f"[REMAKE] Looking for words to click in order: {answer}")
        
        # Split answer into individual words
        words = answer.split()
        
        for word in words:
            print(f"[REMAKE] Looking for word: '{word}'")
            
            # Find this word on screen
            positions = self.find_clickable_text(word, screen)
            
            if positions:
                # Click the first occurrence
                x, y = positions[0]
                print(f"[REMAKE] Clicking '{word}' at ({x}, {y})")
                
                pyautogui.moveTo(x, y, duration=0.3)
                time.sleep(0.2)
                pyautogui.click()
                time.sleep(0.8)  # Wait between word clicks
                
                # Update screen for next word
                screen = self.capture_screen()
                if screen is None:
                    return False
            else:
                print(f"[REMAKE] Could not find word: '{word}'")
                return False
        
        print(f"[REMAKE] All words clicked successfully")
        return True
    
    def _click_fill_blank(self, answer: str, screen: np.ndarray) -> bool:
        """Fill in blank questions"""
        print(f"[FILL] Looking for input field to type: '{answer}'")
        
        # Find input fields
        input_positions = self.find_input_fields(screen)
        
        if not input_positions:
            # Fallback to fixed coordinates
            input_positions = [(1000, 620), (900, 600), (1100, 650)]
        
        for x, y in input_positions:
            print(f"[FILL] Trying input field at ({x}, {y})")
            
            # Click to focus
            pyautogui.moveTo(x, y, duration=0.3)
            time.sleep(0.2)
            pyautogui.click()
            time.sleep(0.3)
            
            # Clear and type
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.typewrite(str(answer))
            time.sleep(0.5)
            
            print(f"[FILL] Typed '{answer}' in input field")
            return True
        
        print(f"[FILL] No input fields found")
        return False
    
    def _click_drag_drop(self, answer: str, screen: np.ndarray) -> bool:
        """Handle drag and drop questions"""
        print(f"[DRAG] Drag and drop not fully implemented yet")
        # This would need more complex logic to find source and target elements
        return False
    
    def _validate_click(self) -> bool:
        """Simple click validation"""
        # For now, just assume click worked
        # Could be enhanced with before/after screenshot comparison
        return True
    
    def submit_answer(self) -> bool:
        """Submit/validate the answer"""
        print("[SUBMIT] Looking for submit button...")
        
        # Common submit button coordinates
        submit_coords = [
            (960, 980),   # Common position 1
            (960, 950),   # Common position 2
            (1000, 980),  # Common position 3
            (920, 980),   # Common position 4
        ]
        
        for x, y in submit_coords:
            print(f"[SUBMIT] Trying submit button at ({x}, {y})")
            
            pyautogui.moveTo(x, y, duration=0.3)
            time.sleep(0.2)
            pyautogui.click()
            time.sleep(1.0)
            
            # Assume success for now
            print(f"[SUBMIT] Answer submitted")
            return True
        
        return False

def test_adaptive_system():
    """Test the adaptive clicking system"""
    print("Adaptive Clicking System - Test Mode")
    print("="*50)
    
    system = AdaptiveClickingSystem()
    
    # Test sequence
    test_cases = [
        ('true_false', 'true'),
        ('multiple_choice', 'c'),
        ('fill_blank', 'notice'),
        ('remake_phrase', 'the quick brown fox'),
    ]
    
    print("Starting test in 5 seconds...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    for question_type, answer in test_cases:
        print(f"\n{'='*50}")
        print(f"Testing: {question_type} = {answer}")
        print('='*50)
        
        # Capture and analyze screen
        screen = system.capture_screen()
        if screen is not None:
            text = system.extract_text_from_screen(screen)
            detected_type = system.detect_question_type(text)
            print(f"Detected type: {detected_type}")
        
        # Try to answer
        success = system.click_answer(question_type, answer)
        
        if success:
            system.submit_answer()
            print(f"✓ {question_type} test completed")
        else:
            print(f"✗ {question_type} test failed")
        
        time.sleep(3)  # Wait between tests

if __name__ == "__main__":
    test_adaptive_system()
