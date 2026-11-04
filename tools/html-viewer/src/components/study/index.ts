/**
 * Study components, available in every page.mdx without import.
 * Static ones are Astro components; interactive ones wrap a React island (hydrated when visible).
 */
import Callout from "./Callout.astro";
import Flashcard from "./Flashcard.astro";
import Flashcards from "./Flashcards.astro";
import FunctionPlot from "./FunctionPlot.astro";
import Plotly from "./Plotly.astro";
import Quiz from "./Quiz.astro";
import Solution from "./Solution.astro";
import Source from "./Source.astro";
import Step from "./Step.astro";
import Steps from "./Steps.astro";
import Tab from "./Tab.astro";
import Tabs from "./Tabs.astro";
import Video from "./Video.astro";

export const components = {
  Callout,
  Flashcard,
  Flashcards,
  FunctionPlot,
  Plotly,
  Quiz,
  Solution,
  Source,
  Step,
  Steps,
  Tab,
  Tabs,
  Video,
};
