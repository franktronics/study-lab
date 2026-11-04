import { useEffect, useRef } from "react";
import { onThemeChange, token } from "@/lib/theme";

export interface PlotlyProps {
  /** Plotly traces (https://plotly.com/javascript/reference/). Colors: leave empty to use the theme colorway. */
  data: Record<string, unknown>[];
  /** Plotly layout, merged over the themed defaults. */
  layout?: Record<string, unknown>;
  height?: number;
}

type Obj = Record<string, unknown>;
const isObj = (v: unknown): v is Obj => typeof v === "object" && v !== null && !Array.isArray(v);

/** Deep merge: page layout values override the themed defaults without dropping nested keys. */
function merge(base: Obj, over: Obj): Obj {
  const out: Obj = { ...base };
  for (const [k, v] of Object.entries(over)) out[k] = isObj(v) && isObj(base[k]) ? merge(base[k], v) : v;
  return out;
}

/** Data charts, 3D surfaces, heatmaps... Plotly is loaded only on pages that use it. */
export default function PlotlyIsland({ data, layout = {}, height = 420 }: PlotlyProps) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let disposed = false;
    let unsubscribe = () => {};
    import("plotly.js-dist-min").then(({ default: Plotly }) => {
      if (disposed || !ref.current) return;
      const el = ref.current;
      unsubscribe = onThemeChange(() => {
        const fg = token("foreground");
        const grid = token("border");
        const axis = { gridcolor: grid, zerolinecolor: grid, linecolor: grid };
        Plotly.react(
          el,
          data,
          merge(
            {
              height,
              margin: { l: 50, r: 20, t: 30, b: 45 },
              paper_bgcolor: "rgba(0,0,0,0)",
              plot_bgcolor: "rgba(0,0,0,0)",
              font: { color: fg, family: "inherit" },
              colorway: ["primary", "emphasis", "violet", "positive", "highlight", "negative"].map(token),
              xaxis: axis,
              yaxis: axis,
              scene: { xaxis: axis, yaxis: axis, zaxis: axis },
            },
            layout,
          ),
          { responsive: true, displaylogo: false },
        );
      });
    });
    return () => {
      disposed = true;
      unsubscribe();
    };
  }, [data, layout, height]);

  return <div ref={ref} className="not-prose my-6 rounded-xl border bg-card p-2" style={{ minHeight: height }} />;
}
