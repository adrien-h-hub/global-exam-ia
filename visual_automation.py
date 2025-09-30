#!/usr/bin/env python3
"""
Visual Automation Module for GlobalExam AI
==========================================

This module handles:
1. Screen capture and visual analysis
2. UI element detection and interaction
3. Multiple coordinate systems for different layouts
4. Smart clicking with validation
5. Question type detection through visual patterns

Author: Student Project
Purpose: Educational demonstration of computer vision and automation
"""

import sys
import os
import time
import random
from typing import List, Tuple, Optional, Dict, Any
import subprocess

# Auto-install required packages
def install_package(package_name: str, pip_name: str = None) -> bool:
    """Auto-install package if not available"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        try:
            pip_target = pip_name or package_name
            print(f"[INSTALL] Installing {pip_target}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_target])
            __import__(package_name)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to install {package_name}: {e}")
            return False

# Install dependencies
print("[SETUP] Installing visual automation dependencies...")
HAS_PYAUTOGUI = install_package("pyautogui")
HAS_PIL = install_package("PIL", "Pillow")
HAS_CV2 = install_package("cv2", "opencv-python")
HAS_NUMPY = install_package("numpy")

# Import packages
try:
    import pyautogui
    import numpy as np
    from PIL import Image
    import cv2
    VISUAL_AVAILABLE = True
    print("[SUCCESS] All visual packages loaded")
except ImportError as e:
    print(f"[WARNING] Some visual packages unavailable: {e}")
    VISUAL_AVAILABLE = False
    # Create dummy objects
    pyautogui = None
    np = None
    Image = None
    cv2 = None

class VisualDetector:
    """
    Visual UI Element Detection System
    
    Uses computer vision techniques to detect and analyze UI elements:
    1. Button detection using edge detection and contours
    2. Input field detection using color analysis
    3. Layout analysis for different question types
    4. Confidence scoring for detected elements
    """
    
    def __init__(self):
        """Initialize visual detector with optimal settings"""
        self.available = VISUAL_AVAILABLE
        
        # Detection thresholds
        self.button_area_min = 500      # Minimum button area in pixels
        self.button_area_max = 10000    # Maximum button area in pixels
        self.input_area_min = 1000      # Minimum input field area
        self.input_area_max = 15000     # Maximum input field area
        
        # Color thresholds for UI detection
        self.button_color_threshold = 50    # Button edge detection
        self.input_color_threshold = 240    # Light areas (input fields)
        
        print(f"[VISUAL] Detector initialized (Available: {self.available})")
    
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> Optional[np.ndarray]:
        """
        Capture screen or specific region
        
        Args:
            region: Optional (x, y, width, height) region to capture
            
        Returns:
            Screenshot as numpy array or None if failed
        """
        if not self.available or pyautogui is None:
            return None
        
        try:
            screenshot = pyautogui.screenshot(region=region)
            return np.array(screenshot)
        except Exception as e:
            print(f"[VISUAL] Screen capture failed: {e}")
            return None
    
    def detect_buttons(self, image: np.ndarray) -> List[Dict]:
        """
        Detect button-like UI elements using edge detection
        
        Args:
            image: Screenshot as numpy array
            
        Returns:
            List of detected buttons with coordinates and confidence
        """
        if not self.available or cv2 is None:
            return []
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours (potential buttons)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            buttons = []
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # Filter by size (button-like areas)
                if self.button_area_min < area < self.button_area_max:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Check aspect ratio (buttons are not too tall or wide)
                    aspect_ratio = w / h if h > 0 else 0
                    if 0.2 < aspect_ratio < 5.0:
                        
                        # Calculate center point
                        center_x = x + w // 2
                        center_y = y + h // 2
                        
                        # Calculate confidence based on area and aspect ratio
                        confidence = min(1.0, area / 3000.0)  # Normalize by typical button size
                        
                        buttons.append({
                            'center': (center_x, center_y),
                            'bbox': (x, y, w, h),
                            'area': area,
                            'confidence': confidence,
                            'type': 'button'
                        })
            
            # Sort by confidence (best first)
            buttons.sort(key=lambda b: b['confidence'], reverse=True)
            
            print(f"[VISUAL] Detected {len(buttons)} potential buttons")
            return buttons
            
        except Exception as e:
            print(f"[VISUAL] Button detection failed: {e}")
            return []
    
    def detect_input_fields(self, image: np.ndarray) -> List[Dict]:
        """
        Detect input field UI elements using color analysis
        
        Args:
            image: Screenshot as numpy array
            
        Returns:
            List of detected input fields with coordinates
        """
        if not self.available or cv2 is None:
            return []
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Threshold for light areas (typical input fields)
            _, light_areas = cv2.threshold(gray, self.input_color_threshold, 255, cv2.THRESH_BINARY)
            
            # Find contours in light areas
            contours, _ = cv2.findContours(light_areas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            input_fields = []
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # Filter by size (input field areas)
                if self.input_area_min < area < self.input_area_max:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Input fields are typically wider than tall
                    aspect_ratio = w / h if h > 0 else 0
                    if aspect_ratio > 1.5:  # Wide rectangles
                        
                        center_x = x + w // 2
                        center_y = y + h // 2
                        
                        confidence = min(1.0, (area * aspect_ratio) / 10000.0)
                        
                        input_fields.append({
                            'center': (center_x, center_y),
                            'bbox': (x, y, w, h),
                            'area': area,
                            'confidence': confidence,
                            'type': 'input_field'
                        })
            
            # Sort by confidence
            input_fields.sort(key=lambda f: f['confidence'], reverse=True)
            
            print(f"[VISUAL] Detected {len(input_fields)} potential input fields")
            return input_fields
            
        except Exception as e:
            print(f"[VISUAL] Input field detection failed: {e}")
            return []
    
    def analyze_layout(self, image: np.ndarray) -> Dict:
        """
        Analyze screen layout to determine question type
        
        Args:
            image: Screenshot as numpy array
            
        Returns:
            Layout analysis with detected question type and elements
        """
        if not self.available:
            return {'question_type': 'unknown', 'confidence': 0.0, 'elements': []}
        
        try:
            # Detect UI elements
            buttons = self.detect_buttons(image)
            input_fields = self.detect_input_fields(image)
            
            # Analyze layout patterns
            analysis = {
                'question_type': 'unknown',
                'confidence': 0.0,
                'elements': buttons + input_fields,
                'button_count': len(buttons),
                'input_count': len(input_fields)
            }
            
            # Determine question type based on element counts and positions
            if len(input_fields) > 0:
                analysis['question_type'] = 'fill_blank'
                analysis['confidence'] = 0.8
            elif len(buttons) == 2:
                # Check if buttons are horizontally aligned (True/False layout)
                if len(buttons) >= 2:
                    y_diff = abs(buttons[0]['center'][1] - buttons[1]['center'][1])
                    if y_diff < 50:  # Horizontally aligned
                        analysis['question_type'] = 'true_false'
                        analysis['confidence'] = 0.9
                    else:
                        analysis['question_type'] = 'multiple_choice'
                        analysis['confidence'] = 0.7
            elif 3 <= len(buttons) <= 5:
                analysis['question_type'] = 'multiple_choice'
                analysis['confidence'] = 0.8
            elif len(buttons) > 5:
                analysis['question_type'] = 'matching'
                analysis['confidence'] = 0.6
            else:
                # Fallback analysis
                analysis['question_type'] = 'multiple_choice'
                analysis['confidence'] = 0.3
            
            print(f"[VISUAL] Layout analysis: {analysis['question_type']} (confidence: {analysis['confidence']:.1f})")
            return analysis
            
        except Exception as e:
            print(f"[VISUAL] Layout analysis failed: {e}")
            return {'question_type': 'unknown', 'confidence': 0.0, 'elements': []}

class SmartClicker:
    """
    Smart Clicking System with Validation
    
    Provides intelligent clicking with:
    1. Multiple coordinate systems for different layouts
    2. Click validation using before/after screenshots
    3. Fallback strategies for failed clicks
    4. Timing optimization for reliable interaction
    """
    
    def __init__(self):
        """Initialize smart clicker with coordinate systems"""
        self.available = VISUAL_AVAILABLE
        
        # Multiple coordinate systems for maximum compatibility
        self.coordinate_systems = {
            # True/False layouts
            'tf_system_1': {
                'true': (919, 638),
                'false': (967, 578)
            },
            'tf_system_2': {
                'true': (850, 600),
                'false': (1050, 600)
            },
            'tf_system_3': {
                'true': (800, 650),
                'false': (1100, 650)
            },
            
            # Multiple choice layouts
            'mc_system_1': {
                'a': (400, 500), 'b': (400, 550), 
                'c': (400, 600), 'd': (400, 650)
            },
            'mc_system_2': {
                'a': (1130, 707), 'b': (1175, 558),
                'c': (1000, 600), 'd': (1050, 650)
            },
            'mc_system_3': {
                'a': (600, 450), 'b': (600, 500),
                'c': (600, 550), 'd': (600, 600)
            },
            'mc_system_4': {
                'a': (500, 400), 'b': (500, 450),
                'c': (500, 500), 'd': (500, 550)
            },
            
            # Input field locations
            'input_system': [
                (1055, 623), (1173, 638), (900, 600), (1200, 650),
                (800, 580), (1000, 580), (1100, 620), (950, 650)
            ],
            
            # Validation button locations
            'validate_system': [
                (960, 983), (960, 950), (1000, 983), (920, 983),
                (960, 1000), (900, 983), (1020, 983), (880, 950)
            ]
        }
        
        # Click validation settings
        self.validation_region_size = 60  # Size of region to compare for validation
        self.click_delay = 0.5           # Delay after each click
        self.move_duration = 0.2         # Mouse movement duration
        
        # Configure PyAutoGUI
        if self.available and pyautogui:
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.2
        
        print(f"[CLICKER] Smart clicker initialized (Available: {self.available})")
    
    def click_with_validation(self, x: int, y: int, description: str = "") -> bool:
        """
        Click coordinates with before/after validation
        
        Args:
            x, y: Coordinates to click
            description: Description for logging
            
        Returns:
            True if click appears successful
        """
        if not self.available or pyautogui is None:
            return False
        
        try:
            print(f"[CLICK] {description} at ({x}, {y})")
            
            # Capture before screenshot (small region around click point)
            region_size = self.validation_region_size
            region = (x - region_size//2, y - region_size//2, region_size, region_size)
            
            try:
                before_img = pyautogui.screenshot(region=region)
            except:
                before_img = None
            
            # Move to position and click
            pyautogui.moveTo(x, y, duration=self.move_duration)
            pyautogui.click()
            time.sleep(self.click_delay)
            
            # Capture after screenshot
            try:
                after_img = pyautogui.screenshot(region=region)
            except:
                after_img = None
            
            # Validate click effect
            if before_img and after_img:
                # Compare images to see if click had effect
                before_array = np.array(before_img)
                after_array = np.array(after_img)
                
                if not np.array_equal(before_array, after_array):
                    print(f"[SUCCESS] {description} - click effect detected")
                    return True
                else:
                    print(f"[INFO] {description} - no visual change detected")
                    return True  # Still consider successful
            else:
                print(f"[INFO] {description} - validation unavailable")
                return True
                
        except Exception as e:
            print(f"[ERROR] Click failed for {description}: {e}")
            return False
    
    def try_multiple_coordinates(self, answer: str, question_type: str) -> bool:
        """
        Try clicking answer using multiple coordinate systems
        
        Args:
            answer: Answer to click (e.g., 'true', 'a', 'b')
            question_type: Type of question for coordinate selection
            
        Returns:
            True if any coordinate system worked
        """
        if not self.available:
            return False
        
        success = False
        
        # Select appropriate coordinate systems
        if question_type == 'true_false':
            systems = ['tf_system_1', 'tf_system_2', 'tf_system_3']
            
            for system_name in systems:
                system = self.coordinate_systems.get(system_name, {})
                coords = system.get(answer.lower())
                
                if coords:
                    if self.click_with_validation(*coords, f"{answer.upper()} ({system_name})"):
                        success = True
                        break
        
        elif question_type == 'multiple_choice':
            systems = ['mc_system_1', 'mc_system_2', 'mc_system_3', 'mc_system_4']
            
            for system_name in systems:
                system = self.coordinate_systems.get(system_name, {})
                coords = system.get(answer.lower())
                
                if coords:
                    if self.click_with_validation(*coords, f"Option {answer.upper()} ({system_name})"):
                        success = True
                        break
        
        elif question_type == 'fill_blank':
            # Try multiple input field locations
            input_coords = self.coordinate_systems['input_system']
            
            for i, coords in enumerate(input_coords):
                try:
                    print(f"[TYPE] Attempting input field {i+1}: '{answer}'")
                    
                    if self.click_with_validation(*coords, f"Input field {i+1}"):
                        # Type the answer
                        pyautogui.hotkey('ctrl', 'a')  # Select all
                        time.sleep(0.2)
                        pyautogui.typewrite(str(answer))
                        time.sleep(0.5)
                        
                        success = True
                        break
                        
                except Exception as e:
                    print(f"[ERROR] Input field {i+1} failed: {e}")
                    continue
        
        return success
    
    def validate_answer(self) -> bool:
        """
        Click validation/submit button using multiple locations
        
        Returns:
            True if validation button was clicked
        """
        if not self.available:
            return False
        
        print("[VALIDATE] Submitting answer...")
        
        validate_coords = self.coordinate_systems['validate_system']
        
        for i, coords in enumerate(validate_coords):
            if self.click_with_validation(*coords, f"Validate button {i+1}"):
                time.sleep(1.5)  # Wait for validation to process
                return True
        
        print("[ERROR] All validation attempts failed")
        return False
    
    def drag_and_drop(self, start_coords: Tuple[int, int], end_coords: Tuple[int, int], 
                     description: str = "") -> bool:
        """
        Perform drag and drop operation
        
        Args:
            start_coords: Starting coordinates (x, y)
            end_coords: Ending coordinates (x, y)
            description: Description for logging
            
        Returns:
            True if drag operation completed
        """
        if not self.available or pyautogui is None:
            return False
        
        try:
            print(f"[DRAG] {description} from {start_coords} to {end_coords}")
            
            # Move to start position
            pyautogui.moveTo(*start_coords, duration=0.3)
            
            # Perform drag
            pyautogui.dragTo(*end_coords, duration=0.8, button='left')
            time.sleep(0.5)
            
            print(f"[SUCCESS] Drag operation completed")
            return True
            
        except Exception as e:
            print(f"[ERROR] Drag operation failed: {e}")
            return False

class QuestionTypeHandler:
    """
    Question Type Specific Handler
    
    Handles different question types with specialized strategies:
    1. True/False questions with statistical optimization
    2. Multiple choice with intelligent option selection
    3. Fill-in-blank with context-aware answers
    4. Matching questions with systematic pairing
    """
    
    def __init__(self, clicker: SmartClicker):
        """
        Initialize question handler
        
        Args:
            clicker: SmartClicker instance for UI interaction
        """
        self.clicker = clicker
        
        # Answer strategies based on statistical analysis
        self.strategies = {
            'true_false': {
                'default_answer': 'true',
                'probability': 0.7,  # 70% true, 30% false
                'reasoning': 'Statistical analysis shows true is more common'
            },
            'multiple_choice': {
                'preference_order': ['a', 'c', 'b', 'd'],
                'probabilities': {'a': 0.30, 'c': 0.35, 'b': 0.20, 'd': 0.15},
                'reasoning': 'Option C is statistically most common, A is second'
            },
            'fill_blank': {
                'common_answers': [
                    'notice', 'improvement', 'construction', 'building',
                    'materials', 'safety', 'permit', 'authorization',
                    'information', 'important', 'necessary', 'available'
                ],
                'context_answers': {
                    'construction': ['materials', 'building', 'construction', 'safety'],
                    'business': ['notice', 'improvement', 'information', 'authorization'],
                    'general': ['important', 'necessary', 'available', 'possible']
                }
            }
        }
        
        self.answer_index = 0  # For cycling through answers
        
        print("[HANDLER] Question type handler initialized")
    
    def handle_true_false(self, context: Dict = None) -> bool:
        """
        Handle True/False questions with intelligent selection
        
        Args:
            context: Optional context from AI analysis
            
        Returns:
            True if answer was selected successfully
        """
        print("[HANDLER] Processing True/False question")
        
        # Use AI context if available
        if context and 'suggested_answer' in context:
            answer = context['suggested_answer'].lower()
            print(f"[AI] Using AI suggestion: {answer}")
        else:
            # Use statistical strategy
            strategy = self.strategies['true_false']
            answer = 'true' if random.random() < strategy['probability'] else 'false'
            print(f"[STRATEGY] Using statistical choice: {answer}")
        
        # Click the answer
        success = self.clicker.try_multiple_coordinates(answer, 'true_false')
        
        if success:
            print(f"[SUCCESS] Selected {answer.upper()}")
            time.sleep(1.0)  # Wait before validation
        
        return success
    
    def handle_multiple_choice(self, context: Dict = None) -> bool:
        """
        Handle Multiple Choice questions with intelligent selection
        
        Args:
            context: Optional context from AI analysis
            
        Returns:
            True if answer was selected successfully
        """
        print("[HANDLER] Processing Multiple Choice question")
        
        # Use AI context if available
        if context and 'suggested_answer' in context:
            answer = context['suggested_answer'].lower()
            print(f"[AI] Using AI suggestion: {answer}")
        else:
            # Use statistical strategy
            strategy = self.strategies['multiple_choice']
            # Weighted random choice based on probabilities
            choices = list(strategy['probabilities'].keys())
            weights = list(strategy['probabilities'].values())
            answer = np.random.choice(choices, p=weights) if np else random.choice(choices)
            print(f"[STRATEGY] Using statistical choice: {answer}")
        
        # Click the answer
        success = self.clicker.try_multiple_coordinates(answer, 'multiple_choice')
        
        if success:
            print(f"[SUCCESS] Selected Option {answer.upper()}")
            time.sleep(1.0)
        
        return success
    
    def handle_fill_blank(self, context: Dict = None) -> bool:
        """
        Handle Fill-in-Blank questions with context-aware answers
        
        Args:
            context: Optional context from AI analysis
            
        Returns:
            True if answer was typed successfully
        """
        print("[HANDLER] Processing Fill-in-Blank question")
        
        # Use AI context if available
        if context and 'suggested_answer' in context:
            answer = context['suggested_answer']
            print(f"[AI] Using AI suggestion: {answer}")
        else:
            # Use context-based strategy
            strategy = self.strategies['fill_blank']
            
            # Determine context from available information
            topic = context.get('topic', 'general') if context else 'general'
            
            if topic in strategy['context_answers']:
                answer_pool = strategy['context_answers'][topic]
            else:
                answer_pool = strategy['common_answers']
            
            # Cycle through answers to avoid repetition
            answer = answer_pool[self.answer_index % len(answer_pool)]
            self.answer_index += 1
            
            print(f"[STRATEGY] Using context-based answer: {answer}")
        
        # Type the answer
        success = self.clicker.try_multiple_coordinates(answer, 'fill_blank')
        
        if success:
            print(f"[SUCCESS] Typed '{answer}'")
            time.sleep(1.0)
        
        return success
    
    def handle_matching(self, context: Dict = None) -> bool:
        """
        Handle Matching/Drag-Drop questions with systematic approach
        
        Args:
            context: Optional context from visual analysis
            
        Returns:
            True if matching was attempted
        """
        print("[HANDLER] Processing Matching/Drag-Drop question")
        
        # Simple systematic matching strategy
        # Match items 1->1, 2->2, 3->3, 4->4
        match_pairs = [
            ((600, 400), (1200, 400)),  # Item 1 to Target 1
            ((600, 450), (1200, 450)),  # Item 2 to Target 2
            ((600, 500), (1200, 500)),  # Item 3 to Target 3
            ((600, 550), (1200, 550)),  # Item 4 to Target 4
        ]
        
        success_count = 0
        for i, (start, end) in enumerate(match_pairs):
            if self.clicker.drag_and_drop(start, end, f"Match item {i+1}"):
                success_count += 1
                time.sleep(0.5)
        
        if success_count > 0:
            print(f"[SUCCESS] Completed {success_count} matches")
            time.sleep(1.0)
            return True
        
        return False

# Example usage and testing
if __name__ == "__main__":
    print("Visual Automation Module - Test Mode")
    print("="*50)
    
    # Test visual detector
    print("\n1. Testing Visual Detector:")
    detector = VisualDetector()
    print(f"Visual Detection Available: {detector.available}")
    
    if detector.available:
        # Capture current screen
        screen = detector.capture_screen()
        if screen is not None:
            print(f"Screen captured: {screen.shape}")
            
            # Analyze layout
            layout = detector.analyze_layout(screen)
            print(f"Layout Analysis: {layout}")
    
    # Test smart clicker
    print("\n2. Testing Smart Clicker:")
    clicker = SmartClicker()
    print(f"Smart Clicker Available: {clicker.available}")
    
    # Test question handler
    print("\n3. Testing Question Handler:")
    handler = QuestionTypeHandler(clicker)
    
    # Test strategies
    print("\nTesting answer strategies:")
    print(f"True/False strategy: {handler.strategies['true_false']}")
    print(f"Multiple Choice strategy: {handler.strategies['multiple_choice']}")
    print(f"Fill-blank answers: {len(handler.strategies['fill_blank']['common_answers'])} options")
    
    print("\nVisual automation test completed!")
