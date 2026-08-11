/**
 * Cookie utility for managing visible_tier setting (1-3)
 */

export function getVisibleTier(): number {
  if (typeof document === 'undefined') return 1;

  const name = 'visible_tier=';
  const decodedCookie = decodeURIComponent(document.cookie);
  const ca = decodedCookie.split(';');

  for (let i = 0; i < ca.length; i++) {
    let c = ca[i].trim();
    if (c.indexOf(name) === 0) {
      const val = parseInt(c.substring(name.length, c.length), 10);
      if (!isNaN(val) && val >= 1 && val <= 3) {
        return val;
      }
    }
  }

  return 1; // Default: 1 (みんなが知ってる動物だけ表示)
}

export function setVisibleTier(tier: number, days = 365): void {
  if (typeof document === 'undefined') return;

  const validTier = Math.min(Math.max(tier, 1), 3);
  const date = new Date();
  date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
  const expires = `expires=${date.toUTCString()}`;

  document.cookie = `visible_tier=${validTier};${expires};path=/;SameSite=Lax`;
}

export type LangAccent = 'en-US' | 'en-GB' | 'zh-CN' | 'zh-TW' | 'es-ES' | 'es-MX' | 'fr-FR' | 'id-ID';

/**
 * 言語・アクセント設定 (lang_accent) の取得
 */
export function getLangAccent(): LangAccent {
  if (typeof document === 'undefined') return 'en-US';

  const name = 'lang_accent=';
  const decodedCookie = decodeURIComponent(document.cookie);
  const ca = decodedCookie.split(';');

  for (let i = 0; i < ca.length; i++) {
    let c = ca[i].trim();
    if (c.indexOf(name) === 0) {
      const val = c.substring(name.length, c.length) as LangAccent;
      if (['en-US', 'en-GB', 'zh-CN', 'zh-TW', 'es-ES', 'es-MX', 'fr-FR', 'id-ID'].includes(val)) {
        return val;
      }
    }
  }

  return 'en-US'; // Default: American English
}

export function setLangAccent(accent: LangAccent, days = 365): void {
  if (typeof document === 'undefined') return;

  const date = new Date();
  date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
  const expires = `expires=${date.toUTCString()}`;

  document.cookie = `lang_accent=${accent};${expires};path=/;SameSite=Lax`;
}

/**
 * 録音モード (Record Mode) の取得
 */
export function getRecordMode(): boolean {
  if (typeof document === 'undefined') return false;

  const name = 'record_mode=';
  const decodedCookie = decodeURIComponent(document.cookie);
  const ca = decodedCookie.split(';');

  for (let i = 0; i < ca.length; i++) {
    let c = ca[i].trim();
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length) === 'true';
    }
  }

  return false;
}

export function setRecordMode(enabled: boolean, days = 365): void {
  if (typeof document === 'undefined') return;

  const date = new Date();
  date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
  const expires = `expires=${date.toUTCString()}`;

  document.cookie = `record_mode=${enabled ? 'true' : 'false'};${expires};path=/;SameSite=Lax`;
}

/**
 * 上書き許可 (Allow Overwrite) の取得
 */
export function getAllowOverwrite(): boolean {
  if (typeof document === 'undefined') return false;

  const name = 'allow_overwrite=';
  const decodedCookie = decodeURIComponent(document.cookie);
  const ca = decodedCookie.split(';');

  for (let i = 0; i < ca.length; i++) {
    let c = ca[i].trim();
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length) === 'true';
    }
  }

  return false;
}

export function setAllowOverwrite(enabled: boolean, days = 365): void {
  if (typeof document === 'undefined') return;

  const date = new Date();
  date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
  const expires = `expires=${date.toUTCString()}`;

  document.cookie = `allow_overwrite=${enabled ? 'true' : 'false'};${expires};path=/;SameSite=Lax`;
}
