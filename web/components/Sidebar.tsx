"use client";

import { Message } from "../app/page";
import { Droplets, Plus, Clock, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";

interface SidebarProps {
    messages: Message[];
}

export default function Sidebar({ messages }: SidebarProps) {
    const userQueries = messages.filter((m) => m.role === "user");

    // Mock grouping logic (In real app, parse ISO timestamps)
    const recent = userQueries.slice(-3).reverse();
    const previous = userQueries.slice(0, -3).reverse();

    return (
        <aside className="w-full flex-shrink-0 flex flex-col h-full bg-sidebar border-r border-sidebar-border">
            {/* Header with Prominent Brand */}
            <div className="p-4 border-b border-[var(--border-color)]">
                <div className="flex items-center gap-2.5 font-semibold text-[var(--text-primary)] mb-6">
                    <div className="w-8 h-8 rounded-lg bg-[var(--color-brand)]/10 flex items-center justify-center text-[var(--color-brand)] border border-[var(--color-brand)]/20">
                        <Droplets size={18} />
                    </div>
                    <span>Jal-Rakshak</span>
                </div>

                <Button className="w-full justify-start gap-2 shadow-sm font-medium" variant="default">
                    <Plus size={16} />
                    <span>New Analysis</span>
                </Button>
            </div>

            <Separator className="opacity-10 bg-[var(--border-color)]" />

            {/* History List - Scrollable */}
            <ScrollArea className="flex-1 px-2 py-4">
                <div className="space-y-6">
                    {/* Group: Today */}
                    <div className="px-2">
                        <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider mb-2 px-2 flex items-center gap-2">
                            <Clock size={10} /> Today
                        </div>
                        {recent.length === 0 ? (
                            <div className="text-xs text-muted-foreground px-2 italic opacity-50">No queries yet</div>
                        ) : (
                            <div className="space-y-0.5">
                                {recent.map((msg, idx) => (
                                    <Button key={idx} variant="ghost" className="w-full justify-between h-8 text-xs font-normal text-muted-foreground hover:text-foreground group px-2">
                                        <span className="truncate max-w-[170px] text-left">{msg.content}</span>
                                        <ChevronRight size={12} className="opacity-0 group-hover:opacity-100 transition-opacity text-muted-foreground" />
                                    </Button>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Group: Previous */}
                    {previous.length > 0 && (
                        <div className="px-2">
                            <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider mb-2 px-2">
                                Previous 7 Days
                            </div>
                            <div className="space-y-0.5">
                                {previous.map((msg, idx) => (
                                    <Button key={idx} variant="ghost" className="w-full justify-start h-8 text-xs font-normal text-muted-foreground hover:text-foreground opacity-80 px-2">
                                        <span className="truncate text-left">{msg.content}</span>
                                    </Button>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </ScrollArea>

            {/* Footer space if needed, or just end the aside */}
        </aside>
    );
}
