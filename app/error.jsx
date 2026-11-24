"use client";

import React, { useEffect } from "react";
import { AlertTriangle, RefreshCw, Home } from "lucide-react";

export default function Error({ error, reset }) {
  useEffect(() => {
    console.error("Dashboard caught error:", error);
  }, [error]);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-4 text-center">
      <div className="bg-white p-8 rounded-2xl shadow-xl border border-slate-200 max-w-md w-full space-y-4">
        <div className="w-12 h-12 bg-rose-100 text-rose-600 rounded-xl flex items-center justify-center mx-auto">
          <AlertTriangle className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-slate-900">เกิดข้อผิดพลาดในการโหลดหน้าเว็บ</h2>
        <p className="text-xs text-slate-500">
          ระบบตรวจพบข้อขัดข้องชั่วคราวในการประมวลผลข้อมูล กรุณากดปุ่มเพื่อลองใหม่อีกครั้ง
        </p>
        <div className="p-3 bg-slate-50 rounded-lg text-left text-xs font-mono text-slate-600 overflow-x-auto max-h-32">
          {error?.message || "Unknown error"}
        </div>
        <div className="flex gap-2 justify-center pt-2">
          <button
            onClick={() => reset()}
            className="bg-sky-600 hover:bg-sky-700 text-white px-4 py-2 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition"
          >
            <RefreshCw className="w-3.5 h-3.5" /> ลองใหม่อีกครั้ง
          </button>
          <button
            onClick={() => window.location.reload()}
            className="bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition"
          >
            <Home className="w-3.5 h-3.5" /> รีเฟรชหน้าเว็บ
          </button>
        </div>
      </div>
    </div>
  );
}
