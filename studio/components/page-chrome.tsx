import Link from "next/link";
import type { ReactNode } from "react";

type PageChromeProps = {
  left: ReactNode;
  right?: ReactNode;
};

export function PageChrome({ left, right }: PageChromeProps) {
  return (
    <header className="chrome">
      <div className="chrome-left">{left}</div>
      {right ? <div className="chrome-right">{right}</div> : null}
    </header>
  );
}

export function StudioMark() {
  return (
    <Link className="mark" href="/">
      OpenFDE.studio
    </Link>
  );
}
