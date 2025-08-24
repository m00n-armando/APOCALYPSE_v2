// --- src/app/api/render/route.ts (vFINAL - ANTI HANTU) ---
import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import fs from 'fs';
import path from 'path';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    // Kita ambil SEMUA yang kita butuhkan dari UI, termasuk direktori
    const { jobList, outputDirectory } = body;

    // ----- [ KEAJAIBAN FINAL TERJADI DI SINI ] -----

    // 1. Siapkan 'Memo Resmi' seperti sebelumnya
    const factoryConfig = {
        output_gallery_path: outputDirectory,
        api_url: "url",
        bearer_token: "token" // JANGAN LUPA GANTI INI
    };
    
    // Tulis memo dan surat perintah
    const configFilePath = path.resolve(outputDirectory, 'factory_config.json');
    const jobFilePath = path.resolve(outputDirectory, 'job_order.json');
    fs.writeFileSync(configFilePath, JSON.stringify(factoryConfig, null, 2));
    fs.writeFileSync(jobFilePath, jobList);

    console.log(`[RESEPSIONIS] >>> Memo Resmi ditulis di: ${configFilePath}`);
    console.log(`[RESEPSIONIS] >>> Surat perintah ditulis di: ${jobFilePath}`);

    // 2. Siapkan alamat file script Python-nya
    const scriptPath = path.resolve(outputDirectory, 'run_apocalypse_factory7.py');

    // 3. === [ INI DIA KUNCI UTAMANYA! ] ===
    // Kita paksa semua backslash (\) menjadi forward slash (/) SEBELUM dilempar ke 'exec'.
    // Ini membuat alamatnya 100% aman dan tidak ambigu untuk shell mana pun.
    const cleanScriptPath = scriptPath.replace(/\\/g, '/');
    const cleanConfigPath = configFilePath.replace(/\\/g, '/');
    const cleanJobPath = jobFilePath.replace(/\\/g, '/');

    // 4. Panggil mandornya dengan alamat yang SUDAH BERSIH dan DIJAMIN AMAN.
    // Setiap path sekarang dibungkus dengan tanda petik ganda untuk menangani spasi.
    const command = `python "${cleanScriptPath}" "${cleanConfigPath}" "${cleanJobPath}"`;
    
    console.log(`[RESEPSIONIS] >>> Mengirim Perintah Final: ${command}`);

    // Eksekusi seperti biasa
    exec(command, (error, stdout, stderr) => {
      if (error) { console.error(`[REAKTOR ERROR]: ${error}`); return; }
      if (stderr) { console.error(`[REAKTOR STDOUT_ERROR]: ${stderr}`); return; }
      console.log(`[REAKTOR OUTPUT]: ${stdout}`);
    });

    return NextResponse.json({ message: "Job successfully sent to the (finally) working factory!" }, { status: 200 });

  } catch (error) {
    console.error('[API ERROR]:', error);
    return NextResponse.json({ error: "Failed to process request" }, { status: 500 });
  }

}
