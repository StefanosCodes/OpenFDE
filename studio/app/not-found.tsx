import Link from "next/link";

export default function NotFound() {
  return (
    <main className="shell shell-center">
      <div className="stack not-found">
        <header className="home-header">
          <h1>OpenFDE.studio</h1>
          <p className="tagline">this page is not an agent.</p>
        </header>
        <Link className="action-link" href="/">
          studio
        </Link>
      </div>
    </main>
  );
}
