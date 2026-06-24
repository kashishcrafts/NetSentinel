#!/usr/bin/env python
"""
Seed database with sample data for development and demonstration.
Run this script after creating tables with: alembic upgrade head
"""

import sys
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User
from models.extended import (
    Alert, AlertStatus, AlertPriority,
    Incident, IncidentStatus,
    IOC, IOCType,
    ThreatIntelligence, MitreMapping,
    NetworkFlow,
    AuditLog
)
from core.database import Base, engine
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def seed_database():
    """Seed database with sample data"""
    Base.metadata.create_all(bind=engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Clear existing data (dev only!)
        print("🔄 Clearing existing data...")
        session.query(AuditLog).delete()
        session.query(MitreMapping).delete()
        session.query(NetworkFlow).delete()
        session.query(IOC).delete()
        session.query(Alert).delete()
        session.query(Incident).delete()
        session.query(ThreatIntelligence).delete()
        session.query(User).delete()
        session.commit()
        
        # Create users
        print("👥 Creating users...")
        users = [
            User(
                email="admin@netsentinel.io",
                username="admin",
                hashed_password=pwd_context.hash("admin123"),
                full_name="System Administrator",
                role="Super Admin"
            ),
            User(
                email="analyst@netsentinel.io",
                username="analyst",
                hashed_password=pwd_context.hash("analyst123"),
                full_name="SOC Analyst",
                role="SOC Analyst"
            ),
            User(
                email="hunter@netsentinel.io",
                username="hunter",
                hashed_password=pwd_context.hash("hunter123"),
                full_name="Threat Hunter",
                role="Threat Hunter"
            ),
            User(
                email="responder@netsentinel.io",
                username="responder",
                hashed_password=pwd_context.hash("responder123"),
                full_name="Incident Responder",
                role="Incident Responder"
            ),
        ]
        session.add_all(users)
        session.commit()
        print(f"✅ Created {len(users)} users")
        
        # Create threats
        print("🎯 Creating threats...")
        threats = [
            ThreatIntelligence(
                threat_name="LokiBot Trojan",
                threat_actor="Unknown",
                severity="critical",
                risk_score=95,
                malware_families=["LokiBot", "Marcher"],
                kill_chain="Delivery, Installation, Command and Control",
                mitre_techniques=["T1566.002", "T1189"],
                mitre_tactics=["TA0001", "TA0002"]
            ),
            ThreatIntelligence(
                threat_name="APT29 Campaign",
                threat_actor="Russian State",
                severity="critical",
                risk_score=98,
                malware_families=["Cozy Bear", "The Dukes"],
                kill_chain="Reconnaissance, Weaponization, Delivery, Exploitation",
                mitre_techniques=["T1087", "T1201"],
                mitre_tactics=["TA0007", "TA0009"]
            ),
            ThreatIntelligence(
                threat_name="Emotet Banking Malware",
                threat_actor="Eastern Europe",
                severity="high",
                risk_score=85,
                malware_families=["Emotet", "Heodo"],
                kill_chain="Delivery, Installation, C2",
                mitre_techniques=["T1566", "T1070"],
                mitre_tactics=["TA0001", "TA0005"]
            ),
        ]
        session.add_all(threats)
        session.commit()
        print(f"✅ Created {len(threats)} threats")
        
        # Create IOCs
        print("📍 Creating IOCs...")
        iocs = [
            IOC(
                value="192.168.1.100",
                ioc_type=IOCType.IP,
                reputation=0.85,
                risk_score=90,
                confidence=0.95,
                source="VirusTotal",
                tags=["malware", "c2", "botnet"]
            ),
            IOC(
                value="malicious.example.com",
                ioc_type=IOCType.DOMAIN,
                reputation=0.92,
                risk_score=95,
                confidence=0.98,
                source="AbuseIPDB",
                tags=["phishing", "c2"]
            ),
            IOC(
                value="5d41402abc4b2a76b9719d911017c592",
                ioc_type=IOCType.HASH,
                reputation=0.88,
                risk_score=92,
                confidence=0.96,
                source="AlienVault OTX",
                tags=["trojan", "banking_malware"]
            ),
        ]
        session.add_all(iocs)
        session.commit()
        print(f"✅ Created {len(iocs)} IOCs")
        
        # Create alerts
        print("🚨 Creating alerts...")
        now = datetime.utcnow()
        alerts = [
            Alert(
                alert_type="network_anomaly",
                title="Suspicious Outbound Connection",
                message="Detected unusual data exfiltration attempt from internal host",
                priority=AlertPriority.CRITICAL,
                severity="critical",
                status=AlertStatus.OPEN,
                anomaly_score=0.92,
                risk_score=95,
                confidence=0.98,
                source_ip="192.168.1.50",
                destination_ip="203.0.113.45",
                protocol="HTTPS",
                threat_id=threats[0].id if threats else None,
                metadata={"port": 443, "bytes_transferred": 5000000}
            ),
            Alert(
                alert_type="authentication_anomaly",
                title="Multiple Failed Login Attempts",
                message="Brute force attack detected on user account",
                priority=AlertPriority.HIGH,
                severity="high",
                status=AlertStatus.ASSIGNED,
                anomaly_score=0.78,
                risk_score=80,
                confidence=0.92,
                source_ip="192.168.1.101",
                destination_ip="192.168.1.10",
                protocol="SSH",
                assigned_to=users[1].id,
                metadata={"failed_attempts": 15, "user": "admin"}
            ),
            Alert(
                alert_type="malware_detection",
                title="Known Malware Detected",
                message="Signature match for Emotet banking malware",
                priority=AlertPriority.CRITICAL,
                severity="critical",
                status=AlertStatus.ESCALATED,
                anomaly_score=0.99,
                risk_score=98,
                confidence=0.99,
                source_ip="192.168.1.102",
                destination_ip="10.0.0.5",
                protocol="TCP",
                threat_id=threats[2].id if threats else None,
                metadata={"signature": "Emotet.A", "hash": "5d41402abc4b2a76b9719d911017c592"}
            ),
        ]
        session.add_all(alerts)
        session.commit()
        print(f"✅ Created {len(alerts)} alerts")
        
        # Create incidents
        print("🔴 Creating incidents...")
        incidents = [
            Incident(
                title="Data Breach Investigation",
                description="Investigating potential exfiltration of customer PII",
                severity="critical",
                status=IncidentStatus.INVESTIGATING,
                threat_count=1,
                alert_count=3,
                evidence_count=5
            ),
            Incident(
                title="Malware Outbreak",
                description="Multiple systems infected with banking malware",
                severity="critical",
                status=IncidentStatus.CONTAINMENT,
                threat_count=1,
                alert_count=5,
                evidence_count=8
            ),
        ]
        session.add_all(incidents)
        session.commit()
        print(f"✅ Created {len(incidents)} incidents")
        
        # Link alerts to incidents
        if alerts and incidents:
            alerts[0].incident_id = incidents[0].id
            alerts[2].incident_id = incidents[1].id
            session.commit()
        
        # Create network flows
        print("📊 Creating network flows...")
        flows = [
            NetworkFlow(
                source_ip="192.168.1.50",
                destination_ip="203.0.113.45",
                source_port=54321,
                destination_port=443,
                protocol="TCP",
                bytes_sent=1000000,
                bytes_received=500000,
                packet_count=12500,
                duration_seconds=300,
                anomaly_score=0.85,
                risk_score=82,
                timestamp=now - timedelta(hours=2)
            ),
            NetworkFlow(
                source_ip="192.168.1.101",
                destination_ip="192.168.1.10",
                source_port=22,
                destination_port=2222,
                protocol="SSH",
                bytes_sent=50000,
                bytes_received=75000,
                packet_count=500,
                duration_seconds=120,
                anomaly_score=0.45,
                risk_score=35,
                timestamp=now - timedelta(hours=1)
            ),
        ]
        session.add_all(flows)
        session.commit()
        print(f"✅ Created {len(flows)} network flows")
        
        # Create audit logs
        print("📝 Creating audit logs...")
        audit_logs = [
            AuditLog(
                user_id=users[0].id,
                action="CREATE",
                entity_type="Alert",
                entity_id=alerts[0].id if alerts else 1,
                old_value=None,
                new_value={"title": "Suspicious Outbound Connection", "priority": "CRITICAL"},
                ip_address="192.168.1.1",
                user_agent="Mozilla/5.0...",
                timestamp=now - timedelta(hours=2)
            ),
            AuditLog(
                user_id=users[1].id,
                action="UPDATE",
                entity_type="Alert",
                entity_id=alerts[1].id if len(alerts) > 1 else 2,
                old_value={"status": "OPEN"},
                new_value={"status": "ASSIGNED", "assigned_to": users[1].id},
                ip_address="192.168.1.2",
                user_agent="Mozilla/5.0...",
                timestamp=now - timedelta(hours=1)
            ),
        ]
        session.add_all(audit_logs)
        session.commit()
        print(f"✅ Created {len(audit_logs)} audit logs")
        
        print("\n✨ Database seeding completed successfully!")
        print(f"\n📋 Sample credentials:")
        print(f"   Admin: admin@netsentinel.io / admin123")
        print(f"   Analyst: analyst@netsentinel.io / analyst123")
        print(f"   Hunter: hunter@netsentinel.io / hunter123")
        print(f"   Responder: responder@netsentinel.io / responder123")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()
