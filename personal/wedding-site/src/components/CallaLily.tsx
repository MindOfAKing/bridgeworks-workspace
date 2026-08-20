// Calla lily, drawn as one continuous line after the reference Emmanuel sent:
// a tilted spathe pinched to a point where it meets the stem, the front lip
// furling inward, the spadix standing in the throat, a long tapering stem.
// Five strokes, no veins, no shading.
//
// `variant="bloom"` gives the flower head alone, for the small divider mark.
//
// Decorative only, so it is hidden from screen readers and carries no contrast
// requirement. It still has to be visible, which is why the stem takes a
// lighter green than the body palette when it sits on burgundy.

export function CallaLily({
  className = '',
  stemClassName = '',
  strokeWidth = 1.4,
  variant = 'full',
}: {
  className?: string;
  stemClassName?: string;
  strokeWidth?: number;
  variant?: 'full' | 'bloom';
}) {
  const bloomOnly = variant === 'bloom';

  return (
    <svg
      viewBox={bloomOnly ? '34 52 186 176' : '20 40 210 500'}
      fill="none"
      aria-hidden
      focusable="false"
      className={className}
      preserveAspectRatio="xMidYMid meet"
    >
      <g
        stroke="currentColor"
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeLinejoin="round"
        vectorEffect="non-scaling-stroke"
      >
        {/* The spathe, one closed sweep pinched at the stem. */}
        <path d="M96 214 C 56 190, 44 146, 66 112 C 90 74, 146 60, 180 84 C 206 102, 206 140, 182 168 C 158 196, 126 212, 96 214 Z" />
        {/* The tip, flicking up at the top right. */}
        <path d="M180 84 C 192 74, 202 74, 202 82" />
        {/* The front lip, furling in toward the throat. */}
        <path d="M96 214 C 124 194, 148 170, 158 142 C 162 130, 156 122, 148 126" />
        {/* Spadix. */}
        <path d="M104 200 C 99 170, 108 138, 126 114 C 136 134, 132 172, 117 196 C 112 205, 106 207, 104 200 Z" />

        {!bloomOnly && (
          <path className={stemClassName} d="M96 216 C 100 300, 102 420, 98 528" />
        )}
      </g>
    </svg>
  );
}
