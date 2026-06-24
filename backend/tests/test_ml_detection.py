import pytest
import numpy as np
from ml.detection_engine import (
    FeatureExtractor, 
    AnomalyDetectionEngine,
    ThreatScoringEngine,
    ExplainabilityModule
)


@pytest.mark.unit
def test_feature_extraction_packet():
    """Test packet feature extraction"""
    extractor = FeatureExtractor()
    
    packet = {
        "size": 1500,
        "ttl": 64,
        "protocol": "TCP",
        "has_payload": True,
        "flags": "SYN"
    }
    
    features = extractor.extract_packet_features(packet)
    
    assert features["packet_size"] == 1500
    assert features["ttl"] == 64
    assert features["has_payload"] == 1
    assert len(features) == 5


@pytest.mark.unit
def test_feature_extraction_flow():
    """Test network flow feature extraction"""
    extractor = FeatureExtractor()
    
    flow_data = {
        "packet_count": 100,
        "bytes_sent": 50000,
        "bytes_received": 75000,
        "duration": 30,
        "protocol": "TCP",
        "destination_port": 443
    }
    
    features = extractor.extract_flow_features(flow_data)
    
    assert features["packet_count"] == 100
    assert features["bytes_sent"] == 50000
    assert features["destination_port"] == 443
    assert "port_anomaly_score" in features


@pytest.mark.unit
def test_anomaly_detection():
    """Test anomaly detection engine"""
    engine = AnomalyDetectionEngine()
    
    # Normal traffic features (should have low anomaly score)
    normal_features = [1, 0.5, 0.3, 100, 0.1]
    
    # Abnormal traffic features (should have high anomaly score)
    abnormal_features = [10, 0.9, 0.9, 1000, 0.9]
    
    normal_score = engine.detect_anomaly(normal_features)
    abnormal_score = engine.detect_anomaly(abnormal_features)
    
    assert isinstance(normal_score, tuple)
    assert len(normal_score) == 2
    assert 0 <= normal_score[0] <= 1
    assert abnormal_score[0] > normal_score[0]


@pytest.mark.unit
def test_risk_scoring():
    """Test risk scoring engine"""
    engine = ThreatScoringEngine()
    
    risk_score = engine.calculate_risk_score(
        anomaly_score=0.85,
        source_reputation=0.9,
        port_anomaly=0.5,
        byte_ratio_anomaly=0.3
    )
    
    assert 0 <= risk_score <= 100
    assert risk_score > 50  # Should be high for high anomaly


@pytest.mark.unit
def test_confidence_calculation():
    """Test confidence calculation"""
    engine = ThreatScoringEngine()
    
    confidence = engine.calculate_confidence(
        model_agreement=0.95,
        data_quality=0.9,
        historical_accuracy=0.92
    )
    
    assert 0 <= confidence <= 100
    assert confidence > 85


@pytest.mark.unit
def test_severity_determination():
    """Test severity determination"""
    engine = ThreatScoringEngine()
    
    assert engine.determine_severity(95) == "critical"
    assert engine.determine_severity(65) == "high"
    assert engine.determine_severity(45) == "medium"
    assert engine.determine_severity(25) == "low"
    assert engine.determine_severity(10) == "info"


@pytest.mark.unit
def test_explainability():
    """Test threat explanation generation"""
    module = ExplainabilityModule()
    
    features = {
        "anomaly_score": 0.85,
        "request_rate": 1000,
        "destination_port": 443,
        "byte_ratio": 0.9
    }
    
    explanation = module.generate_explanation(
        features=features,
        anomaly_score=0.85,
        risk_score=75
    )
    
    assert isinstance(explanation, str)
    assert len(explanation) > 0
    assert "anomaly" in explanation.lower() or "unusual" in explanation.lower()
