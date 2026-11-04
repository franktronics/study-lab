/** UI strings of the study components. Add a language by adding a block (fallback: en). */
const STRINGS = {
  en: {
    definition: "Definition", theorem: "Theorem", note: "Note", warning: "Warning", exam: "Exam", tip: "Tip", example: "Example",
    nextStep: "Next step", showAll: "Show all", showSolution: "Show solution", check: "Check", correct: "Correct!",
    incorrect: "Not quite.", retry: "Try again", flip: "Click to flip", page: "p.", sources: "Sources", chapters: "Chapters",
    toggleTheme: "Toggle theme", home: "All pages", noPages: "No pages yet.",
  },
  fr: {
    definition: "Définition", theorem: "Théorème", note: "Remarque", warning: "Attention", exam: "Examen", tip: "Astuce", example: "Exemple",
    nextStep: "Étape suivante", showAll: "Tout afficher", showSolution: "Voir la solution", check: "Vérifier", correct: "Correct !",
    incorrect: "Pas tout à fait.", retry: "Réessayer", flip: "Cliquer pour retourner", page: "p.", sources: "Sources", chapters: "Chapitres",
    toggleTheme: "Changer de thème", home: "Toutes les pages", noPages: "Aucune page pour l'instant.",
  },
  de: {
    definition: "Definition", theorem: "Satz", note: "Hinweis", warning: "Achtung", exam: "Prüfung", tip: "Tipp", example: "Beispiel",
    nextStep: "Nächster Schritt", showAll: "Alles zeigen", showSolution: "Lösung anzeigen", check: "Prüfen", correct: "Richtig!",
    incorrect: "Nicht ganz.", retry: "Nochmal", flip: "Zum Umdrehen klicken", page: "S.", sources: "Quellen", chapters: "Kapitel",
    toggleTheme: "Design wechseln", home: "Alle Seiten", noPages: "Noch keine Seiten.",
  },
} as const;

export type StringKey = keyof (typeof STRINGS)["en"];

export function t(lang: string | undefined, key: StringKey): string {
  const base = (lang ?? "en").slice(0, 2).toLowerCase() as keyof typeof STRINGS;
  return (STRINGS[base] ?? STRINGS.en)[key];
}
