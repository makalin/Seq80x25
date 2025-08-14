#!/usr/bin/env python3
"""
Audio Effects Processor for Seq80x25
Provides various audio effects and filters for enhanced sound
"""

import numpy as np
from typing import Tuple, Optional, Callable
from enum import Enum


class EffectType(Enum):
    """Available audio effects"""
    REVERB = "reverb"
    DELAY = "delay"
    CHORUS = "chorus"
    FLANGER = "flanger"
    DISTORTION = "distortion"
    FILTER = "filter"
    COMPRESSOR = "compressor"
    TREMOLO = "tremolo"


class AudioEffects:
    """Audio effects processor"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.delay_buffer = np.zeros(sample_rate * 2)  # 2 second delay buffer
        self.delay_index = 0
        
    def apply_reverb(self, audio: np.ndarray, room_size: float = 0.5, 
                     damping: float = 0.5) -> np.ndarray:
        """Apply reverb effect"""
        if room_size <= 0:
            return audio
        
        # Simple convolution-based reverb
        reverb_length = int(room_size * self.sample_rate * 0.1)
        decay = np.exp(-damping * np.linspace(0, 1, reverb_length))
        
        # Create reverb impulse response
        impulse = np.random.randn(reverb_length) * decay
        impulse = impulse / np.sum(np.abs(impulse)) * 0.3
        
        # Apply convolution
        reverb_audio = np.convolve(audio, impulse, mode='same')
        
        # Mix dry and wet signals
        wet_mix = room_size
        dry_mix = 1.0 - wet_mix
        
        return dry_mix * audio + wet_mix * reverb_audio
    
    def apply_delay(self, audio: np.ndarray, delay_time: float = 0.3, 
                    feedback: float = 0.3, mix: float = 0.5) -> np.ndarray:
        """Apply delay effect"""
        if delay_time <= 0 or feedback <= 0:
            return audio
        
        delay_samples = int(delay_time * self.sample_rate)
        output = np.copy(audio)
        
        # Simple delay line implementation
        for i in range(len(audio)):
            if i >= delay_samples:
                delayed_sample = self.delay_buffer[self.delay_index] * feedback
                output[i] += delayed_sample
            
            # Store current sample in delay buffer
            self.delay_buffer[self.delay_index] = audio[i]
            self.delay_index = (self.delay_index + 1) % len(self.delay_buffer)
        
        # Mix dry and delayed signals
        return (1 - mix) * audio + mix * output
    
    def apply_chorus(self, audio: np.ndarray, rate: float = 1.5, 
                     depth: float = 0.002, mix: float = 0.5) -> np.ndarray:
        """Apply chorus effect"""
        if rate <= 0 or depth <= 0:
            return audio
        
        # Generate LFO for chorus
        t = np.linspace(0, len(audio) / self.sample_rate, len(audio))
        lfo = np.sin(2 * np.pi * rate * t) * depth * self.sample_rate
        
        # Create delayed version with varying delay
        chorus_audio = np.zeros_like(audio)
        for i in range(len(audio)):
            delay_samples = int(lfo[i])
            if i >= delay_samples:
                chorus_audio[i] = audio[i - delay_samples]
        
        # Mix dry and chorus signals
        return (1 - mix) * audio + mix * chorus_audio
    
    def apply_flanger(self, audio: np.ndarray, rate: float = 0.5, 
                      depth: float = 0.005, feedback: float = 0.3) -> np.ndarray:
        """Apply flanger effect"""
        if rate <= 0 or depth <= 0:
            return audio
        
        # Generate LFO for flanger
        t = np.linspace(0, len(audio) / self.sample_rate, len(audio))
        lfo = np.sin(2 * np.pi * rate * t) * depth * self.sample_rate
        
        # Apply flanging
        output = np.copy(audio)
        for i in range(len(audio)):
            delay_samples = int(lfo[i])
            if i >= delay_samples:
                output[i] += feedback * output[i - delay_samples]
        
        # Normalize to prevent clipping
        if np.max(np.abs(output)) > 0:
            output = output / np.max(np.abs(output)) * 0.8
        
        return output
    
    def apply_distortion(self, audio: np.ndarray, amount: float = 0.5, 
                         type_: str = "soft") -> np.ndarray:
        """Apply distortion effect"""
        if amount <= 0:
            return audio
        
        if type_ == "soft":
            # Soft clipping distortion
            output = np.tanh(audio * (1 + amount * 5))
        elif type_ == "hard":
            # Hard clipping distortion
            threshold = 1 - amount
            output = np.clip(audio, -threshold, threshold)
        else:
            # Overdrive distortion
            output = audio * (1 + amount * 2)
            output = np.clip(output, -0.8, 0.8)
        
        return output
    
    def apply_filter(self, audio: np.ndarray, filter_type: str = "lowpass", 
                     cutoff: float = 1000, resonance: float = 1.0) -> np.ndarray:
        """Apply filter effect"""
        if cutoff <= 0:
            return audio
        
        # Convert cutoff to normalized frequency
        normalized_cutoff = 2 * cutoff / self.sample_rate
        
        if filter_type == "lowpass":
            # Simple low-pass filter
            b = normalized_cutoff
            a = 1 - b
            output = np.zeros_like(audio)
            output[0] = b * audio[0]
            for i in range(1, len(audio)):
                output[i] = b * audio[i] + a * output[i-1]
        
        elif filter_type == "highpass":
            # Simple high-pass filter
            b = normalized_cutoff
            a = 1 - b
            output = np.zeros_like(audio)
            output[0] = audio[0]
            for i in range(1, len(audio)):
                output[i] = a * (output[i-1] + audio[i] - audio[i-1])
        
        elif filter_type == "bandpass":
            # Simple band-pass filter
            q = resonance
            w0 = normalized_cutoff
            alpha = np.sin(w0) / (2 * q)
            
            b0 = alpha
            b1 = 0
            b2 = -alpha
            a0 = 1 + alpha
            a1 = -2 * np.cos(w0)
            a2 = 1 - alpha
            
            output = np.zeros_like(audio)
            for i in range(2, len(audio)):
                output[i] = (b0 * audio[i] + b1 * audio[i-1] + b2 * audio[i-2] 
                            - a1 * output[i-1] - a2 * output[i-2]) / a0
        
        else:
            return audio
        
        return output
    
    def apply_compressor(self, audio: np.ndarray, threshold: float = 0.5, 
                         ratio: float = 4.0, attack: float = 0.01, 
                         release: float = 0.1) -> np.ndarray:
        """Apply compression effect"""
        if threshold <= 0 or ratio <= 1:
            return audio
        
        # Convert times to samples
        attack_samples = int(attack * self.sample_rate)
        release_samples = int(release * self.sample_rate)
        
        output = np.zeros_like(audio)
        envelope = 0
        
        for i in range(len(audio)):
            # Calculate envelope
            if abs(audio[i]) > envelope:
                envelope += (abs(audio[i]) - envelope) / attack_samples
            else:
                envelope += (abs(audio[i]) - envelope) / release_samples
            
            # Apply compression
            if envelope > threshold:
                gain = threshold + (envelope - threshold) / ratio
                output[i] = audio[i] * (gain / envelope)
            else:
                output[i] = audio[i]
        
        return output
    
    def apply_tremolo(self, audio: np.ndarray, rate: float = 5.0, 
                      depth: float = 0.5) -> np.ndarray:
        """Apply tremolo effect"""
        if rate <= 0 or depth <= 0:
            return audio
        
        # Generate LFO for tremolo
        t = np.linspace(0, len(audio) / self.sample_rate, len(audio))
        lfo = 1 - depth * (1 + np.sin(2 * np.pi * rate * t)) / 2
        
        # Apply tremolo
        return audio * lfo
    
    def apply_multiple_effects(self, audio: np.ndarray, 
                              effects: list) -> np.ndarray:
        """Apply multiple effects in sequence"""
        output = np.copy(audio)
        
        for effect_config in effects:
            effect_type = effect_config.get('type')
            params = effect_config.get('params', {})
            
            if effect_type == EffectType.REVERB:
                output = self.apply_reverb(output, **params)
            elif effect_type == EffectType.DELAY:
                output = self.apply_delay(output, **params)
            elif effect_type == EffectType.CHORUS:
                output = self.apply_chorus(output, **params)
            elif effect_type == EffectType.FLANGER:
                output = self.apply_flanger(output, **params)
            elif effect_type == EffectType.DISTORTION:
                output = self.apply_distortion(output, **params)
            elif effect_type == EffectType.FILTER:
                output = self.apply_filter(output, **params)
            elif effect_type == EffectType.COMPRESSOR:
                output = self.apply_compressor(output, **params)
            elif effect_type == EffectType.TREMOLO:
                output = self.apply_tremolo(output, **params)
        
        return output
    
    def create_effect_preset(self, name: str, effects: list) -> dict:
        """Create a named effect preset"""
        return {
            "name": name,
            "effects": effects
        }


def main():
    """Test the audio effects"""
    effects = AudioEffects()
    
    print("Seq80x25 Audio Effects Test")
    print("=" * 30)
    
    # Generate test audio (sine wave)
    duration = 1.0  # 1 second
    frequency = 440  # A4
    t = np.linspace(0, duration, int(duration * effects.sample_rate))
    test_audio = np.sin(2 * np.pi * frequency * t) * 0.5
    
    print(f"Generated {duration}s test tone at {frequency}Hz")
    
    # Test individual effects
    print("\nTesting individual effects:")
    
    # Reverb
    reverb_audio = effects.apply_reverb(test_audio, room_size=0.3, damping=0.7)
    print("✓ Reverb applied")
    
    # Delay
    delay_audio = effects.apply_delay(test_audio, delay_time=0.2, feedback=0.4)
    print("✓ Delay applied")
    
    # Chorus
    chorus_audio = effects.apply_chorus(test_audio, rate=1.2, depth=0.001)
    print("✓ Chorus applied")
    
    # Distortion
    distortion_audio = effects.apply_distortion(test_audio, amount=0.3, type_="soft")
    print("✓ Distortion applied")
    
    # Filter
    filter_audio = effects.apply_filter(test_audio, filter_type="lowpass", cutoff=800)
    print("✓ Filter applied")
    
    # Test multiple effects
    print("\nTesting multiple effects:")
    effect_chain = [
        {"type": EffectType.REVERB, "params": {"room_size": 0.2, "damping": 0.8}},
        {"type": EffectType.DELAY, "params": {"delay_time": 0.15, "feedback": 0.3}},
        {"type": EffectType.FILTER, "params": {"filter_type": "lowpass", "cutoff": 1000}}
    ]
    
    processed_audio = effects.apply_multiple_effects(test_audio, effect_chain)
    print("✓ Multiple effects applied")
    
    # Create preset
    preset = effects.create_effect_preset("Chiptune", effect_chain)
    print(f"✓ Created preset: {preset['name']}")
    
    print("\nAll effects tests completed!")


if __name__ == "__main__":
    main()
