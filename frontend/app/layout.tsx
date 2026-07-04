import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/shared/navbar/navbar";


const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// favicon.ico converted from .svg to .ico based on: https://stackoverflow.com/a/63946938

export const metadata: Metadata = {
  title: "Megical: Triage Engine",
  description: "Ease medical workflow with an intuitive and AI-integrated web app.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Navbar/>
        <main style={{width: "100%", height: "100%"}}>
        {children}
        </main>
      </body>
    </html>
  );
}
