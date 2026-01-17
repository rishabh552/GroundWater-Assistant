"use client";

import { Message } from "../app/page";
import { Droplets, Plus, Clock, ChevronRight, ChevronUp, ChevronDown, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";

interface SidebarProps {
    messages: Message[];
    onNavigateToMessage?: (messageId: string) => void;
    onNewChat?: () => void;
    onClearHistory?: () => void;
}

export default function Sidebar({ messages, onNavigateToMessage, onNewChat, onClearHistory }: SidebarProps) {
    const userQueries = messages.filter((m) => m.role === "user");

    // Group by relative date
    const groupByDate = (msgs: Message[]) => {
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);
        const weekAgo = new Date(today);
        weekAgo.setDate(weekAgo.getDate() - 7);

        const groups: { label: string; items: Message[] }[] = [
            { label: "Today", items: [] },
            { label: "Yesterday", items: [] },
            { label: "Previous 7 Days", items: [] },
            { label: "Older", items: [] },
        ];

        msgs.forEach((msg) => {
            const msgDate = new Date(msg.timestamp);
            const isToday = msgDate.toDateString() === today.toDateString();
            const isYesterday = msgDate.toDateString() === yesterday.toDateString();
            const isThisWeek = msgDate > weekAgo;

            if (isToday) {
                groups[0].items.push(msg);
            } else if (isYesterday) {
                groups[1].items.push(msg);
            } else if (isThisWeek) {
                groups[2].items.push(msg);
            } else {
                groups[3].items.push(msg);
            }
        });

        return groups.filter(g => g.items.length > 0);
    };

    const groupedQueries = groupByDate(userQueries.slice().reverse());

    const handleNavigate = (msgId: string) => {
        if (onNavigateToMessage) {
            onNavigateToMessage(msgId);
        } else {
            // Fallback: scroll to message in DOM
            const element = document.getElementById(`message-${msgId}`);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                // Add highlight effect
                element.classList.add('ring-2', 'ring-emerald-500/50');
                setTimeout(() => {
                    element.classList.remove('ring-2', 'ring-emerald-500/50');
                }, 2000);
            }
        }
    };

    return (
        <aside className="w-full flex-shrink-0 flex flex-col h-full bg-sidebar border-r border-sidebar-border">
            {/* Header with Prominent Brand */}
            <div className="p-4 border-b border-[var(--border-color)]">
                <div className="flex items-center gap-2.5 font-semibold text-[var(--text-primary)] mb-6">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500/20 to-blue-500/20 flex items-center justify-center text-emerald-400 border border-emerald-500/20 shadow-sm">
                        <Droplets size={18} />
                    </div>
                    <span>GroundWater Assistant</span>
                </div>

                <Button
                    onClick={onNewChat}
                    className="w-full justify-start gap-2 shadow-sm font-medium bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-500 hover:to-emerald-600 text-white border-0"
                >
                    <Plus size={16} />
                    <span>New Analysis</span>
                </Button>
            </div>

            <Separator className="opacity-10 bg-[var(--border-color)]" />

            {/* Chat History Navigation Header */}
            <div className="px-4 py-3 flex items-center justify-between">
                <span className="text-[10px] font-bold text-[var(--text-muted)] uppercase tracking-wider flex items-center gap-2">
                    <Clock size={10} /> Chat History
                </span>
                {userQueries.length > 0 && (
                    <div className="flex items-center gap-1">
                        <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleNavigate(userQueries[userQueries.length - 1].id)}
                            className="h-6 w-6 p-0 hover:bg-emerald-500/10 hover:text-emerald-400"
                            title="Go to latest"
                        >
                            <ChevronDown size={12} />
                        </Button>
                        <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleNavigate(userQueries[0].id)}
                            className="h-6 w-6 p-0 hover:bg-emerald-500/10 hover:text-emerald-400"
                            title="Go to first"
                        >
                            <ChevronUp size={12} />
                        </Button>
                        {onClearHistory && (
                            <Button
                                variant="ghost"
                                size="sm"
                                onClick={onClearHistory}
                                className="h-6 w-6 p-0 hover:bg-red-500/10 hover:text-red-400"
                                title="Clear history"
                            >
                                <Trash2 size={10} />
                            </Button>
                        )}
                    </div>
                )}
            </div>

            {/* History List - Scrollable with Navigation */}
            <ScrollArea className="flex-1 px-2 pb-4">
                <div className="space-y-4">
                    {groupedQueries.length === 0 ? (
                        <div className="text-xs text-muted-foreground px-4 py-8 text-center italic opacity-50">
                            <div className="mb-2 text-2xl">💧</div>
                            No queries yet. Start by asking about a district!
                        </div>
                    ) : (
                        groupedQueries.map((group) => (
                            <div key={group.label} className="px-2">
                                <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider mb-2 px-2 flex items-center gap-2">
                                    <Clock size={10} /> {group.label}
                                </div>
                                <div className="space-y-0.5">
                                    {group.items.map((msg, idx) => (
                                        <Button
                                            key={msg.id}
                                            variant="ghost"
                                            onClick={() => handleNavigate(msg.id)}
                                            className="w-full justify-between h-auto py-2 text-xs font-normal text-muted-foreground hover:text-foreground hover:bg-emerald-500/5 group px-2 transition-all"
                                        >
                                            <div className="flex flex-col items-start gap-0.5 flex-1 min-w-0">
                                                <span className="truncate max-w-full text-left text-[var(--text-secondary)] group-hover:text-[var(--text-primary)] transition-colors">
                                                    {msg.content.length > 40 ? msg.content.substring(0, 40) + "..." : msg.content}
                                                </span>
                                                <span className="text-[9px] text-[var(--text-muted)] opacity-70">
                                                    {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                                </span>
                                            </div>
                                            <ChevronRight size={12} className="opacity-0 group-hover:opacity-100 transition-opacity text-emerald-400 flex-shrink-0 ml-2" />
                                        </Button>
                                    ))}
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </ScrollArea>

            {/* Quick Stats Footer */}
            {userQueries.length > 0 && (
                <div className="p-3 border-t border-[var(--border-color)] bg-[var(--bg-element)]/30">
                    <div className="flex justify-between items-center text-[9px] text-[var(--text-muted)]">
                        <span>{userQueries.length} queries</span>
                        <span>{messages.filter(m => m.role === 'agent').length} responses</span>
                    </div>
                </div>
            )}
        </aside>
    );
}
