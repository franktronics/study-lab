import { useState } from "react";
import { Button } from "@/components/ui/button";
import { t } from "@/lib/i18n";
import { MathText } from "@/lib/math-text";
import { cn } from "@/lib/utils";

export interface QuizOption {
  text: string;
  correct?: boolean;
  /** Shown after checking when this option was selected. */
  explain?: string;
}

export interface QuizProps {
  question: string;
  options: QuizOption[];
  /** General explanation shown after checking. */
  explanation?: string;
  lang?: string;
}

/** Multiple choice question. Several correct options → multi-select. Inline math with $...$. */
export default function QuizIsland({ question, options, explanation, lang }: QuizProps) {
  const multi = options.filter((o) => o.correct).length > 1;
  const [selected, setSelected] = useState<number[]>([]);
  const [checked, setChecked] = useState(false);

  const toggle = (i: number) => {
    if (checked) return;
    setSelected((s) => (multi ? (s.includes(i) ? s.filter((x) => x !== i) : [...s, i]) : [i]));
  };
  const allRight = options.every((o, i) => Boolean(o.correct) === selected.includes(i));

  return (
    <div className="not-prose my-6 rounded-xl border bg-card p-5">
      <p className="mb-4 font-medium">
        <MathText text={question} />
      </p>
      <div className="grid gap-2">
        {options.map((o, i) => {
          const isSelected = selected.includes(i);
          return (
            <button
              key={i}
              type="button"
              onClick={() => toggle(i)}
              className={cn(
                "rounded-lg border px-4 py-2.5 text-left text-sm transition-colors",
                !checked && "hover:bg-accent",
                !checked && isSelected && "border-primary bg-primary/10",
                checked && o.correct && "border-positive bg-positive/10",
                checked && isSelected && !o.correct && "border-negative bg-negative/10",
              )}
            >
              <MathText text={o.text} />
              {checked && isSelected && o.explain && (
                <span className="mt-1 block text-xs text-muted-foreground">
                  <MathText text={o.explain} />
                </span>
              )}
            </button>
          );
        })}
      </div>
      <div className="mt-4 flex items-center gap-3">
        {checked ? (
          <>
            <span className={cn("text-sm font-medium", allRight ? "text-positive" : "text-negative")}>
              {t(lang, allRight ? "correct" : "incorrect")}
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                setChecked(false);
                setSelected([]);
              }}
            >
              {t(lang, "retry")}
            </Button>
          </>
        ) : (
          <Button size="sm" disabled={selected.length === 0} onClick={() => setChecked(true)}>
            {t(lang, "check")}
          </Button>
        )}
      </div>
      {checked && explanation && (
        <p className="mt-4 border-t pt-3 text-sm text-muted-foreground">
          <MathText text={explanation} />
        </p>
      )}
    </div>
  );
}
