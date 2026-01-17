"use client";

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, CircleMarker, Tooltip } from "react-leaflet";
import "leaflet/dist/leaflet.css";

// Risk Colors
const RISK_COLORS: Record<string, string> = {
    "Safe": "#10b981",          // Emerald 500
    "Moderate": "#f59e0b",      // Amber 500
    "Semi-Critical": "#f59e0b", // Amber 500
    "Critical": "#ef4444",      // Red 500
    "Over-Exploited": "#7f1d1d",// Red 900
    "Saline": "#a855f7",        // Purple 500
    "Unknown": "#64748b"        // Slate 500
};

interface DistrictData {
    coords: [number, number];
    risk: string;
}

interface MapData {
    [key: string]: DistrictData;
}

export default function InteractiveMap({ onRegionSelect }: { onRegionSelect: (region: string) => void }) {
    const [mapData, setMapData] = useState<MapData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch("http://localhost:8000/api/map")
            .then((res) => res.json())
            .then((data) => {
                setMapData(data);
                setLoading(false);
            })
            .catch((err) => {
                console.error("Failed to load map data", err);
                setLoading(false);
            });
    }, []);

    if (loading) return (
        <div className="flex items-center justify-center h-full w-full bg-[var(--bg-panel)] text-[var(--text-muted)] animate-pulse">
            <span className="text-xs font-mono uppercase tracking-widest">Loading Satellite Data...</span>
        </div>
    );

    if (!mapData) return (
        <div className="flex items-center justify-center h-full w-full bg-[var(--bg-panel)] text-red-400">
            <span className="text-xs">Data Unavailable</span>
        </div>
    );

    return (
        <div className="w-full h-full relative bg-[var(--bg-app)]">
            <MapContainer
                center={[11.1271, 78.6569]}
                zoom={7}
                scrollWheelZoom={true}
                zoomControl={false}
                style={{ height: "100%", width: "100%", background: "#020617" }}
            >
                {/* Dark Matter Map Tile */}
                <TileLayer
                    attribution='&copy; <a href="https://carto.com/">CARTO</a>'
                    url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                />

                {Object.entries(mapData).map(([name, data]) => {
                    const color = RISK_COLORS[data.risk] || RISK_COLORS["Unknown"];

                    return (
                        <CircleMarker
                            key={name}
                            center={data.coords}
                            radius={6}
                            pathOptions={{
                                color: color,
                                fillColor: color,
                                fillOpacity: 0.8,
                                weight: 1
                            }}
                            eventHandlers={{
                                click: () => onRegionSelect(name),
                            }}
                        >
                            <Tooltip
                                direction="top"
                                offset={[0, -10]}
                                opacity={1}
                                className="leaflet-tooltip-dark" // Custom class if needed or rely on default
                            >
                                <div className="text-center font-sans space-y-1">
                                    <b className="text-xs block text-slate-800">{name}</b>
                                    <span style={{ color: color }} className="text-[10px] font-bold uppercase">{data.risk}</span>
                                </div>
                            </Tooltip>

                            {/* Halo Effect for High Risk Areas */}
                            {(data.risk === "Critical" || data.risk === "Over-Exploited") && (
                                <CircleMarker
                                    center={data.coords}
                                    radius={15}
                                    pathOptions={{ color: color, fillColor: color, fillOpacity: 0.1 }}
                                    stroke={false}
                                />
                            )}
                        </CircleMarker>
                    )
                })}
            </MapContainer>

            {/* Floating Info Overlay */}
            <div className="absolute top-4 right-4 bg-slate-900/90 backdrop-blur-md p-3 rounded-xl border border-white/10 text-xs z-[1000] shadow-2xl max-w-[150px]">
                <h4 className="font-bold mb-2 text-slate-200">Tamil Nadu</h4>
                <div className="text-[10px] text-slate-400 leading-relaxed">
                    Interactive Groundwater Risk Map. Data sourced from latest periodic assessments.
                </div>
            </div>
        </div>
    );
}
