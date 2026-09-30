// Run with the bundled sharp dependency to prepare generated editorial photographs.
const fs = require('node:fs');
const path = require('node:path');
const sharp = require(process.env.SHARP_PATH || 'sharp');
const root = path.resolve(__dirname, '..');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'assets/service-photos/prompts.json'), 'utf8'));
(async () => {
  for (const photo of manifest.images) {
    for (const width of [480, 960]) {
      await sharp(path.join(root, 'assets/service-photos', photo.slug + '.png'))
        .resize({width}).webp({quality:82})
        .toFile(path.join(root, 'static', `service-${photo.slug}-${width}.webp`));
    }
  }
  console.log('Prepared responsive WebP images for all seven services.');
})().catch(error => { console.error(error); process.exitCode = 1; });
