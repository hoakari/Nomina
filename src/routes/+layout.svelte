<script lang="ts">
  import '../app.css';
  import { onMount } from 'svelte';
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

<!-- 初回起動時専用の注意事項お知らせモーダル -->
<FirstNoticeModal />

<!-- タップ・スワイプの軌跡にキラキラ星が残るパーティクルエフェクト -->
<SparkleTrail />

<div class="min-h-screen bg-slate-50 text-slate-800 flex flex-col font-sans">
  {@render children()}
</div>
