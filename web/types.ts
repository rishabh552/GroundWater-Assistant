export interface Message {
    id: string;
    role: "user" | "agent";
    content: string;
    timestamp: Date;
    riskLevel?: string;
    originalQuery?: string; // Store the user's original question for reports
}
