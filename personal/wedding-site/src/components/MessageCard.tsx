// The first messages, 5 May 2025, set in the site's own palette rather than
// pasted in as a phone screenshot. The words are verbatim; only the styling is
// ours, so it stays legible on any screen and belongs to the page.

type Message = { from: 'him' | 'her'; text: string; time: string };

export type MessageThread = {
  date: string;
  messages: Message[];
};

export function MessageCard({ thread, label }: { thread: MessageThread; label: string }) {
  return (
    <figure
      className="mt-6 w-full max-w-sm rounded-sm border border-sage/25 bg-cream-card p-4 shadow-[0_10px_30px_rgba(42,36,34,0.07)]"
      aria-label={label}
    >
      <figcaption className="text-center font-body text-[0.65rem] uppercase tracking-[0.22em] text-muted">
        {thread.date}
      </figcaption>

      <ol className="mt-4 flex flex-col gap-2">
        {thread.messages.map((message, index) => (
          <li
            key={index}
            className={`flex ${message.from === 'her' ? 'justify-end' : 'justify-start'}`}
          >
            <p
              className={`max-w-[85%] rounded-2xl px-3.5 py-2 font-body text-sm leading-snug ${
                message.from === 'her'
                  ? 'rounded-br-sm bg-burgundy text-cream'
                  : 'rounded-bl-sm bg-cream-deep text-ink'
              }`}
            >
              {message.text}
              <span
                className={`ml-2 align-baseline text-[0.65rem] ${
                  message.from === 'her' ? 'text-cream/60' : 'text-muted'
                }`}
              >
                {message.time}
              </span>
            </p>
          </li>
        ))}
      </ol>
    </figure>
  );
}
