<script lang="ts">
  import '../app.css';
  import { onMount } from 'svelte';
  import { dev } from '$app/environment';
  import SparkleTrail from '$lib/components/SparkleTrail.svelte';
  import FirstNoticeModal from '$lib/components/FirstNoticeModal.svelte';
  let { children } = $props();

  onMount(() => {
    // 2本指以上のマルチタッチ操作（ピンチズーム）のみをピンポイントで無効化
    const preventMultiTouch = (e: TouchEvent) => {
      if (e.touches && e.touches.length > 1) {
        e.preventDefault();
      }
    };

    // iOS Safari特有のジェスチャーズームを阻止
    const preventGesture = (e: Event) => e.preventDefault();

    document.addEventListener('touchstart', preventMultiTouch, { passive: false });
    document.addEventListener('touchmove', preventMultiTouch, { passive: false });
    document.addEventListener('gesturestart', preventGesture, { passive: false });
    document.addEventListener('gesturechange', preventGesture, { passive: false });

    return () => {
      document.removeEventListener('touchstart', preventMultiTouch);
      document.removeEventListener('touchmove', preventMultiTouch);
      document.removeEventListener('gesturestart', preventGesture);
      document.removeEventListener('gesturechange', preventGesture);
    };
  });
</script>

<!-- 開発サーバー識別用インジケーター（本番環境ではビルド時に完全に除外されます） -->
{#if dev}
  <div class="fixed top-0 left-0 right-0 z-[99999] bg-gradient-to-r from-amber-400 via-yellow-400 to-orange-400 text-amber-950 text-center font-black text-xs py-1 px-4 border-b-2 border-amber-500 shadow-md flex items-center justify-center gap-2 tracking-wider uppercase select-none pointer-events-none">
    <span>🛠️ LOCAL DEV MODE</span>
    <span class="text-[10px] bg-amber-950/10 px-2 py-0.5 rounded-full font-mono font-bold">ローカル開発環境</span>
  </div>
  <!-- 上部固定バーの重なり防止用スペーサー -->
  <div class="h-7 w-full shrink-0"></div>

  <div class="fixed bottom-3 right-3 z-[99999] pointer-events-none select-none">
    <div class="bg-slate-900/90 text-amber-300 text-xs font-black px-3 py-1.5 rounded-2xl shadow-xl border-2 border-amber-400/80 backdrop-blur-md flex items-center gap-2 tracking-wider">
      <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping inline-block"></span>
      <span>DEV SERVER</span>
    </div>
  </div>
{/if}

<!-- 初回起動時専用の注意事項お知らせモーダル -->
<FirstNoticeModal />

<!-- タップ・スワイプの軌跡にキラキラ星が残るパーティクルエフェクト -->
<SparkleTrail />

<div class="min-h-screen bg-slate-50 text-slate-800 flex flex-col font-sans">
  {@render children()}
</div>
