#!/usr/bin/env python3
import subprocess
import time
import logging
import re
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/bt_auto_connect.log'),
        logging.StreamHandler()
    ]
)

class BluetoothAutoConnector:
    def __init__(self, device_mac, device_name=None, check_interval=30):
        self.device_mac = device_mac.upper()  # Normalize MAC address
        self.device_name = device_name
        self.check_interval = check_interval
        
    def is_bluetooth_available(self):
        """Check if Bluetooth service is available and running"""
        try:
            result = subprocess.run(['systemctl', 'is-active', 'bluetooth'], 
                                  capture_output=True, text=True, timeout=5)
            return result.stdout.strip() == 'active'
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            return False
    
    def start_bluetooth_service(self):
        """Start Bluetooth service if not running"""
        try:
            subprocess.run(['sudo', 'systemctl', 'start', 'bluetooth'], 
                         timeout=10, check=True)
            time.sleep(3)
            logging.info("Bluetooth service started")
            return True
        except subprocess.CalledProcessError:
            logging.error("Failed to start Bluetooth service")
            return False
    
    def enable_bluetooth(self):
        """Enable Bluetooth adapter"""
        try:
            subprocess.run(['sudo', 'bluetoothctl', 'power', 'on'], 
                         timeout=10, check=True)
            time.sleep(2)
            logging.info("Bluetooth adapter enabled")
            return True
        except subprocess.CalledProcessError:
            logging.error("Failed to enable Bluetooth adapter")
            return False
    
    def is_device_connected(self):
        """Check if the target device is currently connected"""
        try:
            result = subprocess.run(['bluetoothctl', 'info', self.device_mac], 
                                  capture_output=True, text=True, timeout=10)
            
            if "Connected: yes" in result.stdout:
                logging.info(f"Device {self.device_mac} is connected")
                return True
            return False
            
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            return False
    
    def is_device_paired(self):
        """Check if device is already paired"""
        try:
            result = subprocess.run(['bluetoothctl', 'devices'], 
                                  capture_output=True, text=True, timeout=10)
            return self.device_mac in result.stdout
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            return False
    
    def is_device_trusted(self):
        """Check if device is trusted"""
        try:
            result = subprocess.run(['bluetoothctl', 'info', self.device_mac], 
                                  capture_output=True, text=True, timeout=10)
            return "Trusted: yes" in result.stdout
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            return False
    
    def trust_device(self):
        """Trust the device"""
        try:
            subprocess.run(['sudo', 'bluetoothctl', 'trust', self.device_mac], 
                         timeout=10, check=True)
            logging.info(f"Device {self.device_mac} trusted")
            return True
        except subprocess.CalledProcessError:
            logging.error(f"Failed to trust device {self.device_mac}")
            return False
    
    def pair_device(self):
        """Pair with the device"""
        try:
            # Start pairing process
            process = subprocess.Popen(
                ['sudo', 'bluetoothctl', 'pair', self.device_mac],
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for pairing to complete (with timeout)
            time.sleep(10)
            process.terminate()
            
            # Check if pairing was successful
            if self.is_device_paired():
                logging.info(f"Successfully paired with {self.device_mac}")
                return True
            else:
                logging.error(f"Failed to pair with {self.device_mac}")
                return False
                
        except Exception as e:
            logging.error(f"Error during pairing: {e}")
            return False
    
    def connect_device(self):
        """Connect to the device"""
        try:
            process = subprocess.Popen(
                ['sudo', 'bluetoothctl', 'connect', self.device_mac],
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for connection to complete
            time.sleep(8)
            process.terminate()
            
            if self.is_device_connected():
                logging.info(f"Successfully connected to {self.device_mac}")
                return True
            else:
                logging.warning(f"Connection attempt to {self.device_mac} may have failed")
                return False
                
        except Exception as e:
            logging.error(f"Error during connection: {e}")
            return False
    
    def scan_for_devices(self, scan_time=10):
        """Scan for Bluetooth devices"""
        try:
            logging.info("Scanning for Bluetooth devices...")
            
            # Start scan
            subprocess.run(['sudo', 'bluetoothctl', 'scan', 'on'], 
                         timeout=5, check=True)
            
            # Wait for devices to be discovered
            time.sleep(scan_time)
            
            # Stop scan
            subprocess.run(['sudo', 'bluetoothctl', 'scan', 'off'], 
                         timeout=5, check=True)
            
            # List devices
            result = subprocess.run(['bluetoothctl', 'devices'], 
                                  capture_output=True, text=True, timeout=10)
            
            logging.info(f"Available devices:\n{result.stdout}")
            return self.device_mac in result.stdout
            
        except subprocess.CalledProcessError as e:
            logging.error(f"Scan failed: {e}")
            return False
    
    def setup_bluetooth(self):
        """Ensure Bluetooth is properly set up"""
        if not self.is_bluetooth_available():
            if not self.start_bluetooth_service():
                return False
        
        if not self.enable_bluetooth():
            return False
        
        return True
    
    def run_connection_sequence(self):
        """Complete connection sequence"""
        # Ensure device is paired and trusted
        if not self.is_device_paired():
            logging.info(f"Device {self.device_mac} not paired, attempting to pair...")
            if not self.pair_device():
                return False
        
        if not self.is_device_trusted():
            logging.info(f"Device {self.device_mac} not trusted, setting trust...")
            if not self.trust_device():
                return False
        
        # Connect to device
        logging.info(f"Attempting to connect to {self.device_mac}...")
        return self.connect_device()
    
    def run(self):
        """Main loop to monitor and maintain Bluetooth connection"""
        logging.info(f"Starting Bluetooth auto-connector for device {self.device_mac}")
        
        while True:
            try:
                # Ensure Bluetooth is set up
                if not self.setup_bluetooth():
                    logging.error("Bluetooth setup failed, retrying...")
                    time.sleep(self.check_interval)
                    continue
                
                # Check if device is connected
                if not self.is_device_connected():
                    logging.warning(f"Device {self.device_mac} not connected")
                    
                    # Try to connect
                    if self.run_connection_sequence():
                        logging.info(f"Successfully connected to {self.device_mac}")
                    else:
                        logging.warning(f"Failed to connect to {self.device_mac}")
                        # Optional: scan for devices if connection fails repeatedly
                        self.scan_for_devices(5)
                
                else:
                    logging.info(f"Device {self.device_mac} is connected")
                
                # Wait before next check
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logging.info("Stopped by user")
                break
            except Exception as e:
                logging.error(f"Unexpected error in main loop: {e}")
                time.sleep(self.check_interval)

def discover_bluetooth_devices():
    """Helper function to discover available Bluetooth devices"""
    try:
        logging.info("Discovering Bluetooth devices...")
        
        # Enable Bluetooth and start scan
        subprocess.run(['sudo', 'bluetoothctl', 'power', 'on'], timeout=5)
        subprocess.run(['sudo', 'bluetoothctl', 'scan', 'on'], timeout=5)
        
        logging.info("Scanning for 15 seconds...")
        time.sleep(15)
        
        # Stop scan and list devices
        subprocess.run(['sudo', 'bluetoothctl', 'scan', 'off'], timeout=5)
        result = subprocess.run(['bluetoothctl', 'devices'], 
                              capture_output=True, text=True, timeout=10)
        
        logging.info("Discovered devices:")
        logging.info(result.stdout)
        
        return result.stdout
        
    except Exception as e:
        logging.error(f"Discovery failed: {e}")
        return None

def main():
    # Configuration - CHANGE THESE VALUES
    DEVICE_MAC = "XX:XX:XX:XX:XX:XX"  # Replace with your device's MAC address
    # DEVICE_NAME = "Your_Device_Name"  # Optional: device name for reference
    
    # Uncomment the next line to discover devices first
    # discover_bluetooth_devices()
    
    # Create and run the auto-connector
    connector = BluetoothAutoConnector(DEVICE_MAC)  # Add , DEVICE_NAME if available
    connector.run()

if __name__ == "__main__":
    main()
