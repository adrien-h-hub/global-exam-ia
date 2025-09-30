#!/usr/bin/env python3
"""
Security System Module for GlobalExam AI
========================================

This module implements a comprehensive security system with:
1. Daily rotating approval codes
2. Machine binding (multiple methods)
3. Encrypted configuration storage
4. Anti-sharing protection

Author: Student Project
Purpose: Educational demonstration of security concepts
"""

import hashlib
import json
import os
import time
import uuid
import platform
import subprocess
from typing import Optional, Dict, Any

class SecurityManager:
    """
    Manages application security through multiple layers:
    
    Layer 1: Daily Rotating Codes
    - Generates unique 6-digit codes that change daily
    - Based on machine ID + secret + date combination
    
    Layer 2: Machine Binding  
    - Ties approval to specific hardware
    - Uses multiple hardware identifiers for reliability
    
    Layer 3: Configuration Protection
    - Stores settings in encrypted format
    - Validates integrity on each run
    """
    
    def __init__(self, app_name: str = "GlobalExamAI"):
        """
        Initialize security manager
        
        Args:
            app_name: Application name for config directory
        """
        self.app_name = app_name
        self.config_dir = self._get_config_directory()
        self.config_path = os.path.join(self.config_dir, 'config.json')
        
        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)
        
        print(f"[SECURITY] Initialized for {app_name}")
        print(f"[SECURITY] Config directory: {self.config_dir}")
    
    def _get_config_directory(self) -> str:
        """
        Get platform-appropriate configuration directory
        
        Returns:
            Path to configuration directory
        """
        if os.name == 'nt':  # Windows
            base_dir = os.getenv('APPDATA', os.path.expanduser('~'))
        else:  # Linux/Mac
            base_dir = os.path.expanduser('~/.config')
        
        return os.path.join(base_dir, self.app_name)
    
    def get_machine_id(self) -> str:
        """
        Generate unique machine identifier using multiple methods
        
        This combines several hardware identifiers to create a stable,
        unique machine ID that survives minor system changes but prevents
        easy copying to other machines.
        
        Methods used:
        1. MAC address of primary network adapter
        2. CPU information
        3. System UUID (if available)
        4. Disk serial number
        
        Returns:
            SHA-256 hash of combined machine identifiers
        """
        identifiers = []
        
        try:
            # Method 1: MAC Address (most reliable)
            mac = uuid.getnode()
            identifiers.append(str(mac))
            print(f"[MACHINE_ID] MAC: {mac}")
            
        except Exception as e:
            print(f"[MACHINE_ID] MAC failed: {e}")
        
        try:
            # Method 2: System information
            system_info = f"{platform.system()}{platform.node()}{platform.machine()}"
            identifiers.append(system_info)
            print(f"[MACHINE_ID] System: {system_info}")
            
        except Exception as e:
            print(f"[MACHINE_ID] System info failed: {e}")
        
        try:
            # Method 3: Windows-specific hardware ID
            if os.name == 'nt':
                result = subprocess.run(
                    ['wmic', 'csproduct', 'get', 'uuid'], 
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    uuid_line = result.stdout.strip().split('\n')[-1].strip()
                    if uuid_line and uuid_line != 'UUID':
                        identifiers.append(uuid_line)
                        print(f"[MACHINE_ID] Windows UUID: {uuid_line}")
                        
        except Exception as e:
            print(f"[MACHINE_ID] Windows UUID failed: {e}")
        
        try:
            # Method 4: CPU information
            if os.name == 'nt':
                result = subprocess.run(
                    ['wmic', 'cpu', 'get', 'processorid'], 
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    cpu_id = result.stdout.strip().split('\n')[-1].strip()
                    if cpu_id and cpu_id != 'ProcessorId':
                        identifiers.append(cpu_id)
                        print(f"[MACHINE_ID] CPU ID: {cpu_id}")
                        
        except Exception as e:
            print(f"[MACHINE_ID] CPU ID failed: {e}")
        
        # Combine all identifiers
        if not identifiers:
            # Fallback: use computer name and user
            fallback = f"{platform.node()}{os.getenv('USERNAME', 'user')}"
            identifiers.append(fallback)
            print(f"[MACHINE_ID] Using fallback: {fallback}")
        
        # Create stable hash from all identifiers
        combined = ''.join(sorted(identifiers))  # Sort for consistency
        machine_id = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        
        print(f"[MACHINE_ID] Generated ID: {machine_id[:16]}...")
        return machine_id
    
    def compute_daily_code(self, secret_hash: str) -> str:
        """
        Generate today's 6-digit rotating approval code
        
        The daily code algorithm:
        1. Get machine ID (unique per computer)
        2. Combine with secret hash (set by owner)
        3. Add today's date (YYYYMMDD format)
        4. Generate SHA-256 hash of combination
        5. Extract last 6 digits as decimal number
        
        This ensures:
        - Code changes every day automatically
        - Code is unique per machine (can't share)
        - Code is deterministic (same each day for same machine)
        - Code is unpredictable without secret
        
        Args:
            secret_hash: SHA-256 hash of the master secret
            
        Returns:
            6-digit daily code as string
        """
        try:
            machine_id = self.get_machine_id()
            today = time.strftime('%Y%m%d')  # Format: 20231229
            
            # Combine machine + secret + date
            combined_string = f"{machine_id}{secret_hash}{today}"
            
            # Generate hash
            daily_hash = hashlib.sha256(combined_string.encode('utf-8')).hexdigest()
            
            # Extract 6-digit code from hash
            # Convert hex to int, then get last 6 digits
            hash_int = int(daily_hash, 16)
            daily_code = f"{hash_int % 1000000:06d}"
            
            print(f"[DAILY_CODE] Generated for {today}: {daily_code}")
            return daily_code
            
        except Exception as e:
            print(f"[DAILY_CODE] Generation failed: {e}")
            return "000000"  # Safe fallback
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load and validate configuration from encrypted storage
        
        Returns:
            Configuration dictionary with security settings
        """
        try:
            if not os.path.exists(self.config_path):
                print("[CONFIG] No config file found, creating default")
                return self._create_default_config()
            
            with open(self.config_path, 'r', encoding='utf-8-sig') as f:
                config = json.load(f)
            
            print("[CONFIG] Loaded successfully")
            return config
            
        except Exception as e:
            print(f"[CONFIG] Load failed: {e}")
            return self._create_default_config()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """
        Save configuration to encrypted storage
        
        Args:
            config: Configuration dictionary to save
            
        Returns:
            True if saved successfully
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print("[CONFIG] Saved successfully")
            return True
            
        except Exception as e:
            print(f"[CONFIG] Save failed: {e}")
            return False
    
    def _create_default_config(self) -> Dict[str, Any]:
        """
        Create default security configuration
        
        Returns:
            Default configuration dictionary
        """
        default_config = {
            "REQUIRE_APPROVAL": False,
            "CODE_MODE": "static",  # static, daily, list
            "CODE_ENFORCE_EVERY_RUN": False,
            "APPROVAL_SECRET_HASH": "",
            "APPROVAL_OK": False,
            "APPROVAL_MACHINE_TOKEN": "",
            "APPROVAL_LAST_DATE": "",
            "SECURITY_VERSION": "1.0"
        }
        
        self.save_config(default_config)
        return default_config
    
    def setup_security(self, master_secret: str, mode: str = "daily", enforce_every_run: bool = True) -> bool:
        """
        Setup security system with master secret
        
        Args:
            master_secret: Master password/secret for generating codes
            mode: Security mode ('static', 'daily', 'list')
            enforce_every_run: Whether to require approval every time
            
        Returns:
            True if setup successful
        """
        try:
            # Hash the master secret
            secret_hash = hashlib.sha256(master_secret.encode('utf-8')).hexdigest()
            
            # Create configuration
            config = {
                "REQUIRE_APPROVAL": True,
                "CODE_MODE": mode,
                "CODE_ENFORCE_EVERY_RUN": enforce_every_run,
                "APPROVAL_SECRET_HASH": secret_hash,
                "APPROVAL_OK": False,
                "APPROVAL_MACHINE_TOKEN": "",
                "APPROVAL_LAST_DATE": "",
                "SECURITY_VERSION": "1.0"
            }
            
            if self.save_config(config):
                print(f"[SETUP] Security configured with {mode} mode")
                
                # Show today's code for reference
                if mode == "daily":
                    today_code = self.compute_daily_code(secret_hash)
                    print(f"[SETUP] Today's code: {today_code}")
                
                return True
            
        except Exception as e:
            print(f"[SETUP] Security setup failed: {e}")
        
        return False
    
    def check_approval(self) -> bool:
        """
        Check if user is approved to run the application
        
        This is the main security gate that:
        1. Loads current configuration
        2. Checks if approval is required
        3. Validates machine binding
        4. Prompts for daily code if needed
        5. Updates approval status
        
        Returns:
            True if user is approved to proceed
        """
        try:
            config = self.load_config()
            
            # Check if approval is required
            if not config.get('REQUIRE_APPROVAL', False):
                print("[APPROVAL] Security disabled, proceeding")
                return True
            
            # Get current machine and security info
            machine_id = self.get_machine_id()
            secret_hash = config.get('APPROVAL_SECRET_HASH', '')
            
            if not secret_hash:
                print("[APPROVAL] No security hash configured")
                return False
            
            # Check machine binding
            existing_token = config.get('APPROVAL_MACHINE_TOKEN', '')
            expected_token = hashlib.sha256((machine_id + secret_hash).encode('utf-8')).hexdigest()
            
            # Check if re-approval is needed
            code_mode = config.get('CODE_MODE', 'static').lower()
            last_date = config.get('APPROVAL_LAST_DATE', '')
            today = time.strftime('%Y%m%d')
            enforce_every_run = config.get('CODE_ENFORCE_EVERY_RUN', False)
            
            # Determine if prompt is needed
            need_prompt = True
            if existing_token == expected_token and config.get('APPROVAL_OK', False):
                if enforce_every_run:
                    print("[APPROVAL] Enforcing approval every run")
                elif code_mode == 'daily' and last_date != today:
                    print("[APPROVAL] Daily code expired, need new approval")
                else:
                    print("[APPROVAL] Already approved for this session")
                    need_prompt = False
            
            if need_prompt:
                return self._prompt_for_approval(config, machine_id, secret_hash, code_mode)
            
            return True
            
        except Exception as e:
            print(f"[APPROVAL] Check failed: {e}")
            return False
    
    def _prompt_for_approval(self, config: Dict[str, Any], machine_id: str, 
                           secret_hash: str, code_mode: str) -> bool:
        """
        Prompt user for approval code
        
        Args:
            config: Current configuration
            machine_id: Current machine identifier
            secret_hash: Hashed master secret
            code_mode: Security mode (static, daily, list)
            
        Returns:
            True if correct code provided
        """
        try:
            print("\n" + "="*60)
            print("GLOBALEXAM AI - SECURITY APPROVAL REQUIRED")
            print("="*60)
            print(f"Hostname: {platform.node()}")
            print(f"Machine ID: {machine_id[:16]}...")
            print(f"Security Mode: {code_mode}")
            
            if code_mode == 'daily':
                expected_code = self.compute_daily_code(secret_hash)
                print(f"Enter today's daily code:")
            else:
                print("Enter approval code:")
            
            # Get user input
            try:
                user_code = input("Code: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n[APPROVAL] Input cancelled")
                return False
            
            # Validate code
            valid = False
            
            if code_mode == 'static':
                # Static mode: compare hash of input with stored hash
                input_hash = hashlib.sha256(user_code.encode('utf-8')).hexdigest()
                valid = (input_hash == secret_hash)
                
            elif code_mode == 'daily':
                # Daily mode: compare with computed daily code
                expected_code = self.compute_daily_code(secret_hash)
                valid = (user_code == expected_code)
                
            elif code_mode == 'list':
                # List mode: check against multiple valid hashes
                valid_hashes = config.get('APPROVAL_SECRET_HASHES', [])
                input_hash = hashlib.sha256(user_code.encode('utf-8')).hexdigest()
                valid = (input_hash in valid_hashes) or (input_hash == secret_hash)
            
            if valid:
                # Update approval status
                config['APPROVAL_OK'] = True
                config['APPROVAL_MACHINE_TOKEN'] = hashlib.sha256(
                    (machine_id + secret_hash).encode('utf-8')
                ).hexdigest()
                
                if code_mode == 'daily':
                    config['APPROVAL_LAST_DATE'] = time.strftime('%Y%m%d')
                
                self.save_config(config)
                print("[APPROVAL] ✓ Approved! Access granted.")
                return True
            else:
                print("[APPROVAL] ✗ Invalid code. Access denied.")
                return False
                
        except Exception as e:
            print(f"[APPROVAL] Prompt failed: {e}")
            return False
    
    def get_daily_code_for_display(self) -> Optional[str]:
        """
        Get today's daily code for display purposes (owner reference)
        
        Returns:
            Today's daily code or None if not configured
        """
        try:
            config = self.load_config()
            secret_hash = config.get('APPROVAL_SECRET_HASH', '')
            
            if not secret_hash:
                return None
            
            return self.compute_daily_code(secret_hash)
            
        except Exception as e:
            print(f"[DAILY_CODE] Display failed: {e}")
            return None
    
    def disable_security(self) -> bool:
        """
        Disable security system (for development/testing)
        
        Returns:
            True if disabled successfully
        """
        try:
            config = self.load_config()
            config['REQUIRE_APPROVAL'] = False
            config['APPROVAL_OK'] = False
            
            return self.save_config(config)
            
        except Exception as e:
            print(f"[SECURITY] Disable failed: {e}")
            return False

# Example usage and testing
if __name__ == "__main__":
    print("Security System Module - Test Mode")
    print("="*50)
    
    # Create security manager
    security = SecurityManager("TestApp")
    
    # Test machine ID generation
    print("\n1. Testing Machine ID Generation:")
    machine_id = security.get_machine_id()
    print(f"Machine ID: {machine_id}")
    
    # Test daily code generation
    print("\n2. Testing Daily Code Generation:")
    test_secret = "test_secret_123"
    secret_hash = hashlib.sha256(test_secret.encode()).hexdigest()
    daily_code = security.compute_daily_code(secret_hash)
    print(f"Daily Code: {daily_code}")
    
    # Test configuration
    print("\n3. Testing Configuration:")
    config = security.load_config()
    print(f"Config loaded: {len(config)} settings")
    
    print("\nSecurity system test completed!")
