"use client";
import { useEffect, useState } from "react";
import { FileText, Image as ImageIcon, Download } from "lucide-react";

interface Artifact {
    type: "image" | "pdf";
    name: string;
    url: string;
}

export default function GalleryPage() {
    const [artifacts, setArtifacts] = useState<Artifact[]>([]);

    useEffect(() => {
        const fetchArtifacts = async () => {
            try {
                const res = await fetch('http://localhost:8000/gallery');
                const data = await res.json();
                setArtifacts(data.artifacts);
            } catch (e) {
                console.error(e);
            }
        };
        fetchArtifacts();
    }, []);

    return (
        <div className="space-y-8">
            <h2 className="text-3xl font-bold text-white border-b border-primary/20 pb-4">ARTIFACT GALLERY</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {artifacts.map((artifact, i) => (
                    <div key={i} className="bg-black/40 border border-primary/20 rounded overflow-hidden group hover:border-primary transition-all">
                        <div className="h-48 bg-black/50 flex items-center justify-center relative overflow-hidden">
                            {/* Preview */}
                            {artifact.type === 'image' ? (
                                // eslint-disable-next-line @next/next/no-img-element
                                <img src={`http://localhost:8000${artifact.url}`} alt="Artifact" className="w-full h-full object-cover group-hover:scale-110 transition-transform opacity-80 group-hover:opacity-100" />
                            ) : (
                                <FileText className="w-16 h-16 text-primary group-hover:scale-110 transition-transform" />
                            )}
                        </div>

                        <div className="p-4 bg-muted/20">
                            <div className="flex justify-between items-start">
                                <div>
                                    <h3 className="font-bold text-primary">{artifact.name}</h3>
                                    <div className="text-xs text-secondary mt-1 uppercase">{artifact.type} EVIDENCE</div>
                                </div>
                                <a
                                    href={`http://localhost:8000${artifact.url}`}
                                    target="_blank"
                                    download
                                    className="p-2 hover:bg-primary/20 rounded text-primary transition-colors"
                                >
                                    <Download className="w-4 h-4" />
                                </a>
                            </div>
                        </div>
                    </div>
                ))}

                {artifacts.length === 0 && (
                    <div className="col-span-full py-12 text-center text-muted border border-dashed border-primary/20 rounded">
                        NO ARTIFACTS CAPTURED YET
                    </div>
                )}
            </div>
        </div>
    );
}
