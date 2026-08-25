import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { PageChrome, StudioMark } from "@/components/page-chrome";
import { PaperDocument } from "@/components/paper-document";
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
    return { title: "Paper" };
  }
  return {
    title: `${agent.paper.title} paper`,
    description: agent.paper.lede,
  };
}

export default async function AgentPaperPage({
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
      <PageChrome
        left={<StudioMark />}
        right={<Link href={`/${agent.slug}/agent`}>View Agent</Link>}
      />
      <div className="paper-shell">
        <PaperDocument
          lede={agent.paper.lede}
          sections={agent.paper.sections}
          title={agent.paper.title}
        />
      </div>
    </main>
  );
}
