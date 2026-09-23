"""Generate header-dark.svg and header-light.svg.

Run from the repo root: python3 assets/build-header.py
"""
from pathlib import Path

LINE_Y = 126
LINE_HALF = 170

PALETTES = {
    "dark": dict(base="#e8e8e8", band="#ffffff", sub="#8f8f8f", line="#5a5a5a"),
    "light": dict(base="#111111", band="#7a7a7a", sub="#6b6b6b", line="#c8c8c8"),
}


def build(p):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="210" viewBox="0 0 1200 210" role="img" aria-label="Deon Roos, software engineer, Pretoria, South Africa">
  <defs>
    <linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="360" y2="0">
      <stop offset="0%" stop-color="{p['base']}"/>
      <stop offset="42%" stop-color="{p['band']}"/>
      <stop offset="58%" stop-color="{p['band']}"/>
      <stop offset="100%" stop-color="{p['base']}"/>
      <animateTransform attributeName="gradientTransform" type="translate"
        values="-420,0; 1240,0; 1240,0" keyTimes="0; 0.5; 1" dur="7s" begin="1.6s"
        calcMode="spline" keySplines="0.45 0 0.2 1; 0 0 1 1" repeatCount="indefinite"/>
    </linearGradient>

    <clipPath id="above">
      <rect class="unfoldUp" x="0" y="0" width="1200" height="{LINE_Y - 4}"/>
    </clipPath>
    <clipPath id="below">
      <rect class="unfoldDown" x="0" y="{LINE_Y + 4}" width="1200" height="{210 - LINE_Y - 4}"/>
    </clipPath>

    <style>
      .name {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        font-size: 88px; font-weight: 800; letter-spacing: -3.5px; fill: url(#shine);
      }}
      .sub {{
        font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
        font-size: 14px; letter-spacing: 2.2px; fill: {p['sub']};
      }}
      .rule {{ stroke: {p['line']}; stroke-width: 1.25; }}

      /* Entrance: the hairline draws from the centre, then the name unfolds
         upward out of it and the location line unfolds downward. */
      .rule {{ animation: lineIn 0.7s cubic-bezier(.2,.8,.2,1) both; }}
      .unfoldUp {{ animation: unfoldUp 0.9s cubic-bezier(.2,.8,.2,1) 0.45s both; }}
      .unfoldDown {{ animation: unfoldDown 0.9s cubic-bezier(.2,.8,.2,1) 0.6s both; }}
      .nameLift {{ animation: lift 0.9s cubic-bezier(.2,.8,.2,1) 0.45s both; }}
      .subDrop {{ animation: drop 0.9s cubic-bezier(.2,.8,.2,1) 0.6s both; }}

      @keyframes lineIn {{
        from {{ transform: translateX(600px) scaleX(0) translateX(-600px); }}
        to   {{ transform: none; }}
      }}
      @keyframes unfoldUp {{
        from {{ transform: translateY({LINE_Y - 4}px) scaleY(0) translateY(-{LINE_Y - 4}px); }}
        to   {{ transform: none; }}
      }}
      @keyframes unfoldDown {{
        from {{ transform: translateY({LINE_Y + 4}px) scaleY(0) translateY(-{LINE_Y + 4}px); }}
        to   {{ transform: none; }}
      }}
      @keyframes lift {{ from {{ transform: translateY(26px); }} to {{ transform: none; }} }}
      @keyframes drop {{ from {{ transform: translateY(-14px); }} to {{ transform: none; }} }}

      @media (prefers-reduced-motion: reduce) {{
        .rule, .unfoldUp, .unfoldDown, .nameLift, .subDrop {{ animation: none; }}
      }}
    </style>
  </defs>

  <line class="rule" x1="{600 - LINE_HALF}" y1="{LINE_Y}" x2="{600 + LINE_HALF}" y2="{LINE_Y}"/>

  <g clip-path="url(#above)">
    <g class="nameLift">
      <text class="name" x="600" y="{LINE_Y - 14}" text-anchor="middle">Deon Roos</text>
    </g>
  </g>

  <g clip-path="url(#below)">
    <g class="subDrop">
      <text class="sub" x="601" y="160" text-anchor="middle">SOFTWARE ENGINEER &#183; PRETORIA, SOUTH AFRICA</text>
    </g>
  </g>
</svg>
'''


if __name__ == "__main__":
    here = Path(__file__).parent
    for name, palette in PALETTES.items():
        (here / f"header-{name}.svg").write_text(build(palette))
        print(f"wrote header-{name}.svg")
