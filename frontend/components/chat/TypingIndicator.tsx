export function TypingIndicator() {
  return (
    <div className="flex items-center gap-2 text-xs text-slate-500 py-2">
      <div className="flex items-center gap-1">
        <span className="h-1.5 w-1.5 rounded-full bg-indigo-600 typing-dot" />
        <span className="h-1.5 w-1.5 rounded-full bg-indigo-600 typing-dot" />
        <span className="h-1.5 w-1.5 rounded-full bg-indigo-600 typing-dot" />
      </div>
      <span className="text-[11px] font-medium text-slate-500">Searching documentation & grounding answer...</span>
    </div>
  );
}