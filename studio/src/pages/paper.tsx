import { PageChrome, StudioMark } from "../components/page-chrome";
import { PaperDocument } from "../components/paper-document";
import { studioPaper } from "../lib/agents";
import { useDocumentTitle } from "../lib/use-document-title";

export function StudioPaperPage() {
  useDocumentTitle("Paper");

  return (
    <main className="shell">
      <PageChrome left={<StudioMark />} />
      <div className="paper-shell">
        <PaperDocument {...studioPaper} />
      </div>
    </main>
  );
}
