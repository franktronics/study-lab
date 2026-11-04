import { useMemo, useState } from "react";
import { Coordinates, Mafs, Plot, Point, Text } from "mafs";
import "mafs/core.css";
import { compile } from "mathjs";
import { Slider } from "@/components/ui/slider";
import { MathText } from "@/lib/math-text";

/** Token names usable as colors (see global.css). */
export type TokenColor = "primary" | "violet" | "emphasis" | "highlight" | "positive" | "negative" | "foreground" | "muted-foreground";

export interface PlotFunction {
  /** Expression in x and the parameters, mathjs syntax: "a * sin(b * x)", "x^2", "exp(-x)". */
  expr: string;
  color?: TokenColor;
  /** Legend label, inline math with $...$. */
  label?: string;
  dashed?: boolean;
}

export interface Param {
  min: number;
  max: number;
  value: number;
  step?: number;
  /** Displayed name, inline math allowed; default: the parameter key. */
  label?: string;
}

export interface FunctionPlotProps {
  functions: PlotFunction[];
  params?: Record<string, Param>;
  xRange?: [number, number];
  yRange?: [number, number];
  /** Fixed points: [{ x, y, label?, color? }]. */
  points?: { x: number; y: number; label?: string; color?: TokenColor }[];
  height?: number;
  /** Allow panning/zooming. */
  zoom?: boolean;
}

const PALETTE: TokenColor[] = ["primary", "emphasis", "violet", "positive", "highlight", "negative"];
const cssColor = (c: TokenColor) => `var(--${c})`;

/** Interactive function plot (Mafs) with parameters driven by sliders. */
export default function FunctionPlotIsland({
  functions,
  params = {},
  xRange = [-5, 5],
  yRange = [-3, 3],
  points = [],
  height = 360,
  zoom = false,
}: FunctionPlotProps) {
  const [values, setValues] = useState<Record<string, number>>(() =>
    Object.fromEntries(Object.entries(params).map(([k, p]) => [k, p.value])),
  );
  const compiled = useMemo(() => functions.map((f) => compile(f.expr)), [functions]);

  return (
    <div className="study-plot not-prose my-6 overflow-hidden rounded-xl border bg-card">
      <Mafs
        height={height}
        viewBox={{ x: xRange, y: yRange, padding: 0 }}
        preserveAspectRatio={false}
        zoom={zoom}
        pan={zoom}
      >
        <Coordinates.Cartesian />
        {compiled.map((fn, i) => {
          const f = functions[i];
          return (
            <Plot.OfX
              key={i}
              y={(x) => {
                const y = fn.evaluate({ ...values, x });
                return typeof y === "number" ? y : NaN;
              }}
              color={cssColor(f.color ?? PALETTE[i % PALETTE.length])}
              style={f.dashed ? "dashed" : "solid"}
              weight={3}
            />
          );
        })}
        {points.map((p, i) => (
          <g key={i}>
            <Point x={p.x} y={p.y} color={cssColor(p.color ?? "emphasis")} />
            {p.label && (
              <Text x={p.x} y={p.y} attach="ne" size={16} color={cssColor(p.color ?? "emphasis")}>
                {p.label}
              </Text>
            )}
          </g>
        ))}
      </Mafs>
      {(Object.keys(params).length > 0 || functions.some((f) => f.label)) && (
        <div className="grid gap-3 border-t p-4">
          {functions.some((f) => f.label) && (
            <div className="flex flex-wrap gap-4 text-sm">
              {functions.map(
                (f, i) =>
                  f.label && (
                    <span key={i} className="inline-flex items-center gap-2">
                      <span className="h-0.5 w-5 rounded" style={{ background: cssColor(f.color ?? PALETTE[i % PALETTE.length]) }} />
                      <MathText text={f.label} />
                    </span>
                  ),
              )}
            </div>
          )}
          {Object.entries(params).map(([key, p]) => (
            <label key={key} className="grid grid-cols-[6rem_1fr_3.5rem] items-center gap-3 text-sm">
              <MathText text={p.label ?? `$${key}$`} />
              <Slider
                min={p.min}
                max={p.max}
                step={p.step ?? (p.max - p.min) / 100}
                value={[values[key]]}
                onValueChange={([v]) => setValues((s) => ({ ...s, [key]: v }))}
              />
              <span className="text-right text-muted-foreground tabular-nums">{values[key].toFixed(2)}</span>
            </label>
          ))}
        </div>
      )}
    </div>
  );
}
