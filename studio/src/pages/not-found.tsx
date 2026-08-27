import { Link } from "react-router-dom";

import { useDocumentTitle } from "../lib/use-document-title";

export function NotFoundPage() {
  useDocumentTitle("Not found");

  return (
    <main className="shell shell-center">
      <div className="stack not-found">
        <header className="home-header">
          <h1>OpenFDE.studio</h1>
          <p className="tagline">this route is not an agent project.</p>
        </header>
        <Link className="action-link" to="/">
          Return to the studio
        </Link>
      </div>
    </main>
  );
}
