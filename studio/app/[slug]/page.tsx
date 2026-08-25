import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { PageChrome, StudioMark } from "@/components/page-chrome";
import { agents, getAgent } from "@/lib/agents";

type AgentParams = Promise<{ slug: string }>;

export const dynamicParams = false;

export function generateStaticParams() {
  return agents.map((agent) => ({ slug: agent.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: AgentParams;
}): Promise<Metadata> {
  const { slug } = await params;
  const agent = getAgent(slug);
  if (!agent) {
    return { title: "OpenFDE.studio" };
  }
  return {
    title: agent.name,
    description: agent.tagline,
  };
}

export default async function AgentDoorwayPage({
  params,
}: {
  params: AgentParams;
}) {
  const { slug } = await params;
  const agent = getAgent(slug);
  if (!agent) {
    notFound();
  }

  return (
    <main className="shell">
      <PageChrome left={<StudioMark />} />
      <div className="shell-center">
        <div className="stack">
          <header className="doorway-header">
            <h1>{agent.name}</h1>
            <p className="tagline">{agent.tagline}</p>
          </header>
          <nav aria-label="Agent" className="action-list">
            <Link className="action-link" href={`/${agent.slug}/paper`}>
              View Paper
            </Link>
            <Link className="action-link" href={`/${agent.slug}/agent`}>
              View Agent
            </Link>
          </nav>
        </div>
      </div>
    </main>
  );
}
