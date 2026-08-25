"use client";

import { FormEvent, useState } from "react";

type Message = {
  role: "user" | "agent";
  text: string;
};

type AgentWorkspaceProps = {
  name: string;
  tagline: string;
};

export function AgentWorkspace({ name, tagline }: AgentWorkspaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [draft, setDraft] = useState("");

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const text = draft.trim();
    if (!text) {
      return;
    }
    setDraft("");
    setMessages((current) => [
      ...current,
      { role: "user", text },
      {
        role: "agent",
        text: `${name} is present. This room is the destination; the model runtime is not bound yet.`,
      },
    ]);
  }

  return (
    <div className="workspace">
      {messages.length === 0 ? (
        <div className="workspace-empty">
          <h1 className="workspace-title">{name}</h1>
          <p className="lede">{tagline}</p>
        </div>
      ) : (
        <ol className="transcript">
          {messages.map((message, index) => (
            <li className={`turn turn-${message.role}`} key={`${message.role}-${index}`}>
              <span className="turn-role">
                {message.role === "user" ? "you" : name}
              </span>
              <p>{message.text}</p>
            </li>
          ))}
        </ol>
      )}
      <form className="composer" onSubmit={onSubmit}>
        <label className="sr-only" htmlFor="agent-draft">
          Message {name}
        </label>
        <input
          autoComplete="off"
          id="agent-draft"
          onChange={(event) => setDraft(event.target.value)}
          placeholder={`Message ${name}`}
          value={draft}
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
