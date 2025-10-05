#!/usr/bin/env python3
"""
Wedding Card Application Backend API Testing Suite
Tests all backend APIs comprehensively with real data
"""

import requests
import json
import sys
from datetime import datetime
import uuid

# Backend URL from frontend/.env
BACKEND_URL = "https://digi-invite-maker.preview.emergentagent.com/api"

# Test credentials
TEST_USERNAME = "aaaaaa"
TEST_PASSWORD = "aaaaaa"

class WeddingCardAPITester:
    def __init__(self):
        self.session_id = None
        self.user_id = None
        self.wedding_id = None
        self.test_results = []
        
    def log_test(self, test_name, success, message, response_data=None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "response_data": response_data,
            "timestamp": datetime.now().isoformat()
        })
        
    def test_authentication(self):
        """Test authentication APIs"""
        print("\n🔐 Testing Authentication APIs...")
        
        # Test login
        try:
            login_data = {
                "username": TEST_USERNAME,
                "password": TEST_PASSWORD
            }
            
            response = requests.post(f"{BACKEND_URL}/auth/login", json=login_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("session_id"):
                    self.session_id = data["session_id"]
                    self.user_id = data["user_id"]
                    self.log_test("Authentication Login", True, 
                                f"Login successful, session_id: {self.session_id[:8]}...", data)
                else:
                    self.log_test("Authentication Login", False, 
                                f"Login response missing required fields: {data}")
            else:
                self.log_test("Authentication Login", False, 
                            f"Login failed with status {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Authentication Login", False, f"Login request failed: {str(e)}")
            
    def test_wedding_data_retrieval(self):
        """Test wedding data retrieval"""
        print("\n📋 Testing Wedding Data Retrieval...")
        
        if not self.session_id:
            self.log_test("Wedding Data GET", False, "No session_id available for testing")
            return
            
        try:
            # Test GET wedding data
            params = {"session_id": self.session_id}
            response = requests.get(f"{BACKEND_URL}/wedding", params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify data structure
                required_fields = [
                    "id", "user_id", "couple_name_1", "couple_name_2", 
                    "wedding_date", "venue_name", "venue_location", 
                    "story_timeline", "schedule_events", "gallery_photos",
                    "bridal_party", "groom_party", "registry_items", "faqs", "theme"
                ]
                
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    self.wedding_id = data.get("id")
                    self.log_test("Wedding Data GET", True, 
                                f"Retrieved wedding data successfully. Wedding ID: {self.wedding_id}", 
                                {k: v for k, v in data.items() if k in ["id", "couple_name_1", "couple_name_2", "theme"]})
                else:
                    self.log_test("Wedding Data GET", False, 
                                f"Missing required fields: {missing_fields}")
            else:
                self.log_test("Wedding Data GET", False, 
                            f"Failed with status {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Wedding Data GET", False, f"Request failed: {str(e)}")
            
    def test_wedding_data_update(self):
        """Test wedding data update"""
        print("\n✏️ Testing Wedding Data Update...")
        
        if not self.session_id:
            self.log_test("Wedding Data PUT", False, "No session_id available for testing")
            return
            
        try:
            # Test data with realistic wedding information
            update_data = {
                "session_id": self.session_id,
                "couple_name_1": "Emily",
                "couple_name_2": "James",
                "wedding_date": "2025-08-15",
                "venue_name": "Rosewood Manor",
                "venue_location": "Rosewood Manor • Sonoma County, California",
                "their_story": "Our love story began at a bookstore cafe where we both reached for the same novel. What started as a conversation about literature blossomed into a beautiful romance filled with shared adventures and dreams.",
                "theme": "modern",
                "story_timeline": [
                    {
                        "year": "2020",
                        "title": "First Meeting",
                        "description": "We met at Powell's Books in Portland during a rainy afternoon, both reaching for the same copy of 'The Seven Husbands of Evelyn Hugo'.",
                        "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop"
                    },
                    {
                        "year": "2022",
                        "title": "First Trip Together",
                        "description": "Our first adventure together was a road trip along the Pacific Coast Highway, creating memories that would last a lifetime.",
                        "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&h=400&fit=crop"
                    }
                ],
                "schedule_events": [
                    {
                        "time": "3:00 PM",
                        "title": "Wedding Ceremony",
                        "description": "Join us as we exchange vows in the beautiful garden pavilion surrounded by blooming roses.",
                        "location": "Rose Garden Pavilion",
                        "duration": "45 minutes",
                        "highlight": True
                    },
                    {
                        "time": "4:00 PM",
                        "title": "Cocktail Reception",
                        "description": "Celebrate with signature cocktails and hors d'oeuvres on the vineyard terrace.",
                        "location": "Vineyard Terrace",
                        "duration": "90 minutes",
                        "highlight": False
                    }
                ],
                "faqs": [
                    {
                        "question": "What is the dress code?",
                        "answer": "We're requesting cocktail attire. Think elegant and comfortable for an outdoor garden setting."
                    },
                    {
                        "question": "Will transportation be provided?",
                        "answer": "We'll have shuttle service from the main hotel to the venue starting at 2:30 PM."
                    }
                ]
            }
            
            response = requests.put(f"{BACKEND_URL}/wedding", json=update_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify the update worked
                if (data.get("couple_name_1") == "Emily" and 
                    data.get("couple_name_2") == "James" and
                    data.get("theme") == "modern"):
                    self.log_test("Wedding Data PUT", True, 
                                "Wedding data updated successfully", 
                                {k: v for k, v in data.items() if k in ["couple_name_1", "couple_name_2", "theme", "updated_at"]})
                else:
                    self.log_test("Wedding Data PUT", False, 
                                f"Update didn't persist correctly: {data}")
            else:
                self.log_test("Wedding Data PUT", False, 
                            f"Failed with status {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Wedding Data PUT", False, f"Request failed: {str(e)}")
            
    def test_data_persistence(self):
        """Test that data persists correctly"""
        print("\n💾 Testing Data Persistence...")
        
        if not self.session_id:
            self.log_test("Data Persistence", False, "No session_id available for testing")
            return
            
        try:
            # Retrieve data again to verify persistence
            params = {"session_id": self.session_id}
            response = requests.get(f"{BACKEND_URL}/wedding", params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if our updates persisted
                if (data.get("couple_name_1") == "Emily" and 
                    data.get("couple_name_2") == "James" and
                    data.get("theme") == "modern"):
                    self.log_test("Data Persistence", True, 
                                "Data changes persisted correctly in database")
                else:
                    self.log_test("Data Persistence", False, 
                                f"Data didn't persist: names={data.get('couple_name_1')}/{data.get('couple_name_2')}, theme={data.get('theme')}")
            else:
                self.log_test("Data Persistence", False, 
                            f"Failed to retrieve data for persistence check: {response.status_code}")
                
        except Exception as e:
            self.log_test("Data Persistence", False, f"Persistence check failed: {str(e)}")
            
    def test_faq_section_update(self):
        """Test FAQ section specific update"""
        print("\n❓ Testing FAQ Section Update...")
        
        if not self.session_id:
            self.log_test("FAQ Section Update", False, "No session_id available for testing")
            return
            
        try:
            faq_data = {
                "session_id": self.session_id,
                "faqs": [
                    {
                        "question": "What time should guests arrive?",
                        "answer": "Please arrive by 2:45 PM to allow time for seating before the 3:00 PM ceremony."
                    },
                    {
                        "question": "Is there parking available?",
                        "answer": "Yes, complimentary valet parking is available at the venue entrance."
                    },
                    {
                        "question": "Can children attend?",
                        "answer": "We love your little ones, but we've planned an adults-only celebration to allow everyone to relax and enjoy the evening."
                    }
                ]
            }
            
            response = requests.put(f"{BACKEND_URL}/wedding/faq", json=faq_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "wedding_data" in data:
                    wedding_data = data["wedding_data"]
                    faqs = wedding_data.get("faqs", [])
                    if len(faqs) == 3 and faqs[0]["question"] == "What time should guests arrive?":
                        self.log_test("FAQ Section Update", True, 
                                    f"FAQ section updated successfully with {len(faqs)} questions")
                    else:
                        self.log_test("FAQ Section Update", False, 
                                    f"FAQ update didn't work correctly: {faqs}")
                else:
                    self.log_test("FAQ Section Update", False, 
                                f"Unexpected response format: {data}")
            else:
                self.log_test("FAQ Section Update", False, 
                            f"Failed with status {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("FAQ Section Update", False, f"FAQ update failed: {str(e)}")
            
    def test_session_management(self):
        """Test session management"""
        print("\n🔑 Testing Session Management...")
        
        if not self.session_id:
            self.log_test("Session Management", False, "No session_id available for testing")
            return
            
        try:
            # Test profile endpoint with session
            params = {"session_id": self.session_id}
            response = requests.get(f"{BACKEND_URL}/profile", params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("username") == TEST_USERNAME:
                    self.log_test("Session Management", True, 
                                f"Session working correctly for user: {data['username']}")
                else:
                    self.log_test("Session Management", False, 
                                f"Session returned wrong user: {data}")
            else:
                self.log_test("Session Management", False, 
                            f"Profile request failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Session Management", False, f"Session test failed: {str(e)}")
            
    def test_data_structure_integrity(self):
        """Test that all data is stored in ONE document per user"""
        print("\n🏗️ Testing Data Structure Integrity...")
        
        if not self.session_id:
            self.log_test("Data Structure", False, "No session_id available for testing")
            return
            
        try:
            params = {"session_id": self.session_id}
            response = requests.get(f"{BACKEND_URL}/wedding", params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify all sections are in one document
                sections = [
                    "couple_name_1", "couple_name_2", "wedding_date", "venue_name", "venue_location",
                    "story_timeline", "schedule_events", "gallery_photos", "bridal_party", 
                    "groom_party", "registry_items", "faqs", "theme"
                ]
                
                present_sections = [section for section in sections if section in data]
                
                if len(present_sections) == len(sections):
                    self.log_test("Data Structure", True, 
                                f"All {len(sections)} sections present in single document")
                else:
                    missing = set(sections) - set(present_sections)
                    self.log_test("Data Structure", False, 
                                f"Missing sections: {missing}")
            else:
                self.log_test("Data Structure", False, 
                            f"Failed to retrieve data: {response.status_code}")
                
        except Exception as e:
            self.log_test("Data Structure", False, f"Structure test failed: {str(e)}")
            
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Wedding Card Backend API Tests...")
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Test Credentials: {TEST_USERNAME}/{TEST_PASSWORD}")
        print("=" * 60)
        
        # Run tests in order
        self.test_authentication()
        self.test_wedding_data_retrieval()
        self.test_wedding_data_update()
        self.test_data_persistence()
        self.test_faq_section_update()
        self.test_session_management()
        self.test_data_structure_integrity()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Show failed tests
        failed_tests = [result for result in self.test_results if not result["success"]]
        if failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"  • {test['test']}: {test['message']}")
        else:
            print("\n🎉 ALL TESTS PASSED!")
            
        return passed == total

if __name__ == "__main__":
    tester = WeddingCardAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)