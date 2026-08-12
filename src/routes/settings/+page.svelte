<script lang="ts">
  import { onMount } from 'svelte';
  import FlagIcon from '$lib/components/FlagIcon.svelte';
  import XIcon from '$lib/components/XIcon.svelte';
  import speciesData from '$lib/data/species.json';
  import { 
    getVisibleTier, setVisibleTier, 
    getLangAccent, setLangAccent, type LangAccent,
    getRecordMode, setRecordMode,
    getAllowOverwrite, setAllowOverwrite
  } from '$lib/utils/cookies';
  import { clearAllAudioRecords, getAllAudioRecordsList, deleteAudioRecord, type AudioRecordItem } from '$lib/utils/audioDb';

  let visibleTier = $state(1);
  let langAccent = $state<LangAccent>('en-US');
  let recordMode = $state(false);
  let allowOverwrite = $state(false);
  let recordedCount = $state(0);
  let isClearAllModalOpen = $state(false);

  // アコーディオン開閉＆録音リストデータ
  let isAccordionOpen = $state(false);
  let recordedList = $state<AudioRecordItem[]>([]);
  let playingSpeciesId = $state<string | null>(null);

  let savedMessage = $state(false);
  let toastText = $state('設定を保存しました！');

  let isInitialized = $state(false);

  onMount(async () => {
    visibleTier = getVisibleTier();
    langAccent = getLangAccent();
    recordMode = getRecordMode();
    allowOverwrite = getAllowOverwrite();
    await refreshRecordedList();
    isInitialized = true;
  });

  // 設定項目が切り替わった時にリアルタイムでCookie保存
  $effect(() => {
    if (isInitialized) {
      setVisibleTier(visibleTier);
      setLangAccent(langAccent);
      setRecordMode(recordMode);
      setAllowOverwrite(allowOverwrite);
    }
  });

  async function refreshRecordedList() {
    recordedList = await getAllAudioRecordsList();
    recordedCount = recordedList.length;
  }

  // 動物IDから名前・画像情報を検索
  function getSpeciesInfo(id: string) {
    for (const cat of speciesData.categories) {
      for (const fam of cat.families) {
        for (const sp of fam.species) {
          if (sp.id === id) return sp;
        }
      }
    }
    return { name_common: id, name_standard_ja: id, image: '' };
  }

  // 録音音声の再生
  function playRecord(item: AudioRecordItem) {
    if (!item.blob) return;
    playingSpeciesId = item.speciesId;
    const url = URL.createObjectURL(item.blob);
    const audio = new Audio(url);
    audio.play().then(() => {
      audio.onended = () => {
        playingSpeciesId = null;
        URL.revokeObjectURL(url);
      };
    }).catch(() => {
      playingSpeciesId = null;
      URL.revokeObjectURL(url);
    });
  }

  // 録音音声のダウンロード
  function downloadRecord(item: AudioRecordItem) {
    if (!item.blob) return;
    const info = getSpeciesInfo(item.speciesId);
    const filename = `nomina_${info.name_common || item.speciesId}.webm`;
    const url = URL.createObjectURL(item.blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  // 個別削除
  async function deleteSingleRecord(speciesId: string) {
    await deleteAudioRecord(speciesId);
    await refreshRecordedList();
  }

  function handleSave() {
    setVisibleTier(visibleTier);
    setLangAccent(langAccent);
    setRecordMode(recordMode);
    setAllowOverwrite(allowOverwrite);

    // トースト表示
    toastText = '設定を保存しました！';
    savedMessage = true;
    setTimeout(() => {
      savedMessage = false;
    }, 2500);
  }

  async function handleClearAllAudio() {
    await clearAllAudioRecords();
    isClearAllModalOpen = false;
    await refreshRecordedList();
    toastText = 'すべての録音データを削除しました';
    savedMessage = true;
    setTimeout(() => {
      savedMessage = false;
    }, 2500);
  }

  const tierDescriptions: Record<number, { title: string; desc: string; icon: string; countText: string }> = {
    1: {
      title: "みんなが知ってる動物だけ表示",
      desc: "イヌ、ネコ、ゾウ、ライオン、パンダなど、子どもたちがよく知っている代表的な人気動物を中心に表示します。",
      icon: "🐶",
      countText: "（約77種）"
    },
    2: {
      title: "動物園などにいる動物まで表示",
      desc: "定番の動物に加えて、日本の動物園や水族館で見られる人気動物や珍しい仲間も表示します。",
      icon: "🦁",
      countText: "（約205種）"
    },
    3: {
      title: "収録している動物をすべて表示",
      desc: "図鑑に収録されているすべての哺乳類（世界中のめずらしい動物や絶滅危惧種）を表示します。",
      icon: "🌍",
      countText: "（全217種）"
    }
  };

  const languageOptions: { code: LangAccent; name: string; subtitle: string; desc: string; bgClass: string; borderClass: string; badgeClass: string }[] = [
    {
      code: 'en-US',
      name: 'アメリカ英語',
      subtitle: 'American English',
      desc: '明るくクリアなアメリカン発音と標準英単語',
      bgClass: 'from-blue-50 to-indigo-50',
      borderClass: 'border-indigo-500',
      badgeClass: 'bg-indigo-500'
    },
    {
      code: 'en-GB',
      name: 'イギリス英語',
      subtitle: 'British English',
      desc: '伝統的な英国式アクセント(Non-rhotic)とイギリス単語',
      bgClass: 'from-rose-50 to-pink-50',
      borderClass: 'border-rose-500',
      badgeClass: 'bg-rose-500'
    },
    {
      code: 'zh-CN',
      name: '中国語（簡体字）',
      subtitle: '简体中文 (中国)',
      desc: '中国本土で広く使われている簡体字表記と普通話発音',
      bgClass: 'from-red-50 to-amber-50',
      borderClass: 'border-red-500',
      badgeClass: 'bg-red-500'
    },
    {
      code: 'zh-TW',
      name: '中国語（繁体字）',
      subtitle: '繁體中文 (台灣)',
      desc: '台湾や香港などで使われる伝統的な繁体字表記と台湾華語発音',
      bgClass: 'from-blue-50 to-cyan-50',
      borderClass: 'border-blue-600',
      badgeClass: 'bg-blue-600'
    },
    {
      code: 'es-ES',
      name: '欧州スペイン語',
      subtitle: 'Español (España)',
      desc: 'スペイン本国で使われる伝統的なカスティーリャ発音',
      bgClass: 'from-yellow-50 to-amber-50',
      borderClass: 'border-amber-500',
      badgeClass: 'bg-amber-600'
    },
    {
      code: 'es-MX',
      name: '中南米スペイン語',
      subtitle: 'Español (México)',
      desc: 'メキシコをはじめ中南米で広く話されている親しみやすいスペイン語',
      bgClass: 'from-emerald-50 to-green-50',
      borderClass: 'border-emerald-500',
      badgeClass: 'bg-emerald-600'
    },
    {
      code: 'pt-PT',
      name: '欧州ポルトガル語',
      subtitle: 'Português (Portugal)',
      desc: 'ポルトガル本国で使われる伝統的なポルトガル語表記と発音',
      bgClass: 'from-teal-50 to-emerald-50',
      borderClass: 'border-teal-500',
      badgeClass: 'bg-teal-600'
    },
    {
      code: 'pt-BR',
      name: 'ブラジルポルトガル語',
      subtitle: 'Português (Brasil)',
      desc: 'ブラジルで広く話されている親しみやすく美しいポルトガル語発音',
      bgClass: 'from-green-50 to-emerald-50',
      borderClass: 'border-green-600',
      badgeClass: 'bg-green-600'
    },
    {
      code: 'fr-FR',
      name: 'フランス語',
      subtitle: 'Français (France)',
      desc: 'エレガントで美しいフランス本国の標準フランス語発音と表記',
      bgClass: 'from-blue-50 to-sky-50',
      borderClass: 'border-blue-500',
      badgeClass: 'bg-blue-500'
    },
    {
      code: 'id-ID',
      name: 'インドネシア語',
      subtitle: 'Bahasa Indonesia',
      desc: '東南アジアで広く話されている親しみやすいインドネシア語発音',
      bgClass: 'from-red-50 to-rose-50',
      borderClass: 'border-red-600',
      badgeClass: 'bg-red-600'
    }
  ];
</script>

<svelte:head>
  <title>設定 | Nomina!</title>
  <meta name="description" content="表示する生きものの数（Tier）などを調整する設定ページです。" />
  <meta property="og:title" content="設定 | Nomina!" />
  <meta property="og:description" content="表示する生きものの数（Tier）などを調整する設定ページです。" />
  <meta property="og:url" content="https://nomina2026.netlify.app/settings" />
  <link rel="canonical" href="https://nomina2026.netlify.app/settings" />
</svelte:head>

<main class="min-h-screen bg-amber-50/50 p-4 sm:p-8">
  <div class="max-w-3xl mx-auto space-y-6">
    <!-- ヘッダー導線 -->
    <div class="flex items-center justify-between">
      <a
        href="/mammals"
        class="inline-flex items-center gap-2 px-4 py-2 bg-white text-amber-700 font-extrabold rounded-2xl shadow-sm border border-amber-200 hover:bg-amber-100 transition-all no-underline"
      >
        <span>←</span>
        <span>哺乳類図鑑に戻る</span>
      </a>
      <a
        href="/"
        class="inline-flex items-center gap-1.5 px-4 py-2 bg-amber-100 text-amber-800 font-extrabold rounded-2xl border border-amber-300 hover:bg-amber-200 transition-all no-underline text-xs"
      >
        <span>🏠</span>
        <span>種類選択トップ</span>
      </a>
    </div>

    <!-- 設定カード -->
    <div class="bg-white rounded-3xl p-6 sm:p-10 shadow-xl border-4 border-amber-200 space-y-8">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 bg-amber-100 rounded-2xl flex items-center justify-center text-2xl">
          ⚙️
        </div>
        <div>
          <h1 class="text-2xl sm:text-3xl font-black text-stone-800">
            図鑑の設定
          </h1>
          <p class="text-sm text-stone-500 font-bold">
            掲載する動物の数や外国語の発音・モードを選択できます
          </p>
        </div>
      </div>

      <!-- 1. スライダーセクション（掲載数） -->
      <section class="space-y-4">
        <h2 class="text-lg font-black text-stone-800 flex items-center gap-2">
          <span>🐾</span>
          <span>掲載数の設定</span>
        </h2>

        <div class="bg-amber-50/80 rounded-2xl p-6 border-2 border-amber-200">
          <div class="flex justify-between text-sm font-black text-amber-800 mb-3 px-1">
            <span>掲載数：代表種のみ</span>
            <span>全種類</span>
          </div>

          <input
            type="range"
            min="1"
            max="3"
            step="1"
            bind:value={visibleTier}
            class="w-full h-4 bg-amber-200 rounded-lg appearance-none cursor-pointer accent-orange-500 hover:accent-orange-600 transition-all focus:outline-none"
          />

          <div class="flex justify-between text-xs font-bold text-stone-400 mt-2 px-1">
            <span>代表種 (1)</span>
            <span>動物園などにいる動物まで表示 (2)</span>
            <span>全種 (3)</span>
          </div>
        </div>

        <!-- 現在選択中のTierの説明メッセージ -->
        {#if tierDescriptions[visibleTier]}
          <div class="bg-gradient-to-br from-orange-50 to-amber-50 border-2 border-orange-200 rounded-2xl p-6 shadow-inner animate-fadeIn">
            <div class="flex items-start gap-4">
              <span class="text-4xl shrink-0 p-2 bg-white rounded-2xl shadow-sm">
                {tierDescriptions[visibleTier].icon}
              </span>
              <div>
                <div class="flex items-center gap-2 flex-wrap mb-1">
                  <h3 class="text-lg font-black text-stone-800">
                    {tierDescriptions[visibleTier].title}
                  </h3>
                  <span class="text-xs px-2.5 py-0.5 bg-orange-500 text-white font-extrabold rounded-full">
                    {tierDescriptions[visibleTier].countText}
                  </span>
                </div>
                <p class="text-sm text-stone-600 font-medium leading-relaxed">
                  {tierDescriptions[visibleTier].desc}
                </p>
              </div>
            </div>
          </div>
        {/if}
      </section>

      <hr class="border-amber-200" />

      <!-- 2. 録音モードの設定セクション -->
      <section class="space-y-4">
        <h2 class="text-lg font-black text-stone-800 flex items-center gap-2">
          <span>🎙️</span>
          <span>自分の声で録音する（録音モード）</span>
        </h2>

        <div class="bg-amber-50/80 rounded-2xl p-5 border-2 border-amber-200 flex flex-col gap-4">
          <!-- 録音モードON/OFFトグル -->
          <div class="flex items-center justify-between gap-4">
            <div>
              <div class="font-black text-stone-800 text-base">録音モード</div>
              <p class="text-xs text-stone-500 font-medium mt-0.5">
                ONにすると、各動物イラストの左上に録音ボタンを表示します。自分の声を録音して日本語音声として再生できます。
              </p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer shrink-0">
              <input type="checkbox" bind:checked={recordMode} class="sr-only peer" />
              <div class="w-14 h-8 bg-stone-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[4px] after:left-[4px] after:bg-white after:border-stone-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-orange-500"></div>
            </label>
          </div>

          <!-- 上書き許可ON/OFFトグル (録音モードがONの場合にのみ機能) -->
          {#if recordMode}
            <div class="pt-3 border-t border-amber-200/80 flex items-center justify-between gap-4 animate-fadeIn">
              <div>
                <div class="font-black text-stone-800 text-sm">録音の上書き許可</div>
                <p class="text-xs text-stone-500 font-medium mt-0.5">
                  ON：常にすべてのカードにマイクボタンを表示し再録音できます。<br />
                  OFF：録音済みデータがある動物カードのマイクボタンを隠します。
                </p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer shrink-0">
                <input type="checkbox" bind:checked={allowOverwrite} class="sr-only peer" />
                <div class="w-12 h-7 bg-stone-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-stone-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-amber-500"></div>
              </label>
            </div>
          {/if}
          <!-- 録音済みデータをすべて削除ボタン -->
          <div class="pt-3 border-t border-amber-200/80 flex items-center justify-between gap-4">
            <div>
              <div class="font-black text-stone-800 text-sm flex items-center gap-2">
                <span>録音済みデータ</span>
                {#if recordedCount > 0}
                  <span class="text-xs bg-amber-500 text-white font-black px-2 py-0.5 rounded-full">{recordedCount}件</span>
                {:else}
                  <span class="text-xs bg-stone-200 text-stone-600 font-bold px-2 py-0.5 rounded-full">なし</span>
                {/if}
              </div>
              <p class="text-xs text-stone-500 font-medium mt-0.5">
                これまでに端末内に保存されたすべての自分の声を一括削除します。
              </p>
            </div>
            <button
              type="button"
              onclick={() => (isClearAllModalOpen = true)}
              disabled={recordedCount === 0}
              class="px-3.5 py-2 bg-red-50 hover:bg-red-100 disabled:opacity-40 disabled:hover:bg-red-50 text-red-700 font-black text-xs rounded-xl transition-all cursor-pointer disabled:cursor-not-allowed border border-red-200 shrink-0 flex items-center gap-1"
            >
              <span>🗑️</span>
              <span>すべて削除</span>
            </button>
          </div>

          <!-- 録音済みデータ一覧アコーディオン (全件の再生・ダウンロード・個別削除) -->
          <div class="pt-3 border-t border-amber-200/80">
            <button
              type="button"
              onclick={() => (isAccordionOpen = !isAccordionOpen)}
              class="w-full flex items-center justify-between p-3 bg-white/90 hover:bg-white rounded-xl border border-amber-200 font-black text-xs sm:text-sm text-stone-800 transition-all cursor-pointer shadow-2xs"
            >
              <div class="flex items-center gap-2">
                <span>📁</span>
                <span>録音済みデータ一覧</span>
                <span class="text-xs bg-amber-100 text-amber-900 font-bold px-2 py-0.5 rounded-full border border-amber-300">
                  {recordedCount}件
                </span>
              </div>
              <div class="flex items-center gap-1 text-stone-500 font-bold text-xs">
                <span>{isAccordionOpen ? 'とじる' : 'ひらく'}</span>
                <span class="transition-transform duration-200 {isAccordionOpen ? 'rotate-180' : ''}">▼</span>
              </div>
            </button>

            <!-- アコーディオンコンテンツ (録音一覧) -->
            {#if isAccordionOpen}
              <div class="mt-3 space-y-2 max-h-72 overflow-y-auto pr-1 animate-fadeIn">
                {#if recordedList.length === 0}
                  <div class="p-6 text-center text-xs font-bold text-stone-400 bg-white/60 rounded-xl border border-stone-200">
                    録音されたデータはまだありません 🐾<br />
                    （録音モードをONにして動物カードのマイクボタンから録音できます）
                  </div>
                {:else}
                  {#each recordedList as item}
                    {@const info = getSpeciesInfo(item.speciesId)}
                    <div class="flex items-center justify-between p-2.5 bg-white rounded-xl border border-stone-200 shadow-2xs gap-2">
                      <!-- 動物アイコン ＆ 名称 -->
                      <div class="flex items-center gap-2.5 min-w-0">
                        {#if info.image}
                          <img src={info.image} alt={info.name_common} loading="lazy" decoding="async" class="w-8 h-8 object-contain rounded-lg shrink-0 bg-stone-100 p-0.5 border border-stone-200" />
                        {:else}
                          <div class="w-8 h-8 rounded-lg bg-amber-100 flex items-center justify-center text-sm shrink-0">🐾</div>
                        {/if}
                        <div class="min-w-0">
                          <div class="font-black text-xs sm:text-sm text-stone-800 truncate">
                            {info.name_common || item.speciesId}
                          </div>
                          <div class="text-[10px] text-stone-400 font-bold truncate">
                            {info.name_standard_ja || item.speciesId}
                          </div>
                        </div>
                      </div>

                      <!-- アクションボタン群 (再生, ダウンロード, 削除) -->
                      <div class="flex items-center gap-1.5 shrink-0">
                        <!-- 再生ボタン -->
                        <button
                          type="button"
                          onclick={() => playRecord(item)}
                          title="音声を再生する"
                          class="px-2.5 py-1.5 bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-xs rounded-lg transition-all flex items-center gap-1 shadow-2xs cursor-pointer"
                        >
                          <span>{playingSpeciesId === item.speciesId ? '🔊' : '▶'}</span>
                          <span class="hidden sm:inline">再生</span>
                        </button>

                        <!-- ダウンロードボタン -->
                        <button
                          type="button"
                          onclick={() => downloadRecord(item)}
                          title="音声ファイルを保存ダウンロードする"
                          class="px-2.5 py-1.5 bg-sky-500 hover:bg-sky-600 text-white font-bold text-xs rounded-lg transition-all flex items-center gap-1 shadow-2xs cursor-pointer"
                        >
                          <span>⬇️</span>
                          <span class="hidden sm:inline">保存</span>
                        </button>

                        <!-- 個別削除ボタン -->
                        <button
                          type="button"
                          onclick={() => deleteSingleRecord(item.speciesId)}
                          title="この録音を削除する"
                          class="p-1.5 bg-stone-100 hover:bg-red-100 text-stone-500 hover:text-red-600 rounded-lg transition-colors cursor-pointer border border-stone-200"
                        >
                          🗑️
                        </button>
                      </div>
                    </div>
                  {/each}
                {/if}
              </div>
            {/if}
          </div>
        </div>
      </section>

      <hr class="border-amber-200" />

      <!-- 3. 外国語の設定セクション (全6言語) -->
      <section class="space-y-4">
        <div>
          <h2 class="text-lg font-black text-stone-800 flex items-center gap-2">
            <span>🌐</span>
            <span>外国語の発音・モード設定</span>
          </h2>
          <p class="text-xs text-stone-500 font-bold mt-1">
            図鑑のボタンを押したときに再生される言葉と地域アクセントを選べます
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {#each languageOptions as langOpt}
            <button
              type="button"
              onclick={() => (langAccent = langOpt.code)}
              class="p-5 rounded-2xl border-3 text-left transition-all cursor-pointer flex flex-col justify-between space-y-3 relative overflow-hidden
                {langAccent === langOpt.code
                  ? `bg-gradient-to-br ${langOpt.bgClass} ${langOpt.borderClass} shadow-md scale-[1.02]`
                  : 'bg-white border-stone-200 hover:border-amber-300 hover:bg-stone-50'}"
            >
              <div class="flex items-center justify-between">
                <FlagIcon code={langOpt.code} size="lg" />
                {#if langAccent === langOpt.code}
                  <span class="text-xs {langOpt.badgeClass} text-white font-black px-2.5 py-1 rounded-full">
                    選択中
                  </span>
                {/if}
              </div>

              <div>
                <h3 class="font-black text-stone-800 text-base flex items-center gap-2">
                  <FlagIcon code={langOpt.code} size="sm" />
                  <span>{langOpt.name}</span>
                </h3>
                <p class="text-[11px] font-extrabold text-amber-800/80">{langOpt.subtitle}</p>
                <p class="text-xs text-stone-500 font-bold mt-1 leading-snug">{langOpt.desc}</p>
              </div>
            </button>
          {/each}
        </div>
      </section>

      <!-- 3. 公式Xアカウント -->
      <section class="pt-6 border-t border-amber-200/80">
        <a
          href="https://x.com/nomina2026"
          target="_blank"
          rel="noopener noreferrer"
          class="flex items-center justify-between p-4 bg-stone-100 hover:bg-stone-200 text-stone-800 rounded-2xl transition-all border border-stone-200 group no-underline"
        >
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-black flex items-center justify-center shrink-0">
              <XIcon class="w-4 h-4 text-white" />
            </div>
            <div>
              <div class="font-bold text-sm text-stone-800">
                公式X (@nomina2026)
              </div>
              <p class="text-xs text-stone-500 font-medium">
                ご意見・お問い合わせ・お知らせ
              </p>
            </div>
          </div>
          <span class="text-xs font-bold text-stone-500 group-hover:text-black transition-colors shrink-0">
            表示 ↗
          </span>
        </a>
      </section>

      <!-- 保存ボタン & トースト -->
      <div class="pt-4 flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-amber-200">
        <button
          type="button"
          onclick={handleSave}
          class="w-full sm:w-auto px-8 py-4 bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-black text-lg rounded-2xl shadow-lg hover:shadow-xl hover:scale-105 active:scale-95 transition-all cursor-pointer flex items-center justify-center gap-2"
        >
          <span>💾</span>
          <span>設定を保存する</span>
        </button>

        {#if savedMessage}
          <div class="px-4 py-2 bg-emerald-500 text-white font-extrabold text-sm rounded-xl shadow-md animate-bounce flex items-center gap-1.5">
            <span>✅</span>
            <span>{toastText}</span>
          </div>
        {/if}
      </div>
    </div>
  </div>
</main>

<!-- 🗑️ 全録音データ一括削除確認モーダル -->
{#if isClearAllModalOpen}
  <div
    role="dialog"
    aria-modal="true"
    tabindex="-1"
    onclick={(e) => e.stopPropagation()}
    onkeydown={(e) => e.stopPropagation()}
    class="fixed inset-0 bg-stone-900/70 backdrop-blur-sm z-[20000] flex items-center justify-center p-4"
  >
    <div class="bg-white rounded-3xl max-w-sm w-full p-6 shadow-2xl border-4 border-red-400 flex flex-col items-center gap-4 relative text-center animate-in fade-in zoom-in-95 duration-200">
      <div class="w-16 h-16 rounded-2xl bg-red-100 text-red-600 flex items-center justify-center text-3xl shadow-sm">
        🗑️
      </div>

      <div>
        <h3 class="text-lg font-black text-stone-800">
          すべての録音データを削除しますか？
        </h3>
        <p class="text-xs font-bold text-stone-500 mt-1 leading-relaxed">
          これまでに保存された <span class="text-red-600 font-black">{recordedCount}件</span> のすべての自分の声が端末から一括削除され、元の標準読み上げ音声に戻ります。<br />この操作は取り消せません。
        </p>
      </div>

      <div class="w-full flex flex-col gap-2 pt-2">
        <button
          type="button"
          onclick={handleClearAllAudio}
          class="w-full py-3.5 bg-red-600 hover:bg-red-700 text-white font-black text-base rounded-2xl shadow-md hover:scale-[1.02] active:scale-95 transition-all cursor-pointer border-b-4 border-red-800"
        >
          🗑️ すべて削除する
        </button>

        <button
          type="button"
          onclick={() => (isClearAllModalOpen = false)}
          class="w-full py-2.5 bg-stone-100 hover:bg-stone-200 text-stone-600 font-extrabold text-xs rounded-xl transition-all cursor-pointer"
        >
          キャンセル
        </button>
      </div>
    </div>
  </div>
{/if}
