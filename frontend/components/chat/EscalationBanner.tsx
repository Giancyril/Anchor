"use client";

import { AlertCircle, Mail, ArrowRight } from "lucide-react";

interface EscalationBannerProps {
  onEscalate?: () => void;
}

export function EscalationBanner({ onEscalate }: EscalationBannerProps) {
  return (
    <div className="mt-3 rounded-xl border border-amber-200 bg-amber-50/60 p-3.5 text-xs text-amber-900">
      <div className="flex items-start gap-2.5">
        <AlertCircle className="h-4 w-4 text-amber-600 shrink-0 mt-0.5" />
        <div className="flex-1">
          <p className="font-medium text-amber-950">
            Information not found in documentation
          </p>
          <p className="mt-0.5 text-amber-800 leading-relaxed">
            Our automated agent is grounded strictly in company materials and cannot extrapolate. Would you like to escalate this inquiry to our human support team?
          </p>
          <div className="mt-2.5 flex items-center gap-2">
            <a
              href="mailto:support@company.com?subject=Support%20Inquiry%20Escalation"
              className="inline-flex items-center gap-1.5 rounded-lg bg-amber-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-amber-700 transition"
            >
              <Mail className="h-3.5 w-3.5" />
              <span>Contact Support Team</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}