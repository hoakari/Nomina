<script lang="ts">
  import { onMount } from 'svelte';
  import XIcon from '$lib/components/XIcon.svelte';

  let showModal = $state(false);

  const NOTICE_KEY = 'nomina_notice_accepted_v1';

  onMount(() => {
    try {
      const accepted = localStorage.getItem(NOTICE_KEY);
      if (!accepted) {
        showModal = true;
      }
    } catch {
      showModal = true;
    }
  });

  function handleAccept() {
    try {
      localStorage.setItem(NOTICE_KEY, 'true');
      document.cookie = `${NOTICE_KEY}=true; path=/; max-age=31536000; SameSite=Lax`;
    } catch {}
    showModal = false;
  }
</script>

{#if showModal}
  <!-- モーダル背景バックドロップ -->
  <div class="fixed inset-0 bg-stone-900/60 backdrop-blur-sm z-[10000] flex items-center justify-center p-3 sm:p-4 transition-all duration-300">
    <!-- モーダル本体 (画面高さの88vh以内に納めてスクロール対応) -->
    <div class="bg-white/95 backdrop-blur-md rounded-3xl max-w-lg w-full max-h-[88vh] p-5 sm:p-7 shadow-2xl border-4 border-amber-300 flex flex-col justify-between relative overflow-hidden animate-in fade-in zoom-in-95 duration-200">
      
      <!-- 背景装飾アイコン -->
      <div class="absolute -right-8 -bottom-8 text-8xl opacity-10 pointer-events-none select-none">
        🐾
      </div>

      <!-- ヘッダー (固定) -->
      <div class="flex items-center gap-3 border-b border-amber-100 pb-3 shrink-0">
        <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-2xl bg-gradient-to-br from-amber-400 to-orange-500 text-white flex items-center justify-center text-xl sm:text-2xl shadow-md shrink-0">
          💡
        </div>
        <div>
          <h2 class="text-lg sm:text-2xl font-black text-amber-900 leading-tight">
            ご利用前の大切なお知らせ
          </h2>
          <p class="text-xs font-bold text-amber-700 mt-0.5">
            当サイトをご利用いただくにあたって
          </p>
        </div>
      </div>

      <!-- ご注意・説明項目 (スクロール可能領域) -->
      <div class="flex flex-col gap-3 text-stone-700 text-xs sm:text-sm leading-relaxed font-medium overflow-y-auto my-3 pr-1 shrink">
        
        <!-- 1. 個人サイト -->
        <div class="flex items-start gap-2.5 sm:gap-3 bg-amber-50/70 p-3 sm:p-3.5 rounded-2xl border border-amber-200/60 shrink-0">
          <span class="text-lg sm:text-xl shrink-0">🏠</span>
          <div class="w-full">
            <span class="font-bold text-amber-900 block text-xs mb-0.5">個人運営の教育用Webアプリです</span>
            本サービスは個人が開発・運営している非公式の教育・図鑑Webアプリケーションです。
            <div class="mt-1.5 pt-1.5 border-t border-amber-200/50 flex items-center justify-between">
              <span class="text-[11px] font-bold text-amber-800">お問合せ・公式X：</span>
              <a
                href="https://x.com/nomina2026"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center gap-1 px-2.5 py-0.5 bg-black text-white text-[11px] font-bold rounded-full hover:bg-stone-800 transition-all no-underline"
              >
                <XIcon class="w-3 h-3 text-white" />
                <span>@nomina2026</span>
              </a>
            </div>
          </div>
        </div>

        <!-- 2. 内容の正確性について -->
        <div class="flex items-start gap-2.5 sm:gap-3 bg-orange-50/70 p-3 sm:p-3.5 rounded-2xl border border-orange-200/60 shrink-0">
          <span class="text-lg sm:text-xl shrink-0">🔬</span>
          <div>
            <span class="font-bold text-orange-900 block text-xs mb-0.5">掲載情報について</span>
            可能な限り最新の学術情報に基づいて制作しておりますが、生物学的分類や外国語の表示・発音等に一部誤りや例外が含まれる可能性がございます。
          </div>
        </div>

        <!-- 3. ローカル保存 -->
        <div class="flex items-start gap-2.5 sm:gap-3 bg-emerald-50/70 p-3 sm:p-3.5 rounded-2xl border border-emerald-200/60 shrink-0">
          <span class="text-lg sm:text-xl shrink-0">💾</span>
          <div>
            <span class="font-bold text-emerald-900 block text-xs mb-0.5">データは端末内にのみ保存されます</span>
            お気に入りや各種設定、録音された音声データ等はお使いの端末（ブラウザ）内にのみローカル保存され、外部サーバーへ自動送信・収集されることは一切ございません。
          </div>
        </div>

        <!-- 4. Cookie & IndexedDB -->
        <div class="flex items-start gap-2.5 sm:gap-3 bg-sky-50/70 p-3 sm:p-3.5 rounded-2xl border border-sky-200/60 shrink-0">
          <span class="text-lg sm:text-xl shrink-0">🍪</span>
          <div>
            <span class="font-bold text-sky-900 block text-xs mb-0.5">CookieおよびIndexedDBの使用ポリシー</span>
            言語・掲載数の設定保持および録音データの端末内保存（IndexedDB）のために使用しています。アクセス解析等のサードパーティCookieは一切使用しておりません。<br />
            <span class="text-sky-950 font-bold text-[11px] block mt-1 pt-1 border-t border-sky-200/60">
              ⚠️ ブラウザの設定、履歴クリア、プライベートモード利用等により、保存された録音音声や設定データが勝手に削除される場合がございますのでご注意ください。
            </span>
          </div>
        </div>

      </div>

      <!-- 同意ボタン (下部固定) -->
      <div class="pt-2 shrink-0">
        <button
          onclick={handleAccept}
          class="w-full py-3.5 sm:py-4 bg-gradient-to-r from-orange-500 via-amber-500 to-amber-600 hover:from-orange-600 hover:to-amber-700 text-white font-black text-base sm:text-lg rounded-2xl shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-95 transition-all cursor-pointer flex items-center justify-center gap-2 border-b-4 border-amber-700"
        >
          <span>確認して図鑑をはじめる</span>
          <span class="text-xl">✨</span>
        </button>
      </div>

    </div>
  </div>
{/if}
