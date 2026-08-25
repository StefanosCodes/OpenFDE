import type { Metadata } from "next";
import { IBM_Plex_Sans, Newsreader } from "next/font/google";
import "./globals.css";

const sans = IBM_Plex_Sans({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-sans",
  display: "swap",
});

const serif = Newsreader({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-serif",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "OpenFDE.studio",
    template: "%s · OpenFDE.studio",
  },
  description: "An open-source studio for builders. Pick an agent, read the paper, enter the room.",
  metadataBase: new URL("https://openfde.studio"),
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html className={`${sans.variable} ${serif.variable}`} lang="en">
      <body>{children}</body>
    </html>
  );
}
