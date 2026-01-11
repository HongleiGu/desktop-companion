"use client"

import './globals.css';
import { ReactNode } from "react";
import { QueryClient, QueryClientProvider } from "react-query";
import Modals from '../components/Modals';

const queryClient = new QueryClient();

// export const metadata = {
//   title: '桌面伴侣',
//   description: 'Next.js + Tauri Desktop Companion'
// };

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>
        <QueryClientProvider client={queryClient}>
          {children}
        </QueryClientProvider>

        {/* ✅ Modals read from global state */}
        <Modals />
      </body>
    </html>
  );
}
