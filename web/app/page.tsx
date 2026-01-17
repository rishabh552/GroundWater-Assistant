"use client";

import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import ChatArea from "../components/ChatArea";
import { LayoutDashboard, Sparkles, AlertOctagon } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";

export interface Message {
  id: string;
  role: "user" | "agent";
  content: string;
  timestamp: Date;
  riskLevel?: string;
  originalQuery?: string; // Store the user's original question for reports
}

// Dynamically import map to avoid SSR issues with Leaflet
import dynamic from 'next/dynamic';
const InteractiveMap = dynamic(() => import('../components/InteractiveMap'), {
  ssr: false,
  loading: () => <div className="w-full h-full bg-[var(--bg-element)] animate-pulse flex items-center justify-center text-[var(--text-muted)]">Initializing Satellite Map...</div>
});

const STORAGE_KEY = 'jal-rakshak-chat-history';

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  // Persist hydration check
  const [isLoaded, setIsLoaded] = useState(false);

  // Load chat history on mount
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const parsed = JSON.parse(saved, (key, value) => {
          if (key === "timestamp") return new Date(value);
          return value;
        });
        setMessages(parsed);
      } catch (e) {
        console.error("Failed to parse chat history", e);
      }
    }
    setIsLoaded(true);
  }, []);

  // Save chat history on update
  useEffect(() => {
    if (isLoaded) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
    }
  }, [messages, isLoaded]);

  const handleSendMessage = async (query: string) => {
    if (!query.trim() || isLoading) return;

    // Add user message
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
        body: JSON.stringify({ query }),
      });

      if (!response.ok) throw new Error("Failed to get response");

      const data = await response.json();

      // Add agent message
      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "agent",
        content: data.response,
        timestamp: new Date(),
        riskLevel: data.risk_level,
        originalQuery: query, // Store the original query
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
    // Auto-trigger search when clicking map
    handleSendMessage(`What is the groundwater status in ${region}?`);
  };

  // New chat - clear messages
  const handleNewChat = () => {
    if (messages.length > 0 && !confirm('Start a new analysis? Current chat will be cleared.')) return;
    setMessages([]);
    localStorage.removeItem(STORAGE_KEY);
  };

  // Clear all history
  const handleClearHistory = () => {
    if (!confirm('Clear all chat history? This cannot be undone.')) return;
    setMessages([]);
    localStorage.removeItem(STORAGE_KEY);
  };

  // Navigate to specific message
  const handleNavigateToMessage = (messageId: string) => {
    const element = document.getElementById(`message-${messageId}`);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      // Highlight effect
      element.classList.add('ring-2', 'ring-emerald-500/50', 'rounded-xl');
      setTimeout(() => {
        element.classList.remove('ring-2', 'ring-emerald-500/50', 'rounded-xl');
      }, 2000);
    }
  };

  if (!isLoaded) return null; // Prevent hydration mismatch

  return (
    <main className="container-main grid grid-cols-[280px_1fr] lg:grid-cols-[280px_1fr_400px] h-screen w-full overflow-hidden bg-[var(--bg-app)]">

      {/* Left Sidebar */}
      <div className="hidden md:flex h-full overflow-hidden border-r border-[var(--border-color)]">
        <Sidebar
          messages={messages}
          onNewChat={handleNewChat}
          onClearHistory={handleClearHistory}
          onNavigateToMessage={handleNavigateToMessage}
        />
      </div>
      {/* Center Chat Area */}
      <div className="flex flex-col h-full overflow-hidden relative border-r border-[var(--border-color)]">
        <ChatArea
          messages={messages}
          isLoading={isLoading}
          onSendMessage={handleSendMessage}
        />
      </div>

      {/* Right Panel: Map & Context */}
      <div className="hidden lg:flex flex-col h-full bg-background overflow-hidden border-l border-border relative z-10 w-[400px]">
        {/* Map Header */}
        <div className="p-4 border-b border-border flex items-center justify-between bg-card/50 backdrop-blur-md">
          <h3 className="text-xs font-bold text-foreground flex items-center gap-2 uppercase tracking-widest">
            <LayoutDashboard size={14} className="text-primary" />
            District Intelligence
          </h3>
          <Badge variant="outline" className="text-[10px] border-primary/20 bg-primary/10 text-primary font-mono px-2 py-0.5 animate-pulse">
            LIVE
          </Badge>
        </div>

        {/* Map Container */}
        <div className="flex-1 relative w-full bg-black">
          <div className="absolute inset-0 shadow-[inset_0_0_50px_rgba(0,0,0,0.5)] z-10 pointer-events-none" />
          <InteractiveMap onRegionSelect={handleRegionSelect} />
        </div>

        {/* Selected Context / Quick Stats - EXPANDED ANALYTICS */}
        <div className="h-1/2 flex flex-col border-t border-border bg-card">

          {/* Tab/Header */}
          <div className="p-3 border-b border-border flex items-center justify-between">
            <h4 className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider flex items-center gap-2">
              <Sparkles size={10} /> Live Analytics
            </h4>
            <div className="text-[9px] text-muted-foreground font-mono">UPDATED: Just now</div>
          </div>

          <ScrollArea className="flex-1 p-4">
            <div className="space-y-6">

              {/* Matrix: Key Metrics */}
              <div className="grid grid-cols-2 gap-3">
                <Card className="p-3 rounded-lg border-border bg-accent/20 shadow-none">
                  <div className="text-muted-foreground text-[9px] uppercase font-bold mb-1">Avg Depth</div>
                  <div className="text-lg font-mono font-semibold text-foreground">14.2m <span className="text-destructive text-[10px]">-2%</span></div>
                </Card>
                <Card className="p-3 rounded-lg border-border bg-accent/20 shadow-none">
                  <div className="text-muted-foreground text-[9px] uppercase font-bold mb-1">Stations Online</div>
                  <div className="text-lg font-mono font-semibold text-foreground">1,204 <span className="text-primary text-[10px]">●</span></div>
                </Card>
              </div>

              {/* Chart: Risk Distribution */}
              <div>
                <div className="text-[9px] font-bold text-muted-foreground uppercase mb-3 flex justify-between">
                  <span>Risk Distribution</span>
                  <span>Total: 38 Dists</span>
                </div>
                {/* Multi-colored Progress Bar */}
                <div className="h-2 w-full flex rounded-full overflow-hidden mb-2 bg-muted">
                  <div className="h-full bg-destructive w-[20%]" title="Critical" />
                  <div className="h-full bg-orange-700 w-[10%]" title="Over-Exploited" />
                  <div className="h-full bg-yellow-500 w-[30%]" title="Moderate" />
                  <div className="h-full bg-green-500 w-[40%]" title="Safe" />
                </div>
                {/* Legend */}
                <div className="flex justify-between text-[9px] text-muted-foreground font-mono">
                  <span className="flex items-center gap-1"><div className="w-1.5 h-1.5 rounded-full bg-destructive" /> Crit</span>
                  <span className="flex items-center gap-1"><div className="w-1.5 h-1.5 rounded-full bg-orange-700" /> Extr</span>
                  <span className="flex items-center gap-1"><div className="w-1.5 h-1.5 rounded-full bg-yellow-500" /> Mod</span>
                  <span className="flex items-center gap-1"><div className="w-1.5 h-1.5 rounded-full bg-green-500" /> Safe</span>
                </div>
              </div>

              {/* List: Critical Alerts */}
              <div>
                <div className="text-[9px] font-bold text-muted-foreground uppercase mb-3 border-b border-border pb-2">
                  Priority Alerts
                </div>
                <div className="space-y-2">
                  <div className="flex items-start gap-2 p-2 rounded hover:bg-accent transition-colors cursor-pointer group">
                    <AlertOctagon size={12} className="text-destructive mt-0.5" />
                    <div className="flex-1">
                      <div className="text-xs font-semibold text-foreground group-hover:text-destructive transition-colors">Perambalur District</div>
                      <div className="text-[10px] text-muted-foreground leading-tight mt-0.5">Groundwater depletion rate at 4% annually. Immediate restriction advised.</div>
                    </div>
                    <div className="text-[8px] text-muted-foreground whitespace-nowrap">2h ago</div>
                  </div>

                  <div className="flex items-start gap-2 p-2 rounded hover:bg-accent transition-colors cursor-pointer group">
                    <AlertOctagon size={12} className="text-orange-700 mt-0.5" />
                    <div className="flex-1">
                      <div className="text-xs font-semibold text-foreground group-hover:text-orange-700 transition-colors">Tiruvannamalai</div>
                      <div className="text-[10px] text-muted-foreground leading-tight mt-0.5">Borewell density exceeded threshold. <span className="underline decoration-dotted">View Order</span></div>
                    </div>
                    <div className="text-[8px] text-muted-foreground whitespace-nowrap">5h ago</div>
                  </div>
                </div>
              </div>

            </div>
          </ScrollArea>
        </div>
      </div>
    </main>
  );
}
