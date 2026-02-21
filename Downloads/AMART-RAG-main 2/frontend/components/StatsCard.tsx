interface StatsCardProps {
    title: string;
    value: string | number;
    icon?: React.ReactNode;
    trend?: string;
    color?: "primary" | "accent" | "secondary";
}

export default function StatsCard({ title, value, icon, trend, color = "primary" }: StatsCardProps) {
    const borderColor = color === "accent" ? "border-accent/40" : "border-primary/40";
    const textColor = color === "accent" ? "text-accent" : "text-primary";

    return (
        <div className={`bg-black/40 border ${borderColor} p-6 rounded relative overflow-hidden group hover:bg-black/60 transition-all`}>
            <div className="absolute top-0 right-0 p-2 opacity-20 group-hover:opacity-40 transition-opacity">
                {icon}
            </div>
            <h3 className="text-secondary text-sm font-bold uppercase tracking-wider">{title}</h3>
            <div className={`text-4xl font-mono font-bold mt-2 ${textColor} terminal-text`}>
                {value}
            </div>
            {trend && (
                <div className="text-xs text-secondary mt-2">
                    {trend}
                </div>
            )}
        </div>
    );
}
