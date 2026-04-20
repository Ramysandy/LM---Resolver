"""Groq API client module for high-performance inference."""

import json
import time
import asyncio
from typing import Dict, Any, List
from groq import Groq
import streamlit as st
from config import GROQ_API_KEY, GROQ_MODEL, SYSTEM_PROMPT


class GroqAddressResolver:
    """Client for Groq-powered address resolution."""

    def __init__(self, api_key: str = GROQ_API_KEY):
        """Initialize Groq client."""
        if not api_key:
            raise ValueError("GROQ_API_KEY not found. Please set it in .env or Streamlit secrets.")
        self.client = Groq(api_key=api_key)
        self.model = GROQ_MODEL
        self.system_prompt = SYSTEM_PROMPT

    def resolve_address(self, address: str) -> tuple[Dict[str, Any], float]:
        """
        Resolve unstructured address through Groq with powerful single-shot extraction.
        
        Args:
            address: Unstructured delivery address
            
        Returns:
            Tuple of (parsed_json, inference_time_ms)
        """
        start_time = time.time()
        
        try:
            # Single powerful extraction prompt - comprehensive GCC mapping
            extraction_prompt = f"""You are a GCC (Gulf Cooperation Council) address extraction expert. Extract EVERY detail from this address text to prevent failed deliveries.

INPUT TEXT: "{address}"

EXTRACTION RULES (STRICT):
1. Neighborhood/Area Mapping: 
   - "JVC" = "Jumeirah Village Circle" (Dubai)
   - "Al Olaya" = "Al Olaya" (Riyadh)
   - "Deira" = "Deira" (Dubai)
   - "Bur Dubai" = "Bur Dubai" (Dubai)
   - Extract EXACTLY what's in input, use mappings above

2. Landmarks & Buildings:
   - Extract ALL landmarks mentioned: mosque, park, bank, pharmacy, mall, shopping center, etc.
   - Extract building names: "Blue Gate", "Big Pharmacy", "Green Building" = building (not landmark)
   - Separate landmarks from buildings

3. Delivery Details:
   - Floor/Unit: Extract ONLY actual numbers in input ("4th floor", "Unit A", "4") - NEVER make up "1111"
   - Street/Road names: Extract exactly as stated
   - Instructions: Extract delivery notes from input

4. Quality Rules:
   - DO NOT hallucinate ANY data
   - If field not in input, return empty string "" or empty array []
   - Only extract information that is EXPLICITLY stated

RETURN ONLY THIS JSON (no markdown, no explanations, no trailing text):
{{
  "neighborhood": "extracted or empty string",
  "street": "extracted or empty string",
  "building": "extracted building name or empty string",
  "floor_unit": "extracted floor/unit or empty string",
  "landmarks": ["landmark1", "landmark2"],
  "instructions": "delivery instructions from input or empty string",
  "city": "Dubai|Abu Dhabi|Riyadh|Jeddah|Sharjah or empty string"
}}"""
            
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a logistics JSON extraction agent. Extract data accurately and completely from unstructured text. If data is in the input, extract it. Do not hallucinate."},
                    {"role": "user", "content": extraction_prompt},
                ],
                temperature=0.05,  # Ultra-low for consistency
                max_tokens=500,
            )
            
            response_text = message.choices[0].message.content.strip()
            
            # Parse JSON response
            parsed_data = json.loads(response_text)
            
            # Validate and clean JSON using lighter touch
            cleaned_data = self._validate_and_clean_json(parsed_data)
            
            # Calculate proper risk score based on field completeness (rounded, no floating point slop)
            cleaned_data["risk_score"] = round(self._calculate_risk_score(cleaned_data, address), 2)
            
            # Set requires_customer_call based on risk score
            cleaned_data["requires_customer_call"] = cleaned_data["risk_score"] > 0.6
            
            # Inject realistic geo coordinates based on extracted city/neighborhood
            cleaned_data["geo_coordinates"] = self._get_geo_coordinates(
                cleaned_data.get("city", ""),
                cleaned_data.get("neighborhood", ""),
                cleaned_data.get("landmarks", [])
            )
            
            inference_time = (time.time() - start_time) * 1000  # Convert to ms
            
            return cleaned_data, inference_time
            
        except json.JSONDecodeError as e:
            inference_time = (time.time() - start_time) * 1000
            st.error(f"Failed to parse Groq response as JSON: {e}")
            return self._error_response(address), inference_time
        except Exception as e:
            inference_time = (time.time() - start_time) * 1000
            st.error(f"Groq API error: {str(e)}")
            return self._error_response(address), inference_time
    
    @staticmethod
    def _validate_and_clean_json(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and clean JSON - ON LIGHT TOUCH.
        Only reject actual hallucinations like "1111", "9999".
        Trust the AI extraction.
        """
        required_fields = {
            "neighborhood": "",
            "street": "",
            "building": "",
            "floor_unit": "",
            "landmarks": [],
            "instructions": "",
            "risk_score": 0.5,
            "city": "",
            "requires_customer_call": False,
        }
        
        # ONLY reject these EXACT hallucination patterns
        HALLUCINATION_PATTERNS = ["1111", "9999", "0000", "8888", "7777", "6666", "5555", "4444", "3333", "2222"]
        
        cleaned = {}
        
        for field, default in required_fields.items():
            if field not in data:
                cleaned[field] = default
                continue
            
            value = data[field]
            
            # Skip empty/None values
            if value is None or (isinstance(value, str) and value.strip() == ""):
                cleaned[field] = default
                continue
            
            # For string fields: check ONLY for exact hallucination patterns
            if isinstance(value, str):
                # ONLY reject if value is one of the hallucination patterns
                if any(pattern == value.strip() for pattern in HALLUCINATION_PATTERNS):
                    cleaned[field] = default
                    continue
                
                if field in ["neighborhood", "street", "building", "city", "instructions"]:
                    # Keep the value as-is (don't blank it out just because it's lowercase or looks weird)
                    cleaned[field] = value.strip() if value.strip() != "Unknown" else ""
                elif field == "floor_unit":
                    # For floor: accept if it has digits or looks like a floor descriptor
                    f_str = value.strip()
                    if any(pattern == f_str for pattern in HALLUCINATION_PATTERNS):
                        cleaned[field] = ""
                    elif f_str and f_str != "Unknown":
                        cleaned[field] = f_str
                    else:
                        cleaned[field] = ""
            
            elif field == "landmarks":
                if isinstance(value, list):
                    cleaned_landmarks = []
                    for landmark in value:
                        l_str = str(landmark).strip() if landmark else ""
                        # ONLY skip exact hallucination patterns
                        if l_str and l_str not in HALLUCINATION_PATTERNS and l_str != "Unknown":
                            cleaned_landmarks.append(l_str)
                    cleaned[field] = cleaned_landmarks
                else:
                    cleaned[field] = []
            
            elif field == "risk_score":
                try:
                    score = float(value)
                    cleaned[field] = round(max(0.0, min(1.0, score)), 2)
                except (ValueError, TypeError):
                    cleaned[field] = 0.5
            
            elif field == "requires_customer_call":
                if isinstance(value, bool):
                    cleaned[field] = value
                else:
                    cleaned[field] = False
            
            else:
                cleaned[field] = value
        
        return cleaned
    
    @staticmethod
    def _calculate_risk_score(data: Dict[str, Any], original_address: str) -> float:
        """
        Calculate risk score based on extraction completeness.
        0.0-0.3: Excellent extraction (all fields present)
        0.3-0.6: Good extraction (most fields present)
        0.6-1.0: Poor extraction (missing key fields)
        """
        score = 0.5  # Base
        
        # Positive signals (reduce risk)
        if data.get("neighborhood"):
            score -= 0.15
        if data.get("building"):
            score -= 0.1
        if data.get("street"):
            score -= 0.1
        if data.get("floor_unit"):
            score -= 0.05
        if data.get("landmarks") and len(data["landmarks"]) > 0:
            score -= 0.1
        if data.get("city"):
            score -= 0.1
        
        # Negative signals (increase risk)
        has_ambiguous = any(word in original_address.lower() for word in ["near", "close", "around", "maybe", "possibly"])
        if has_ambiguous:
            score += 0.15
        
        # Cap between 0 and 1, rounded to 2 decimal places
        return round(max(0.0, min(1.0, score)), 2)

    @staticmethod
    def _get_geo_coordinates(city: str, neighborhood: str, landmarks: list) -> Dict[str, float]:
        """
        Return realistic GPS coordinates for GCC locations.
        Uses a lookup table of real coordinates — NOT AI-guessed, NOT placeholder 25.0/55.0.
        """
        city_lc = city.lower().strip()
        area_lc = neighborhood.lower().strip()

        # Precise neighborhood-level lookup (most specific, checked first)
        AREA_COORDS = {
            # Dubai neighborhoods
            "jumeirah village circle": (25.0617, 55.2059),
            "jvc": (25.0617, 55.2059),
            "downtown dubai": (25.1972, 55.2796),
            "dubai marina": (25.0805, 55.1403),
            "jumeirah": (25.2084, 55.2484),
            "deira": (25.2706, 55.3097),
            "bur dubai": (25.2537, 55.2969),
            "business bay": (25.1883, 55.2636),
            "palm jumeirah": (25.1124, 55.1390),
            "al barsha": (25.1057, 55.1999),
            "discovery gardens": (25.0337, 55.1530),
            "international city": (25.1655, 55.4121),
            "silicon oasis": (25.1176, 55.3802),
            "mirdif": (25.2220, 55.4201),
            "qusais": (25.2811, 55.3869),
            "karama": (25.2369, 55.3041),
            "satwa": (25.2287, 55.2730),
            "al quoz": (25.1475, 55.2278),
            "jbr": (25.0779, 55.1354),
            "difc": (25.2084, 55.2811),
            "creek": (25.2285, 55.3273),
            # Riyadh neighborhoods
            "al olaya": (24.6936, 46.6852),
            "al malaz": (24.6819, 46.7448),
            "al nakheel": (24.7543, 46.6279),
            "al muruj": (24.7271, 46.6621),
            "al sulaimaniyah": (24.6930, 46.6739),
            "al-sulaimaniyah": (24.6930, 46.6739),
            "king fahad district": (24.7601, 46.6358),
            "al woroud": (24.7314, 46.6298),
            # Jeddah neighborhoods
            "al hamra": (21.5547, 39.1531),
            "al zahra": (21.5700, 39.1655),
            "al rawdah": (21.5362, 39.1880),
            "al andalus": (21.5183, 39.2178),
            "al khalidiyah": (21.5460, 39.1918),
            # Abu Dhabi neighborhoods
            "al reem island": (24.5000, 54.4030),
            "khalifa city": (24.4240, 54.5906),
            "al raha beach": (24.4200, 54.6130),
            "yas island": (24.4968, 54.6073),
            "corniche": (24.4628, 54.3555),
        }

        # City-level fallback coordinates
        CITY_COORDS = {
            "dubai": (25.2048, 55.2708),
            "abu dhabi": (24.4539, 54.3773),
            "riyadh": (24.7136, 46.6753),
            "jeddah": (21.5433, 39.1727),
            "sharjah": (25.3460, 55.4209),
            "ajman": (25.4052, 55.5136),
            "al ain": (24.2075, 55.7447),
            "dammam": (26.4124, 50.1971),
        }

        # Check neighborhood first (most precise, exact match)
        if area_lc and area_lc in AREA_COORDS:
            lat, lon = AREA_COORDS[area_lc]
            return {"latitude": lat, "longitude": lon}

        # Partial match on area name (only if area_lc is non-empty to avoid "" matching everything)
        if area_lc:
            for key, coords in AREA_COORDS.items():
                if key in area_lc or area_lc in key:
                    return {"latitude": coords[0], "longitude": coords[1]}

        # Fall back to city
        if city_lc and city_lc in CITY_COORDS:
            lat, lon = CITY_COORDS[city_lc]
            return {"latitude": lat, "longitude": lon}

        # Default: Dubai center (better than 25.0, 55.0)
        return {"latitude": 25.2048, "longitude": 55.2708}

    @staticmethod
    def _error_response(address: str) -> Dict[str, Any]:
        """Generate error response structure."""
        return {
            "neighborhood": "",
            "street": "",
            "building": "",
            "floor_unit": "",
            "landmarks": [],
            "instructions": address,
            "risk_score": 1.0,
            "geo_coordinates": {"latitude": 25.2048, "longitude": 55.2708},
            "city": "",
            "requires_customer_call": True,
        }

    async def resolve_address_async(self, address: str) -> tuple[Dict[str, Any], float]:
        """
        Async version for concurrent requests.
        
        Args:
            address: Unstructured delivery address
            
        Returns:
            Tuple of (parsed_json, inference_time_ms)
        """
        # Run sync method in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.resolve_address, address)


class StressTestRunner:
    """Runner for Yellow Friday stress tests."""

    def __init__(self, groq_resolver: GroqAddressResolver, num_requests: int = 10):
        """Initialize stress test runner."""
        self.resolver = groq_resolver
        self.num_requests = num_requests
        self.results: List[Dict[str, Any]] = []

    async def run_concurrent_requests(
        self, addresses: List[str]
    ) -> Dict[str, Any]:
        """
        Run multiple concurrent address resolutions.
        
        Args:
            addresses: List of addresses to resolve
            
        Returns:
            Test results and metrics
        """
        start_time = time.time()
        
        tasks = [
            self.resolver.resolve_address_async(addr) 
            for addr in addresses[:self.num_requests]
        ]
        
        results = await asyncio.gather(*tasks)
        
        total_time = (time.time() - start_time) * 1000
        
        # Extract inference times
        inference_times = [result[1] for result in results]
        
        return {
            "total_time_ms": total_time,
            "num_requests": len(results),
            "avg_inference_ms": sum(inference_times) / len(inference_times),
            "max_inference_ms": max(inference_times),
            "min_inference_ms": min(inference_times),
            "requests_per_second": len(results) / (total_time / 1000),
            "results": [result[0] for result in results],
        }
