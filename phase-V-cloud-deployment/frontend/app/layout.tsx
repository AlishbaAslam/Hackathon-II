import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "../contexts/AuthContext";
import ChatWidget from "../components/chat/ChatWidget";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "TodoFlow - Streamline Your Productivity",
  description: "A modern task management solution designed to help you organize, prioritize, and accomplish your goals with ease.",
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={`${inter.className} antialiased`}>
        <AuthProvider>
          <div className="min-h-screen bg-gradient-to-br from-[--background-gradient-start] to-[--background-gradient-end]">
            {children}
            <ChatWidget />
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}