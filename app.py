# app.py - Flask Backend
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import io
import base64
from datetime import datetime
import json
import time

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size

# Simulated AI Model
class FRAAnalyzer:
    def __init__(self):
        self.fault_types = {
            'axial_displacement': {'name': 'Axial Winding Displacement', 'severity': 'Critical'},
            'radial_deformation': {'name': 'Radial Winding Deformation', 'severity': 'High'},
            'core_grounding': {'name': 'Core Grounding Fault', 'severity': 'Critical'},
            'bushing_fault': {'name': 'Bushing Connection Issue', 'severity': 'Medium'},
            'normal': {'name': 'Normal Operation', 'severity': 'Low'}
        }
    
    def parse_csv(self, file_content):
        """Parse CSV file - supports multiple formats"""
        try:
            # Try reading as CSV
            df = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
            
            # Detect format
            if 'Frequency' in df.columns or 'frequency' in df.columns:
                freq_col = 'Frequency' if 'Frequency' in df.columns else 'frequency'
                amp_col = next((c for c in df.columns if 'Amplitude' in c or 'amplitude' in c), df.columns[1])
                format_detected = "Omicron CSV Format"
            else:
                # Assume first two columns
                freq_col = df.columns[0]
                amp_col = df.columns[1]
                format_detected = "Generic CSV Format"
            
            frequency = df[freq_col].values
            amplitude = df[amp_col].values
            
            return {
                'success': True,
                'frequency': frequency.tolist(),
                'amplitude': amplitude.tolist(),
                'format': format_detected,
                'points': len(frequency)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_sample_data(self):
        """Generate synthetic FRA data with fault"""
        freq = np.logspace(1, 6, 500)  # 10 Hz to 1 MHz
        
        # Base response
        amplitude = -20 - 15 * np.log10(freq / 1000) + np.random.normal(0, 1.5, 500)
        
        # Add resonance peaks
        amplitude += 10 * np.exp(-((np.log10(freq) - 4.5) ** 2) / 0.1)
        amplitude += 8 * np.exp(-((np.log10(freq) - 3.8) ** 2) / 0.15)
        
        # Add fault signature (shift in resonance)
        amplitude += 5 * np.exp(-((np.log10(freq) - 4.7) ** 2) / 0.08)
        
        return freq.tolist(), amplitude.tolist()
    
    def analyze(self, frequency, amplitude):
        """Mock AI analysis - simulates CNN model prediction"""
        # Simulate processing time
        time.sleep(0.5)
        
        # Simple heuristic to detect "faults"
        freq_array = np.array(frequency)
        amp_array = np.array(amplitude)
        
        # Find resonance peaks
        peaks = self._find_peaks(amp_array)
        
        # Analyze fault based on peak characteristics
        if len(peaks) > 0:
            peak_freq = freq_array[peaks[0]]
            
            if 10000 <= peak_freq <= 100000:
                fault_type = 'axial_displacement'
                confidence = 87
                fault_freq_range = [10000, 100000]
            elif 1000 <= peak_freq <= 10000:
                fault_type = 'core_grounding'
                confidence = 76
                fault_freq_range = [1000, 10000]
            else:
                fault_type = 'radial_deformation'
                confidence = 82
                fault_freq_range = [100000, 500000]
        else:
            fault_type = 'normal'
            confidence = 95
            fault_freq_range = None
        
        fault_info = self.fault_types[fault_type]
        
        return {
            'fault_type': fault_info['name'],
            'fault_code': fault_type,
            'confidence': confidence,
            'severity': fault_info['severity'],
            'fault_frequency_range': fault_freq_range,
            'recommendations': self._get_recommendations(fault_type),
            'explanation': self._get_explanation(fault_type, confidence)
        }
    
    def _find_peaks(self, amplitude):
        """Simple peak detection"""
        peaks = []
        for i in range(1, len(amplitude) - 1):
            if amplitude[i] > amplitude[i-1] and amplitude[i] > amplitude[i+1]:
                peaks.append(i)
        return peaks[:3]  # Return top 3 peaks
    
    def _get_recommendations(self, fault_type):
        recommendations = {
            'axial_displacement': [
                'Schedule visual inspection of winding clamps within 7 days',
                'Perform winding resistance test to confirm diagnosis',
                'Monitor transformer load - reduce to 80% if possible',
                'Retest FRA in 30 days to track progression'
            ],
            'core_grounding': [
                'Check core grounding connections immediately',
                'Inspect for moisture ingress in tank',
                'Measure insulation resistance (IR test)',
                'Consider dissolved gas analysis (DGA)'
            ],
            'radial_deformation': [
                'Investigate recent through-fault events or short circuits',
                'Perform turns ratio test (TTR)',
                'Check for signs of overheating',
                'Schedule detailed internal inspection'
            ],
            'normal': [
                'Transformer operating within normal parameters',
                'Continue routine maintenance schedule',
                'Store this signature as baseline for future comparison'
            ]
        }
        return recommendations.get(fault_type, [])
    
    def _get_explanation(self, fault_type, confidence):
        explanations = {
            'axial_displacement': f'AI detected resonance peak shift in 10-100 kHz range (confidence: {confidence}%). This pattern strongly correlates with axial winding displacement, typically caused by electromagnetic forces during short circuits or mechanical stress.',
            'core_grounding': f'Abnormal damping in low frequency range (1-10 kHz) indicates possible core grounding issues (confidence: {confidence}%). This may result from insulation degradation or improper grounding connections.',
            'radial_deformation': f'High frequency resonance anomalies (100-500 kHz) suggest radial winding deformation (confidence: {confidence}%). Often caused by through-fault currents exceeding design limits.',
            'normal': f'Frequency response signature matches normal operation patterns with {confidence}% confidence. No significant deviations detected from expected transformer behavior.'
        }
        return explanations.get(fault_type, '')

analyzer = FRAAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and parsing"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    try:
        file_content = file.read()
        result = analyzer.parse_csv(file_content)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze FRA data"""
    data = request.json
    frequency = data.get('frequency', [])
    amplitude = data.get('amplitude', [])
    
    if not frequency or not amplitude:
        return jsonify({'success': False, 'error': 'Invalid data'}), 400
    
    try:
        result = analyzer.analyze(frequency, amplitude)
        return jsonify({'success': True, 'analysis': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sample', methods=['GET'])
def get_sample():
    """Get sample FRA data for demo"""
    freq, amp = analyzer.generate_sample_data()
    return jsonify({
        'success': True,
        'frequency': freq,
        'amplitude': amp,
        'format': 'Sample Data (Synthetic)',
        'points': len(freq)
    })

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    app.run(debug=True, host='0.0.0.0', port=port)