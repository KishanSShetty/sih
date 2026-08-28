"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { ShieldCheck, Mail, AlertTriangle, AlertCircle, Activity, Loader2, Info, Lock, CheckCircle2, Shield, Search } from "lucide-react";

interface ScanResult {
    id: number;
    subject: string;
    sender: string;
    risk_score: number;
    risk_level: string;
    explanation: string;
    timestamp: string;
    content_preview: string;
}

interface ScanStats {
    total_scans: number;
    high_risk: number;
    suspicious: number;
    safe_emails: number;
    total_emails_scanned_24h: number;
    phishing_detected_24h: number;
    safe_emails_24h: number;
    detection_rate: number;
}

const container = {
    hidden: { opacity: 0 },
    show: {
        opacity: 1,
        transition: { staggerChildren: 0.1 }
    }
};

const item = {
    hidden: { y: 20, opacity: 0 },
    show: { y: 0, opacity: 1 }
};

export default function GmailVerificationPage() {
    const [recentScans, setRecentScans] = useState<ScanResult[]>([]);
    const [stats, setStats] = useState<ScanStats | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [statsRes, recentRes] = await Promise.all([
                    fetch("http://localhost:8002/api/v1/email-scans/stats"),
                    fetch("http://localhost:8002/api/v1/email-scans/recent?limit=20")
                ]);
                const statsData = await statsRes.json();
                const recentData = await recentRes.json();
                setStats(statsData);
                setRecentScans(recentData);
            } catch (error) {
                console.error("Failed to fetch Gmail verification data:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
        const interval = setInterval(fetchData, 15000);
        return () => clearInterval(interval);
    }, []);

    const formatTime = (isoString: string) => {
        const date = new Date(isoString);
        return new Intl.DateTimeFormat('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true,
            month: 'short',
            day: 'numeric'
        }).format(date);
    };

    if (loading || !stats) {
        return (
            <div className="flex h-[50vh] flex-col items-center justify-center text-muted-foreground gap-4">
                <motion.div animate={{ rotate: 360 }} transition={{ duration: 2, repeat: Infinity, ease: "linear" }}>
                    <Loader2 className="w-8 h-8 text-blue-500" />
                </motion.div>
                <p className="animate-pulse">Loading Gmail Verification Engine...</p>
            </div>
        );
    }

    const latestScan = recentScans.length > 0 ? recentScans[0] : null;

    return (
        <motion.div variants={container} initial="hidden" animate="show" className="space-y-8 pb-10">
            
            {/* HEADER */}
            <motion.div variants={item} className="flex justify-between items-start">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-slate-900 flex items-center gap-3">
                        <Mail className="w-8 h-8 text-blue-600" />
                        Gmail Security Verification
                    </h1>
                    <p className="text-slate-500 mt-2">
                        Inspect opened Gmail messages for phishing, impersonation and authentication threats.
                    </p>
                </div>
                <div className="flex items-center gap-2 bg-emerald-50 text-emerald-700 px-4 py-2 rounded-full border border-emerald-100 shadow-sm">
                    <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                    <span className="text-sm font-semibold uppercase tracking-wider">Protection Active</span>
                </div>
            </motion.div>

            {/* TOP METRIC CARDS */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <motion.div variants={item} className="p-5 rounded-2xl border border-slate-200 bg-white shadow-sm flex flex-col justify-between">
                    <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-widest flex items-center gap-2"><Activity size={14}/> Emails Scanned</h3>
                    <div className="mt-4 text-3xl font-bold text-slate-900">{stats.total_scans.toLocaleString()}</div>
                </motion.div>
                
                <motion.div variants={item} className="p-5 rounded-2xl border border-slate-200 bg-white shadow-sm flex flex-col justify-between">
                    <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-widest flex items-center gap-2"><Shield size={14}/> Threats Detected</h3>
                    <div className="mt-4 text-3xl font-bold text-slate-900">{stats.high_risk + stats.suspicious}</div>
                </motion.div>
                
                <motion.div variants={item} className="p-5 rounded-2xl border border-slate-200 bg-white shadow-sm flex flex-col justify-between relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-24 h-24 bg-rose-50 rounded-bl-full -mr-8 -mt-8" />
                    <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-widest flex items-center gap-2 relative z-10"><AlertTriangle size={14}/> High-Risk Emails</h3>
                    <div className="mt-4 text-3xl font-bold text-rose-600 relative z-10">{stats.high_risk}</div>
                </motion.div>
                
                <motion.div variants={item} className="p-5 rounded-2xl border border-emerald-200 bg-emerald-50/50 shadow-sm flex flex-col justify-between">
                    <h3 className="text-xs font-semibold text-emerald-600 uppercase tracking-widest flex items-center gap-2"><CheckCircle2 size={14}/> Protection Status</h3>
                    <div className="mt-4 text-xl font-bold text-emerald-700">ACTIVE</div>
                    <div className="text-xs text-emerald-600 mt-1">Extension Connected</div>
                </motion.div>
            </div>

            {/* CURRENT EMAIL VERIFICATION PANEL */}
            <motion.div variants={item} className="bg-slate-900 rounded-3xl p-8 text-white shadow-xl relative overflow-hidden">
                <div className="absolute top-0 right-0 w-96 h-96 bg-blue-500/10 rounded-bl-full -mr-20 -mt-20 blur-3xl pointer-events-none" />
                <div className="flex justify-between items-start relative z-10">
                    <div>
                        <h2 className="text-sm font-semibold uppercase tracking-widest text-slate-400 mb-6 flex items-center gap-2">
                            <Search size={16} /> Last Scanned Email
                        </h2>
                        
                        {latestScan ? (
                            <div className="space-y-6">
                                <div>
                                    <div className="text-xs text-slate-400 mb-1 uppercase font-semibold">Sender</div>
                                    <div className="text-xl font-medium text-white">{latestScan.sender || "UNKNOWN"}</div>
                                </div>
                                
                                <div>
                                    <div className="text-xs text-slate-400 mb-1 uppercase font-semibold">Subject</div>
                                    <div className="text-lg text-slate-300">{latestScan.subject || "UNKNOWN"}</div>
                                </div>
                            </div>
                        ) : (
                            <div className="text-slate-400 italic">No recent scans detected. Open an email in Gmail to begin.</div>
                        )}
                    </div>
                    
                    {latestScan && (
                        <div className="flex flex-col items-end">
                            <div className="text-xs text-slate-400 mb-2 uppercase font-semibold">Overall Risk</div>
                            <div className={`text-6xl font-black mb-2 tracking-tighter ${latestScan.risk_level === 'CRITICAL' ? 'text-rose-500' : latestScan.risk_level === 'SUSPICIOUS' ? 'text-amber-500' : 'text-emerald-400'}`}>
                                {Math.round(latestScan.risk_score * 100)}%
                            </div>
                            <div className={`px-4 py-1.5 rounded-full text-sm font-bold tracking-widest ${latestScan.risk_level === 'CRITICAL' ? 'bg-rose-500/20 text-rose-400' : latestScan.risk_level === 'SUSPICIOUS' ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                                {latestScan.risk_level}
                            </div>
                        </div>
                    )}
                </div>
            </motion.div>

            {/* MIDDLE GRIDS: SIGNALS & AUTHENTICATION */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                
                {/* THREAT SIGNALS */}
                <motion.div variants={item} className="p-6 rounded-2xl border border-slate-200 bg-white shadow-sm">
                    <h2 className="text-sm font-semibold uppercase tracking-widest text-slate-500 mb-6 flex items-center gap-2">
                        <Activity size={16} /> Threat Signals
                    </h2>
                    
                    <div className="space-y-4">
                        {['Urgency', 'Authority', 'Fear', 'Impersonation'].map((signal) => (
                            <div key={signal} className="flex justify-between items-center p-3 rounded-lg bg-slate-50 border border-slate-100">
                                <span className="font-medium text-slate-700">{signal}</span>
                                <span className="text-xs font-bold px-3 py-1 bg-slate-200 text-slate-500 rounded-full">UNKNOWN</span>
                            </div>
                        ))}
                    </div>
                </motion.div>

                {/* EMAIL AUTHENTICATION */}
                <motion.div variants={item} className="p-6 rounded-2xl border border-slate-200 bg-white shadow-sm">
                    <h2 className="text-sm font-semibold uppercase tracking-widest text-slate-500 mb-6 flex items-center gap-2">
                        <ShieldCheck size={16} /> Email Authentication
                    </h2>
                    
                    <div className="space-y-4">
                        <div className="grid grid-cols-2 text-xs uppercase font-semibold text-slate-400 mb-2 px-2">
                            <span>Check</span>
                            <span className="text-right">Status</span>
                        </div>
                        {['SPF', 'DKIM', 'DMARC'].map((check) => (
                            <div key={check} className="flex justify-between items-center p-3 rounded-lg bg-slate-50 border border-slate-100">
                                <span className="font-medium text-slate-700">{check}</span>
                                <span className="text-xs font-bold px-3 py-1 bg-slate-200 text-slate-500 rounded-full">UNKNOWN</span>
                            </div>
                        ))}
                    </div>
                    
                    <div className="mt-6 pt-4 border-t border-slate-100">
                        <div className="text-xs text-slate-400 mb-1 uppercase font-semibold">Authentication Source</div>
                        <div className="text-sm text-slate-600 font-medium">Authentication-Results</div>
                    </div>
                </motion.div>

            </div>

            {/* LOWER GRIDS: INFRASTRUCTURE & EXPLANATION */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                
                {/* EMAIL INFRASTRUCTURE */}
                <motion.div variants={item} className="p-6 rounded-2xl border border-slate-200 bg-white shadow-sm">
                    <h2 className="text-sm font-semibold uppercase tracking-widest text-slate-500 mb-6 flex items-center gap-2">
                        <Info size={16} /> Email Infrastructure
                    </h2>
                    
                    <div className="grid grid-cols-2 gap-y-6">
                        <div>
                            <div className="text-xs text-slate-400 mb-1 uppercase font-semibold">Origin IP</div>
                            <div className="text-sm font-medium text-slate-700">UNKNOWN</div>
                        </div>
                        <div>
                            <div className="text-xs text-slate-400 mb-1 uppercase font-semibold">Received Chain</div>
                            <div className="text-sm font-medium text-slate-700">UNKNOWN</div>
                        </div>
                        <div>
                            <div className="text-xs text-slate-400 mb-1 uppercase font-semibold">MX Record</div>
                            <div className="text-sm font-medium text-slate-700">UNKNOWN</div>
                        </div>
                        <div>
                            <div className="text-xs text-slate-400 mb-1 uppercase font-semibold">Domain Age</div>
                            <div className="text-sm font-medium text-slate-700">UNKNOWN</div>
                        </div>
                    </div>
                </motion.div>

                {/* WHY THIS EMAIL WAS FLAGGED */}
                <motion.div variants={item} className="p-6 rounded-2xl border border-slate-200 bg-white shadow-sm flex flex-col">
                    <h2 className="text-sm font-semibold uppercase tracking-widest text-slate-500 mb-6 flex items-center gap-2">
                        <AlertCircle size={16} /> Why This Email Was Flagged
                    </h2>
                    
                    <div className="flex-1 bg-slate-50 rounded-xl p-5 border border-slate-100 flex items-center">
                        {latestScan ? (
                            <p className="text-slate-700 leading-relaxed font-medium">
                                {latestScan.explanation}
                            </p>
                        ) : (
                            <p className="text-slate-400 italic">No analysis available.</p>
                        )}
                    </div>
                </motion.div>

            </div>

            {/* FORENSICS CAPABILITY */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                
                {/* CURRENT FORENSIC ANALYSIS */}
                <motion.div variants={item} className="p-6 rounded-2xl border border-slate-200 bg-white shadow-sm">
                    <h2 className="text-sm font-semibold uppercase tracking-widest text-slate-500 mb-6 flex items-center gap-2">
                        <Activity size={16} /> Forensic Analysis
                    </h2>
                    
                    <div className="space-y-3">
                        {[
                            { name: 'Raw MIME Acquisition', status: 'VERIFIED' },
                            { name: 'Header Analysis', status: 'VERIFIED' },
                            { name: 'SPF Verification', status: 'VERIFIED' },
                            { name: 'DKIM Verification', status: 'VERIFIED' },
                            { name: 'DMARC Verification', status: 'VERIFIED' },
                            { name: 'DNS Analysis', status: 'VERIFIED' },
                        ].map((tech) => (
                            <div key={tech.name} className="flex justify-between items-center border-b border-slate-50 pb-2 last:border-0">
                                <span className="text-sm text-slate-600">{tech.name}</span>
                                <span className="text-[10px] font-bold px-2 py-0.5 bg-emerald-100 text-emerald-700 rounded uppercase tracking-wider">{tech.status}</span>
                            </div>
                        ))}
                    </div>
                </motion.div>

                {/* ADVANCED FORENSICS PLACEHOLDER */}
                <motion.div variants={item} className="p-6 rounded-2xl border border-slate-200 bg-slate-50 shadow-sm opacity-80">
                    <div className="flex justify-between items-start mb-6">
                        <h2 className="text-sm font-semibold uppercase tracking-widest text-slate-400 flex items-center gap-2">
                            <Lock size={16} /> Advanced Forensics
                        </h2>
                        <span className="text-[10px] font-bold px-2 py-1 bg-blue-100 text-blue-700 rounded uppercase tracking-wider">NEXT PHASE</span>
                    </div>
                    
                    <p className="text-sm text-slate-500 mb-6">
                        Advanced forensic analysis will provide deeper message-header correlation, authentication verification, infrastructure intelligence and expanded threat attribution.
                    </p>

                    <div className="space-y-3">
                        {['Deep MIME Forensics', 'Advanced Header Correlation', 'Domain Intelligence', 'IP Intelligence', 'Academic Forensic Report'].map((tech) => (
                            <div key={tech} className="flex justify-between items-center border-b border-slate-200/50 pb-2 last:border-0">
                                <span className="text-sm text-slate-400 line-through">{tech}</span>
                                <span className="text-[10px] font-bold px-2 py-0.5 bg-slate-200 text-slate-500 rounded uppercase tracking-wider">COMING SOON</span>
                            </div>
                        ))}
                    </div>
                </motion.div>
            </div>

            {/* RECENT EMAIL SCANS TABLE */}
            <motion.div variants={item} className="p-6 rounded-2xl border border-slate-200 bg-white shadow-sm overflow-hidden">
                <h2 className="text-sm font-semibold uppercase tracking-widest text-slate-500 mb-6 flex items-center gap-2">
                    <Activity size={16} /> Recent Email Scans
                </h2>
                
                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm">
                        <thead className="bg-slate-50 text-slate-500 border-y border-slate-200">
                            <tr>
                                <th className="px-4 py-3 font-semibold uppercase tracking-wider text-xs">Time</th>
                                <th className="px-4 py-3 font-semibold uppercase tracking-wider text-xs">Sender</th>
                                <th className="px-4 py-3 font-semibold uppercase tracking-wider text-xs">Subject</th>
                                <th className="px-4 py-3 font-semibold uppercase tracking-wider text-xs">Risk</th>
                                <th className="px-4 py-3 font-semibold uppercase tracking-wider text-xs">Status</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {recentScans.map((scan) => (
                                <tr key={scan.id} className="hover:bg-slate-50 transition-colors cursor-pointer group">
                                    <td className="px-4 py-4 text-slate-500 whitespace-nowrap">{formatTime(scan.timestamp)}</td>
                                    <td className="px-4 py-4 font-medium text-slate-900 max-w-[200px] truncate">{scan.sender || "UNKNOWN"}</td>
                                    <td className="px-4 py-4 text-slate-600 max-w-[300px] truncate">{scan.subject || "UNKNOWN"}</td>
                                    <td className="px-4 py-4 font-semibold text-slate-700">{Math.round(scan.risk_score * 100)}%</td>
                                    <td className="px-4 py-4">
                                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold tracking-widest uppercase
                                            ${scan.risk_level === 'CRITICAL' ? 'bg-rose-100 text-rose-700' : 
                                              scan.risk_level === 'SUSPICIOUS' ? 'bg-amber-100 text-amber-700' : 
                                              'bg-emerald-100 text-emerald-700'}`}>
                                            {scan.risk_level}
                                        </span>
                                    </td>
                                </tr>
                            ))}
                            {recentScans.length === 0 && (
                                <tr>
                                    <td colSpan={5} className="px-4 py-8 text-center text-slate-500 italic">No recent email scans found.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </motion.div>

        </motion.div>
    );
}
