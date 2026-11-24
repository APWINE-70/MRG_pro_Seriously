import "./globals.css";

export const metadata = {
  title: "Lanna Power Distribution | แดชบอร์ดวิเคราะห์ความน่าเชื่อถือระบบไฟฟ้าดับ (SAIFI/SAIDI)",
  description: "ระบบแดชบอร์ดสนับสนุนการตัดสินใจของผู้บริหาร บริษัท ล้านนาพาวเวอร์ดิสทริบิวชัน จำกัด",
};

export default function RootLayout({ children }) {
  return (
    <html lang="th" suppressHydrationWarning>
      <body className="antialiased min-h-screen bg-slate-50 text-slate-900" suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
