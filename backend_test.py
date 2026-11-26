#!/usr/bin/env python3
"""
Backend API Testing for THE traders Bro platform
Tests all authentication, lecture, and trade endpoints
"""

import requests
import sys
import json
from datetime import datetime

class TradersBackendTester:
    def __init__(self):
        self.base_url = "https://traders-bro.preview.emergentagent.com/api"
        self.token = None
        self.user_data = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}: PASSED")
        else:
            print(f"❌ {name}: FAILED - {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details
        })

    def test_user_registration(self):
        """Test user registration"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_data = {
            "name": f"Test User {timestamp}",
            "email": f"testuser_{timestamp}@example.com",
            "password": "TestPassword123!"
        }
        
        try:
            response = requests.post(f"{self.base_url}/auth/register", json=user_data)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and 'user' in data:
                    self.token = data['access_token']
                    self.user_data = data['user']
                    self.log_test("User Registration", True)
                    return True
                else:
                    self.log_test("User Registration", False, "Missing token or user in response")
            else:
                self.log_test("User Registration", False, f"Status {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("User Registration", False, f"Exception: {str(e)}")
        return False

    def test_user_login(self):
        """Test user login with existing credentials"""
        if not self.user_data:
            self.log_test("User Login", False, "No user data from registration")
            return False
            
        login_data = {
            "email": self.user_data['email'],
            "password": "TestPassword123!"
        }
        
        try:
            response = requests.post(f"{self.base_url}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data:
                    self.token = data['access_token']  # Update token
                    self.log_test("User Login", True)
                    return True
                else:
                    self.log_test("User Login", False, "Missing token in response")
            else:
                self.log_test("User Login", False, f"Status {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("User Login", False, f"Exception: {str(e)}")
        return False

    def test_get_user_profile(self):
        """Test getting current user profile"""
        if not self.token:
            self.log_test("Get User Profile", False, "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.base_url}/auth/me", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if 'id' in data and 'email' in data and 'name' in data:
                    self.log_test("Get User Profile", True)
                    return True
                else:
                    self.log_test("Get User Profile", False, "Missing required fields in user data")
            else:
                self.log_test("Get User Profile", False, f"Status {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Get User Profile", False, f"Exception: {str(e)}")
        return False

    def test_create_lecture(self):
        """Test creating a new lecture"""
        if not self.token:
            self.log_test("Create Lecture", False, "No auth token available")
            return False, None
            
        lecture_data = {
            "title": "Understanding Order Blocks - Test Lecture",
            "description": "A comprehensive guide to identifying and trading order blocks in the market",
            "content": "Order blocks are significant price levels where large institutions have placed substantial orders. These levels often act as support or resistance... [detailed content would continue here]",
            "video_url": "https://youtube.com/watch?v=test123",
            "ict_concepts": ["Order Block", "Smart Money Concepts", "Supply and Demand"]
        }
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(f"{self.base_url}/lectures", json=lecture_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if 'id' in data and data['title'] == lecture_data['title']:
                    self.log_test("Create Lecture", True)
                    return True, data['id']
                else:
                    self.log_test("Create Lecture", False, "Invalid response structure")
            else:
                self.log_test("Create Lecture", False, f"Status {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Create Lecture", False, f"Exception: {str(e)}")
        return False, None

    def test_get_lectures(self):
        """Test retrieving all lectures"""
        try:
            response = requests.get(f"{self.base_url}/lectures")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Get All Lectures", True, f"Retrieved {len(data)} lectures")
                    return True
                else:
                    self.log_test("Get All Lectures", False, "Response is not a list")
            else:
                self.log_test("Get All Lectures", False, f"Status {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Get All Lectures", False, f"Exception: {str(e)}")
        return False

    def test_get_single_lecture(self, lecture_id):
        """Test retrieving a specific lecture by ID"""
        if not lecture_id:
            self.log_test("Get Single Lecture", False, "No lecture ID provided")
            return False
            
        try:
            response = requests.get(f"{self.base_url}/lectures/{lecture_id}")
            
            if response.status_code == 200:
                data = response.json()
                if 'id' in data and data['id'] == lecture_id:
                    # Check if views were incremented
                    if 'views' in data:
                        self.log_test("Get Single Lecture", True, f"Views: {data['views']}")
                        return True
                    else:
                        self.log_test("Get Single Lecture", False, "Views field missing")
                else:
                    self.log_test("Get Single Lecture", False, "Invalid lecture data")
            else:
                self.log_test("Get Single Lecture", False, f"Status {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Get Single Lecture", False, f"Exception: {str(e)}")
        return False

    def test_create_trade(self):
        """Test creating a new trade"""
        if not self.token:
            self.log_test("Create Trade", False, "No auth token available")
            return False, None
            
        trade_data = {
            "pair": "EUR/USD",
            "direction": "long",
            "entry_price": 1.2345,
            "exit_price": 1.2400,
            "stop_loss": 1.2300,
            "take_profit": 1.2500,
            "position_size": 1.0,
            "profit_loss": 55.0,
            "strategy": "Identified strong order block at 1.2340 level with confluence from daily demand zone. Entry on retest with tight stop loss below the block.",
            "ict_concepts": ["Order Block", "Demand Zone", "Retest"],
            "notes": "Market showed clear smart money accumulation at this level"
        }
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(f"{self.base_url}/trades", json=trade_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if 'id' in data and data['pair'] == trade_data['pair']:
                    self.log_test("Create Trade", True)
                    return True, data['id']
                else:
                    self.log_test("Create Trade", False, "Invalid response structure")
            else:
                self.log_test("Create Trade", False, f"Status {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Create Trade", False, f"Exception: {str(e)}")
        return False, None

    def test_get_trades(self):
        """Test retrieving all trades"""
        try:
            response = requests.get(f"{self.base_url}/trades")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Get All Trades", True, f"Retrieved {len(data)} trades")
                    return True
                else:
                    self.log_test("Get All Trades", False, "Response is not a list")
            else:
                self.log_test("Get All Trades", False, f"Status {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Get All Trades", False, f"Exception: {str(e)}")
        return False

    def test_get_single_trade(self, trade_id):
        """Test retrieving a specific trade by ID"""
        if not trade_id:
            self.log_test("Get Single Trade", False, "No trade ID provided")
            return False
            
        try:
            response = requests.get(f"{self.base_url}/trades/{trade_id}")
            
            if response.status_code == 200:
                data = response.json()
                if 'id' in data and data['id'] == trade_id:
                    self.log_test("Get Single Trade", True)
                    return True
                else:
                    self.log_test("Get Single Trade", False, "Invalid trade data")
            else:
                self.log_test("Get Single Trade", False, f"Status {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Get Single Trade", False, f"Exception: {str(e)}")
        return False

    def test_get_user_trades(self):
        """Test retrieving current user's trades"""
        if not self.token:
            self.log_test("Get User Trades", False, "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.base_url}/user/trades", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Get User Trades", True, f"Retrieved {len(data)} user trades")
                    return True
                else:
                    self.log_test("Get User Trades", False, "Response is not a list")
            else:
                self.log_test("Get User Trades", False, f"Status {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Get User Trades", False, f"Exception: {str(e)}")
        return False

    def test_create_journal_entry(self):
        """Test creating a new journal entry"""
        if not self.token:
            self.log_test("Create Journal Entry", False, "No auth token available")
            return False, None
            
        journal_data = {
            "date": "2024-01-15",
            "pair": "EUR/USD",
            "outcome": "win",
            "session": "London",
            "timeframe": "15m",
            "bias": "bullish",
            "rules_followed": True,
            "chart_link": "https://tradingview.com/chart/test123",
            "notes": "Strong order block setup with good confluence"
        }
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(f"{self.base_url}/journal", json=journal_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if 'id' in data and data['pair'] == journal_data['pair']:
                    self.log_test("Create Journal Entry", True)
                    return True, data['id']
                else:
                    self.log_test("Create Journal Entry", False, "Invalid response structure")
            else:
                self.log_test("Create Journal Entry", False, f"Status {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Create Journal Entry", False, f"Exception: {str(e)}")
        return False, None

    def test_get_journal_entries(self):
        """Test retrieving user's journal entries"""
        if not self.token:
            self.log_test("Get Journal Entries", False, "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.base_url}/journal", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Get Journal Entries", True, f"Retrieved {len(data)} journal entries")
                    return True
                else:
                    self.log_test("Get Journal Entries", False, "Response is not a list")
            else:
                self.log_test("Get Journal Entries", False, f"Status {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Get Journal Entries", False, f"Exception: {str(e)}")
        return False

    def test_get_single_journal_entry(self, journal_id):
        """Test retrieving a specific journal entry by ID"""
        if not journal_id:
            self.log_test("Get Single Journal Entry", False, "No journal ID provided")
            return False
            
        if not self.token:
            self.log_test("Get Single Journal Entry", False, "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.base_url}/journal/{journal_id}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if 'id' in data and data['id'] == journal_id:
                    self.log_test("Get Single Journal Entry", True)
                    return True
                else:
                    self.log_test("Get Single Journal Entry", False, "Invalid journal data")
            else:
                self.log_test("Get Single Journal Entry", False, f"Status {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Get Single Journal Entry", False, f"Exception: {str(e)}")
        return False

    def test_delete_journal_entry(self, journal_id):
        """Test deleting a journal entry"""
        if not journal_id:
            self.log_test("Delete Journal Entry", False, "No journal ID provided")
            return False
            
        if not self.token:
            self.log_test("Delete Journal Entry", False, "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.delete(f"{self.base_url}/journal/{journal_id}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if 'message' in data:
                    self.log_test("Delete Journal Entry", True)
                    return True
                else:
                    self.log_test("Delete Journal Entry", False, "No success message in response")
            else:
                self.log_test("Delete Journal Entry", False, f"Status {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Delete Journal Entry", False, f"Exception: {str(e)}")
        return False

    def test_unauthorized_access(self):
        """Test that protected endpoints require authentication"""
        protected_endpoints = [
            ("POST", "/lectures", {"title": "Test", "description": "Test", "content": "Test"}),
            ("POST", "/trades", {"pair": "EUR/USD", "direction": "long", "entry_price": 1.0, "exit_price": 1.1, "stop_loss": 0.9, "position_size": 1.0, "profit_loss": 10.0, "strategy": "Test"}),
            ("POST", "/journal", {"date": "2024-01-15", "pair": "EUR/USD", "outcome": "win", "session": "London", "timeframe": "15m", "bias": "bullish", "rules_followed": True}),
            ("GET", "/user/trades", None),
            ("GET", "/journal", None),
            ("GET", "/auth/me", None)
        ]
        
        success_count = 0
        for method, endpoint, data in protected_endpoints:
            try:
                if method == "POST":
                    response = requests.post(f"{self.base_url}{endpoint}", json=data)
                else:
                    response = requests.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 401:
                    success_count += 1
                else:
                    print(f"  ⚠️  {endpoint} did not return 401 (got {response.status_code})")
            except Exception as e:
                print(f"  ⚠️  Error testing {endpoint}: {str(e)}")
        
        if success_count == len(protected_endpoints):
            self.log_test("Unauthorized Access Protection", True)
            return True
        else:
            self.log_test("Unauthorized Access Protection", False, f"{success_count}/{len(protected_endpoints)} endpoints protected")
        return False

    def run_all_tests(self):
        """Run all backend tests"""
        print("🧪 Starting Backend API Tests for THE traders Bro")
        print("=" * 60)
        
        # Authentication Tests
        print("\n📝 Authentication Tests:")
        if not self.test_user_registration():
            print("❌ Cannot continue without successful registration")
            return False
            
        self.test_user_login()
        self.test_get_user_profile()
        
        # Lecture Tests
        print("\n📚 Lecture Tests:")
        lecture_success, lecture_id = self.test_create_lecture()
        self.test_get_lectures()
        if lecture_id:
            self.test_get_single_lecture(lecture_id)
        
        # Trade Tests
        print("\n📈 Trade Tests:")
        trade_success, trade_id = self.test_create_trade()
        self.test_get_trades()
        if trade_id:
            self.test_get_single_trade(trade_id)
        self.test_get_user_trades()
        
        # Journal Tests
        print("\n📓 Journal Tests:")
        journal_success, journal_id = self.test_create_journal_entry()
        self.test_get_journal_entries()
        if journal_id:
            self.test_get_single_journal_entry(journal_id)
            # Test delete last so we don't break get tests
            self.test_delete_journal_entry(journal_id)
        
        # Security Tests
        print("\n🔒 Security Tests:")
        self.test_unauthorized_access()
        
        # Summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        success_rate = (self.tests_passed / self.tests_run) * 100 if self.tests_run > 0 else 0
        print(f"✅ Success Rate: {success_rate:.1f}%")
        
        if success_rate < 80:
            print("⚠️  Warning: Low success rate indicates significant issues")
            return False
        elif success_rate < 100:
            print("⚠️  Some tests failed - review results above")
            return False
        else:
            print("🎉 All tests passed!")
            return True

def main():
    """Main test execution"""
    tester = TradersBackendTester()
    success = tester.run_all_tests()
    
    # Save detailed results for frontend testing
    results = {
        "timestamp": datetime.now().isoformat(),
        "summary": f"{tester.tests_passed}/{tester.tests_run} tests passed",
        "success_rate": (tester.tests_passed / tester.tests_run) * 100 if tester.tests_run > 0 else 0,
        "test_results": tester.test_results
    }
    
    with open("/app/backend_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())