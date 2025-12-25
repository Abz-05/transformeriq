import pandas as pd
import numpy as np

def generate_fra_data(fault_type='normal'):
    freq = np.logspace(1, 6, 500)
    amp = -20 - 15 * np.log10(freq / 1000) + np.random.normal(0, 1.5, 500)
    
    if fault_type == 'axial_displacement':
        # Add fault signature: significant variance in high freq
        amp += 15 * np.exp(-((np.log10(freq) - 4.7) ** 2) / 0.08)
    elif fault_type == 'core_grounding':
        # Add fault signature: low freq shift
        amp[:100] += np.random.normal(15, 2, 100)
    
    df = pd.DataFrame({
        'Frequency': freq,
        'Amplitude': amp,
        'Phase': np.random.uniform(-30, 45, len(freq))
    })
    
    filename = f'sample_{fault_type}.csv'
    df.to_csv(filename, index=False)
    print(f"✅ Generated: {filename}")

if __name__ == "__main__":
    # Generate multiple samples
    for fault in ['normal', 'axial_displacement', 'core_grounding']:
        generate_fra_data(fault)
