import fs from 'fs';
import path from 'path';
import csv from 'csv-parser';

const DATA_DIR = path.join(__dirname, '../../data/master_clean');

export async function loadCSV(filename: string): Promise<any[]> {
  return new Promise((resolve, reject) => {
    const results: any[] = [];
    const filePath = path.join(DATA_DIR, filename);

    if (!fs.existsSync(filePath)) {
      reject(new Error(`CSV file not found: ${filename}`));
      return;
    }

    fs.createReadStream(filePath)
      .pipe(csv())
      .on('data', (data) => results.push(data))
      .on('end', () => resolve(results))
      .on('error', (error) => reject(error));
  });
}

export function normalizeString(value: any): string {
  if (value === null || value === undefined) return '';
  return String(value).trim();
}

export function toFloat(value: any): number | null {
  if (value === null || value === undefined) return null;
  if (typeof value === 'number') return value;
  if (typeof value === 'string') {
    const s = value.trim();
    if (s === '' || s === '-') return null;
    const num = parseFloat(s);
    return isNaN(num) ? null : num;
  }
  return null;
}
