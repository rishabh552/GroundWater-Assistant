import { useState, useEffect, useCallback, useRef } from 'react';

export function useTextToSpeech(lang: string = 'en-US') {
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [isSupported, setIsSupported] = useState(false);
    const synthRef = useRef<SpeechSynthesis | null>(null);

    useEffect(() => {
        if (typeof window !== 'undefined' && window.speechSynthesis) {
            // Delay state update to avoid "synchronous setState in effect" warning
            setTimeout(() => {
                setIsSupported(true);
            }, 0);
            synthRef.current = window.speechSynthesis;
        }
    }, []);

    const speak = useCallback((text: string) => {
        if (!synthRef.current) return;

        // Cancel any ongoing speech
        synthRef.current.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = lang;

        // Attempt to find a native voice for the language
        const voices = synthRef.current.getVoices();
        const voice = voices.find(v => v.lang.startsWith(lang));
        if (voice) {
            utterance.voice = voice;
        }

        utterance.onstart = () => setIsSpeaking(true);
        utterance.onend = () => setIsSpeaking(false);
        utterance.onerror = (e) => {
            // Ignore interruption errors caused by manual cancellation or new speech starting
            if (e.error === 'interrupted' || e.error === 'canceled') {
                setIsSpeaking(false);
                return;
            }

            // Safely log the error code if available
            if (e.error === 'not-allowed') {
                console.warn("TTS Error: 'not-allowed'. This is usually because the browser blocks auto-audio before user interaction.");
            } else {
                console.error("TTS Error:", e.error || "Unknown error", e);
            }
            setIsSpeaking(false);
        };

        synthRef.current.speak(utterance);
    }, [lang]);

    const cancel = useCallback(() => {
        if (synthRef.current) {
            synthRef.current.cancel();
            setIsSpeaking(false);
        }
    }, []);

    return {
        speak,
        cancel,
        isSpeaking,
        isSupported
    };
}
