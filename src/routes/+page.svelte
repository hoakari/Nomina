<script lang="ts">
  import XIcon from '$lib/components/XIcon.svelte';
  let toastMessage = $state<string | null>(null);

  interface CategoryItem {
    id: string;
    name_hiragana: string;
    name_kanji: string;
    icon: string;
    desc: string;
    bg_gradient: string;
    border_color: string;
    href?: string;
    is_ready: boolean;
    species_count_text?: string;
  }

  const mainCategories: CategoryItem[] = [
    {
      id: 'mammals',
      name_hiragana: 'ほにゅうるい',
      name_kanji: '哺乳類',
      icon: '🦁',
      desc: 'イヌ、ネコ、ゾウ、ライオン、クジラなど、おっぱいをのんでそだつなかま！',
      bg_gradient: 'from-amber-100 via-orange-100 to-yellow-100 hover:from-amber-200 hover:to-orange-200',
      border_color: 'border-amber-400',
      href: '/mammals',
      is_ready: true,
      species_count_text: '全217種 収録中！'
    },
    {
      id: 'birds',
      name_hiragana: 'ちょうるい',
      name_kanji: '鳥類',
      icon: '🐦',
      desc: 'ペンギン、ワシ、フクロウ、インコなど、はねがあって空を飛ぶなかま！',
      bg_gradient: 'from-sky-50 via-blue-100 to-indigo-50 hover:from-sky-100 hover:to-blue-150',
      border_color: 'border-sky-300',
      is_ready: false
    },
    {
      id: 'reptiles',
      name_hiragana: 'はちゅうるい',
      name_kanji: '爬虫類',
      icon: '🦎',
      desc: 'トカゲ、カメ、ヘビ、ワニなど、うろこを持ったかっこいいなかま！',
      bg_gradient: 'from-emerald-50 via-teal-100 to-green-50 hover:from-emerald-100 hover:to-teal-150',
      border_color: 'border-emerald-300',
      is_ready: false
    },
    {
      id: 'amphibians',
      name_hiragana: 'りょうせいるい',
      name_kanji: '両生類',
      icon: '🐸',
      desc: 'カエル、イモリ、サンショウウオなど、水と陸のりょうほうでくらすなかま！',
      bg_gradient: 'from-lime-50 via-green-100 to-emerald-50 hover:from-lime-100 hover:to-green-150',
      border_color: 'border-lime-300',
      is_ready: false
    },
    {
      id: 'fishes',
      name_hiragana: 'ぎょるい',
      name_kanji: '魚類',
      icon: '🐟',
      desc: 'マグロ、サメ、クマノミ、チョウチョウウオなど、海や川をすいすい泳ぐなかま！',
      bg_gradient: 'from-cyan-50 via-sky-100 to-blue-100 hover:from-cyan-100 hover:to-sky-150',
      border_color: 'border-cyan-300',
      is_ready: false
    },
    {
      id: 'foods',
      name_hiragana: 'やさい・くだもの',
      name_kanji: '農作物',
      icon: '🍎',
      desc: 'リンゴ、イチゴ、バナナ、トマト、ニンジンなど、畑や木からとれるおいしい仲間！',
      bg_gradient: 'from-rose-50 via-pink-100 to-red-50 hover:from-rose-100 hover:to-pink-150',
      border_color: 'border-pink-300',
      is_ready: false
    }
  ];

  function handleComingSoon(catName: string) {
    toastMessage = `🚧 「${catName}」は、ただいま準備中だよ！楽しみにしてね！`;
    setTimeout(() => {
      toastMessage = null;
    }, 3500);
  }
</script>

<svelte:head>
  <title>Nomina（ノミーナ！）| しゅるい選択・子どもいきものずかん</title>
  <meta name="description" content="あそびたい図鑑の種類をえらんでね！哺乳類、鳥類、爬虫類、魚類など、楽しく学べる子ども英語いきもの図鑑。" />
</svelte:head>

<div class="min-h-screen bg-gradient-to-b from-amber-50 via-orange-50/40 to-yellow-50 flex flex-col justify-between p-4 sm:p-8">
  <!-- ヘッダーエリア -->
  <header class="max-w-5xl mx-auto w-full flex items-center justify-between py-4">
    <div class="flex items-center gap-3">
      <div class="w-12 h-12 bg-white rounded-2xl p-1 shadow-md border-2 border-amber-200 flex items-center justify-center shrink-0 overflow-hidden">
        <img src="/favicon.png" alt="Nomina Icon" class="w-full h-full object-contain rounded-xl" />
      </div>
      <div>
        <h1 class="text-2xl sm:text-4xl font-black text-slate-800 tracking-tight">
          Nomina! <span class="text-xs sm:text-sm font-extrabold text-orange-600 bg-orange-100 px-2.5 py-0.5 rounded-full border border-orange-200">ノミーナ！</span>
        </h1>
        <p class="text-xs text-stone-500 font-bold">子ども英語＆いきもの・たべもの図鑑</p>
      </div>
    </div>

    <div class="flex items-center gap-2">
      <a
        href="https://x.com/nomina2026"
        target="_blank"
        rel="noopener noreferrer"
        class="inline-flex items-center gap-1.5 px-3.5 py-2 bg-black hover:bg-stone-800 text-white font-black text-xs sm:text-sm rounded-2xl shadow-sm transition-all no-underline shrink-0"
        title="公式X (@nomina2026)"
      >
        <XIcon class="w-4 h-4 text-white" />
        <span class="hidden sm:inline">公式X</span>
      </a>

      <a
        href="/settings"
        class="inline-flex items-center gap-1.5 px-4 py-2 bg-white text-stone-700 font-black text-xs sm:text-sm rounded-2xl shadow-sm border-2 border-amber-200 hover:bg-amber-100 transition-all no-underline"
      >
        <span>⚙️</span>
        <span>せってい</span>
      </a>
    </div>
  </header>

  <!-- タイトル案内 -->
  <main class="max-w-5xl mx-auto w-full my-6 flex-1 space-y-8">
    <div class="text-center space-y-2">
      <div class="inline-block px-4 py-1 bg-gradient-to-r from-orange-500 to-amber-500 text-white text-xs font-black rounded-full shadow-sm animate-pulse">
        ✨ なにであそぶ？ えらんでね！
      </div>
      <h2 class="text-3xl sm:text-4xl font-black text-slate-800">
        しゅるいをえらぼう！
      </h2>
      <p class="text-sm text-stone-600 font-bold max-w-lg mx-auto">
        カードをタップすると、たのしい図鑑がはじまるよ！
      </p>
    </div>

    <!-- トースト通知 -->
    {#if toastMessage}
      <div class="max-w-md mx-auto p-4 bg-amber-500 text-white font-extrabold text-sm rounded-2xl shadow-xl border-2 border-amber-300 text-center animate-bounce flex items-center justify-center gap-2">
        <span>{toastMessage}</span>
      </div>
    {/if}

    <!-- 種類選択グリッド -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {#each mainCategories as cat}
        {#if cat.is_ready && cat.href}
          <!-- 準備完了（哺乳類） -->
          <a
            href={cat.href}
            class="group relative p-6 sm:p-8 rounded-3xl border-4 {cat.border_color} bg-gradient-to-br {cat.bg_gradient} 
                   shadow-lg hover:shadow-2xl hover:scale-105 active:scale-95 transition-all duration-300 flex flex-col justify-between space-y-4 no-underline"
          >
            <div class="flex items-center justify-between">
              <span class="text-5xl sm:text-6xl drop-shadow-md group-hover:scale-110 transition-transform">
                {cat.icon}
              </span>
              <span class="px-3 py-1 bg-orange-500 text-white text-xs font-black rounded-full shadow-sm">
                あそべるよ！
              </span>
            </div>

            <div>
              <h3 class="text-2xl sm:text-3xl font-black text-slate-800 tracking-tight">
                {cat.name_hiragana}
              </h3>
              <p class="text-xs font-black text-amber-800/80 mt-0.5">
                （{cat.name_kanji}）
              </p>
              <p class="text-xs text-slate-600 font-medium leading-relaxed mt-2">
                {cat.desc}
              </p>
            </div>

            <div class="pt-2 flex items-center justify-between border-t border-amber-300/60">
              <span class="text-xs font-extrabold text-amber-900 bg-white/70 px-2.5 py-1 rounded-lg">
                {cat.species_count_text}
              </span>
              <span class="text-sm font-black text-orange-600 group-hover:translate-x-1 transition-transform">
                ずかんをみる →
              </span>
            </div>
          </a>
        {:else}
          <!-- 準備中カード -->
          <button
            type="button"
            onclick={() => handleComingSoon(cat.name_hiragana)}
            class="relative p-6 sm:p-8 rounded-3xl border-4 border-slate-200/80 bg-white/60 hover:bg-stone-100/80 opacity-90 hover:opacity-100
                   shadow-sm hover:shadow-md transition-all duration-200 flex flex-col justify-between space-y-4 text-left cursor-pointer group"
          >
            <div class="flex items-center justify-between">
              <span class="text-5xl sm:text-6xl grayscale group-hover:grayscale-0 transition-all opacity-70 group-hover:opacity-100">
                {cat.icon}
              </span>
              <span class="px-3 py-1 bg-stone-300 text-stone-700 text-xs font-extrabold rounded-full">
                🚧 じゅんびちゅう
              </span>
            </div>

            <div>
              <h3 class="text-2xl sm:text-3xl font-black text-stone-600 group-hover:text-stone-800 transition-colors">
                {cat.name_hiragana}
              </h3>
              <p class="text-xs font-extrabold text-stone-400 mt-0.5">
                （{cat.name_kanji}）
              </p>
              <p class="text-xs text-stone-400 font-medium leading-relaxed mt-2">
                {cat.desc}
              </p>
            </div>

            <div class="pt-2 flex items-center justify-between border-t border-stone-200/60 text-xs text-stone-400 font-bold">
              <span>準備中の仲間たち</span>
              <span>もうちょっと待ってね 🔒</span>
            </div>
          </button>
        {/if}
      {/each}
    </div>
  </main>

  <!-- フッター -->
  <footer class="max-w-5xl mx-auto w-full py-6 text-center text-xs text-stone-500 font-bold border-t border-amber-200/60 mt-8 flex flex-col sm:flex-row items-center justify-between gap-3">
    <p>© 2026 Nomina! (ノミーナ！) - 子どもえいご＆いきものずかん</p>
    <a
      href="https://x.com/nomina2026"
      target="_blank"
      rel="noopener noreferrer"
      class="inline-flex items-center gap-1.5 text-stone-700 hover:text-black transition-colors font-extrabold no-underline"
    >
      <XIcon class="w-4 h-4 text-black" />
      <span>公式X (@nomina2026)</span>
    </a>
  </footer>
</div>
