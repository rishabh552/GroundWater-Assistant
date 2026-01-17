"use client";

import { useRef, useEffect, useState } from "react";
import { Message } from "../app/page";
import MessageBubble from "./MessageBubble";
import { Send, Loader2 } from "lucide-react";

interface ChatAreaProps {
    messages: Message[];
    isLoading: boolean;
    onSendMessage: (query: string) => void;
}

export default function ChatArea({
    messages,
    isLoading,
    onSendMessage
}: ChatAreaProps) {
    const [input, setInput] = useState("");
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLTextAreaElement>(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    useEffect(() => {
        inputRef.current?.focus();
    }, []);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (input.trim() && !isLoading) {
            onSendMessage(input);
            setInput("");
        }
    };

    return (
        <main className="flex-1 flex flex-col h-full overflow-hidden bg-[var(--bg-app)] relative">

            {/* Header / Top Bar (Minimal) */}
            <div className="h-14 flex items-center justify-between px-6 border-b border-[var(--border-color)] bg-[var(--bg-app)] z-10 sticky top-0">
                <span className="text-sm font-medium text-[var(--text-secondary)]">Groundwater Assistant</span>
                <span className="text-xs text-[var(--text-muted)]">v1.2</span>
            </div>

            {/* Messages Area - Centered Column */}
            <div className="flex-1 overflow-y-auto p-4">
                <div className="max-w-3xl mx-auto flex flex-col gap-6 py-6">
                    {messages.length === 0 ? (
                        <div className="flex flex-col items-center justify-center min-h-[40vh] text-center mt-10">
                            <div className="w-16 h-16 rounded-2xl bg-[var(--bg-element)] flex items-center justify-center mb-6 text-3xl">
                                💧
                            </div>
                            <h2 className="text-xl font-semibold text-[var(--text-primary)] mb-2">
                                How can I help with groundwater data?
                            </h2>
                            <p className="text-sm text-[var(--text-secondary)] mb-8">
                                I can provide risk assessments, borewell advice, and district reports.
                            </p>

                            <div className="grid grid-cols-2 gap-3 w-full max-w-lg">
                                {["Chennai Risk Status", "Borewell rules in Erode", "Download Salem Report", "Coimbatore Water Level"].map((text) => (
                                    <button
                                        key={text}
                                        onClick={() => onSendMessage(text)}
                                        className="text-sm p-3 rounded-lg border border-[var(--border-color)] bg-[var(--bg-element)] hover:bg-[var(--bg-hover)] text-[var(--text-secondary)] transition-colors text-left"
                                    >
                                        {text}
                                    </button>
                                ))}
                            </div>
                        </div>
                    ) : (
                        messages.map((msg) => <MessageBubble key={msg.id} message={msg} />)
                    )}

                    {isLoading && (
                        <div className="flex items-center gap-3">
                            <div className="w-6 h-6 rounded-full bg-[var(--bg-element)] flex items-center justify-center">
                                <Loader2 size={12} className="animate-spin text-[var(--text-muted)]" />
                            </div>
                            <span className="text-sm text-[var(--text-secondary)] animate-pulse">Thinking...</span>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Input Area - Centered & Clean */}
            <div className="p-4 pb-6 bg-[var(--bg-app)] z-20">
                <div className="max-w-3xl mx-auto">
                    <form onSubmit={handleSubmit} className="relative bg-[var(--bg-element)] border border-[var(--border-color)] rounded-xl shadow-sm focus-within:ring-1 focus-within:ring-[var(--border-color)] transition-all">
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
                            placeholder="Ask a question..."
                            className="w-full bg-transparent border-none text-[var(--text-primary)] placeholder-[var(--text-muted)] px-4 py-3.5 pr-12 text-sm focus:outline-none resize-none min-h-[52px] max-h-[200px]"
                            rows={1}
                            style={{ height: '52px' }} // Simple fixed height for now, could be auto-growing
                            disabled={isLoading}
                        />
                        <button
                            type="submit"
                            disabled={isLoading || !input.trim()}
                            className="absolute right-2 bottom-2 p-1.5 rounded-lg bg-[var(--text-primary)] text-[var(--bg-app)] disabled:opacity-30 disabled:bg-transparent disabled:text-[var(--text-muted)] hover:opacity-90 transition-all"
                        >
                            <Send size={16} />
                        </button>
                    </form>
                    <div className="text-center mt-2">
                        <p className="text-[10px] text-[var(--text-muted)]">
                            AI can make mistakes. Please verify important information.
                        </p>
                    </div>
                </div>
            </div>
        </main>
    );
}
