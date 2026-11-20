// The World in One Day — 20 November 2026
//
// This program is the delivery step for the front-page image. The artwork
// itself is rendered ahead of time by gen_image.py and stored next to this
// file as entry.png; all this program does is place an exact copy of that
// file where the harness expects the finished entry to be.
//
// It uses only the Node standard library, makes no network calls, and
// always produces the same bytes: the image is read in full and written
// out untouched, so repeated runs are byte-identical.

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// Resolve the folder this file lives in, so the program works no matter
// which directory it is launched from.
const here = dirname(fileURLToPath(import.meta.url));
const sourceImage = join(here, "entry.png");

// The harness tells us where the finished entry belongs through
// MAKEFUN_OUTPUT_DIR; fall back to /output when it is not set.
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const destination = resolve(outputDir, "entry.png");

function deliverEntry(): void {
  if (!existsSync(sourceImage)) {
    throw new Error(`entry image missing: ${sourceImage} (run gen_image.py first)`);
  }

  // Read the whole image into memory, then write it out verbatim.
  // No decoding or re-encoding happens, so the bytes cannot drift.
  const imageBytes = readFileSync(sourceImage);

  mkdirSync(outputDir, { recursive: true });
  writeFileSync(destination, imageBytes);

  // Read the copy back and confirm it matches what we wrote, so a
  // truncated or partial write can never pass silently.
  const writtenBack = readFileSync(destination);
  if (writtenBack.length !== imageBytes.length) {
    throw new Error(
      `delivery mismatch: wrote ${imageBytes.length} bytes, ` +
      `found ${writtenBack.length} bytes at ${destination}`,
    );
  }

  console.log(`entry.png (${imageBytes.length} bytes) -> ${destination}`);
}

deliverEntry();
