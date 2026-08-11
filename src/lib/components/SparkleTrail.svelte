<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';

  interface Particle {
    id: number;
    x: number;
    y: number;
    size: number;
    color: string;
    symbol: string;
    vx: number;
    vy: number;
    opacity: number;
    rotation: number;
    scale: number;
  }

  let particles = $state<Particle[]>([]);
  let nextId = 0;
  const symbols = ['✨', '⭐', '🌟', '💫', '💖', '💛', '🌸', '❄️'];
  const colors = ['#f59e0b', '#ec4899', '#8b5cf6', '#3b82f6', '#10b981', '#f43f5e', '#fbbf24'];

  const isSettingsPage = $derived($page.url.pathname === '/settings');

  function createParticle(x: number, y: number) {
    if (isSettingsPage) return;

    const symbol = symbols[Math.floor(Math.random() * symbols.length)];
    const color = colors[Math.floor(Math.random() * colors.length)];
    const angle = Math.random() * Math.PI * 2;
    const speed = 1.2 + Math.random() * 3;

    const p: Particle = {
      id: nextId++,
      x,
      y,
      size: 16 + Math.random() * 18,
      color,
      symbol,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed - 1.2, // ふわっと昇る
      opacity: 1,
      rotation: Math.random() * 360,
      scale: 1
    };

    particles = [...particles.slice(-45), p];
  }

  function handlePointerMove(e: PointerEvent) {
    if (isSettingsPage) return;
    if (Math.random() < 0.65) {
      createParticle(e.clientX, e.clientY);
    }
  }

  function handlePointerDown(e: PointerEvent) {
    if (isSettingsPage) return;
    for (let i = 0; i < 5; i++) {
      createParticle(e.clientX, e.clientY);
    }
  }

  onMount(() => {
    let animFrame: number;

    const update = () => {
      particles = particles
        .map(p => ({
          ...p,
          x: p.x + p.vx,
          y: p.y + p.vy,
          vy: p.vy + 0.08,
          opacity: p.opacity - 0.035,
          scale: p.scale * 0.96,
          rotation: p.rotation + 3
        }))
        .filter(p => p.opacity > 0);

      animFrame = requestAnimationFrame(update);
    };

    update();

    window.addEventListener('pointermove', handlePointerMove);
    window.addEventListener('pointerdown', handlePointerDown);

    return () => {
      cancelAnimationFrame(animFrame);
      window.removeEventListener('pointermove', handlePointerMove);
      window.removeEventListener('pointerdown', handlePointerDown);
    };
  });
</script>

{#if !isSettingsPage}
  <div class="fixed inset-0 pointer-events-none z-[9999] overflow-hidden">
    {#each particles as p (p.id)}
      <div
        class="absolute select-none will-change-transform"
        style="
          left: {p.x}px;
          top: {p.y}px;
          font-size: {p.size}px;
          opacity: {p.opacity};
          transform: translate(-50%, -50%) rotate({p.rotation}deg) scale({p.scale});
          color: {p.color};
          filter: drop-shadow(0 2px 4px rgba(0,0,0,0.15));
        "
      >
        {p.symbol}
      </div>
    {/each}
  </div>
{/if}
