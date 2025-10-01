#!/usr/bin/env python3
"""
Test Script for Adaptive Clicking System
========================================

This script tests the new adaptive clicking system that can handle:
1. True/False questions (fixed positions)
2. Multiple choice questions (fixed positions)
3. Remake phrase questions (dynamic positions)
4. Fill in blank questions (dynamic input fields)

Run this on a GlobalExam question to test if it works correctly.
"""

import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from adaptive_clicking_system import AdaptiveClickingSystem
import time

def test_question_detection():
    """Test the question type detection"""
    print("="*60)
    print("TESTING QUESTION TYPE DETECTION")
    print("="*60)
    
    system = AdaptiveClickingSystem()
    
    # Capture current screen
    screen = system.capture_screen()
    if screen is None:
        print("❌ Could not capture screen")
        return
    
    # Extract text
    print("📖 Extracting text from screen...")
    text = system.extract_text_from_screen(screen)
    print(f"Found text (first 200 chars): {text[:200]}...")
    
    # Detect question type
    print("🔍 Detecting question type...")
    question_type = system.detect_question_type(text)
    print(f"✅ Detected question type: {question_type}")
    
    return question_type

def test_single_answer(question_type, answer):
    """Test answering a single question"""
    print(f"\n{'='*60}")
    print(f"TESTING: {question_type.upper()} = {answer}")
    print("="*60)
    
    system = AdaptiveClickingSystem()
    
    print("⏳ Starting test in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    # Try to answer
    print(f"🎯 Attempting to answer {question_type} with '{answer}'")
    success = system.click_answer(question_type, answer)
    
    if success:
        print("✅ Answer click successful!")
        
        # Try to submit
        print("📤 Attempting to submit answer...")
        submit_success = system.submit_answer()
        
        if submit_success:
            print("✅ Submit successful!")
            return True
        else:
            print("❌ Submit failed")
            return False
    else:
        print("❌ Answer click failed")
        return False

def interactive_test():
    """Interactive testing mode"""
    print("="*60)
    print("INTERACTIVE ADAPTIVE SYSTEM TEST")
    print("="*60)
    print("This will help you test the adaptive clicking system.")
    print("Make sure you're on a GlobalExam question page.")
    print("="*60)
    
    while True:
        print("\nOPTIONS:")
        print("1. Auto-detect question type")
        print("2. Test True/False question")
        print("3. Test Multiple Choice question")
        print("4. Test Fill in Blank question")
        print("5. Test Remake Phrase question")
        print("6. Exit")
        
        try:
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == '1':
                detected_type = test_question_detection()
                if detected_type:
                    # Ask for answer based on detected type
                    if detected_type == 'true_false':
                        answer = input("Enter answer (true/false): ").strip()
                        test_single_answer(detected_type, answer)
                    elif detected_type == 'multiple_choice':
                        answer = input("Enter answer (a/b/c/d): ").strip()
                        test_single_answer(detected_type, answer)
                    elif detected_type == 'fill_blank':
                        answer = input("Enter text to type: ").strip()
                        test_single_answer(detected_type, answer)
                    elif detected_type == 'remake_phrase':
                        answer = input("Enter words in order (space separated): ").strip()
                        test_single_answer(detected_type, answer)
            
            elif choice == '2':
                answer = input("Enter True/False answer (true/false): ").strip()
                test_single_answer('true_false', answer)
            
            elif choice == '3':
                answer = input("Enter Multiple Choice answer (a/b/c/d): ").strip()
                test_single_answer('multiple_choice', answer)
            
            elif choice == '4':
                answer = input("Enter text to type: ").strip()
                test_single_answer('fill_blank', answer)
            
            elif choice == '5':
                answer = input("Enter words in correct order (space separated): ").strip()
                test_single_answer('remake_phrase', answer)
            
            elif choice == '6':
                print("Exiting test...")
                break
            
            else:
                print("Invalid choice. Please select 1-6.")
        
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

def quick_test_sequence():
    """Quick test of common question types"""
    print("="*60)
    print("QUICK TEST SEQUENCE")
    print("="*60)
    print("This will test the most common question types.")
    print("Position your browser on a GlobalExam question.")
    print("="*60)
    
    # Auto-detect first
    detected_type = test_question_detection()
    
    if detected_type:
        print(f"\n🎯 Detected: {detected_type}")
        
        # Suggest appropriate test based on detection
        if detected_type == 'true_false':
            print("💡 Suggestion: Try 'true' or 'false'")
            answer = input("Enter your answer: ").strip()
            test_single_answer(detected_type, answer)
        
        elif detected_type == 'multiple_choice':
            print("💡 Suggestion: Try 'c' (statistically most common)")
            answer = input("Enter your answer (a/b/c/d): ").strip() or 'c'
            test_single_answer(detected_type, answer)
        
        elif detected_type == 'fill_blank':
            print("💡 Suggestion: Try 'notice' (common answer)")
            answer = input("Enter text to type: ").strip() or 'notice'
            test_single_answer(detected_type, answer)
        
        elif detected_type == 'remake_phrase':
            print("💡 This requires the correct word order")
            answer = input("Enter words in correct order: ").strip()
            test_single_answer(detected_type, answer)
        
        else:
            print("❓ Unknown question type detected")

def main():
    """Main test function"""
    print("GlobalExam AI - Adaptive System Tester")
    print("="*50)
    
    print("\nTEST MODES:")
    print("1. Interactive test (recommended)")
    print("2. Quick test sequence")
    print("3. Exit")
    
    try:
        choice = input("\nSelect mode (1-3): ").strip()
        
        if choice == '1':
            interactive_test()
        elif choice == '2':
            quick_test_sequence()
        elif choice == '3':
            print("Exiting...")
        else:
            print("Invalid choice.")
    
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
