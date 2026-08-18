import React from "react";

interface AnchorLogoProps {
  className?: string;
  size?: "sm" | "md" | "lg";
}

export function AnchorLogo({ className = "", size = "md" }: AnchorLogoProps) {
  const sizeMap = {
    sm: "h-7 w-7",
    md: "h-9 w-9",
    lg: "h-11 w-11",
  };

  const iconSizes = {
    sm: "w-4 h-4",
    md: "w-5 h-5",
    lg: "w-6 h-6",
  };

  return (
    <div
      className={`relative flex shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-600 via-indigo-700 to-indigo-900 text-white shadow-md shadow-indigo-500/25 ring-1 ring-white/20 transition-transform duration-200 group-hover:scale-105 ${sizeMap[size]} ${className}`}
    >
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={`${iconSizes[size]} transition-all`}
      >
        {/* Anchor Ring */}
        <circle cx="12" cy="5" r="2.5" />
        {/* Center Vertical Shank */}
        <line x1="12" y1="7.5" x2="12" y2="21" />
        {/* Cross Stock */}
        <line x1="6.5" y1="10" x2="17.5" y2="10" />
        {/* Curved Fluke Base */}
        <path d="M4 14.5C4 18.5 7.5 21 12 21C16.5 21 20 18.5 20 14.5" />
        {/* Fluke Arrow Tips */}
        <path d="M4 14.5L2.5 13" />
        <path d="M20 14.5L21.5 13" />
      </svg>
      {/* Subtle Inner Glow Point */}
      <span className="absolute top-1 right-1 h-1.5 w-1.5 rounded-full bg-indigo-300 opacity-75 blur-xs" />
    </div>
  );
}