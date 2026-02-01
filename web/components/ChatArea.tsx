"use client";

import { useRef, useEffect, useState } from "react";
import { Message } from "../types";
import MessageBubble from "./MessageBubble";
import { Send, Loader2, Mic, MicOff, Volume2, VolumeX, Sparkles, Droplets } from "lucide-react";
import { useSpeechRecognition } from "../hooks/useSpeechRecognition";
import { useTextToSpeech } from "../hooks/useTextToSpeech";
import { useLanguage } from "../contexts/LanguageContext";
import { Separator } from "@/components/ui/separator";

interface ChatAreaProps {
    messages: Message[];
    isLoading: boolean;
    onSendMessage: (query: string) => void;
    userRole?: string;
    onDeleteMessage?: (id: string) => void;
}

export default function ChatArea({
    messages,
    isLoading,
    onSendMessage,
    userRole = "farmer",
    onDeleteMessage
}: ChatAreaProps) {
    const { t, language } = useLanguage();
    const [input, setInput] = useState("");
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLTextAreaElement>(null);
    const [autoSpeak, setAutoSpeak] = useState(userRole === "farmer");

    const localeCode = language === 'ta' ? 'ta-IN' : 'en-US';

    const { isListening, startListening, stopListening, isSupported: sttSupported } = useSpeechRecognition({
        onResult: (text) => setInput(text),
        lang: localeCode
    });

    const { speak, cancel: cancelSpeech, isSpeaking, isSupported: ttsSupported } = useTextToSpeech(localeCode);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    useEffect(() => {
        inputRef.current?.focus();
    }, []);

    const lastSpokenIdRef = useRef<string | null>(messages.length > 0 ? messages[messages.length - 1].id : null);

    useEffect(() => {
        if (!autoSpeak || messages.length === 0) return;

        const lastMsg = messages[messages.length - 1];

        // Only speak if it's a NEW agent message
        if (lastMsg.role === 'agent' && lastMsg.id !== lastSpokenIdRef.current) {
            lastSpokenIdRef.current = lastMsg.id;
            const cleanText = lastMsg.content.replace(/[*#]/g, '');
            speak(cleanText);
        }
    }, [messages, autoSpeak, speak]);

    useEffect(() => {
        setAutoSpeak(userRole === "farmer");
    }, [userRole]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        cancelSpeech();
        if (input.trim() && !isLoading) {
            onSendMessage(input);
            setInput("");
        }
    };

    const toggleListening = () => {
        if (isListening) {
            stopListening();
        } else {
            startListening();
        }
    };

    return (
        <main className="flex-1 flex flex-col h-full overflow-hidden bg-transparent relative"> {/* Transparent bg for glass parent */}

            {/* Glass Header */}
            <div className="h-16 flex items-center justify-between px-6 border-b border-[var(--border-subtle)] bg-[var(--bg-surface)]/40 backdrop-blur-md z-10">
                <div className="flex items-center gap-3">
                    <div className="flex flex-col">
                        <span className="text-sm font-bold text-[var(--text-primary)]">{t("app_title")}</span>
                        <span className="text-[10px] text-[var(--text-muted)] font-mono flex items-center gap-1">
                            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                            AI Online
                        </span>
                    </div>
                </div>

                {ttsSupported && (
                    <button
                        onClick={() => {
                            if (isSpeaking) cancelSpeech();
                            setAutoSpeak(!autoSpeak);
                        }}
                        className={`p-2 rounded-full transition-all duration-300 ${autoSpeak ? 'text-emerald-600 bg-emerald-50' : 'text-[var(--text-muted)] hover:bg-[var(--bg-surface)] hover:text-[var(--text-primary)]'}`}
                        title={autoSpeak ? t("mute_stop") : t("mute_start")}
                    >
                        {autoSpeak ? <Volume2 size={18} /> : <VolumeX size={18} />}
                    </button>
                )}
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 scroll-smooth">
                <div className="max-w-3xl mx-auto flex flex-col gap-8 py-8">
                    {messages.length === 0 ? (
                        <div className="flex flex-col items-center justify-center min-h-[50vh] text-center mt-4 animate-fade-in">
                            <div className="relative mb-8">
                                <div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-emerald-400 to-cyan-500 flex items-center justify-center text-white shadow-xl shadow-emerald-500/30">
                                    <Droplets size={40} fill="currentColor" className="opacity-90" />
                                </div>
                                <div className="absolute -top-2 -right-2 w-8 h-8 rounded-full bg-white flex items-center justify-center shadow-md animate-bounce">
                                    <Sparkles size={14} className="text-yellow-500" />
                                </div>
                            </div>

                            <h2 className="text-2xl font-bold text-[var(--text-primary)] mb-3 tracking-tight">
                                {t("welcome_title")}
                            </h2>
                            <p className="text-sm text-[var(--text-secondary)] mb-10 max-w-md leading-relaxed">
                                {t("welcome_subtitle")}
                            </p>

                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full max-w-xl">
                                {[t("example_chennai"), t("example_erode"), t("example_salem"), t("example_coimbatore")].map((text) => (
                                    <button
                                        key={text}
                                        onClick={() => onSendMessage(text)}
                                        className="text-sm p-4 rounded-xl border border-[var(--border-subtle)] bg-white/50 dark:bg-slate-800/50 hover:bg-white dark:hover:bg-slate-700 hover:border-emerald-200 hover:shadow-md text-[var(--text-secondary)] hover:text-emerald-700 dark:hover:text-emerald-400 transition-all duration-300 text-left group"
                                    >
                                        <div className="flex justify-between items-center">
                                            {text}
                                            <span className="opacity-0 group-hover:opacity-100 transition-opacity text-emerald-500">→</span>
                                        </div>
                                    </button>
                                ))}
                            </div>
                        </div>
                    ) : (
                        messages.map((msg) => (
                            <div key={msg.id} id={`message-${msg.id}`} className="transition-all duration-500 ease-out animate-in slide-in-from-bottom-4 fade-in">
                                <MessageBubble message={msg} onDelete={onDeleteMessage} />
                            </div>
                        ))
                    )}

                    {isLoading && (
                        <div className="flex items-center gap-3 animate-pulse pl-2">
                            <div className="w-8 h-8 rounded-full bg-gradient-to-r from-emerald-100 to-cyan-100 flex items-center justify-center shadow-sm">
                                <Loader2 size={14} className="animate-spin text-emerald-600" />
                            </div>
                            <span className="text-xs font-medium text-[var(--text-muted)] tracking-wide">{t("thinking")}</span>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Floating Input Area (Capsule Style) */}
            <div className="p-6 pt-2 z-20">
                <div className="max-w-3xl mx-auto">
                    <form
                        onSubmit={handleSubmit}
                        className={`
                            relative bg-[var(--bg-surface)]/80 backdrop-blur-xl border transition-all duration-300 rounded-[2rem] shadow-lg
                            ${isListening
                                ? 'border-red-400 ring-4 ring-red-500/10 shadow-red-500/10'
                                : 'border-[var(--border-subtle)] hover:border-emerald-400/50 hover:shadow-xl hover:shadow-emerald-500/5 focus-within:border-emerald-500 focus-within:ring-4 focus-within:ring-emerald-500/10'
                            }
                        `}
                    >
                        <textarea
                            ref={inputRef}
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter' && !e.shiftKey) {
                                    e.preventDefault();
                                    handleSubmit(e);
                                }
                            }}
                            placeholder={isListening ? t("listening") : t("input_placeholder")}
                            className="w-full bg-transparent border-none text-[var(--text-primary)] placeholder-[var(--text-muted)] px-6 py-4 pr-32 text-sm focus:outline-none resize-none min-h-[60px] max-h-[120px] rounded-[2rem]"
                            rows={1}
                            disabled={isLoading}
                        />

                        <div className="absolute right-2 bottom-2 top-2 flex items-center gap-2 pr-1">
                            {/* Mic Button */}
                            {sttSupported && (
                                <button
                                    type="button"
                                    onClick={toggleListening}
                                    className={`
                                        h-10 w-10 flex items-center justify-center rounded-full transition-all duration-300
                                        ${isListening
                                            ? 'text-white bg-gradient-to-r from-red-500 to-pink-500 animate-pulse shadow-md transform scale-105'
                                            : 'text-[var(--text-muted)] hover:bg-[var(--bg-app-gradient-start)] hover:text-emerald-600'
                                        }
                                    `}
                                    title="Voice Input"
                                >
                                    {isListening ? <MicOff size={18} /> : <Mic size={20} />}
                                </button>
                            )}

                            <Separator orientation="vertical" className="h-6 bg-[var(--border-subtle)]" />

                            {/* Send Button */}
                            <button
                                type="submit"
                                disabled={isLoading || !input.trim()}
                                className={`
                                    h-10 w-10 flex items-center justify-center rounded-full transition-all duration-300
                                    ${input.trim() && !isLoading
                                        ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-white shadow-md hover:shadow-lg hover:scale-105'
                                        : 'bg-[var(--bg-subtle)] text-[var(--text-muted)] opacity-50 cursor-not-allowed'
                                    }
                                `}
                            >
                                <Send size={18} className={input.trim() ? 'ml-0.5' : ''} />
                            </button>
                        </div>
                    </form>

                    <div className="text-center mt-3">
                        <p className="text-[10px] text-[var(--text-muted)] font-medium opacity-70">
                            {t("disclaimer")}
                        </p>
                    </div>
                </div>
            </div>
        </main>
    );
}
