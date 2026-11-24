import "./globals.css";

export const metadata = {
  title: "Lanna Power Distribution | แดชบอร์ดวิเคราะห์ความน่าเชื่อถือระบบไฟฟ้าดับ (SAIFI/SAIDI)",
  description: "ระบบแดชบอร์ดสนับสนุนการตัดสินใจของผู้บริหาร บริษัท ล้านนาพาวเวอร์ดิสทริบิวชัน จำกัด",
};

export default function RootLayout({ children }) {
  return (
    <html lang="th">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
      </head>
      <body className="font-sans antialiased min-h-screen bg-slate-50 text-slate-900">
        {children}
      </body>
    </html>
  );
}
