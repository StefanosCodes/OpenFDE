import Link from "next/link";
import { agents } from "@/lib/agents";

export default function Home() {
  return (
    <main className="shell shell-center">
      <div className="stack">
        <header className="home-header">
          <h1>OpenFDE.studio</h1>
          <p className="tagline">open source for builders</p>
        </header>
        <nav aria-label="Agents" className="nav-list">
          {agents.map((agent) => (
            <Link className="nav-link" href={`/${agent.slug}`} key={agent.slug}>
              {agent.name}
            </Link>
          ))}
        </nav>
        <footer className="home-footer">
          <Link href="/paper">paper</Link>
          <a
            href="https://github.com/StefanosCodes/OpenFDE"
            rel="noreferrer"
            target="_blank"
          >
            source
          </a>
        </footer>
      </div>
    </main>
  );
}
