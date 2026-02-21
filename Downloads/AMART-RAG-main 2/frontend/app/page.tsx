"use client";
import React, { useState, useEffect } from "react";
import StatsCard from "@/components/StatsCard";
import TerminalWidget from "@/components/TerminalWidget";
import { Play, Shield, Skull, Zap, AlertTriangle } from "lucide-react";

export default function Home() {
  const [stats, setStats] = useState({ total_attacks: 0, successful_breaks: 0, success_rate: 0 });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Poll stats
    const fetchStats = async () => {
      try {
        const res = await fetch('http://localhost:8000/stats');
        const data = await res.json();
        setStats(data);
      } catch (e) {
        console.error(e);
      }
    };
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  const startAttack = async () => {
    setLoading(true);
    try {
      await fetch('http://localhost:8000/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mode: 'full' }),
      });
      // Just trigger, don't wait for completion logic here as it's async
    } catch (e) {
      console.error(e);
    }
    setTimeout(() => setLoading(false), 2000); // Re-enable button
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-end border-b border-primary/20 pb-4">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">MISSION CONTROL</h2>
          <p className="text-secondary">ACTIVE TARGET: <span className="text-accent font-bold">LLAMA-3-8B-INSTRUCT</span></p>
        </div>
        <div className="text-right">
          <div className="text-xs text-secondary">RAM USAGE</div>
          <div className="text-xl font-bold text-primary">18.4 / 24.0 GB</div>
        </div>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatsCard
          title="Total Attacks"
          value={stats.total_attacks}
          icon={<Zap className="w-8 h-8" />}
        />
        <StatsCard
          title="Success Rate"
          value={`${stats.success_rate}%`}
          color="accent"
          icon={<AlertTriangle className="w-8 h-8" />}
          trend="+5.2% vs last hr"
        />
        <StatsCard
          title="Secrets Leaked"
          value={stats.successful_breaks}
          color="secondary"
          icon={<Skull className="w-8 h-8" />}
        />
      </div>

      {/* Main Action & Terminal */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[500px]">
        {/* Controls */}
        <div className="col-span-1 bg-black/40 border border-primary/20 p-6 rounded flex flex-col gap-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-primary/20 rounded-full">
              <Shield className="w-6 h-6 text-primary" />
            </div>
            <div>
              <div className="text-white font-bold">ATTACK MODE</div>
              <div className="text-xs text-secondary">SEQUENTIAL EXECUTION</div>
            </div>
          </div>

          <p className="text-sm text-gray-400">
            Initiate a full Red-Team cycle.
            Sequence: DeepSeek (Attack) &rarr; Llama3 (Victim) &rarr; Flux (Vision).
          </p>

          <button
            onClick={startAttack}
            disabled={loading}
            className={`
              mt-auto py-6 text-xl font-bold rounded border tracking-widest transition-all
              ${loading
                ? 'bg-accent/20 border-accent/50 text-accent cursor-not-allowed animate-pulse'
                : 'bg-primary/10 border-primary text-primary hover:bg-primary/20 hover:scale-[1.02] active:scale-95'
              }
            `}
          >
            {loading ? "INITIALIZING..." : "INITIATE ATTACK"}
          </button>
        </div>

        {/* Console */}
        <div className="col-span-2">
          <TerminalWidget />
        </div>
      </div>
    </div>
  );
}
