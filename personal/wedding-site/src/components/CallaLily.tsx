// Calla lily, drawn in a botanical line style after the reference Emmanuel sent:
// a furled spathe with a long recurved tip, veins running lengthwise up the cone,
// a stippled spadix, and slim leaves with a mid vein.
//
// `variant="bloom"` gives the single flower head, for use as a small divider mark.
//
// Decorative only, so it is hidden from screen readers and carries no contrast
// requirement. It still has to be visible, which is why the stem takes a lighter
// green than the body palette when it sits on burgundy.

function Bloom({ detail = true }: { detail?: boolean }) {
  return (
    <g>
      {/* Right edge of the cone, from the base up to the rim. */}
      <path d="M112 152 C 136 126, 150 96, 146 66 C 143 48, 138 40, 132 38" />
      {/* Far rim of the mouth. */}
      <path d="M132 38 C 116 26, 92 22, 72 32" />
      {/* The long recurved tip. */}
      <path d="M72 32 C 58 22, 42 16, 29 22 C 38 29, 52 36, 64 44" />
      {/* Near rim, dipping across the opening. */}
      <path d="M64 44 C 86 60, 114 56, 132 38" opacity="0.9" />
      {/* Left edge of the cone, from the tip back down to the stem. */}
      <path d="M64 44 C 70 82, 92 122, 112 152" />
      {/* Veins, lengthwise up the cone. Dropped at small sizes, where they
          crowd into a blot rather than reading as veins. */}
      {detail ? (
        <>
      <g opacity="0.7">
        <path d="M110 146 C 96 116, 80 78, 70 48" />
        <path d="M112 147 C 104 114, 96 76, 90 52" />
        <path d="M114 148 C 114 116, 114 78, 112 52" />
        <path d="M116 148 C 124 118, 130 84, 130 52" />
        <path d="M118 149 C 132 124, 142 96, 143 70" />
      </g>
      {/* Spadix, standing in the throat. */}
      <path d="M92 52 C 88 66, 88 80, 92 90 C 97 80, 98 64, 96 52 C 95 48, 93 48, 92 52 Z" />
      <g fill="currentColor" stroke="none" opacity="0.85">
        <circle cx="93" cy="60" r="1" />
        <circle cx="94" cy="68" r="1" />
        <circle cx="93" cy="76" r="1" />
        <circle cx="94" cy="84" r="1" />
      </g>
        </>
      ) : null}
    </g>
  );
}

function Leaf({ blade, vein }: { blade: string; vein: string }) {
  return (
    <g>
      <path d={blade} />
      <path d={vein} opacity="0.7" />
    </g>
  );
}

export function CallaLily({
  className = '',
  stemClassName = '',
  strokeWidth = 1.5,
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
      viewBox={bloomOnly ? '20 8 142 152' : '0 0 200 520'}
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
        {!bloomOnly && (
          <g className={stemClassName}>
            {/* Main stem. */}
            <path d="M112 152 C 106 250, 100 360, 106 508" />
            {/* Stem of the second, smaller bloom. */}
            <path d="M158 208 C 144 250, 120 310, 106 386" />
            <Leaf
              blade="M104 430 C 74 372, 62 296, 76 232 C 100 288, 110 366, 104 430 Z"
              vein="M100 420 C 86 360, 82 296, 78 244"
            />
            <Leaf
              blade="M106 400 C 128 350, 152 306, 176 282 C 160 336, 134 380, 106 400 Z"
              vein="M108 394 C 130 352, 152 318, 172 290"
            />
          </g>
        )}

        {!bloomOnly && (
          <g transform="translate(104 132) scale(0.5) rotate(10)">
            <Bloom detail={!bloomOnly} />
          </g>
        )}

        <Bloom detail={!bloomOnly} />
      </g>
    </svg>
  );
}
