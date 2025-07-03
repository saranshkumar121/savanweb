# Basic Web Automation Tutorial - Complete Guide
# Terminal me run karne ke liye: python basic_automation.py

import requests
import json
import time
from datetime import datetime

print("🚀 Web Automation Tutorial Start Ho Gaya!")
print("=" * 50)

# Step 1: Simple GET Request - Website se data lena
def get_request_example():
    """
    GET Request ka matlab hai website se data manga
    Jaise aap browser me URL type karte ho, waise hi ye kaam karta hai
    """
    print("\n📥 GET Request Example:")
    
    try:
        # JSONPlaceholder - ye free API hai testing ke liye
        url = "https://jsonplaceholder.typicode.com/posts/1"
        
        # Request bhejte hain
        response = requests.get(url)
        
        # Status code check karte hain (200 means success)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # JSON data ko Python dictionary me convert karte hain
            data = response.json()
            print("✅ Data mil gaya:")
            print(f"Title: {data['title']}")
            print(f"Body: {data['body'][:50]}...")  # Sirf 50 characters dikhate hain
        else:
            print("❌ Data nahi mila")
            
    except Exception as e:
        print(f"❌ Error: {e}")

# Step 2: POST Request - Website pe data bhejna
def post_request_example():
    """
    POST Request ka matlab hai website pe data send karna
    Jaise form fill karke submit karte hain
    """
    print("\n📤 POST Request Example:")
    
    try:
        url = "https://jsonplaceholder.typicode.com/posts"
        
        # Data jo hum bhejenge
        new_post = {
            "title": "Mera Automation Post",
            "body": "Ye post automation se bani hai Python se!",
            "userId": 1
        }
        
        # POST request bhejte hain
        response = requests.post(url, json=new_post)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:  # 201 means created successfully
            created_data = response.json()
            print("✅ Post successfully create ho gaya!")
            print(f"New Post ID: {created_data['id']}")
        else:
            print("❌ Post create nahi hua")
            
    except Exception as e:
        print(f"❌ Error: {e}")

# Step 3: Headers aur Authentication
def advanced_request_example():
    """
    Real world me hume headers aur authentication use karna padta hai
    """
    print("\n🔒 Advanced Request with Headers:")
    
    try:
        url = "https://httpbin.org/headers"
        
        # Custom headers - ye website ko batata hai kon sa browser/app use kar raha hai
        headers = {
            "User-Agent": "Mera Python Automation Bot 1.0",
            "Accept": "application/json",
            "Authorization": "Bearer fake-token-123"  # Fake token for example
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Headers successfully send ho gaye:")
            print(f"User-Agent: {data['headers']['User-Agent']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

# Step 4: Form Data Submit karna
def form_submission_example():
    """
    HTML forms ko submit karne ka tarika
    """
    print("\n📝 Form Submission Example:")
    
    try:
        url = "https://httpbin.org/post"
        
        # Form data - jaise website pe form fill karte hain
        form_data = {
            "name": "Rahul Kumar",
            "email": "rahul@example.com",
            "message": "Ye automation se bheja gaya hai!"
        }
        
        response = requests.post(url, data=form_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Form successfully submit ho gaya!")
            print(f"Submitted Data: {result['form']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

# Step 5: File Download karna
def file_download_example():
    """
    Internet se file download karne ka tarika
    """
    print("\n⬇️ File Download Example:")
    
    try:
        # Small image file download karte hain
        url = "https://httpbin.org/uuid"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            # Current timestamp ke saath filename banate hain
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"downloaded_data_{timestamp}.json"
            
            # File save karte hain
            with open(filename, 'w') as file:
                file.write(response.text)
            
            print(f"✅ File save ho gayi: {filename}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

# Step 6: Multiple Requests - Batch Processing
def batch_processing_example():
    """
    Ek saath multiple requests bhejne ka tarika
    """
    print("\n🔄 Batch Processing Example:")
    
    try:
        base_url = "https://jsonplaceholder.typicode.com/posts"
        
        # 1 se 5 tak posts fetch karte hain
        for i in range(1, 6):
            url = f"{base_url}/{i}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                print(f"📄 Post {i}: {data['title'][:30]}...")
            
            # Har request ke beech me thoda wait karte hain (good practice)
            time.sleep(0.5)
        
        print("✅ Batch processing complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

# Step 7: Error Handling aur Retry Logic
def robust_request_example():
    """
    Real world automation me error handling bahut important hai
    """
    print("\n🛡️ Robust Request with Error Handling:")
    
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            # Deliberately slow endpoint to show retry logic
            url = "https://httpbin.org/delay/1"
            
            print(f"🔄 Attempt {attempt + 1} of {max_retries}")
            
            # Timeout set karte hain
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print("✅ Request successful!")
                return response
            
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout on attempt {attempt + 1}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed on attempt {attempt + 1}: {e}")
        
        if attempt < max_retries - 1:
            print(f"⏳ Waiting before retry...")
            time.sleep(2)
    
    print("❌ All attempts failed!")

# Main function - Sab kuch run karta hai
def main():
    """
    Main function jo sare examples run karta hai
    """
    print("🎯 Complete Web Automation Tutorial")
    print("Ye script terminal me run hoti hai, browser ki zarurat nahi!")
    print("\n")
    
    # Sare examples ek ek karke run karte hain
    get_request_example()
    time.sleep(1)
    
    post_request_example()
    time.sleep(1)
    
    advanced_request_example()
    time.sleep(1)
    
    form_submission_example()
    time.sleep(1)
    
    file_download_example()
    time.sleep(1)
    
    batch_processing_example()
    time.sleep(1)
    
    robust_request_example()
    
    print("\n" + "=" * 50)
    print("🎉 Tutorial Complete! Aapne sikha:")
    print("✅ GET requests - Data fetch karna")
    print("✅ POST requests - Data submit karna")
    print("✅ Headers aur authentication")
    print("✅ Form submission")
    print("✅ File downloading")
    print("✅ Batch processing")
    print("✅ Error handling")
    print("\n💡 Ab aap real websites ke saath kaam kar sakte hain!")

# Script run karne ke liye
if __name__ == "__main__":
    main()
