"""Face++ API service for face recognition"""
import requests
import base64
import os
import time
from flask import current_app
from PIL import Image
import io


class FacePlusPlusService:
    def __init__(self):
        self.api_key = current_app.config['FACE_API_KEY']
        self.api_secret = current_app.config['FACE_API_SECRET']
        self.base_url = "https://api-us.faceplusplus.com/facepp/v3"
        print(f"✅ Face++ Service initialized with key: {self.api_key[:8]}...")

    def compress_image_base64(self, base64_data, max_size_kb=150):
        """Compress base64 image to reduce upload size - FIXED VERSION"""
        try:
            if not base64_data or len(base64_data) < 100:
                return base64_data

            # Remove data URL prefix if present
            if ',' in base64_data:
                base64_data = base64_data.split(',')[1]

            # Decode
            image_data = base64.b64decode(base64_data)

            current_size_kb = len(image_data) / 1024
            if current_size_kb <= max_size_kb:
                # Already small enough
                return f"data:image/jpeg;base64,{base64_data}"

            print(f"📏 Compressing image: {current_size_kb:.1f}KB -> target {max_size_kb}KB")

            # Use PIL to compress
            try:
                # Open image
                image = Image.open(io.BytesIO(image_data))

                # Calculate target dimensions
                # Reduce dimensions if image is very large
                if current_size_kb > 300:
                    # Calculate scaling factor
                    scale_factor = (max_size_kb / current_size_kb) ** 0.5  # Square root for area
                    scale_factor = max(0.5, min(scale_factor, 0.8))  # Keep between 50-80%

                    new_width = int(image.width * scale_factor)
                    new_height = int(image.height * scale_factor)
                    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    print(f"   Resized to: {new_width}x{new_height} ({scale_factor*100:.0f}%)")

                # Save with appropriate quality
                if current_size_kb > 500:
                    quality = 70
                elif current_size_kb > 300:
                    quality = 75
                elif current_size_kb > 150:
                    quality = 80
                else:
                    quality = 85

                # Save with compression
                buffer = io.BytesIO()
                image.save(buffer, format='JPEG', quality=quality, optimize=True)
                compressed_data = buffer.getvalue()

                new_size_kb = len(compressed_data) / 1024
                print(f"✅ Compressed to: {new_size_kb:.1f}KB (quality: {quality}%)")

                # Convert back to base64
                compressed_base64 = base64.b64encode(compressed_data).decode('utf-8')
                return f"data:image/jpeg;base64,{compressed_base64}"

            except Exception as pil_error:
                print(f"⚠️ PIL compression failed: {pil_error}")
                return f"data:image/jpeg;base64,{base64_data}"

        except Exception as e:
            print(f"⚠️ Compression error: {e}")
            return f"data:image/jpeg;base64,{base64_data}"

    def compare_faces(self, face_image1, face_image2, image1_is_url=False, image2_is_url=False):
        """Compare two faces - can use base64 images or URLs"""
        url = f"{self.base_url}/compare"

        # Compress images before sending (if they're base64)
        if not image1_is_url and face_image1:
            face_image1 = self.compress_image_base64(face_image1)
            # Extract pure base64 for Face++ API
            if ',' in face_image1:
                face_image1 = face_image1.split(',')[1]

        if not image2_is_url and face_image2:
            face_image2 = self.compress_image_base64(face_image2)
            if ',' in face_image2:
                face_image2 = face_image2.split(',')[1]

        data = {
            'api_key': self.api_key,
            'api_secret': self.api_secret,
        }

        # Handle different image types
        if image1_is_url:
            data['image_url1'] = face_image1
        else:
            data['image_base64_1'] = face_image1

        if image2_is_url:
            data['image_url2'] = face_image2
        else:
            data['image_base64_2'] = face_image2

        try:
            print("🔍 Comparing faces with Face++...")

            # Try with retry logic
            for attempt in range(3):
                try:
                    response = requests.post(url, data=data, timeout=25)
                    result = response.json()
                    print(f"📊 Face++ Compare Response received (attempt {attempt + 1})")
                    break  # Success, exit retry loop
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                    if attempt == 2:  # Last attempt
                        raise
                    print(f"⚠️ Face++ timeout attempt {attempt + 1}, retrying in 2 seconds...")
                    time.sleep(2)

            print(f"📊 Face++ Compare Response keys: {list(result.keys())}")

            if 'error_message' in result:
                print(f"❌ Face++ Error: {result['error_message']}")
                return 0, False  # RETURNS 2 VALUES - FIXED!

            confidence = result.get('confidence', 0)
            print(f"✅ Face comparison confidence: {confidence}%")

            # IMPORTANT: Return ONLY 2 values to match existing code
            return confidence, True  # ← FIXED: Only 2 values!

        except requests.exceptions.Timeout:
            print("❌ Face++ API timeout after 25 seconds")
            return 0, False  # RETURNS 2 VALUES
        except Exception as e:
            print(f"❌ Face comparison error: {e}")
            return 0, False  # RETURNS 2 VALUES

    def detect_face_quality(self, image_data, is_url=False):
        """Check if image has a good quality face"""
        url = f"{self.base_url}/detect"

        # Compress image if it's base64
        if not is_url and image_data:
            image_data = self.compress_image_base64(image_data)
            if ',' in image_data:
                image_data = image_data.split(',')[1]

        data = {
            'api_key': self.api_key,
            'api_secret': self.api_secret,
            'return_attributes': 'facequality'
        }

        if is_url:
            data['image_url'] = image_data
        else:
            data['image_base64'] = image_data

        try:
            response = requests.post(url, data=data, timeout=15)
            result = response.json()

            if 'faces' in result and len(result['faces']) > 0:
                quality = result['faces'][0]['attributes']['facequality']['value']
                return quality >= 30  # Minimum quality threshold

            return False

        except Exception as e:
            print(f"❌ Face detection error: {e}")
            return False

    def create_faceset(self, faceset_token='worknest_faceset'):
        """Create a faceset for storing staff faces"""
        url = f"{self.base_url}/faceset/create"
        data = {
            'api_key': self.api_key,
            'api_secret': self.api_secret,
            'faceset_token': faceset_token,
            'display_name': 'WorkNest Staff Faces',
            'outer_id': 'worknest_staff'
        }

        try:
            print("🏗️ Creating Face++ faceset...")
            response = requests.post(url, data=data, timeout=10)
            result = response.json()

            print(f"📊 Create Faceset Response: {result}")

            if 'error_message' in result:
                # If faceset already exists, that's fine
                if 'FACESET_EXIST' in result['error_message']:
                    print("✅ Faceset already exists")
                    return True
                print(f"❌ Face++ Error: {result['error_message']}")
                return False

            success = 'faceset_token' in result
            if success:
                print("✅ Faceset created successfully!")
            else:
                print("❌ Failed to create faceset")

            return success

        except Exception as e:
            print(f"❌ Create faceset error: {e}")
            return False