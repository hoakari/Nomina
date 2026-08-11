<script lang="ts">
  import { onMount } from 'svelte';
  import Header from '$lib/components/Header.svelte';
  import SpeciesCard from '$lib/components/SpeciesCard.svelte';
  import speciesData from '$lib/data/species.json';
  import { getVisibleTier } from '$lib/utils/cookies';

  let activeTab = $state('feliformia');
  let visibleTier = $state(1);

  onMount(() => {
    visibleTier = getVisibleTier();
  });

  // 選択されたカテゴリ＆Tierに応じたフィルタリング済みデータ
  let currentCategory = $derived.by(() => {
    const rawCat = speciesData.categories.find(c => c.id === activeTab) || speciesData.categories[0];
    const filteredFamilies = rawCat.families.map(fam => {
      const filteredSpecies = fam.species.filter(sp => (sp.tier || 1) <= visibleTier);
      return {
        ...fam,
        species: filteredSpecies
      };
    }).filter(fam => fam.species.length > 0);

    return {
      ...rawCat,
      families: filteredFamilies
    };
  });
</script>

<svelte:head>
  <title>ほにゅうるい（哺乳類）図鑑 | Nomina!</title>
  <meta name="description" content="ほにゅうるい（哺乳類）の生きもの図鑑。イラストをタップして名前を楽しく学べます。" />
</svelte:head>

<!-- トップの種類選択へ戻るミニバー -->
<div class="bg-amber-100/80 border-b border-amber-200 px-4 py-1.5 text-xs font-bold text-amber-800 flex items-center justify-between">
  <a
    href="/"
    class="inline-flex items-center gap-1 text-amber-800 hover:text-orange-600 transition-colors no-underline font-extrabold"
  >
    <span>🏠</span>
    <span>しゅるいせんたくへもどる</span>
  </a>
  <span class="text-[11px] text-amber-700/80">ほにゅうるい（哺乳類）ずかん</span>
</div>

<!-- ヘッダー (亜目タブ切替) -->
<Header bind:activeTab visibleTier={visibleTier} />

<!-- メインコンテンツエリア -->
<main class="flex-1 max-w-6xl w-full mx-auto p-4 sm:p-6 space-y-8">
  <!-- 亜目（Suborder）の案内カード -->
  <section class="bg-gradient-to-r from-amber-100 via-orange-50 to-pink-100 p-5 rounded-3xl border-2 border-amber-200 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
    <div>
      <div class="inline-flex items-center gap-1.5 px-3 py-1 bg-gradient-to-r from-orange-500 to-pink-500 text-white font-extrabold text-xs rounded-full shadow-2xs">
        <span>🐾 生物分類グループ</span>
      </div>
      <h2 class="text-2xl sm:text-3xl font-black text-slate-800 mt-2 flex items-baseline gap-2 flex-wrap">
        <span>{(currentCategory as any).name_kids || currentCategory.name_ja}</span>
        <span class="text-sm sm:text-base font-extrabold text-amber-700/80 font-sans">（{currentCategory.name_ja}）</span>
      </h2>
      <p class="text-xs text-slate-600 font-bold mt-1">
        学名分類グループ: <span class="font-mono text-amber-700">{currentCategory.name_en}</span>
      </p>
    </div>
    
    <div class="flex flex-col sm:items-end gap-2 shrink-0">
      <div class="text-right text-xs bg-white/90 px-4 py-2.5 rounded-2xl border border-amber-200 shadow-2xs">
        <p class="font-extrabold text-amber-800 text-sm">💡 タップしてあそぼう！</p>
        <p class="text-slate-600 font-medium mt-0.5">カードを押すと、なまえを教えてくれるよ</p>
      </div>

      <a
        href="/settings"
        class="inline-flex items-center gap-1 text-xs font-black text-amber-800 hover:text-orange-600 bg-amber-200/60 hover:bg-amber-200 px-3 py-1.5 rounded-xl border border-amber-300 transition-all no-underline"
      >
        <span>⚙️</span>
        <span>掲載数の設定（Tier {visibleTier}）</span>
      </a>
    </div>
  </section>

  <!-- 科（Family）ごとのセクション表示 -->
  {#each currentCategory.families as family}
    <section class="space-y-4">
      <div class="flex items-center gap-3 border-b-3 border-amber-300 pb-2.5">
        <span class="text-2xl">🏷️</span>
        <h3 class="text-xl sm:text-2xl font-black text-slate-800">
          {family.name_ja} <span class="text-sm font-bold text-amber-700/70 font-mono">({family.name_en})</span>
        </h3>
      </div>

      <!-- 種カードのグリッド表示 -->
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
        {#each family.species as speciesItem}
          <SpeciesCard species={speciesItem} />
        {/each}
      </div>
    </section>
  {/each}
</main>

<!-- フッター -->
<footer class="w-full bg-slate-200/60 border-t border-slate-300 py-6 mt-12 text-center text-xs text-slate-500 font-bold">
  <div class="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
    <p>© 2026 Nomina! (ノミーナ！) - 子どもえいご＆いきものずかん</p>
    <div class="flex items-center gap-4">
      <a href="/" class="hover:underline">しゅるい選択</a>
      <a href="/settings" class="hover:underline">設定</a>
    </div>
  </div>
</footer>
