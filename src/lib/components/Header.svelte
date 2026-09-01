<script lang="ts">
  import { untrack } from 'svelte';
  import speciesData from '$lib/data/species_mammals.json';
  import XIcon from '$lib/components/XIcon.svelte';

  let { activeTab = $bindable("caniformia"), visibleTier = 1, onTabChange } = $props<{
    activeTab?: string;
    visibleTier?: number;
    onTabChange?: (tab: string) => void;
  }>();

  const iconMap: Record<string, string> = {
    feliformia: "🐱",
    caniformia: "🐶",
    rodentia: "🐿️",
    primates: "🐒",
    cetartiodactyla: "🐮",
    perissodactyla: "🐴",
    chiroptera: "🦇",
    eulipotyphla: "🦔",
    lagomorpha: "🐰",
    proboscidea: "🐘",
    sirenia: "🧜‍♀️",
    cingulata: "🛡️",
    pilosa: "🦥",
    monotremata: "🦆",
    diprotodontia: "🦘",
    dasyuromorphia: "👿",
    didelphimorphia: "🦝",
    peramelemorphia: "🐰",
    microbiotheria: "🐭",
    paucituberculata: "🐭",
    notoryctemorphia: "⛏️",
    pholidota: "🛡️",
    tubulidentata: "🐽",
    hyracoidea: "🐹",
    macroscelidea: "🐭",
    afrosoricida: "🦔",
    dermoptera: "🐿️",
    scandentia: "🐿️"
  };

  let categories = $derived.by(() => {
    return speciesData.categories
      .filter(cat => {
        // このカテゴリー内に Tier 条件を満たす動物が1匹以上いるかチェック
        return cat.families.some(fam =>
          fam.species.some(sp => (sp.tier || 1) <= visibleTier)
        );
      })
      .map(cat => ({
        id: cat.id,
        name: (cat as any).name_short || cat.name_ja,
        icon: iconMap[cat.id] || "🐾"
      }));
  });

  // activeTab が表示可能なカテゴリーに含まれていない場合、最初の表示可能カテゴリーへ自動切り替え
  $effect(() => {
    const cats = categories;
    if (cats.length > 0) {
      untrack(() => {
        const exists = cats.some(c => c.id === activeTab);
        if (!exists) {
          activeTab = cats[0].id;
          onTabChange?.(cats[0].id);
        }
      });
    }
  });
</script>

<header class="w-full bg-gradient-to-r from-amber-400 via-orange-400 to-pink-400 p-4 shadow-lg sticky top-0 z-50">
  <div class="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-3">
    <!-- ロゴとタイトル -->
    <div class="flex items-center justify-between w-full md:w-auto gap-3 shrink-0">
      <a href="/" class="flex items-center gap-3 no-underline group" title="しゅるい選択へ">
        <div class="w-12 h-12 bg-white rounded-2xl p-1 shadow-md group-hover:scale-110 transition-transform overflow-hidden flex items-center justify-center shrink-0">
          <img src="/favicon.png" alt="Nomina Icon" loading="lazy" decoding="async" class="w-full h-full object-contain rounded-xl" />
        </div>
        <div>
          <h1 class="text-2xl sm:text-3xl font-black text-white drop-shadow-md tracking-wider leading-[0.85] flex flex-col justify-center">
            <span>Nomina!</span>
            <span class="text-yellow-200 text-base sm:text-lg font-extrabold mt-0.5">ノミーナ！</span>
          </h1>
          <p class="text-xs text-white/90 font-bold">ほにゅうるい（哺乳類）ずかん</p>
        </div>
      </a>

      <!-- X & 設定アイコンボタン -->
      <div class="flex items-center gap-2 shrink-0">
        <a
          href="https://x.com/nomina2026"
          target="_blank"
          rel="noopener noreferrer"
          title="公式X (@nomina2026)"
          class="w-10 h-10 bg-black/80 hover:bg-black text-white rounded-full flex items-center justify-center transition-all shadow-sm border-2 border-white/40 hover:border-white shrink-0 no-underline"
        >
          <XIcon class="w-4 h-4 text-white" />
        </a>

        <a
          href="/settings"
          title="せってい"
          class="w-10 h-10 bg-white/30 hover:bg-white text-white hover:text-orange-600 rounded-full flex items-center justify-center text-xl font-bold transition-all shadow-sm border-2 border-white/40 hover:border-white shrink-0 no-underline"
        >
          ⚙️
        </a>
      </div>
    </div>

    <!-- 亜目/目（Suborder/Order）カテゴリタブ (横スクロール可能 & マウスオーバーで⇔カーソル) -->
    <nav class="flex items-center gap-2 overflow-x-auto max-w-full p-2 cursor-ew-resize">
      {#each categories as cat}
        <button
          onclick={() => {
            activeTab = cat.id;
            onTabChange?.(cat.id);
          }}
          class="px-3.5 py-2 rounded-2xl font-black text-sm transition-all duration-200 whitespace-nowrap shadow-sm border-2 cursor-pointer shrink-0
            {activeTab === cat.id 
              ? 'bg-white text-orange-600 border-white scale-105 shadow-md' 
              : 'bg-white/30 text-white border-transparent hover:bg-white/40'}"
        >
          <span class="mr-1">{cat.icon}</span>
          {cat.name}
        </button>
      {/each}
    </nav>
  </div>
</header>
