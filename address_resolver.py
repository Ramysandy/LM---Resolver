"""Address resolution pipeline with multi-stage agentic reasoning."""

from typing import Dict, Any, List
import time
from dataclasses import dataclass
from groq_client import GroqAddressResolver


@dataclass
class ResolutionStage:
    """Represents a stage in the resolution pipeline."""
    name: str
    description: str
    status: str  # "pending", "processing", "complete"
    result: Dict[str, Any] = None


class AddressResolutionPipeline:
    """Multi-stage address resolution pipeline."""

    def __init__(self, groq_resolver: GroqAddressResolver):
        """Initialize pipeline."""
        self.resolver = groq_resolver
        self.stages: List[ResolutionStage] = []

    def process_address(
        self, address: str, show_stages: bool = True
    ) -> tuple[Dict[str, Any], List[Dict[str, Any]], float]:
        """
        Process address through 3-stage pipeline (for UI display).
        Uses single powerful API call, then breaks results into stages.
        
        Args:
            address: Unstructured address
            show_stages: Whether to return stage details
            
        Returns:
            Tuple of (final_resolved_json, stages_breakdown, total_time_ms)
        """
        start_time = time.time()
        
        # SINGLE POWERFUL API CALL - get everything at once
        final_resolved, api_time = self.resolver.resolve_address(address)
        
        # Now break the resolved data into stages for UI display
        # These are calculated from the SINGLE API response, not separate calls
        
        # Stage 1: Show what was extracted
        stage1 = ResolutionStage(
            name="NLP Entity Parsing",
            description="Extract landmarks, neighborhood, city, building details",
            status="complete",
            result={
                "entities": {
                    "neighborhood": final_resolved.get("neighborhood", ""),
                    "city": final_resolved.get("city", ""),
                    "building": final_resolved.get("building", ""),
                    "landmarks": final_resolved.get("landmarks", []),
                },
                "inference_time_ms": api_time,
            },
        )
        self.stages.append(stage1)
        
        # Stage 2: Risk assessment based on extracted data
        risk_score = final_resolved.get("risk_score", 0.5)
        stage2 = ResolutionStage(
            name="Risk-Based Validation",
            description="Assign certainty score, identify if customer call needed",
            status="complete",
            result={
                "risk_score": risk_score,
                "inference_time_ms": 0,  # Already included in API call
                "requires_call": risk_score > 0.6,
            },
        )
        self.stages.append(stage2)
        
        # Stage 3: Geo coordinates
        coords = final_resolved.get("geo_coordinates", {"latitude": 24.0, "longitude": 54.0})
        stage3 = ResolutionStage(
            name="Geo-Synthesis",
            description="Generate latitude/longitude based on landmark data",
            status="complete",
            result={
                "coordinates": coords,
                "inference_time_ms": 0,  # Already included in API call
            },
        )
        self.stages.append(stage3)
        
        total_time = (time.time() - start_time) * 1000
        
        stages_data = [
            {
                "name": stage.name,
                "description": stage.description,
                "status": stage.status,
                "result": stage.result,
            }
            for stage in self.stages
        ]
        
        return final_resolved, stages_data, total_time


    def reset_stages(self) -> None:
        """Reset pipeline stages."""
        self.stages = []
