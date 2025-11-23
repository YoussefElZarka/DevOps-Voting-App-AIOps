from flask import Flask, request, jsonify, render_template_string
import os
import time
import logging
from datetime import datetime
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class PredictiveAgent:
    """AI Agent for predictive analytics and anomaly detection"""
    
    def __init__(self):
        self.prometheus_url = os.getenv('PROMETHEUS_URL', 'http://prometheus:9090')
        logger.info(f"AI Agent initialized with Prometheus: {self.prometheus_url}")
        self.alerts = []
        self.last_analysis_time = None
        
    def analyze_metrics(self, source="automated"):
        """Run predictive analysis"""
        logger.info(f"Running analysis from source: {source}")
        
        # Simulate metric analysis
        anomalies = []
        
        # Simulate different scenarios
        scenarios = [
            {
                "type": "CPU_SPIKE",
                "severity": "WARNING",
                "message": "CPU usage trending up. Current: 75%, Predicted: 90% in 15 minutes",
                "metric_value": 75,
                "predicted_value": 90,
                "time_to_critical": 15
            },
            {
                "type": "MEMORY_LEAK",
                "severity": "MEDIUM",
                "message": "Potential memory leak detected in worker service",
                "metric_value": 512,
                "rate": "2MB/min",
                "affected_service": "worker"
            },
            {
                "type": "ERROR_RATE_INCREASE",
                "severity": "HIGH",
                "message": "Error rate increased by 45% in last 5 minutes",
                "baseline": 2.3,
                "current": 8.7,
                "increase_percentage": 45
            },
            {
                "type": "QUEUE_OVERFLOW",
                "severity": "WARNING",
                "message": "Redis queue depth approaching threshold",
                "current_depth": 850,
                "threshold": 1000,
                "percentage": 85
            }
        ]
        
        # Randomly select 1-3 anomalies
        num_anomalies = random.randint(1, 3)
        anomalies = random.sample(scenarios, num_anomalies)
        
        # Add timestamp
        for anomaly in anomalies:
            anomaly['detected_at'] = datetime.now().isoformat()
            anomaly['source'] = source
        
        self.alerts = anomalies
        self.last_analysis_time = datetime.now()
        
        return anomalies
    
    def get_status(self):
        """Get agent status"""
        return {
            "status": "running",
            "prometheus_url": self.prometheus_url,
            "alerts_count": len(self.alerts),
            "last_analysis": self.last_analysis_time.isoformat() if self.last_analysis_time else None,
            "uptime": "running"
        }

# Initialize agent
agent = PredictiveAgent()

# HTML Dashboard Template
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AI Monitoring Agent Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
        .header h1 {
            color: #333;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .status-badge {
            display: inline-block;
            padding: 8px 16px;
            background: #4CAF50;
            color: white;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .stat-card h3 {
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .stat-value {
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
        }
        .alerts-container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
        .alerts-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .alert-card {
            border-left: 4px solid #FFA500;
            background: #FFF9E6;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            transition: all 0.3s;
        }
        .alert-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateX(5px);
        }
        .alert-card.warning { border-left-color: #FFA500; background: #FFF9E6; }
        .alert-card.high { border-left-color: #FF5722; background: #FFE9E6; }
        .alert-card.medium { border-left-color: #FF9800; background: #FFF3E0; }
        .alert-card.critical { border-left-color: #F44336; background: #FFEBEE; }
        .alert-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .alert-type {
            font-weight: bold;
            font-size: 18px;
            color: #333;
        }
        .severity-badge {
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            color: white;
        }
        .severity-warning { background: #FFA500; }
        .severity-high { background: #FF5722; }
        .severity-medium { background: #FF9800; }
        .severity-critical { background: #F44336; }
        .alert-message {
            color: #666;
            margin-bottom: 10px;
            line-height: 1.6;
        }
        .alert-details {
            font-size: 12px;
            color: #999;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        .btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #667eea;
        }
        .no-alerts {
            text-align: center;
            padding: 40px;
            color: #999;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(102,126,234,0.3);
            border-top-color: #667eea;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>
                🤖 AI Monitoring Agent
                <span class="status-badge">{{ status }}</span>
            </h1>
            <p style="color: #666; margin-top: 10px;">
                Real-time predictive analytics and anomaly detection
            </p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <h3>Active Alerts</h3>
                <div class="stat-value">{{ alerts_count }}</div>
            </div>
            <div class="stat-card">
                <h3>Last Analysis</h3>
                <div class="stat-value" style="font-size: 18px;">{{ last_analysis }}</div>
            </div>
            <div class="stat-card">
                <h3>Prometheus URL</h3>
                <div style="font-size: 14px; color: #666; margin-top: 10px;">{{ prometheus_url }}</div>
            </div>
        </div>

        <div class="alerts-container">
            <div class="alerts-header">
                <h2>🚨 Detected Anomalies</h2>
                <button class="btn" onclick="runAnalysis()">🔄 Run Analysis</button>
            </div>
            
            <div class="loading" id="loading">
                <span class="spinner"></span>
                <p style="margin-top: 10px;">Analyzing metrics...</p>
            </div>
            
            <div id="alerts-list">
                {% if alerts %}
                    {% for alert in alerts %}
                    <div class="alert-card {{ alert.severity|lower }}">
                        <div class="alert-header">
                            <span class="alert-type">{{ alert.type }}</span>
                            <span class="severity-badge severity-{{ alert.severity|lower }}">{{ alert.severity }}</span>
                        </div>
                        <div class="alert-message">{{ alert.message }}</div>
                        <div class="alert-details">
                            <span>⏰ {{ alert.detected_at }}</span>
                            <span>📍 Source: {{ alert.source }}</span>
                        </div>
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="no-alerts">
                        <h3>✅ No anomalies detected</h3>
                        <p style="margin-top: 10px; color: #999;">Click "Run Analysis" to scan for issues</p>
                    </div>
                {% endif %}
            </div>
        </div>
    </div>

    <script>
        async function runAnalysis() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('alerts-list').style.opacity = '0.5';
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ source: 'manual_dashboard' })
                });
                
                const data = await response.json();
                
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } catch (error) {
                alert('Error running analysis: ' + error.message);
                document.getElementById('loading').style.display = 'none';
                document.getElementById('alerts-list').style.opacity = '1';
            }
        }

        // Auto-refresh every 30 seconds
        setInterval(() => {
            fetch('/status')
                .then(r => r.json())
                .then(data => {
                    if (data.alerts_count !== {{ alerts_count }}) {
                        window.location.reload();
                    }
                });
        }, 30000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Dashboard home page"""
    status = agent.get_status()
    return render_template_string(
        DASHBOARD_HTML,
        status=status['status'],
        alerts_count=status['alerts_count'],
        last_analysis=status['last_analysis'] or 'Never',
        prometheus_url=status['prometheus_url'],
        alerts=agent.alerts
    )

@app.route('/status')
def status():
    """Get agent status"""
    return jsonify(agent.get_status())

@app.route('/analyze', methods=['POST'])
def analyze():
    """Run analysis endpoint"""
    data = request.get_json() or {}
    source = data.get('source', 'api')
    
    anomalies = agent.analyze_metrics(source=source)
    
    return jsonify({
        "status": "success",
        "anomalies_detected": len(anomalies),
        "anomalies": anomalies,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/alerts')
def get_alerts():
    """Get current alerts"""
    return jsonify({
        "alerts": agent.alerts,
        "count": len(agent.alerts)
    })

if __name__ == '__main__':
    logger.info("🤖 AI Monitoring Agent starting...")
    app.run(host='0.0.0.0', port=5001, debug=True)
