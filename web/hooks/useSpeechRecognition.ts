import { useState, useEffect, useRef, useCallback } from 'react';

// === Type Definitions ===

interface SpeechRecognitionEvent extends Event {
    resultIndex: number;
    results: SpeechRecognitionResultList;
}

interface SpeechRecognitionResultList {
    length: number;
    [index: number]: SpeechRecognitionResult;
}

interface SpeechRecognitionResult {
    isFinal: boolean;
    [index: number]: SpeechRecognitionAlternative;
}

interface SpeechRecognitionAlternative {
    transcript: string;
}

interface SpeechRecognitionErrorEvent extends Event {
    error: string;
    message?: string;
}

interface SpeechRecognition extends EventTarget {
    continuous: boolean;
    interimResults: boolean;
    lang: string;
    start: () => void;
    stop: () => void;
    onresult: ((event: SpeechRecognitionEvent) => void) | null;
    onerror: ((event: SpeechRecognitionErrorEvent) => void) | null;
    onend: (() => void) | null;
}

// Constructor type
type SpeechRecognitionConstructor = new () => SpeechRecognition;

// Extend Window interface locally
interface IWindow extends Window {
    SpeechRecognition?: SpeechRecognitionConstructor;
    webkitSpeechRecognition?: SpeechRecognitionConstructor;
}

export interface UseSpeechRecognitionProps {
    onResult: (transcript: string) => void;
    lang?: string; // 'en-US', 'ta-IN', 'hi-IN'
}

export function useSpeechRecognition({ onResult, lang = 'en-US' }: UseSpeechRecognitionProps) {
    const [isListening, setIsListening] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [isSupported, setIsSupported] = useState(false);

    const recognitionRef = useRef<SpeechRecognition | null>(null);

    useEffect(() => {
        if (typeof window !== 'undefined') {
            const iWindow = window as unknown as IWindow;
            const SpeechRecognitionCtor = iWindow.SpeechRecognition || iWindow.webkitSpeechRecognition;

            if (SpeechRecognitionCtor) {
                // Delay state update to avoid warnings or hydration mismatches
                setTimeout(() => setIsSupported(true), 0);

                recognitionRef.current = new SpeechRecognitionCtor();
                if (recognitionRef.current) {
                    recognitionRef.current.continuous = false;
                    recognitionRef.current.interimResults = true;
                    recognitionRef.current.lang = lang;
                }
            } else {
                setError("Speech recognition is not supported in this browser.");
            }
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    // Update language dynamically
    useEffect(() => {
        if (recognitionRef.current) {
            recognitionRef.current.lang = lang;
        }
    }, [lang]);

    const startListening = useCallback(() => {
        if (!recognitionRef.current) return;

        setError(null);
        try {
            recognitionRef.current.start();
            setIsListening(true);
        } catch (err) {
            console.warn("Speech recognition already active", err);
        }
    }, []);

    const stopListening = useCallback(() => {
        if (!recognitionRef.current) return;
        recognitionRef.current.stop();
        setIsListening(false);
    }, []);

    useEffect(() => {
        const recognition = recognitionRef.current;
        if (!recognition) return;

        recognition.onresult = (event: SpeechRecognitionEvent) => {
            let finalTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                }
            }

            if (finalTranscript) {
                onResult(finalTranscript);
            }
        };

        recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
            console.error("Speech recognition error", event.error);
            if (event.error === 'not-allowed') {
                setError("Microphone access denied.");
            } else if (event.error === 'no-speech') {
                // Ignore no-speech errors
            } else {
                setError(`Error: ${event.error}`);
            }
            setIsListening(false);
        };

        recognition.onend = () => {
            setIsListening(false);
        };

        return () => {
            recognition.onresult = null;
            recognition.onerror = null;
            recognition.onend = null;
        };
    }, [onResult]);

    return {
        isListening,
        startListening,
        stopListening,
        error,
        isSupported
    };
}
