"use client";

import { Message } from "../types";
import { Droplets, Plus, Clock, ChevronRight, Trash2, Sprout, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { useLanguage } from "../contexts/LanguageContext";

interface SidebarProps {
    messages: Message[];
    onNavigateToMessage?: (messageId: string) => void;
    onNewChat?: () => void;
    onClearHistory?: () => void;
    userRole: string;
    onRoleChange: (role: string) => void;
    onDeleteConversation?: (id: string) => void;
}

export default function Sidebar({ messages, onNavigateToMessage, onNewChat, onClearHistory, userRole, onRoleChange, onDeleteConversation }: SidebarProps) {
    const { language, setLanguage, t } = useLanguage();
    const userQueries = messages.filter((m) => m.role === "user");

    // Group by relative date
    const groupByDate = (msgs: Message[]) => {
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);
        const weekAgo = new Date(today);
        weekAgo.setDate(weekAgo.getDate() - 7);

        const groups: { label: string; items: Message[] }[] = [
            { label: t("today"), items: [] },
            { label: t("yesterday"), items: [] },
            { label: t("previous_7_days"), items: [] },
            { label: t("older"), items: [] },
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
            const element = document.getElementById(`message-${msgId}`);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                element.classList.add('ring-2', 'ring-emerald-500/50');
                setTimeout(() => {
                    element.classList.remove('ring-2', 'ring-emerald-500/50');
                }, 2000);
            }
        }
    };

    return (
        <aside className="w-full h-full flex flex-col bg-transparent"> {/* bg-transparent because parent has glass-panel */}

            {/* Header */}
            <div className="p-5">
                <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 shadow-lg shadow-emerald-500/20 flex items-center justify-center text-white">
                            <Droplets size={18} fill="currentColor" className="opacity-90" />
                        </div>
                        <span className="font-bold text-[var(--text-primary)] tracking-tight hidden md:inline">{t("app_title")}</span>
                    </div>

                    {/* Language Toggler (Glass Pill) */}
                    <button
                        onClick={() => setLanguage(language === 'en' ? 'ta' : 'en')}
                        className="h-8 w-8 rounded-full bg-[var(--bg-app-gradient-start)] border border-[var(--border-glass)] text-[10px] font-bold text-[var(--text-secondary)] hover:text-emerald-600 hover:scale-105 transition-all shadow-sm"
                        title="Change Language"
                    >
                        {language === 'en' ? 'TA' : 'EN'}
                    </button>
                </div>

                <Button
                    onClick={onNewChat}
                    className="w-full justify-start gap-2 shadow-md hover:shadow-lg font-medium bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white border-0 transition-all duration-300 transform hover:-translate-y-0.5"
                >
                    <Plus size={18} />
                    <span>{t("new_analysis")}</span>
                </Button>

                {/* User Role Selector (Segmented Control) */}
                <div className="mt-6">
                    <div className="flex p-1 bg-[var(--bg-app-gradient-start)]/80 rounded-xl border border-[var(--border-subtle)]">
                        <button
                            onClick={() => onRoleChange("farmer")}
                            className={`flex-1 py-1.5 text-xs font-semibold rounded-lg transition-all duration-300 flex items-center justify-center ${userRole === "farmer"
                                ? "bg-white dark:bg-slate-700 text-emerald-600 shadow-sm"
                                : "text-[var(--text-muted)] hover:text-[var(--text-primary)]"
                                }`}>
                            <Sprout size={14} className="mr-1.5" /> {t("farmer")}
                        </button>
                        <button
                            onClick={() => onRoleChange("officer")}
                            className={`flex-1 py-1.5 text-xs font-semibold rounded-lg transition-all duration-300 flex items-center justify-center ${userRole === "officer"
                                ? "bg-white dark:bg-slate-700 text-blue-600 shadow-sm"
                                : "text-[var(--text-muted)] hover:text-[var(--text-primary)]"
                                }`}
                        >
                            <Shield size={14} className="mr-1.5" /> {t("officer")}
                        </button>
                    </div>
                </div>
            </div>

            <Separator className="opacity-50 bg-[var(--border-subtle)] mx-5 w-auto" />

            {/* History Header */}
            <div className="px-5 py-4 flex items-center justify-between">
                <span className="text-[10px] font-bold text-[var(--text-muted)] uppercase tracking-widest flex items-center gap-2">
                    <Clock size={11} /> {t("chat_history")}
                </span>
                {userQueries.length > 0 && (
                    <div className="flex items-center gap-1 opacity-60 hover:opacity-100 transition-opacity">
                        {onClearHistory && (
                            <button
                                onClick={onClearHistory}
                                className="p-1 hover:bg-red-50 text-[var(--text-muted)] hover:text-red-500 rounded-md transition-colors"
                                title="Clear history"
                            >
                                <Trash2 size={12} />
                            </button>
                        )}
                    </div>
                )}
            </div>

            {/* History List */}
            <ScrollArea className="flex-1 px-3 pb-4">
                <div className="space-y-5 px-2">
                    {groupedQueries.length === 0 ? (
                        <div className="text-xs text-[var(--text-muted)] py-10 text-center italic opacity-60">
                            {t("no_queries")}
                        </div>
                    ) : (
                        groupedQueries.map((group) => (
                            <div key={group.label}>
                                <div className="text-[9px] font-bold text-[var(--text-muted)]/70 uppercase tracking-widest mb-2 px-2">
                                    {group.label}
                                </div>
                                <div className="space-y-1">
                                    {group.items.map((msg) => (
                                        <button
                                            key={msg.id}
                                            onClick={() => handleNavigate(msg.id)}
                                            className="w-full text-left flex items-center justify-between group p-2 rounded-lg hover:bg-[var(--bg-app-gradient-start)] dark:hover:bg-slate-800/50 transition-all duration-200 border border-transparent hover:border-[var(--border-subtle)]"
                                        >
                                            <div className="flex flex-col gap-0.5 flex-1 min-w-0">
                                                <span className="text-xs font-medium text-[var(--text-secondary)] group-hover:text-[var(--text-primary)] truncate transition-colors">
                                                    {msg.content}
                                                </span>
                                                <span className="text-[9px] text-[var(--text-muted)] opacity-60">
                                                    {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                                </span>
                                            </div>

                                            <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                                {onDeleteConversation && (
                                                    <div
                                                        onClick={(e) => {
                                                            e.stopPropagation();
                                                            onDeleteConversation(msg.id);
                                                        }}
                                                        className="p-1.5 text-[var(--text-muted)] hover:text-red-500 hover:bg-red-500/10 rounded-md transition-all"
                                                        title="Delete conversation"
                                                    >
                                                        <Trash2 size={12} />
                                                    </div>
                                                )}
                                                <ChevronRight size={12} className="text-emerald-500" />
                                            </div>
                                        </button>
                                    ))}
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </ScrollArea>

            {/* Footer Stats */}
            {
                userQueries.length > 0 && (
                    <div className="p-4 bg-[var(--bg-surface)]/30 backdrop-blur-sm border-t border-[var(--border-subtle)]">
                        <div className="flex justify-between items-center text-[10px] font-medium text-[var(--text-muted)]">
                            <span>{userQueries.length} {t("queries")}</span>
                            <div className="h-3 w-[1px] bg-[var(--border-subtle)]"></div>
                            <span>{messages.filter(m => m.role === 'agent').length} {t("responses")}</span>
                        </div>
                    </div>
                )
            }
        </aside >
    );
}
