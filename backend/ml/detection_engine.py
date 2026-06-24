import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import os
from datetime import datetime


class FeatureExtractor:
    """Extract features from network flows and packets."""
    
    @staticmethod
    def extract_packet_features(packet_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract features from a single packet."""
        features = {
            "packet_size": packet_data.get("size", 0),
            "ttl": packet_data.get("ttl", 64),
            "protocol": FeatureExtractor._encode_protocol(packet_data.get("protocol", "TCP")),
            "has_payload": 1 if packet_data.get("payload") else 0,
            "flags": FeatureExtractor._encode_flags(packet_data.get("flags", 0)),
        }
        return features

    @staticmethod
    def extract_flow_features(flow_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract features from network flow."""
        features = {
            "packet_count": flow_data.get("packet_count", 0),
            "bytes_sent": flow_data.get("bytes_sent", 0),
            "bytes_received": flow_data.get("bytes_received", 0),
            "duration": flow_data.get("duration", 0),
            "request_rate": FeatureExtractor._calculate_request_rate(
                flow_data.get("packet_count", 0),
                flow_data.get("duration", 1)
            ),
            "protocol": FeatureExtractor._encode_protocol(flow_data.get("protocol", "TCP")),
            "port_anomaly": FeatureExtractor._port_anomaly_score(flow_data.get("destination_port", 0)),
            "byte_ratio": FeatureExtractor._calculate_byte_ratio(
                flow_data.get("bytes_sent", 0),
                flow_data.get("bytes_received", 0)
            ),
        }
        return features

    @staticmethod
    def extract_behavioral_features(flow_history: list) -> Dict[str, float]:
        """Extract behavioral features from flow history."""
        if not flow_history:
            return {}
        
        bytes_sent_list = [f.get("bytes_sent", 0) for f in flow_history]
        packet_counts = [f.get("packet_count", 0) for f in flow_history]
        
        features = {
            "avg_bytes_sent": np.mean(bytes_sent_list) if bytes_sent_list else 0,
            "std_bytes_sent": np.std(bytes_sent_list) if len(bytes_sent_list) > 1 else 0,
            "avg_packets": np.mean(packet_counts) if packet_counts else 0,
            "traffic_variance": np.var(bytes_sent_list) if bytes_sent_list else 0,
        }
        return features

    @staticmethod
    def _encode_protocol(protocol: str) -> float:
        protocol_map = {"TCP": 0, "UDP": 1, "ICMP": 2, "HTTP": 3, "HTTPS": 4, "DNS": 5, "SSH": 6, "FTP": 7}
        return float(protocol_map.get(protocol.upper(), 0))

    @staticmethod
    def _encode_flags(flags: int) -> float:
        return float(flags & 0xFF)

    @staticmethod
    def _calculate_request_rate(packet_count: int, duration: float) -> float:
        if duration <= 0:
            return 0
        return packet_count / duration

    @staticmethod
    def _port_anomaly_score(port: int) -> float:
        """Score anomaly based on port number."""
        reserved_ports = set(range(0, 1024))
        well_known = {80, 443, 22, 21, 25, 53, 123, 3306, 5432, 27017}
        
        if port in well_known:
            return 0.1
        elif port in reserved_ports:
            return 0.3
        elif port > 49152:
            return 0.2
        else:
            return 0.5

    @staticmethod
    def _calculate_byte_ratio(bytes_sent: int, bytes_received: int) -> float:
        total = bytes_sent + bytes_received
        if total == 0:
            return 0.5
        return bytes_sent / total


class AnomalyDetectionEngine:
    """Ensemble anomaly detection using multiple models."""
    
    def __init__(self):
        self.isolation_forest = Pipeline([
            ("scaler", StandardScaler()),
            ("model", IsolationForest(contamination=0.1, random_state=42))
        ])
        self.model_path = "models/anomaly_detector.pkl"
        self.scaler = StandardScaler()
        self.is_trained = False

    def train(self, X: np.ndarray, y: Optional[np.ndarray] = None):
        """Train the anomaly detection models."""
        try:
            self.isolation_forest.fit(X)
            self.scaler.fit(X)
            self.is_trained = True
            os.makedirs("models", exist_ok=True)
            joblib.dump(self, self.model_path)
        except Exception as e:
            print(f"Error training anomaly detector: {e}")

    def detect_anomaly(self, features: Dict[str, float]) -> Tuple[float, str]:
        """
        Detect if features represent an anomaly.
        Returns: (anomaly_score, severity)
        """
        if not self.is_trained:
            return 0.0, "low"
        
        try:
            feature_array = np.array(list(features.values())).reshape(1, -1)
            
            # Isolation Forest score
            if_score = self.isolation_forest.predict(feature_array)[0]
            
            # Calculate statistical anomaly score
            scaled_features = self.scaler.transform(feature_array)
            statistical_score = np.abs(scaled_features).mean()
            
            # Ensemble score
            anomaly_score = (abs(if_score) + statistical_score) / 2
            
            # Normalize to 0-1
            anomaly_score = min(1.0, max(0.0, anomaly_score))
            
            # Determine severity
            if anomaly_score > 0.8:
                severity = "critical"
            elif anomaly_score > 0.6:
                severity = "high"
            elif anomaly_score > 0.4:
                severity = "medium"
            else:
                severity = "low"
            
            return anomaly_score, severity
        except Exception as e:
            print(f"Error detecting anomaly: {e}")
            return 0.0, "low"

    @staticmethod
    def load(model_path: str = "models/anomaly_detector.pkl"):
        """Load trained model."""
        if os.path.exists(model_path):
            return joblib.load(model_path)
        return AnomalyDetectionEngine()


class ThreatScoringEngine:
    """Calculate threat and risk scores."""
    
    @staticmethod
    def calculate_risk_score(
        anomaly_score: float,
        source_reputation: float = 0.0,
        port_anomaly: float = 0.0,
        byte_ratio_anomaly: float = 0.0,
    ) -> float:
        """Calculate overall risk score (0-100)."""
        weights = {
            "anomaly": 0.5,
            "reputation": 0.2,
            "port": 0.15,
            "byte_ratio": 0.15,
        }
        
        risk_score = (
            anomaly_score * 100 * weights["anomaly"] +
            source_reputation * weights["reputation"] +
            port_anomaly * 100 * weights["port"] +
            byte_ratio_anomaly * 100 * weights["byte_ratio"]
        )
        
        return min(100.0, max(0.0, risk_score))

    @staticmethod
    def calculate_confidence(
        model_agreement: float,
        data_quality: float = 0.9,
        historical_accuracy: float = 0.92,
    ) -> float:
        """Calculate confidence score for detection (0-100)."""
        confidence = (model_agreement * 0.4 + data_quality * 0.3 + historical_accuracy * 0.3) * 100
        return min(100.0, max(0.0, confidence))

    @staticmethod
    def determine_severity(risk_score: float) -> str:
        """Determine severity level based on risk score."""
        if risk_score >= 80:
            return "critical"
        elif risk_score >= 60:
            return "high"
        elif risk_score >= 40:
            return "medium"
        elif risk_score >= 20:
            return "low"
        else:
            return "info"


class ExplainabilityModule:
    """Explain threat detections."""
    
    @staticmethod
    def generate_explanation(
        features: Dict[str, float],
        anomaly_score: float,
        risk_score: float,
    ) -> str:
        """Generate human-readable explanation for detection."""
        explanation_parts = []
        
        if anomaly_score > 0.7:
            explanation_parts.append("Unusual behavioral pattern detected.")
        
        if features.get("request_rate", 0) > 1000:
            explanation_parts.append("Abnormally high request rate observed.")
        
        if features.get("port_anomaly", 0) > 0.5:
            explanation_parts.append("Connection to suspicious port detected.")
        
        if features.get("byte_ratio", 0.5) > 0.9 or features.get("byte_ratio", 0.5) < 0.1:
            explanation_parts.append("Asymmetric data transfer pattern detected.")
        
        if not explanation_parts:
            explanation_parts.append("Multiple statistical anomalies detected.")
        
        return " ".join(explanation_parts)


class DetectionPipeline:
    """Complete detection pipeline."""
    
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.anomaly_engine = AnomalyDetectionEngine()
        self.threat_scorer = ThreatScoringEngine()
        self.explainability = ExplainabilityModule()

    def process_network_flow(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a network flow through the entire pipeline."""
        # Extract features
        flow_features = self.feature_extractor.extract_flow_features(flow_data)
        
        # Detect anomaly
        anomaly_score, anomaly_severity = self.anomaly_engine.detect_anomaly(flow_features)
        
        # Calculate risk score
        risk_score = self.threat_scorer.calculate_risk_score(
            anomaly_score,
            source_reputation=flow_data.get("source_reputation", 0.0),
            port_anomaly=flow_features.get("port_anomaly", 0.0),
            byte_ratio_anomaly=abs(flow_features.get("byte_ratio", 0.5) - 0.5),
        )
        
        # Determine severity
        severity = self.threat_scorer.determine_severity(risk_score)
        
        # Calculate confidence
        confidence = self.threat_scorer.calculate_confidence(
            model_agreement=anomaly_score,
            data_quality=flow_data.get("data_quality", 0.9),
        )
        
        # Generate explanation
        explanation = self.explainability.generate_explanation(
            flow_features,
            anomaly_score,
            risk_score,
        )
        
        return {
            "anomaly_score": round(anomaly_score, 3),
            "risk_score": round(risk_score, 1),
            "severity": severity,
            "confidence": round(confidence, 1),
            "explanation": explanation,
            "features_used": flow_features,
            "timestamp": datetime.utcnow().isoformat(),
        }
