// IndexedDB ユーティリティ: 録音音声データの端末内保存・取得・削除

const DB_NAME = 'nomina_audio_db';
const DB_VERSION = 1;
const STORE_NAME = 'recordings';

function openDB(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    if (typeof window === 'undefined' || !('indexedDB' in window)) {
      reject(new Error('IndexedDB is not supported'));
      return;
    }
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onupgradeneeded = (event) => {
      const db = (event.target as IDBOpenDBRequest).result;
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME);
      }
    };

    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

/**
 * 録音音声データ (Blob) を保存
 */
export async function saveAudioRecord(speciesId: string, audioBlob: Blob): Promise<void> {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite');
    const store = tx.objectStore(STORE_NAME);
    const request = store.put(audioBlob, speciesId);

    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
  });
}

/**
 * 録音音声データ (Blob) を取得
 */
export async function getAudioRecord(speciesId: string): Promise<Blob | null> {
  try {
    const db = await openDB();
    return new Promise((resolve) => {
      const tx = db.transaction(STORE_NAME, 'readonly');
      const store = tx.objectStore(STORE_NAME);
      const request = store.get(speciesId);

      request.onsuccess = () => {
        resolve((request.result as Blob) || null);
      };
      request.onerror = () => resolve(null);
    });
  } catch {
    return null;
  }
}

/**
 * 録音音声データを削除
 */
export async function deleteAudioRecord(speciesId: string): Promise<void> {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite');
    const store = tx.objectStore(STORE_NAME);
    const request = store.delete(speciesId);

    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
  });
}

/**
 * 録音済みデータの全種IDリストを取得
 */
export async function getAllRecordedSpeciesIds(): Promise<string[]> {
  try {
    const db = await openDB();
    return new Promise((resolve) => {
      const tx = db.transaction(STORE_NAME, 'readonly');
      const store = tx.objectStore(STORE_NAME);
      const request = store.getAllKeys();

      request.onsuccess = () => {
        resolve((request.result as string[]) || []);
      };
      request.onerror = () => resolve([]);
    });
  } catch {
    return [];
  }
}

/**
 * すべての録音音声データを一括削除
 */
export async function clearAllAudioRecords(): Promise<void> {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite');
    const store = tx.objectStore(STORE_NAME);
    const request = store.clear();

    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
  });
}

export interface AudioRecordItem {
  speciesId: string;
  blob: Blob;
}

/**
 * すべての録音アイテム (speciesId と Blob) のリストを取得
 */
export async function getAllAudioRecordsList(): Promise<AudioRecordItem[]> {
  try {
    const db = await openDB();
    return new Promise((resolve) => {
      const tx = db.transaction(STORE_NAME, 'readonly');
      const store = tx.objectStore(STORE_NAME);
      const reqKeys = store.getAllKeys();
      const reqVals = store.getAll();

      tx.oncomplete = () => {
        const keys = (reqKeys.result as string[]) || [];
        const vals = (reqVals.result as Blob[]) || [];
        const res: AudioRecordItem[] = [];
        for (let i = 0; i < keys.length; i++) {
          if (vals[i]) {
            res.push({ speciesId: keys[i], blob: vals[i] });
          }
        }
        resolve(res);
      };

      tx.onerror = () => resolve([]);
    });
  } catch {
    return [];
  }
}
