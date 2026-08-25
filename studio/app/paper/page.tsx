import type { Metadata } from "next";
import { PageChrome, StudioMark } from "@/components/page-chrome";
import { PaperDocument } from "@/components/paper-document";
import { studioPaper } from "@/lib/agents";

export const metadata: Metadata = {
  title: "Paper",
  description: studioPaper.lede,
};

export default function StudioPaperPage() {
  return (
    <main className="shell">
      <PageChrome left={<StudioMark />} />
      <div className="paper-shell">
        <PaperDocument
          lede={studioPaper.lede}
          sections={studioPaper.sections}
          title={studioPaper.title}
        />
      </div>
    </main>
  );
}
