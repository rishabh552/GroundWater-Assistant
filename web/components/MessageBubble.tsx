"use client";

import { Message } from "../app/page";
import { FileDown, User } from "lucide-react";
import { useState } from "react";

interface MessageBubbleProps {
    message: Message;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
    const isUser = message.role === "user";
    const [downloading, setDownloading] = useState(false);

    const handleDownloadReport = async () => {
        setDownloading(true);
        try {
            // Extract location from message content or use a default
            let location = "Tamil Nadu District";

            // Try to extract district names from the message
            const districtPattern = /(Chennai|Salem|Coimbatore|Madurai|Tiruchirappalli|Kallakurichi|Erode|Pudukkottai|Vellore|Tirunelveli|Thanjavur|Kanyakumari|Nagapattinam|Cuddalore|Dindigul|Karur|Namakkal|Perambalur|Ramanathapuram|Sivaganga|Tenkasi|Theni|Tiruppur|Tiruvannamalai|Tuticorin|Viluppuram|Virudhunagar|Ariyalur|Chengalpattu|Dharmapuri|Kanchipuram|Krishnagiri|Mayiladuthurai|Nilgiris|Ranipet|Tirupattur)/gi;
            const match = message.content.match(districtPattern);
            if (match && match[0]) {
                location = match[0];
            }

            // Use original query if available, otherwise use a generic title
            const queryText = message.originalQuery || "Groundwater Risk Assessment";

            const response = await fetch("http://localhost:8000/api/report", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    query: queryText,
                    location: location,
                    risk_level: message.riskLevel || "Unknown",
                    full_response: message.content
                })
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Report generation failed: ${errorText}`);
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `GroundWater_Report_${location.replace(/\s+/g, '_')}_${Date.now()}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error("Download failed", error);
            alert(`Failed to download report: ${error instanceof Error ? error.message : 'Unknown error'}`);
        } finally {
            setDownloading(false);
        }
    };

    // Simple textual badges for risk
    const getRiskLabel = (risk: string) => {
        switch (risk) {
            case "Safe": return <span className="text-[var(--risk-safe)] font-semibold">Safe</span>;
            case "Moderate": return <span className="text-[var(--risk-moderate)] font-semibold">Moderate Risk</span>;
            case "Critical": return <span className="text-[var(--risk-critical)] font-semibold">Critical</span>;
            case "Over-Exploited": return <span className="text-[var(--risk-extreme)] font-semibold">Over-Exploited</span>;
            default: return null;
        }
    };

    // Premium User Message Design
    if (isUser) {
        return (
            <div className="flex justify-end gap-3 group">
                <div className="flex flex-col items-end gap-1.5 max-w-[75%]">
                    {/* User message bubble with premium gradient border */}
                    <div className="relative">
                        {/* Subtle glow effect on hover */}
                        <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/20 to-blue-500/20 rounded-2xl rounded-tr-sm blur-xl opacity-0 group-hover:opacity-50 transition-opacity duration-300" />

                        {/* Main bubble */}
                        <div className="relative bg-gradient-to-br from-[#1a1a2e] to-[#16162a] border border-[#2a2a4a]/60 text-[var(--text-primary)] px-4 py-3 rounded-2xl rounded-tr-sm shadow-lg backdrop-blur-sm">
                            <p className="text-sm leading-relaxed">{message.content}</p>
                        </div>
                    </div>

                    {/* Timestamp */}
                    <span className="text-[10px] text-[var(--text-muted)] opacity-0 group-hover:opacity-100 transition-opacity duration-200 pr-1">
                        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                </div>

                {/* User avatar */}
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-emerald-500/30 to-blue-500/30 border border-emerald-500/20 flex items-center justify-center flex-shrink-0 shadow-md">
                    <User size={14} className="text-emerald-400" />
                </div>
            </div>
        );
    }

    // Agent Message (unchanged logic, updated brand icon)
    return (
        <div className="flex gap-4 max-w-[90%] fade-in-up">
            <div className="w-8 h-8 rounded-lg flex-shrink-0 bg-gradient-to-br from-[var(--bg-element)] to-[#1a2a1a] flex items-center justify-center border border-emerald-500/20 text-emerald-400 shadow-md">
                {/* Brand Icon */}
                <span className="font-bold text-xs">💧</span>
            </div>

            <div className="flex-1 space-y-2">
                <div className="text-sm text-[var(--text-secondary)] leading-relaxed whitespace-pre-wrap">
                    {message.content}
                </div>

                {message.riskLevel && (
                    <div className="flex flex-wrap items-center gap-3 pt-2">
                        <div className="text-xs bg-[var(--bg-element)] px-2 py-1 rounded border border-[var(--border-color)]">
                            Status: {getRiskLabel(message.riskLevel)}
                        </div>
                        <button
                            onClick={handleDownloadReport}
                            disabled={downloading}
                            className="flex items-center gap-2 px-3 py-1 bg-transparent hover:bg-[var(--bg-element)] rounded text-xs text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors"
                        >
                            <FileDown size={14} />
                            {downloading ? "Generating..." : "PDF Report"}
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}
