<script lang="ts">
  import { onMount, onDestroy, untrack } from 'svelte';
  import { getLangAccent, getRecordMode, getAllowOverwrite, getDisplayMode, type LangAccent, type DisplayMode } from '$lib/utils/cookies';
  import { getAudioRecord, saveAudioRecord, deleteAudioRecord } from '$lib/utils/audioDb';
  import { trimSilenceFromAudioBlob } from '$lib/utils/audioTrimmer';
  import FlagIcon from '$lib/components/FlagIcon.svelte';

  export interface Species {
    id: string;
    tier: number;
    name_common: string;
    name_hiragana?: string;
    name_kanji?: string;
    name_standard_ja: string;
    name_en: string;
    name_en_gb?: string;
    name_zh_cn?: string;
    name_zh_tw?: string;
    name_es_es?: string;
    name_es_mx?: string;
    name_pt_pt?: string;
    name_pt_br?: string;
    name_fr_fr?: string;
    name_id_id?: string;
    image: string;
    audio?: string;
    description_note?: string;
    bg_color?: string;
    accent_color?: string;
  }

  let { species } = $props<{ species: Species }>();

  let isTapped = $state(false);
  let isSpeaking = $state(false);
  let currentAccent = $state<LangAccent>('en-US');
  let displayMode = $state<DisplayMode>('katakana');

  const displayName = $derived.by(() => {
    if (displayMode === 'hiragana') return species.name_hiragana || species.name_common;
    if (displayMode === 'kanji') return species.name_kanji || species.name_common;
    return species.name_common;
  });

  // 画像のロード完了・エラー状態管理
  let isImageLoaded = $state(false);
  let isImageError = $state(false);

  // species が変更された際に画像ロード状態をリセット
  $effect(() => {
    const _img = species.image;
    const _id = species.id;
    untrack(() => {
      isImageLoaded = false;
      isImageError = false;
    });
  });

  // 録音モード・端末内IndexedDB録音状態
  let recordMode = $state(false);
  let allowOverwrite = $state(false);
  let hasRecordedAudio = $state(false);
  let recordedAudioUrl = $state<string | null>(null);

  // 録音モーダル状態
  let isRecordingModalOpen = $state(false);
  let isRecording = $state(false);
  let isProcessingAudio = $state(false);
  let recordingSeconds = $state(0);
  let recordingTimer = $state<any>(null);
  let mediaRecorder = $state<MediaRecorder | null>(null);
  let audioChunks = $state<Blob[]>([]);

  // 削除確認モーダル状態
  let isDeleteModalOpen = $state(false);

  // マイクボタン・削除ボタンの表示判定
  let shouldShowRecordBtn = $derived(recordMode && (allowOverwrite || !hasRecordedAudio));

  onMount(() => {
    currentAccent = getLangAccent();
    displayMode = getDisplayMode();
    recordMode = getRecordMode();
    allowOverwrite = getAllowOverwrite();

    // Chrome/Edge等でのボイス一覧非同期ロード対策
    if ('speechSynthesis' in window) {
      window.speechSynthesis.getVoices();
      window.speechSynthesis.onvoiceschanged = () => {
        window.speechSynthesis.getVoices();
      };
    }
  });

  // species.id が切り替わった時に古い録音データを安全に破棄＆最新データを再ロード
  $effect(() => {
    const currentId = species.id;
    untrack(() => {
      if (recordedAudioUrl) {
        URL.revokeObjectURL(recordedAudioUrl);
        recordedAudioUrl = null;
      }
      hasRecordedAudio = false;

      loadRecordedAudio();
    });
  });

  onDestroy(() => {
    if (recordedAudioUrl) {
      URL.revokeObjectURL(recordedAudioUrl);
    }
    stopRecordingTimer();
  });

  async function loadRecordedAudio() {
    try {
      const blob = await getAudioRecord(species.id);
      if (blob) {
        hasRecordedAudio = true;
        if (recordedAudioUrl) URL.revokeObjectURL(recordedAudioUrl);
        recordedAudioUrl = URL.createObjectURL(blob);
      } else {
        hasRecordedAudio = false;
        recordedAudioUrl = null;
      }
    } catch {
      hasRecordedAudio = false;
      recordedAudioUrl = null;
    }
  }

  // 英国英語の非ローティック発音補正
  function toBritishPhonetic(text: string): string {
    let w = text;
    w = w.replace(/\bServal\b/gi, 'Servah');
    w = w.replace(/\bCaracal\b/gi, 'Caracah');
    w = w.replace(/\bCheetah\b/gi, 'Cheetah');
    w = w.replace(/\bJaguar\b/gi, 'Jag-yu-ah');
    w = w.replace(/\bPuma\b/gi, 'Pew-mah');
    return w;
  }

  // 中南米スペイン語のセセオ(seseo)発音補正 (z, ce, ci を s 音に強制)
  function toLatinSpanishPhonetic(text: string): string {
    let w = text;
    w = w.replace(/z/g, 's').replace(/Z/g, 'S');
    w = w.replace(/ce/g, 'se').replace(/Ce/g, 'Se');
    w = w.replace(/ci/g, 'si').replace(/Ci/g, 'Si');
    return w;
  }

  // 英語ボイスでスペイン語単語を発音させるためのフォネティック変換 (カタカナ・英語読み防止)
  function toSpanishPhoneticForEnglishVoice(text: string, isLatinAm: boolean): string {
    let w = text;
    w = w.replace(/[óÓ]/g, 'o').replace(/[áÁ]/g, 'a').replace(/[éÉ]/g, 'e').replace(/[íÍ]/g, 'i').replace(/[úÚ]/g, 'u');
    w = w.replace(/[ñÑ]/g, 'ny');

    const words = w.split(' ');
    const res = words.map(word => {
      let sw = word;
      sw = sw.replace(/ll/gi, 'y');
      sw = sw.replace(/j/gi, 'h');
      if (isLatinAm) {
        sw = sw.replace(/z/gi, 's').replace(/c([ei])/gi, 's$1');
      } else {
        sw = sw.replace(/z/gi, 'th').replace(/c([ei])/gi, 'th$1');
      }
      sw = sw.replace(/a/gi, 'ah');
      sw = sw.replace(/e/gi, 'eh');
      sw = sw.replace(/i/gi, 'ee');
      sw = sw.replace(/o/gi, 'oh');
      sw = sw.replace(/u/gi, 'oo');
      return sw;
    });
    return res.join(' ');
  }

  onMount(() => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.getVoices();
      if (window.speechSynthesis.onvoiceschanged !== undefined) {
        window.speechSynthesis.onvoiceschanged = () => {
          window.speechSynthesis.getVoices();
        };
      }
    }
  });

  // 選択言語に応じた単語取得
  function getForeignName(accent: LangAccent): string {
    if (accent === 'en-GB') return species.name_en_gb || species.name_en;
    if (accent === 'zh-CN') return species.name_zh_cn || species.name_en;
    if (accent === 'zh-TW') return species.name_zh_tw || species.name_en;
    if (accent === 'es-ES') return species.name_es_es || species.name_en;
    if (accent === 'es-MX') return species.name_es_mx || species.name_en;
    if (accent === 'pt-PT') return species.name_pt_pt || species.name_en;
    if (accent === 'pt-BR') return species.name_pt_br || species.name_en;
    if (accent === 'fr-FR') return species.name_fr_fr || species.name_en;
    if (accent === 'id-ID') return species.name_id_id || species.name_en;
    return species.name_en;
  }

  // Web Speech API を用いた名前の読み上げ
  function speak(text: string, lang: LangAccent | 'ja-JP') {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();

      let speakText = text;
      if (lang === 'en-GB') {
        speakText = toBritishPhonetic(text);
      } else if (lang === 'es-MX') {
        speakText = toLatinSpanishPhonetic(text);
      }

      const utterance = new SpeechSynthesisUtterance(speakText);
      utterance.lang = lang;
      utterance.rate = (lang === 'zh-CN' || lang === 'zh-TW') ? 0.95 : 0.88;
      utterance.pitch = 1.0;

      const voices = window.speechSynthesis.getVoices();

      if (voices.length > 0) {
        let targetVoice = null;

        if (lang === 'en-GB') {
          targetVoice = voices.find(v => 
            v.lang.replace('_', '-').toLowerCase() === 'en-gb' || 
            (v.lang.toLowerCase().startsWith('en') && (v.name.includes('UK') || v.name.includes('British') || v.name.includes('England') || v.name.includes('Hazel') || v.name.includes('George') || v.name.includes('Sonia')))
          ) || voices.find(v => v.lang.toLowerCase().startsWith('en'));
        } else if (lang === 'en-US') {
          targetVoice = voices.find(v => 
            v.lang.replace('_', '-').toLowerCase() === 'en-us' || 
            (v.lang.toLowerCase().startsWith('en') && (v.name.includes('US') || v.name.includes('American') || v.name.includes('Zira') || v.name.includes('David')))
          ) || voices.find(v => v.lang.toLowerCase().startsWith('en'));
        } else if (lang === 'zh-CN') {
          targetVoice = voices.find(v => 
            v.lang.replace('_', '-').toLowerCase() === 'zh-cn' || 
            (v.lang.toLowerCase().startsWith('zh') && (v.name.includes('Chinese') || v.name.includes('China') || v.name.includes('Mandarin') || v.name.includes('Huihui') || v.name.includes('Yaoyao')))
          ) || voices.find(v => v.lang.toLowerCase().startsWith('zh'));
        } else if (lang === 'zh-TW') {
          targetVoice = voices.find(v => 
            v.lang.replace('_', '-').toLowerCase() === 'zh-tw' || 
            (v.lang.toLowerCase().startsWith('zh') && (v.name.includes('Taiwan') || v.name.includes('Hanhan') || v.name.includes('Yating')))
          ) || voices.find(v => v.lang.toLowerCase().startsWith('zh'));
        } else if (lang === 'es-ES') {
          targetVoice = voices.find(v => 
            v.lang.replace('_', '-').toLowerCase() === 'es-es' || 
            (v.lang.toLowerCase().startsWith('es') && (v.name.includes('Spain') || v.name.includes('Spanish') || v.name.includes('Helena') || v.name.includes('Pablo') || v.name.includes('Laura') || v.name.includes('Monica')))
          ) || voices.find(v => v.lang.toLowerCase().startsWith('es')) ||
          voices.find(v => v.lang.toLowerCase().startsWith('en')) ||
          voices.find(v => !v.lang.toLowerCase().startsWith('ja'));
        } else if (lang === 'es-MX') {
          targetVoice = voices.find(v => {
            const l = v.lang.replace('_', '-').toLowerCase();
            return l === 'es-mx' || l === 'es-us' || l === 'es-419' || l === 'es-ar' || l === 'es-cl' || l === 'es-co' ||
                   (l.startsWith('es') && (v.name.includes('Mexico') || v.name.includes('Mexican') || v.name.includes('Hilda') || v.name.includes('Raul') || v.name.includes('Sabina')));
          }) || voices.find(v => v.lang.toLowerCase().startsWith('es')) ||
          voices.find(v => v.lang.toLowerCase().startsWith('en')) ||
          voices.find(v => !v.lang.toLowerCase().startsWith('ja'));
        } else if (lang === 'pt-PT') {
          targetVoice = voices.find(v => 
            v.lang.replace('_', '-').toLowerCase() === 'pt-pt' || 
            (v.lang.toLowerCase().startsWith('pt') && (v.name.includes('Portugal') || v.name.includes('European') || v.name.includes('Joana') || v.name.includes('Helia')))
          ) || voices.find(v => v.lang.toLowerCase().startsWith('pt')) ||
          voices.find(v => v.lang.toLowerCase().startsWith('en'));
        } else if (lang === 'pt-BR') {
          targetVoice = voices.find(v => 
            v.lang.replace('_', '-').toLowerCase() === 'pt-br' || 
            (v.lang.toLowerCase().startsWith('pt') && (v.name.includes('Brazil') || v.name.includes('Brazilian') || v.name.includes('Luciana') || v.name.includes('Felipe')))
          ) || voices.find(v => v.lang.toLowerCase().startsWith('pt')) ||
          voices.find(v => v.lang.toLowerCase().startsWith('en'));
        } else if (lang === 'fr-FR') {
          targetVoice = voices.find(v => 
            v.lang.replace('_', '-').toLowerCase() === 'fr-fr' || 
            (v.lang.toLowerCase().startsWith('fr') && (v.name.includes('French') || v.name.includes('France') || v.name.includes('Hortense') || v.name.includes('Julie') || v.name.includes('Paul')))
          ) || voices.find(v => v.lang.toLowerCase().startsWith('fr')) ||
          voices.find(v => v.lang.toLowerCase().startsWith('en'));
        } else if (lang === 'id-ID') {
          targetVoice = voices.find(v => 
            v.lang.replace('_', '-').toLowerCase() === 'id-id' || 
            (v.lang.toLowerCase().startsWith('id') && (v.name.includes('Indonesian') || v.name.includes('Indonesia') || v.name.includes('Andika') || v.name.includes('Gadis')))
          ) || voices.find(v => v.lang.toLowerCase().startsWith('id')) ||
          voices.find(v => v.lang.toLowerCase().startsWith('en'));
        }

        if (targetVoice) {
          utterance.voice = targetVoice;
          utterance.lang = targetVoice.lang;

          // 若しターゲットボイスがスペイン語ネイティブボイス(es-*)でない場合（英語ボイス等にフォールバックした場合）、
          // 英語ボイスに綺麗なスペイン語発音(Gahtoh, Pehrroh, Thohrroh/Sohrroh)で発音させる補正テキストを適用
          if ((lang === 'es-ES' || lang === 'es-MX') && !targetVoice.lang.toLowerCase().startsWith('es')) {
            utterance.text = toSpanishPhoneticForEnglishVoice(text, lang === 'es-MX');
          }
        }
      }

      utterance.onstart = () => { isSpeaking = true; };
      utterance.onend = () => { isSpeaking = false; };
      utterance.onerror = () => { isSpeaking = false; };

      window.speechSynthesis.speak(utterance);
    }
  }

  // 録音の開始
  async function startRecording() {
    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('NOT_SUPPORTED');
      }

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunks = [];
      let options: MediaRecorderOptions = {};
      if (typeof MediaRecorder !== 'undefined') {
        if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
          options = { mimeType: 'audio/webm;codecs=opus' };
        } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
          options = { mimeType: 'audio/mp4' };
        }
      }

      const recorder = new MediaRecorder(stream, options);
      
      recorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) {
          audioChunks.push(e.data);
        }
      };

      recorder.onstop = async () => {
        stream.getTracks().forEach(track => track.stop());
        if (audioChunks.length > 0) {
          isProcessingAudio = true;
          const mimeType = recorder.mimeType || 'audio/webm';
          const rawBlob = new Blob(audioChunks, { type: mimeType });
          try {
            // 前後の無音・小音量部分を自動カットしてトリミング保存
            const trimmedBlob = await trimSilenceFromAudioBlob(rawBlob);
            await saveAudioRecord(species.id, trimmedBlob || rawBlob);
          } catch (saveErr) {
            console.error('Failed to process/save trimmed audio, falling back to raw blob:', saveErr);
            await saveAudioRecord(species.id, rawBlob);
          } finally {
            await loadRecordedAudio();
            isProcessingAudio = false;
          }
        }
        isRecordingModalOpen = false;
        isRecording = false;
        stopRecordingTimer();
      };

      mediaRecorder = recorder;
      recorder.start();
      isRecording = true;
      recordingSeconds = 0;
      recordingTimer = setInterval(() => {
        recordingSeconds += 1;
      }, 1000);
    } catch (err: any) {
      console.error('Recording error:', err);
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        alert('マイクアクセスが拒否されました。ブラウザのサイト設定からマイク権限を「許可」に変更してください。');
      } else if (err.message === 'NOT_SUPPORTED') {
        alert('お使いの環境（非SSL等）ではマイクAPIが利用できません。https:// 環境またはブラウザの例外設定をご確認ください。');
      } else {
        alert(`マイクエラーが発生しました (${err.name || err.message || 'Error'})。マイク設定をご確認ください。`);
      }
      isRecordingModalOpen = false;
    }
  }

  function stopRecordingTimer() {
    if (recordingTimer) {
      clearInterval(recordingTimer);
      recordingTimer = null;
    }
  }

  // 録音完了して保存
  function finishRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
    }
  }

  // 録音取り消し
  function cancelRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.ondataavailable = null;
      mediaRecorder.onstop = () => {
        if (mediaRecorder) {
          mediaRecorder.stream.getTracks().forEach(t => t.stop());
        }
      };
      mediaRecorder.stop();
    }
    stopRecordingTimer();
    isRecording = false;
    isRecordingModalOpen = false;
  }

  // 録音削除の実行
  async function confirmDeleteRecord() {
    await deleteAudioRecord(species.id);
    if (recordedAudioUrl) {
      URL.revokeObjectURL(recordedAudioUrl);
      recordedAudioUrl = null;
    }
    hasRecordedAudio = false;
    isDeleteModalOpen = false;
  }

  function handleTap() {
    isTapped = true;
    setTimeout(() => { isTapped = false; }, 400);

    // 優先順位1: ユーザーが自分で録音した声があればそれを最優先で再生！
    if (recordedAudioUrl) {
      const audio = new Audio(recordedAudioUrl);
      isSpeaking = true;
      audio.play().then(() => {
        audio.onended = () => { isSpeaking = false; };
      }).catch(() => {
        speak(species.name_common, 'ja-JP');
      });
      return;
    }

    // 優先順位2: 提供オーディオファイル
    if (species.audio && species.audio !== '') {
      const audio = new Audio(species.audio);
      isSpeaking = true;
      audio.play().then(() => {
        audio.onended = () => { isSpeaking = false; };
      }).catch(() => {
        speak(species.name_common, 'ja-JP');
      });
    } else {
      speak(species.name_common, 'ja-JP');
    }
  }

  function handleForeignTap(e: MouseEvent) {
    e.stopPropagation();
    const accent = getLangAccent();
    currentAccent = accent;
    const targetName = getForeignName(accent);
    speak(targetName, accent);
  }

  const badgeColorClass = $derived(
    currentAccent === 'en-GB' ? 'bg-rose-500/10 hover:bg-rose-500/20 text-rose-700 border-rose-200' :
    currentAccent === 'zh-CN' ? 'bg-red-500/10 hover:bg-red-500/20 text-red-700 border-red-200' :
    currentAccent === 'zh-TW' ? 'bg-blue-500/10 hover:bg-blue-500/20 text-blue-700 border-blue-200' :
    currentAccent === 'es-ES' ? 'bg-amber-500/10 hover:bg-amber-500/20 text-amber-700 border-amber-200' :
    currentAccent === 'es-MX' ? 'bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-700 border-emerald-200' :
    currentAccent === 'pt-PT' ? 'bg-teal-500/10 hover:bg-teal-500/20 text-teal-700 border-teal-200' :
    currentAccent === 'pt-BR' ? 'bg-green-500/10 hover:bg-green-500/20 text-green-700 border-green-200' :
    'bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-700 border-indigo-200'
  );

  const listenBadgeClass = $derived(
    currentAccent === 'en-GB' ? 'bg-rose-500' :
    currentAccent === 'zh-CN' ? 'bg-red-500' :
    currentAccent === 'zh-TW' ? 'bg-blue-600' :
    currentAccent === 'es-ES' ? 'bg-amber-600' :
    currentAccent === 'es-MX' ? 'bg-emerald-600' :
    currentAccent === 'pt-PT' ? 'bg-teal-600' :
    currentAccent === 'pt-BR' ? 'bg-green-600' :
    'bg-indigo-500'
  );
</script>

<div
  role="button"
  tabindex="0"
  onclick={handleTap}
  onkeydown={(e) => e.key === 'Enter' && handleTap()}
  class="relative flex flex-col items-center bg-gradient-to-b {species.bg_color || 'from-white to-slate-50'} 
         p-5 rounded-3xl border-4 {species.accent_color || 'border-amber-300'} 
         shadow-lg hover:shadow-2xl transition-all duration-300 transform active:scale-95 cursor-pointer select-none
         {isTapped ? 'animate-bounce-tap ring-4 ring-yellow-400' : ''}"
>
  <!-- 動物画像 / イラスト -->
  <div class="relative w-40 h-40 sm:w-48 sm:h-48 rounded-2xl overflow-hidden bg-white/70 p-2 shadow-inner border-2 border-white flex items-center justify-center">
    <!-- 🎙️ 絵の左上の録音ボタン / 自分の声バッジエリア -->
    {#if hasRecordedAudio}
      <div class="absolute top-2 left-2 z-20 flex items-center gap-1">
        <button
          type="button"
          onclick={(e) => {
            e.stopPropagation();
            if (allowOverwrite) {
              isRecordingModalOpen = true;
              startRecording();
            }
          }}
          title={allowOverwrite ? "タップして自分の声を再録音する" : "自分の声で録音済み"}
          class="flex items-center gap-1 bg-gradient-to-r from-red-500 to-rose-600 hover:from-red-600 hover:to-rose-700 text-white text-[11px] font-black px-2.5 py-1 rounded-full shadow-md border border-white/80 active:scale-95 transition-all cursor-pointer"
        >
          <span class="w-2 h-2 rounded-full bg-white animate-pulse"></span>
          <span>🎙️ 自分の声</span>
        </button>
        
        <button
          type="button"
          onclick={(e) => { e.stopPropagation(); isDeleteModalOpen = true; }}
          title="録音した声を削除する"
          class="w-6 h-6 bg-white/90 hover:bg-red-600 hover:text-white text-slate-700 rounded-full flex items-center justify-center text-xs shadow-md border border-slate-200 transition-all cursor-pointer hover:scale-110 active:scale-90"
        >
          🗑️
        </button>
      </div>
    {:else if shouldShowRecordBtn}
      <div class="absolute top-2 left-2 z-20">
        <button
          type="button"
          onclick={(e) => { e.stopPropagation(); isRecordingModalOpen = true; startRecording(); }}
          title="この動物の名前を自分の声で録音する"
          class="flex items-center gap-1 bg-gradient-to-r from-red-500 to-rose-600 hover:from-red-600 hover:to-rose-700 text-white text-xs font-black px-2.5 py-1 rounded-full shadow-lg border-2 border-white hover:scale-105 active:scale-95 transition-all cursor-pointer animate-pulse"
        >
          <span class="w-2 h-2 rounded-full bg-white"></span>
          <span>録音 🎙️</span>
        </button>
      </div>
    {/if}

    <!-- 画像ロード中スケルトン・プレースホルダー -->
    {#if !isImageLoaded && !isImageError}
      <div class="absolute inset-0 flex flex-col items-center justify-center bg-amber-50/60 rounded-2xl animate-pulse z-10">
        <span class="text-4xl opacity-40 animate-bounce">🐾</span>
      </div>
    {/if}

    <!-- 画像エラー/未準備時のフォールバック表示 (足跡の仮画像「🐾」) -->
    {#if isImageError}
      <div class="emoji-fallback-container absolute inset-0 flex flex-col items-center justify-center bg-gradient-to-br from-white/90 to-amber-50/80 rounded-2xl p-2 z-10">
        <span class="text-7xl drop-shadow-md animate-float">🐾</span>
        <span class="text-[11px] font-black text-amber-800/80 mt-1 bg-white/80 px-2.5 py-0.5 rounded-full border border-amber-200 shadow-2xs">イラスト準備中</span>
      </div>
    {/if}

    <img
      src={species.image}
      alt={species.name_common}
      loading="lazy"
      decoding="async"
      class="w-full h-full object-contain drop-shadow-md transition-all duration-300 hover:scale-105 {isImageLoaded && !isImageError ? 'opacity-100 scale-100' : 'opacity-0 scale-95'}"
      onload={() => {
        isImageLoaded = true;
        isImageError = false;
      }}
      onerror={() => {
        isImageLoaded = false;
        isImageError = true;
      }}
    />

    <!-- 再生中インジケーター -->
    {#if isSpeaking}
      <div class="absolute inset-0 bg-yellow-400/20 backdrop-blur-[1px] flex items-center justify-center animate-pulse z-30">
        <span class="text-4xl animate-bounce">🔊</span>
      </div>
    {/if}
  </div>

  <!-- 名称表示（日本語・和名・選択中外国語） -->
  <div class="mt-4 text-center w-full space-y-1.5">
    <!-- 1. 一般呼称 (メイン) -->
    <h3 class="text-2xl sm:text-3xl font-black text-slate-800 tracking-tight drop-shadow-sm flex items-center justify-center gap-1.5">
      <span>{displayName}</span>
    </h3>

    <!-- 2. 標準和名 -->
    <div class="inline-block px-3 py-0.5 rounded-full bg-white/80 border border-slate-200 text-xs font-bold text-slate-600 shadow-2xs">
      和名: <span class="font-extrabold text-slate-700">{species.name_standard_ja}</span>
    </div>

    <!-- 3. 外国語名 (ボタン化して外国語単独再生も可能) -->
    <button
      onclick={handleForeignTap}
      title="外国語の発音を聞く"
      class="block mx-auto mt-1 px-3 py-1 rounded-xl transition-colors flex items-center justify-center gap-1.5 border font-black text-sm {badgeColorClass}"
    >
      <FlagIcon code={currentAccent} size="sm" />
      <span>{getForeignName(currentAccent)}</span>
      <span class="text-xs {listenBadgeClass} text-white px-1.5 py-0.5 rounded-full font-bold">🔊</span>
    </button>
  </div>

  <!-- 特徴・メモ -->
  {#if species.description_note}
    <p class="mt-3 text-xs text-slate-500 font-semibold bg-white/60 px-3 py-1 rounded-lg w-full text-center">
      💡 {species.description_note}
    </p>
  {/if}
</div>

<!-- 🎙️ 録音中ポップアップダイアログ -->
{#if isRecordingModalOpen}
  <div
    role="dialog"
    aria-modal="true"
    tabindex="-1"
    onclick={(e) => e.stopPropagation()}
    onkeydown={(e) => e.stopPropagation()}
    class="fixed inset-0 bg-stone-900/70 backdrop-blur-sm z-[20000] flex items-center justify-center p-4"
  >
    <div class="bg-white rounded-3xl max-w-sm w-full p-6 shadow-2xl border-4 border-red-400 flex flex-col items-center gap-5 relative text-center animate-in fade-in zoom-in-95 duration-200">
      
      <!-- 録音中 / 編集中の状態メッセージ -->
      {#if isProcessingAudio}
        <div class="flex items-center gap-2 bg-amber-100 text-amber-800 px-4 py-2 rounded-full border border-amber-300 font-black text-sm animate-pulse shadow-sm">
          <span class="w-4 h-4 rounded-full border-2 border-amber-600 border-t-transparent animate-spin"></span>
          <span>✂️ 音声を自動編集中...</span>
        </div>
      {:else}
        <div class="flex items-center gap-2 bg-red-100 text-red-600 px-4 py-1.5 rounded-full border border-red-300 font-black text-sm animate-pulse">
          <span class="w-3 h-3 rounded-full bg-red-600 animate-ping"></span>
          <span>ろくおん中... 00:{recordingSeconds < 10 ? '0' + recordingSeconds : recordingSeconds}</span>
        </div>
      {/if}

      <!-- 大きなマイクアイコンアニメーション -->
      <div class="relative w-24 h-24 rounded-full bg-gradient-to-br from-red-500 to-orange-500 text-white flex items-center justify-center text-5xl shadow-xl {isProcessingAudio ? 'animate-spin' : 'animate-bounce'}">
        {isProcessingAudio ? '✂️' : '🎙️'}
        {#if !isProcessingAudio}
          <div class="absolute inset-0 rounded-full border-4 border-red-400 animate-ping opacity-30"></div>
        {/if}
      </div>

      <!-- アナウンスガイド -->
      <div>
        <h3 class="text-xl font-black text-stone-800">
          「{species.name_common}」
        </h3>
        <p class="text-xs font-bold text-stone-500 mt-1">
          {isProcessingAudio ? '前後のはっきり聞こえない無音部分をカットしています...' : 'マイクに向かってはっきり声をだしてね！'}
        </p>
      </div>

      <!-- 操作ボタン -->
      <div class="w-full flex flex-col gap-2 pt-2">
        <button
          type="button"
          onclick={finishRecording}
          disabled={isProcessingAudio}
          class="w-full py-3.5 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 disabled:opacity-50 text-white font-black text-base rounded-2xl shadow-md hover:scale-[1.02] active:scale-95 transition-all cursor-pointer disabled:cursor-not-allowed border-b-4 border-emerald-700 flex items-center justify-center gap-2"
        >
          {#if isProcessingAudio}
            <span class="w-4 h-4 rounded-full border-2 border-white border-t-transparent animate-spin"></span>
            <span>編集保存中...</span>
          {:else}
            <span>✅ 録音完了して保存する</span>
          {/if}
        </button>

        {#if !isProcessingAudio}
          <button
            type="button"
            onclick={cancelRecording}
            class="w-full py-2.5 bg-stone-100 hover:bg-stone-200 text-stone-600 font-extrabold text-xs rounded-xl transition-all cursor-pointer"
          >
            とりけす（キャンセル）
          </button>
        {/if}
      </div>
    </div>
  </div>
{/if}

<!-- 🗑️ 録音削除確認ポップアップ -->
{#if isDeleteModalOpen}
  <div
    role="dialog"
    aria-modal="true"
    tabindex="-1"
    onclick={(e) => e.stopPropagation()}
    onkeydown={(e) => e.stopPropagation()}
    class="fixed inset-0 bg-stone-900/70 backdrop-blur-sm z-[20000] flex items-center justify-center p-4"
  >
    <div class="bg-white rounded-3xl max-w-sm w-full p-6 shadow-2xl border-4 border-amber-300 flex flex-col items-center gap-4 relative text-center animate-in fade-in zoom-in-95 duration-200">
      
      <div class="w-16 h-16 rounded-2xl bg-red-100 text-red-600 flex items-center justify-center text-3xl shadow-sm">
        🗑️
      </div>

      <div>
        <h3 class="text-lg font-black text-stone-800">
          「{species.name_common}」の録音声を削除しますか？
        </h3>
        <p class="text-xs font-bold text-stone-500 mt-1 leading-relaxed">
          削除すると、元の標準音声読み上げに戻ります。この操作は取り消せません。
        </p>
      </div>

      <div class="w-full flex flex-col gap-2 pt-2">
        <button
          type="button"
          onclick={confirmDeleteRecord}
          class="w-full py-3.5 bg-red-500 hover:bg-red-600 text-white font-black text-base rounded-2xl shadow-md hover:scale-[1.02] active:scale-95 transition-all cursor-pointer border-b-4 border-red-700"
        >
          🗑️ はい、削除する
        </button>

        <button
          type="button"
          onclick={() => { isDeleteModalOpen = false; }}
          class="w-full py-2.5 bg-stone-100 hover:bg-stone-200 text-stone-600 font-extrabold text-xs rounded-xl transition-all cursor-pointer"
        >
          キャンセル
        </button>
      </div>
    </div>
  </div>
{/if}
