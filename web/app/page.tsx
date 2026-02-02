"use client";

import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import ChatArea from "../components/ChatArea";
import { LayoutDashboard, Sparkles, AlertOctagon } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Message } from "../types";

// Dynamically import map to avoid SSR issues with Leaflet
import dynamic from 'next/dynamic';
const InteractiveMap = dynamic(() => import('../components/InteractiveMap'), {
  ssr: false,
  loading: () => <div className="w-full h-full bg-[var(--bg-app-gradient-start)] animate-pulse flex items-center justify-center text-[var(--text-muted)]">Initializing...</div>
});

const STORAGE_KEY = 'jal-rakshak-chat-history';

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);
  const [userRole, setUserRole] = useState("farmer");

  // Load chat history
  useEffect(() => {
    const key = `${STORAGE_KEY}-${userRole}`;
    const saved = localStorage.getItem(key);
    if (saved) {
      try {
        const parsed = JSON.parse(saved, (key, value) => {
          if (key === "timestamp") return new Date(value);
          return value;
        });
        setMessages(parsed);
      } catch (e) {
        console.error("Failed to parse chat history", e);
        setMessages([]);
      }
    } else {
      setMessages([]);
    }
    setIsLoaded(true);
  }, [userRole]);

  // Save chat history
  useEffect(() => {
    if (isLoaded) {
      const key = `${STORAGE_KEY}-${userRole}`;
      localStorage.setItem(key, JSON.stringify(messages));
    }
  }, [messages, isLoaded, userRole]);

  const handleSendMessage = async (query: string) => {
    if (!query.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: query,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, user_role: userRole }),
      });

      if (!response.ok) throw new Error("Failed to get response");
      const data = await response.json();

      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "agent",
        content: data.response,
        timestamp: new Date(),
        riskLevel: data.risk_level,
        originalQuery: query,
      };
      setMessages((prev) => [...prev, agentMessage]);
    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "agent",
        content: "Sorry, I encountered an error. Please make sure the API server is running.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegionSelect = (region: string) => {
    handleSendMessage(`What is the groundwater status in ${region}?`);
  };

  const handleNewChat = () => {
    if (messages.length > 0 && !confirm('Start a new analysis?')) return;
    setMessages([]);
    localStorage.removeItem(`${STORAGE_KEY}-${userRole}`);
  };

  const handleClearHistory = () => {
    if (!confirm('Clear all chat history?')) return;
    setMessages([]);
    localStorage.removeItem(`${STORAGE_KEY}-${userRole}`);
  };

  const handleNavigateToMessage = (messageId: string) => {
    const element = document.getElementById(`message-${messageId}`);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      element.classList.add('ring-2', 'ring-emerald-500/50', 'rounded-xl');
      setTimeout(() => element.classList.remove('ring-2', 'ring-emerald-500/50', 'rounded-xl'), 2000);
    }
  };

  const handleDeleteMessage = (messageId: string) => {
    if (confirm('Delete this message?')) {
      setMessages(prev => prev.filter(msg => msg.id !== messageId));
    }
  };

  const handleDeleteConversation = (userMsgId: string) => {
    if (confirm('Delete this conversation thread?')) {
      setMessages(prev => {
        const index = prev.findIndex(m => m.id === userMsgId);
        if (index === -1) return prev;

        const newMessages = [...prev];
        // Check if next message is an agent response
        if (index + 1 < newMessages.length && newMessages[index + 1].role === 'agent') {
          // Remove both user message and agent response
          newMessages.splice(index, 2);
        } else {
          // Remove just the user message
          newMessages.splice(index, 1);
        }
        return newMessages;
      });
    }
  };

  if (!isLoaded) return null;

  return (
    // Floating Layout Container with Gaps (p-4 gap-4)
    <main className="h-screen w-full overflow-hidden p-2 md:p-4 gap-4 grid grid-cols-[280px_1fr] lg:grid-cols-[280px_1fr_400px]">

      {/* 1. Floating Sidebar */}
      <div className="hidden md:flex h-full glass-panel rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow">
        <Sidebar
          messages={messages}
          onNewChat={handleNewChat}
          onClearHistory={handleClearHistory}
          onNavigateToMessage={handleNavigateToMessage}
          userRole={userRole}
          onRoleChange={setUserRole}
          onDeleteConversation={handleDeleteConversation}
        />
      </div>

      {/* 2. Floating Chat Area (Center) */}
      <div className="flex flex-col h-full glass-panel rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow relative">
        <ChatArea
          messages={messages}
          isLoading={isLoading}
          onSendMessage={handleSendMessage}
          userRole={userRole}
          onDeleteMessage={handleDeleteMessage}
          onDeleteConversation={handleDeleteConversation}
        />
      </div>

      {/* 3. Floating Right Panel (Map) */}
      <div className="hidden lg:flex flex-col h-full glass-panel rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow">
        {/* Map Header */}
        <div className="p-4 border-b border-[var(--border-subtle)] flex items-center justify-between bg-[var(--bg-surface)]/50 backdrop-blur-sm">
          <h3 className="text-xs font-bold text-[var(--text-primary)] flex items-center gap-2 uppercase tracking-widest">
            <LayoutDashboard size={14} className="text-emerald-500" />
            District Intelligence
          </h3>
          <Badge variant="outline" className="text-[10px] border-emerald-500/20 bg-emerald-500/10 text-emerald-600 font-mono px-2 py-0.5 animate-pulse">
            LIVE
          </Badge>
        </div>

        {/* Map Container */}
        <div className="flex-1 relative w-full bg-black/5">
          <InteractiveMap onRegionSelect={handleRegionSelect} />
        </div>

        {/* Floating Context Panel (Bottom of Right Column) */}
        <div className="h-1/2 flex flex-col border-t border-[var(--border-subtle)] bg-[var(--bg-surface)]/80 backdrop-blur-md">
          <div className="p-3 border-b border-[var(--border-subtle)] flex items-center justify-between">
            <h4 className="text-[10px] font-bold text-[var(--text-muted)] uppercase tracking-wider flex items-center gap-2">
              <Sparkles size={10} /> Live Analytics
            </h4>
            <div className="text-[9px] text-[var(--text-muted)] font-mono">UPDATED: Just now</div>
          </div>

          <ScrollArea className="flex-1 p-4">
            <div className="space-y-6">
              {/* Metrics */}
              <div className="grid grid-cols-2 gap-3">
                <Card className="p-3 rounded-xl border-[var(--border-subtle)] bg-white/50 dark:bg-slate-800/50 shadow-none">
                  <div className="text-[var(--text-muted)] text-[9px] uppercase font-bold mb-1">At Risk</div>
                  <div className="text-lg font-mono font-semibold text-[var(--text-primary)]">24 <span className="text-red-500 text-[10px]">67%</span></div>
                </Card>
                <Card className="p-3 rounded-xl border-[var(--border-subtle)] bg-white/50 dark:bg-slate-800/50 shadow-none">
                  <div className="text-[var(--text-muted)] text-[9px] uppercase font-bold mb-1">Mapped</div>
                  <div className="text-lg font-mono font-semibold text-[var(--text-primary)]">36 <span className="text-emerald-500 text-[10px]">●</span></div>
                </Card>
              </div>

              {/* Progress Bar */}
              <div>
                <div className="text-[9px] font-bold text-[var(--text-muted)] uppercase mb-3 flex justify-between">
                  <span>Risk Distribution</span>
                </div>
                <div className="h-2 w-full flex rounded-full overflow-hidden mb-2 bg-[var(--border-subtle)]">
                  <div className="h-full bg-red-600" style={{ width: '44%' }} title="Over-Exploited" />
                  <div className="h-full bg-orange-500" style={{ width: '6%' }} title="Critical" />
                  <div className="h-full bg-yellow-500" style={{ width: '17%' }} title="Semi-Critical" />
                  <div className="h-full bg-emerald-500" style={{ width: '25%' }} title="Safe" />
                </div>
              </div>

              {/* Alerts List */}
              <div className="space-y-3">
                <div className="text-[9px] font-bold text-[var(--text-muted)] uppercase border-b border-[var(--border-subtle)] pb-2">
                  Priority Alerts
                </div>
                {[
                  { name: "Chennai", status: "Over-exploited", desc: "Extraction exceeds recharge.", color: "text-red-600" },
                  { name: "Salem", status: "Over-exploited", desc: "Industrial demand critical.", color: "text-red-600" },
                  { name: "Coimbatore", status: "Critical", desc: "High borewell density.", color: "text-orange-500" }
                ].map((item) => (
                  <div key={item.name} className="flex items-start gap-3 p-2 rounded-lg hover:bg-[var(--bg-app-gradient-start)] dark:hover:bg-slate-800/50 transition-colors cursor-pointer group" onClick={() => handleSendMessage(`What is the groundwater status in ${item.name}?`)}>
                    <AlertOctagon size={14} className={`${item.color} mt-0.5`} />
                    <div className="flex-1">
                      <div className={`text-xs font-semibold text-[var(--text-primary)] group-hover:${item.color} transition-colors`}>{item.name}</div>
                      <div className="text-[10px] text-[var(--text-secondary)] leading-tight mt-0.5">{item.desc}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </ScrollArea>
        </div>
      </div>
    </main>
  );
}
