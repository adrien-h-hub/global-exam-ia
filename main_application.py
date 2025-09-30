#!/usr/bin/env python3
"""
Main Application Module for GlobalExam AI
========================================

This is the main application that combines all modules:
1. Security system with daily codes and machine binding
2. OCR and AI analysis for intelligent question understanding
3. Visual automation for UI interaction
4. Comprehensive question handling for all types

Author: Student Project
Purpose: Educational demonstration of integrated AI automation system
"""

import sys
import os
import time
import argparse
from typing import Dict, Optional, Any
from pathlib import Path

# Add current directory to path for module imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import our custom modules
try:
    from security_system_v3 import OneTimeLicenseManager
    from ocr_ai_analysis import OCREngine, AIQuestionAnalyzer
    from visual_automation import VisualDetector, SmartClicker, QuestionTypeHandler
    MODULES_AVAILABLE = True
    print("[IMPORT] All modules imported successfully")
except ImportError as e:
    print(f"[ERROR] Module import failed: {e}")
    MODULES_AVAILABLE = False

class GlobalExamAI:
    """
    Main GlobalExam AI Application
    
    Integrates all subsystems for comprehensive automation:
    - Security: Daily codes, machine binding, approval system
    - Intelligence: OCR text reading, AI question analysis
    - Automation: Visual detection, smart clicking, multi-layout support
    - Reliability: Multiple fallback strategies, error recovery
    """
    
    def __init__(self, app_name: str = "GlobalExamAI"):
        """
        Initialize the complete GlobalExam AI system
        
        Args:
            app_name: Application name for configuration
        """
        self.app_name = app_name
        self.debug = True
        self.max_questions = 30
        
        # Initialize subsystems
        print(f"\n[INIT] Initializing {app_name}...")
        print("="*60)
        
        if not MODULES_AVAILABLE:
            raise RuntimeError("Required modules not available")
        
        # License system
        self.license_manager = OneTimeLicenseManager(app_name)
        print("[✓] Security system initialized")
        
        # OCR and AI analysis
        self.ocr_engine = OCREngine()
        self.ai_analyzer = AIQuestionAnalyzer()
        print("[✓] OCR and AI analysis initialized")
        
        # Visual automation
        self.visual_detector = VisualDetector()
        self.smart_clicker = SmartClicker()
        self.question_handler = QuestionTypeHandler(self.smart_clicker)
        print("[✓] Visual automation initialized")
        
        # Statistics tracking
        self.stats = {
            'questions_attempted': 0,
            'questions_successful': 0,
            'question_types': {},
            'start_time': None,
            'end_time': None
        }
        
        print(f"[✓] {app_name} fully initialized")
        print("="*60)
    
    def check_license_authorization(self) -> bool:
        """
        Check license authorization before running automation
        
        Returns:
            True if authorized to proceed
        """
        print("\n[LICENCE] Vérification de l'autorisation...")
        
        try:
            authorized = self.license_manager.check_authorization()
            
            if authorized:
                print("[LICENCE] ✓ Licence valide - démarrage de l'automatisation")
                return True
            else:
                print("[LICENCE] ✗ Licence invalide - impossible de continuer")
                return False
                
        except Exception as e:
            print(f"[LICENCE] Vérification échouée : {e}")
            return False
    
    def analyze_current_question(self) -> Dict[str, Any]:
        """
        Comprehensive analysis of current question using all available methods
        
        Returns:
            Combined analysis from visual detection, OCR, and AI
        """
        print("\n[ANALYSIS] Analyzing current question...")
        
        analysis = {
            'visual': None,
            'ocr_text': "",
            'ai_analysis': None,
            'final_type': 'unknown',
            'confidence': 0.0,
            'suggested_answer': None,
            'reasoning': ""
        }
        
        try:
            # Step 1: Visual analysis
            screen = self.visual_detector.capture_screen()
            if screen is not None:
                analysis['visual'] = self.visual_detector.analyze_layout(screen)
                print(f"[VISUAL] Detected: {analysis['visual']['question_type']} "
                      f"(confidence: {analysis['visual']['confidence']:.1f})")
            
            # Step 2: OCR text extraction
            if screen is not None and self.ocr_engine.available:
                # Try different regions for text extraction
                regions = [
                    (200, 200, 1200, 300),  # Question area
                    (200, 300, 1200, 500),  # Options area
                    None  # Full screen
                ]
                
                for region in regions:
                    if region:
                        region_screen = self.visual_detector.capture_screen(region)
                        if region_screen is not None:
                            text = self.ocr_engine.extract_text(region_screen)
                            if text:
                                analysis['ocr_text'] += " " + text
                    else:
                        text = self.ocr_engine.extract_text(screen)
                        if text:
                            analysis['ocr_text'] += " " + text
                
                analysis['ocr_text'] = analysis['ocr_text'].strip()
                if analysis['ocr_text']:
                    print(f"[OCR] Extracted: {analysis['ocr_text'][:100]}...")
            
            # Step 3: AI analysis of extracted text
            if analysis['ocr_text']:
                analysis['ai_analysis'] = self.ai_analyzer.analyze_question(analysis['ocr_text'])
                print(f"[AI] Analysis: {analysis['ai_analysis']['question_type']} "
                      f"-> {analysis['ai_analysis']['suggested_answer']} "
                      f"(confidence: {analysis['ai_analysis']['confidence']:.1f})")
            
            # Step 4: Combine analyses for final decision
            analysis = self._combine_analyses(analysis)
            
            print(f"[FINAL] Type: {analysis['final_type']}, "
                  f"Answer: {analysis['suggested_answer']}, "
                  f"Confidence: {analysis['confidence']:.1f}")
            
        except Exception as e:
            print(f"[ANALYSIS] Failed: {e}")
            # Fallback analysis
            analysis.update({
                'final_type': 'multiple_choice',
                'suggested_answer': 'a',
                'confidence': 0.3,
                'reasoning': 'Fallback due to analysis failure'
            })
        
        return analysis
    
    def _combine_analyses(self, analysis: Dict) -> Dict:
        """
        Combine visual, OCR, and AI analyses into final decision
        
        Args:
            analysis: Dictionary with individual analyses
            
        Returns:
            Updated analysis with final decision
        """
        visual = analysis.get('visual', {})
        ai = analysis.get('ai_analysis', {})
        
        # Priority system for determining final answer
        if ai and ai.get('confidence', 0) > 0.7:
            # High confidence AI analysis takes priority
            analysis.update({
                'final_type': ai['question_type'],
                'suggested_answer': ai['suggested_answer'],
                'confidence': ai['confidence'],
                'reasoning': f"AI analysis: {ai['reasoning']}"
            })
        elif visual and visual.get('confidence', 0) > 0.8:
            # High confidence visual analysis
            visual_type = visual['question_type']
            if visual_type == 'true_false':
                answer = 'true'  # Statistical preference
            elif visual_type == 'multiple_choice':
                answer = 'c'     # Statistical preference
            elif visual_type == 'fill_blank':
                answer = 'notice'  # Common answer
            else:
                answer = 'a'     # Fallback
            
            analysis.update({
                'final_type': visual_type,
                'suggested_answer': answer,
                'confidence': visual['confidence'],
                'reasoning': f"Visual detection: {visual_type}"
            })
        elif ai and ai.get('confidence', 0) > 0.4:
            # Medium confidence AI analysis
            analysis.update({
                'final_type': ai['question_type'],
                'suggested_answer': ai['suggested_answer'],
                'confidence': ai['confidence'],
                'reasoning': f"AI analysis (medium confidence): {ai['reasoning']}"
            })
        else:
            # Fallback to statistical best guesses
            analysis.update({
                'final_type': 'multiple_choice',
                'suggested_answer': 'c',
                'confidence': 0.4,
                'reasoning': 'Statistical fallback (C is most common)'
            })
        
        return analysis
    
    def answer_question(self, question_num: int) -> bool:
        """
        Answer a single question using comprehensive analysis
        
        Args:
            question_num: Question number for tracking
            
        Returns:
            True if question was answered successfully
        """
        print(f"\n{'='*70}")
        print(f"QUESTION {question_num}")
        print('='*70)
        
        try:
            # Save screenshot for debugging
            if self.debug:
                screen = self.visual_detector.capture_screen()
                if screen is not None:
                    from PIL import Image
                    img = Image.fromarray(screen)
                    img.save(f"question_{question_num:02d}_{int(time.time())}.png")
                    print(f"[DEBUG] Screenshot saved for question {question_num}")
            
            # Analyze question
            analysis = self.analyze_current_question()
            
            # Update statistics
            self.stats['questions_attempted'] += 1
            q_type = analysis['final_type']
            self.stats['question_types'][q_type] = self.stats['question_types'].get(q_type, 0) + 1
            
            # Answer based on analysis
            success = False
            
            if q_type == 'true_false':
                success = self.question_handler.handle_true_false(analysis)
            elif q_type == 'multiple_choice':
                success = self.question_handler.handle_multiple_choice(analysis)
            elif q_type == 'fill_blank':
                success = self.question_handler.handle_fill_blank(analysis)
            elif q_type == 'matching':
                success = self.question_handler.handle_matching(analysis)
            else:
                # Fallback: try multiple choice
                print("[FALLBACK] Unknown type, trying multiple choice")
                success = self.question_handler.handle_multiple_choice(analysis)
            
            # Validate answer
            if success:
                time.sleep(1.0)  # Wait before validation
                validation_success = self.smart_clicker.validate_answer()
                
                if validation_success:
                    self.stats['questions_successful'] += 1
                    print(f"[SUCCESS] Question {question_num} completed successfully")
                    return True
                else:
                    print(f"[WARNING] Question {question_num} answered but validation failed")
                    return False
            else:
                print(f"[ERROR] Question {question_num} answering failed")
                return False
                
        except Exception as e:
            print(f"[ERROR] Question {question_num} processing failed: {e}")
            return False
    
    def run_automation(self) -> Dict[str, Any]:
        """
        Run the complete automation system
        
        Returns:
            Statistics and results from the automation run
        """
        print("\n" + "="*70)
        print("GLOBALEXAM AI - ULTIMATE AUTOMATION SYSTEM")
        print("="*70)
        print("Features:")
        print("• Security: Daily codes + Machine binding")
        print("• Intelligence: OCR + AI question analysis")
        print("• Automation: Visual detection + Smart clicking")
        print("• Reliability: Multiple fallbacks + Error recovery")
        print("="*70)
        
        # License check
        if not self.check_license_authorization():
            return {'error': 'License authorization failed'}
        
        # Pre-flight checks
        print("\n[PREFLIGHT] System checks...")
        print(f"• OCR Available: {self.ocr_engine.available}")
        print(f"• Visual Detection: {self.visual_detector.available}")
        print(f"• Smart Clicking: {self.smart_clicker.available}")
        
        # Countdown
        print("\n[COUNTDOWN] Starting automation in:")
        for i in range(5, 0, -1):
            print(f"  {i} seconds...")
            time.sleep(1)
        
        print("\n[RUNNING] Automation started!")
        self.stats['start_time'] = time.time()
        
        # Main automation loop
        for question_num in range(1, self.max_questions + 1):
            try:
                success = self.answer_question(question_num)
                
                # Progress update
                success_rate = (self.stats['questions_successful'] / 
                               self.stats['questions_attempted']) * 100
                
                print(f"\n[PROGRESS] Question {question_num}: "
                      f"{'✓' if success else '✗'}")
                print(f"[PROGRESS] Success rate: "
                      f"{self.stats['questions_successful']}/{self.stats['questions_attempted']} "
                      f"({success_rate:.1f}%)")
                
                # Wait between questions
                time.sleep(2.5)
                
            except KeyboardInterrupt:
                print("\n[STOP] Automation stopped by user")
                break
            except Exception as e:
                print(f"[ERROR] Question {question_num} failed: {e}")
                time.sleep(1.0)  # Brief pause before continuing
        
        # Finalize statistics
        self.stats['end_time'] = time.time()
        duration = self.stats['end_time'] - self.stats['start_time']
        
        # Final report
        print(f"\n{'='*70}")
        print("AUTOMATION COMPLETED")
        print("="*70)
        print(f"Questions attempted: {self.stats['questions_attempted']}")
        print(f"Questions successful: {self.stats['questions_successful']}")
        print(f"Success rate: {(self.stats['questions_successful']/max(1,self.stats['questions_attempted']))*100:.1f}%")
        print(f"Duration: {duration:.1f} seconds")
        print(f"Question types encountered:")
        for q_type, count in self.stats['question_types'].items():
            print(f"  • {q_type}: {count}")
        print("="*70)
        
        return self.stats

def setup_security_interactive():
    """Interactive security setup for first-time users"""
    print("\n" + "="*60)
    print("SECURITY SETUP - FIRST TIME CONFIGURATION")
    print("="*60)
    
    security = SecurityManager()
    
    print("\nThis will set up the security system with:")
    print("• Daily rotating approval codes")
    print("• Machine binding (prevents sharing)")
    print("• Encrypted configuration storage")
    
    try:
        master_secret = input("\nEnter master secret (password): ").strip()
        if not master_secret:
            print("Error: Master secret cannot be empty")
            return False
        
        mode = input("Security mode (daily/static) [daily]: ").strip().lower()
        if not mode:
            mode = "daily"
        
        enforce = input("Require approval every run? (y/n) [y]: ").strip().lower()
        enforce_every_run = enforce != 'n'
        
        # Setup security
        if security.setup_security(master_secret, mode, enforce_every_run):
            print("\n[SUCCESS] Security system configured!")
            
            if mode == "daily":
                daily_code = security.get_daily_code_for_display()
                if daily_code:
                    print(f"[INFO] Today's code: {daily_code}")
                    print("[INFO] This code changes daily and is unique to this machine")
            
            return True
        else:
            print("\n[ERROR] Security setup failed")
            return False
            
    except (EOFError, KeyboardInterrupt):
        print("\n[CANCELLED] Security setup cancelled")
        return False

def main():
    """Main entry point with command line interface"""
    parser = argparse.ArgumentParser(description="GlobalExam AI - Ultimate Automation System")
    
    # Command line arguments
    parser.add_argument("--setup-security", action="store_true", 
                       help="Setup security system (first time only)")
    parser.add_argument("--disable-security", action="store_true",
                       help="Disable security system (development mode)")
    parser.add_argument("--show-daily-code", action="store_true",
                       help="Show today's daily approval code")
    parser.add_argument("--show-machine-id", action="store_true", 
                       help="Show machine ID for approval")
    parser.add_argument("--max-questions", type=int, default=30,
                       help="Maximum number of questions to process")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug mode with screenshots")
    
    args = parser.parse_args()
    
    try:
        # Handle utility commands
        if args.setup_security:
            setup_security_interactive()
            return
        
        if args.show_machine_id:
            security = SecurityManager()
            machine_id = security.get_machine_id()
            print(f"Machine ID: {machine_id}")
            return
        
        if args.show_daily_code:
            security = SecurityManager()
            daily_code = security.get_daily_code_for_display()
            if daily_code:
                print(f"Today's daily code: {daily_code}")
            else:
                print("No security configured or daily mode not enabled")
            return
        
        if args.disable_security:
            security = SecurityManager()
            if security.disable_security():
                print("Security system disabled")
            else:
                print("Failed to disable security")
            return
        
        # Main automation
        print("Starting GlobalExam AI Ultimate Automation...")
        
        # Initialize application
        app = GlobalExamAI()
        app.debug = args.debug
        app.max_questions = args.max_questions
        
        # Run automation
        results = app.run_automation()
        
        # Handle results
        if 'error' in results:
            print(f"Automation failed: {results['error']}")
            sys.exit(1)
        else:
            success_rate = (results['questions_successful'] / 
                          max(1, results['questions_attempted'])) * 100
            print(f"\nFinal success rate: {success_rate:.1f}%")
            
            if success_rate >= 70:
                print("🎉 Excellent performance!")
            elif success_rate >= 50:
                print("👍 Good performance!")
            else:
                print("📈 Room for improvement - check logs for issues")
    
    except KeyboardInterrupt:
        print("\n[EXIT] Application interrupted by user")
    except Exception as e:
        print(f"[FATAL] Application error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
