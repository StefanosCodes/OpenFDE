import type { PaperSection } from "@/lib/agents";

type PaperDocumentProps = {
  title: string;
  lede: string;
  sections: readonly PaperSection[];
};

export function PaperDocument({ title, lede, sections }: PaperDocumentProps) {
  return (
    <article className="paper">
      <h1>{title}</h1>
      <p className="lede">{lede}</p>
      {sections.map((section) => (
        <section key={section.heading}>
          <h2>{section.heading}</h2>
          {section.paragraphs.map((paragraph) => (
            <p key={paragraph}>{paragraph}</p>
          ))}
        </section>
      ))}
    </article>
  );
}
