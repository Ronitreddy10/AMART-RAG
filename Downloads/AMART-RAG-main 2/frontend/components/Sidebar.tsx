import { ShieldAlert, Terminal, FileText, Settings, Activity } from "lucide-react";
import Link from "next/link";

export default function Sidebar() {
    return (
        <div className="h-screen w-64 bg-black/50 border-r border-primary/20 flex flex-col p-4 backdrop-blur-sm fixed left-0 top-0">
            <div className="flex items-center gap-2 mb-8 mx-auto">
                <ShieldAlert className="w-8 h-8 text-accent animate-pulse" />
                <h1 className="text-xl font-bold tracking-widest text-primary terminal-text">RED TEAM<br /><span className="text-xs text-secondary">COMMAND CENTER</span></h1>
            </div>

            <nav className="flex flex-col gap-4">
                <Link href="/" className="flex items-center gap-3 p-3 rounded hover:bg-primary/20 hover:text-white transition-all group">
                    <Activity className="w-5 h-5 group-hover:animate-spin" />
                    <span>Dashboard</span>
                </Link>
                <Link href="/logs" className="flex items-center gap-3 p-3 rounded hover:bg-primary/20 hover:text-white transition-all">
                    <Terminal className="w-5 h-5" />
                    <span>Attack Logs</span>
                </Link>
                <Link href="/gallery" className="flex items-center gap-3 p-3 rounded hover:bg-primary/20 hover:text-white transition-all">
                    <FileText className="w-5 h-5" />
                    <span>Artifacts</span>
                </Link>
                <Link href="/settings" className="flex items-center gap-3 p-3 rounded hover:bg-primary/20 hover:text-white transition-all opacity-50 cursor-not-allowed">
                    <Settings className="w-5 h-5" />
                    <span>Settings</span>
                </Link>
            </nav>

            <div className="mt-auto text-xs text-secondary text-center">
                SYSTEM STATUS: ONLINE
                <br />
                v1.0.0
            </div>
        </div>
    );
}
