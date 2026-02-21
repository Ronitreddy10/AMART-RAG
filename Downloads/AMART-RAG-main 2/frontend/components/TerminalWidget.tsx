"use client";
import { useEffect, useState, useRef } from 'react';

export default function TerminalWidget() {
    const [logs, setLogs] = useState<string[]>([]);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const res = await fetch('http://localhost:8000/logs');
                const data = await res.json();
                if (data.logs) {
                    setLogs(data.logs);
                }
            } catch (e) {
                console.error("Failed to fetch logs", e);
            }
        };

        const interval = setInterval(fetchLogs, 2000);
        fetchLogs();
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [logs]);

    return (
        <div className="bg-black border border-secondary/50 rounded p-4 font-mono text-sm h-96 overflow-hidden flex flex-col shadow-[0_0_15px_rgba(0,255,65,0.1)]">
            <div className="flex justify-between items-center mb-2 border-b border-secondary/20 pb-2">
                <span className="text-secondary font-bold">TERMINAL OUTPUT</span>
                <div className="flex gap-2">
                    <div className="w-3 h-3 rounded-full bg-accent/50"></div>
                    <div className="w-3 h-3 rounded-full bg-yellow-500/50"></div>
                    <div className="w-3 h-3 rounded-full bg-secondary/50"></div>
                </div>
            </div>

            <div ref={scrollRef} className="flex-1 overflow-y-auto space-y-1 p-2">
                {logs.map((log, i) => (
                    <div key={i} className="terminal-text text-primary/80 hover:text-primary transition-colors">
                        <span className="text-secondary mr-2">$</span>
                        {log}
                    </div>
                ))}
                {logs.length === 0 && (
                    <div className="text-muted animate-pulse">Waiting for stream...</div>
                )}
            </div>
        </div>
    );
}
