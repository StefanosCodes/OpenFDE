import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { AgentWorkspace } from "@/components/agent-workspace";
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
    return { title: "Agent" };
  }
  return {
    title: agent.name,
    description: agent.tagline,
  };
}

export default async function AgentRoomPage({
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
    <main className="workspace-page">
      <PageChrome
        left={<StudioMark />}
        right={<Link href={`/${agent.slug}/paper`}>View Paper</Link>}
      />
      <AgentWorkspace name={agent.name} tagline={agent.tagline} />
    </main>
  );
}
