"use client";

import { Message } from "../app/page";
import { FileDown } from "lucide-react";
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
            a.download = `Jal_Rakshak_Report_${location.replace(/\s+/g, '_')}_${Date.now()}.pdf`;
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

    if (isUser) {
        return (
            <div className="flex justify-end">
                <div className="bg-[var(--bg-element)] text-[var(--text-primary)] px-4 py-2.5 rounded-2xl rounded-tr-sm max-w-[80%] text-sm leading-6">
                    {message.content}
                </div>
            </div>
        );
    }

    return (
        <div className="flex gap-4 max-w-[90%] fade-in-up">
            <div className="w-8 h-8 rounded-lg flex-shrink-0 bg-[var(--bg-element)] flex items-center justify-center border border-[var(--border-color)] text-[var(--text-primary)]">
                {/* Brand Icon instead of generic Bot */}
                <div className="font-bold text-xs">JR</div>
            </div>

            <div className="flex-1 space-y-2">
                {/* Removed repetitive "Jal-Rakshak AI" header - cleaner look */}
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
