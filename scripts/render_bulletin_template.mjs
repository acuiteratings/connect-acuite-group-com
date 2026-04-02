import fs from "node:fs/promises";
import { chromium } from "playwright";

function readArg(flag) {
  const index = process.argv.indexOf(flag);
  if (index === -1 || index + 1 >= process.argv.length) {
    return "";
  }
  return process.argv[index + 1];
}

async function main() {
  const templatePath = readArg("--template");
  const name = readArg("--name");
  const date = readArg("--date");
  const photoUrl = readArg("--photo-url");
  const outputPath = readArg("--output");

  if (!templatePath || !name || !date || !outputPath) {
    throw new Error("Missing required arguments.");
  }

  let html = await fs.readFile(templatePath, "utf8");
  html = html.replaceAll("{{NAME}}", name);
  html = html.replaceAll("{{DATE}}", date);
  html = html.replaceAll("{{PHOTO_URL}}", photoUrl || "");

  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1200, height: 675 } });
    await page.setContent(html, { waitUntil: "networkidle" });
    await page.screenshot({ path: outputPath, type: "png" });
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error.message || String(error));
  process.exit(1);
});
